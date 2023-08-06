import inspect
import itertools
import json
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Type, Union

import gorilla
from langchain.python import PythonREPL
from langchain.tools.playwright.click import ClickTool
from langchain.tools.playwright.current_page import CurrentWebPageTool
from langchain.tools.playwright.extract_hyperlinks import ExtractHyperlinksTool
from langchain.tools.playwright.extract_text import ExtractTextTool
from langchain.tools.playwright.get_elements import GetElementsTool
from langchain.tools.playwright.navigate import NavigateTool
from langchain.tools.playwright.navigate_back import NavigateBackTool
from langchain.utilities.bash import BashProcess
from vcr.cassette import Cassette
from vcr.errors import CannotOverwriteExistingCassetteException
from vcr.patch import CassettePatcherBuilder
from vcr.request import Request

log = logging.getLogger(__name__)


LANGCHAIN_VISUALIZER_PATCH_ID = "lc-viz"
VCR_LANGCHAIN_PATCH_ID = "lc-vcr"
# override prefix to use if langchain-visualizer is there as well
VCR_VIZ_INTEROP_PREFIX = "_vcr_"


CUSTOM_PATCHERS: List[Any] = []


def add_patchers(*patchers: Any) -> None:
    CUSTOM_PATCHERS.extend(patchers)


log = logging.getLogger(__name__)


def lookup(cassette: Cassette, request: Request) -> Optional[Any]:
    """
    Code modified from OG vcrpy:
    https://github.com/kevin1024/vcrpy/blob/v4.2.1/vcr/stubs/__init__.py#L225

    Because we are running a tool, we exit early compared to the original function
    because the network reset logic is not needed here.
    """
    if cassette.can_play_response_for(request):
        log.info("Playing response for {} from cassette".format(request))
        return cassette.play_response(request)
    else:
        if cassette.write_protected and cassette.filter_request(request):
            raise CannotOverwriteExistingCassetteException(
                cassette=cassette, failed_request=request
            )
        return None


class GenericPatch:
    """
    Generic class for patching into tool overrides

    Inherit from this, and ideally create a copy of the function you're patching in
    order to ensure that everything always gets converted into kwargs for
    serialization. See PythonREPLPatch as an example of what to do.
    """

    cassette: Cassette
    cls: Type
    fn_name: str
    og_fn: Callable
    generic_override: Callable
    same_signature_override: Callable
    is_async: bool

    def __init__(self, cassette: Cassette, cls: Type, fn_name: str):
        self.cassette = cassette
        self.cls = cls
        self.fn_name = fn_name

        # if the backup for the OG function has already been set, then that most likely
        # means langchain visualizer got to it first. we'll let the visualizer call out
        # to us because we always want to visualize a call even if it's cached -- we
        # don't want to hide cached calls in the visualization graph
        viz_was_here = False
        try:
            self.og_fn = gorilla.get_original_attribute(
                self.cls, self.fn_name, LANGCHAIN_VISUALIZER_PATCH_ID
            )
            viz_was_here = True
        except AttributeError:
            self.og_fn = getattr(self.cls, self.fn_name)

        self.is_async = inspect.iscoroutinefunction(self.og_fn)

        if self.is_async:
            self.generic_override = self.get_async_generic_override_fn()
        else:
            self.generic_override = self.get_generic_override_fn()
        self.same_signature_override = self.get_same_signature_override()
        override_name = (
            VCR_VIZ_INTEROP_PREFIX + self.fn_name if viz_was_here else self.fn_name
        )
        self.patch = gorilla.Patch(
            destination=self.cls,
            name=override_name,
            obj=self.same_signature_override,
            settings=gorilla.Settings(store_hit=True, allow_hit=not viz_was_here),
        )

    def get_request(self, kwargs: Dict[str, Any]) -> Request:
        """
        Build the request in a consistently repeatable manner.

        This allows us to search for previous instances of the same query in the vcrpy
        requests cache.
        """
        tool_class_name = self.cls.__name__
        # record fn_name as well in case we're patching two different functions
        # from the same class
        tool_fn_name = self.fn_name
        fake_uri = f"tool://{tool_class_name}/{tool_fn_name}"
        return Request(
            method="POST",
            uri=fake_uri,
            body=json.dumps(kwargs, sort_keys=True),
            headers={},
        )

    def get_generic_override_fn(self) -> Callable:
        def fn_override(og_self: Any, **kwargs: str) -> Any:
            """
            Actual override functionality.

            As mentioned above, only kwargs are allowed to ensure that all arguments get
            serialized properly for caching.
            """
            request = self.get_request(kwargs)
            cached_response = lookup(self.cassette, request)
            if cached_response is not None:
                return cached_response

            new_response = self.og_fn(og_self, **kwargs)
            self.cassette.append(request, new_response)
            return new_response

        return fn_override

    def get_async_generic_override_fn(self) -> Callable:
        async def async_fn_override(og_self: Any, **kwargs: str) -> Any:
            """
            Actual override functionality.

            As mentioned above, only kwargs are allowed to ensure that all arguments get
            serialized properly for caching.
            """
            request = self.get_request(kwargs)
            cached_response = lookup(self.cassette, request)
            if cached_response is not None:
                return cached_response

            new_response = await self.og_fn(og_self, **kwargs)
            self.cassette.append(request, new_response)
            return new_response

        return async_fn_override

    def get_same_signature_override(self) -> Callable:
        """Override this function in the inherited class to convert args to kwargs"""
        return self.get_generic_override_fn()

    def __enter__(self) -> None:
        gorilla.apply(self.patch, id=VCR_LANGCHAIN_PATCH_ID)

    def __exit__(self, *_: List[Any]) -> None:
        gorilla.revert(self.patch)


class PythonREPLPatch(GenericPatch):
    def __init__(self, cassette: Cassette):
        super().__init__(cassette, PythonREPL, "run")

    def get_same_signature_override(self) -> Callable:
        def run(og_self: PythonREPL, command: str) -> str:
            """Same signature override patched into PythonREPL"""
            return self.generic_override(og_self, command=command)

        return run


class BashProcessPatch(GenericPatch):
    def __init__(self, cassette: Cassette):
        super().__init__(cassette, BashProcess, "run")

    def get_same_signature_override(self) -> Callable:
        def run(og_self: BashProcess, commands: Union[str, List[str]]) -> str:
            """Same signature override patched into BashProcess"""
            return self.generic_override(og_self, commands=commands)

        return run


class NavigateToolPatch(GenericPatch):
    def __init__(self, cassette: Cassette):
        super().__init__(cassette, NavigateTool, "run")

    def get_same_signature_override(self) -> Callable:
        def run(og_self: NavigateTool, url: str) -> str:
            return self.generic_override(og_self, tool_input=url)

        return run


class NavigateToolAsyncPatch(GenericPatch):
    def __init__(self, cassette: Cassette):
        super().__init__(cassette, NavigateTool, "arun")

    def get_same_signature_override(self) -> Callable:
        async def arun(og_self: NavigateTool, url: str) -> str:
            return await self.generic_override(og_self, tool_input=url)

        return arun


class ClickToolPatch(GenericPatch):
    def __init__(self, cassette: Cassette):
        super().__init__(cassette, ClickTool, "run")

    def get_same_signature_override(self) -> Callable:
        def run(og_self: ClickTool, selector: str) -> str:
            return self.generic_override(og_self, tool_input=selector)

        return run


class ClickToolAsyncPatch(GenericPatch):
    def __init__(self, cassette: Cassette):
        super().__init__(cassette, ClickTool, "arun")

    def get_same_signature_override(self) -> Callable:
        async def arun(og_self: ClickTool, selector: str) -> str:
            return await self.generic_override(og_self, tool_input=selector)

        return arun


class CurrentWebPageToolPatch(GenericPatch):
    def __init__(self, cassette: Cassette):
        super().__init__(cassette, CurrentWebPageTool, "run")

    def get_same_signature_override(self) -> Callable:
        def run(og_self: CurrentWebPageTool, tool_input: Dict) -> str:
            return self.generic_override(og_self, tool_input=tool_input)

        return run


class CurrentWebPageToolAsyncPatch(GenericPatch):
    def __init__(self, cassette: Cassette):
        super().__init__(cassette, CurrentWebPageTool, "arun")

    def get_same_signature_override(self) -> Callable:
        async def arun(og_self: CurrentWebPageTool, tool_input: Dict) -> str:
            return await self.generic_override(og_self, tool_input=tool_input)

        return arun


def get_overridden_build(og_build: Callable) -> Callable:
    def build(og_self: CassettePatcherBuilder) -> Iterable[Any]:
        patches = [patcher(og_self._cassette) for patcher in CUSTOM_PATCHERS]
        return itertools.chain(og_build(og_self), patches)

    return build


class ExtractHyperlinksToolPatch(GenericPatch):
    def __init__(self, cassette: Cassette):
        super().__init__(cassette, ExtractHyperlinksTool, "run")

    def get_same_signature_override(self) -> Callable:
        def run(og_self: ExtractHyperlinksTool, tool_input: Dict) -> str:
            return self.generic_override(og_self, tool_input=tool_input)

        return run


class ExtractHyperlinksToolAsyncPatch(GenericPatch):
    def __init__(self, cassette: Cassette):
        super().__init__(cassette, ExtractHyperlinksTool, "arun")

    def get_same_signature_override(self) -> Callable:
        async def arun(og_self: ExtractHyperlinksTool, tool_input: Dict) -> str:
            return await self.generic_override(og_self, tool_input=tool_input)

        return arun


class ExtractTextToolPatch(GenericPatch):
    def __init__(self, cassette: Cassette):
        super().__init__(cassette, ExtractTextTool, "run")

    def get_same_signature_override(self) -> Callable:
        def run(og_self: ExtractTextTool, tool_input: Dict) -> str:
            return self.generic_override(og_self, tool_input=tool_input)

        return run


class ExtractTextToolAsyncPatch(GenericPatch):
    def __init__(self, cassette: Cassette):
        super().__init__(cassette, ExtractTextTool, "arun")

    def get_same_signature_override(self) -> Callable:
        async def arun(og_self: ExtractTextTool, tool_input: Dict) -> str:
            return await self.generic_override(og_self, tool_input=tool_input)

        return arun


class GetElementsToolPatch(GenericPatch):
    def __init__(self, cassette: Cassette):
        super().__init__(cassette, GetElementsTool, "run")

    def get_same_signature_override(self) -> Callable:
        def run(og_self: GetElementsTool, tool_input: Dict) -> str:
            return self.generic_override(og_self, tool_input=tool_input)

        return run


class GetElementsToolAsyncPatch(GenericPatch):
    def __init__(self, cassette: Cassette):
        super().__init__(cassette, GetElementsTool, "arun")

    def get_same_signature_override(self) -> Callable:
        async def arun(og_self: GetElementsTool, tool_input: Dict) -> str:
            return await self.generic_override(og_self, tool_input=tool_input)

        return arun


class NavigateBackToolPatch(GenericPatch):
    def __init__(self, cassette: Cassette):
        super().__init__(cassette, NavigateBackTool, "run")

    def get_same_signature_override(self) -> Callable:
        def run(og_self: NavigateBackTool, tool_input: Dict) -> str:
            return self.generic_override(og_self, tool_input=tool_input)

        return run


class NavigateBackToolAsyncPatch(GenericPatch):
    def __init__(self, cassette: Cassette):
        super().__init__(cassette, NavigateBackTool, "arun")

    def get_same_signature_override(self) -> Callable:
        async def arun(og_self: NavigateBackTool, tool_input: Dict) -> str:
            return await self.generic_override(og_self, tool_input=tool_input)

        return arun


CassettePatcherBuilder.build = get_overridden_build(CassettePatcherBuilder.build)
# add this after overriding the above build function, to make sure that users of this
# library can also add their own custom patchers in
add_patchers(
    PythonREPLPatch,
    BashProcessPatch,
    NavigateToolPatch,
    NavigateToolAsyncPatch,
    ClickToolPatch,
    ClickToolAsyncPatch,
    CurrentWebPageToolPatch,
    CurrentWebPageToolAsyncPatch,
    ExtractHyperlinksToolPatch,
    ExtractHyperlinksToolAsyncPatch,
    ExtractTextToolPatch,
    ExtractTextToolAsyncPatch,
    GetElementsToolPatch,
    GetElementsToolAsyncPatch,
    NavigateBackToolPatch,
    NavigateBackToolAsyncPatch,
)
