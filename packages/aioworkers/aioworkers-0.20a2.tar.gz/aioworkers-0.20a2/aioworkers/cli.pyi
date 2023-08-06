import argparse
from . import utils as utils
from .core import command as command
from .core.config import Config as Config
from .core.context import Context as Context, GroupResolver as GroupResolver
from .core.plugin import Plugin as Plugin, search_plugins as search_plugins
from typing import Any, Optional

parser: Any
group: Any
PROMPT: str

class PidFileType(argparse.FileType):
    def __call__(self, string: Any): ...

context: Any

def main(*config_files: Any, args: Optional[Any] = ..., config_dirs: Any = ..., commands: Any = ..., config_dict: Optional[Any] = ...): ...
def process_iter(cfg: Any): ...
def create_process(cfg: Any): ...
def loop_run(conf: Optional[Any] = ..., future: Optional[Any] = ..., group_resolver: Optional[Any] = ..., ns: Optional[Any] = ..., cmds: Optional[Any] = ..., argv: Optional[Any] = ..., loop: Optional[Any] = ..., prompt: Optional[Any] = ..., process_name: Optional[Any] = ...): ...

class UriType(argparse.FileType):
    def __call__(self, string: Any): ...

class ExtendAction(argparse.Action):
    def __call__(self, parser: Any, namespace: Any, values: Any, option_string: Optional[Any] = ...) -> None: ...

class plugin(Plugin):
    def add_arguments(self, parser: Any) -> None: ...

def main_with_conf(*args: Any, **kwargs: Any) -> None: ...
