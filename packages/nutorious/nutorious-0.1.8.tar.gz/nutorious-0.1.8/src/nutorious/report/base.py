from __future__ import annotations

from typing import Callable

from attrs import define
from rich.console import Console
from rich.live import Live
from watchfiles import watch
from watchfiles.filters import DefaultFilter

from nutorious.config import load_config
from nutorious.context import Context
from nutorious.journal import load_journal


@define
class BaseOptions:
    journal_path: str
    watch: bool


class YmlFilesFilter(DefaultFilter):
    def __call__(self, change: "Change", path: str) -> bool:
        return path.endswith(".yml") and super().__call__(change, path)


def display_report(options: BaseOptions, build_report_table_fn: Callable[[Context], Table]):
    context = __load_context(options)

    if options.watch:
        with Live(build_report_table_fn(context), auto_refresh=False) as live:
            for changes in watch(options.journal_path, watch_filter=YmlFilesFilter()):
                context = __load_context(options)
                live.update(build_report_table_fn(context), refresh=True)
    else:
        console = Console()
        try:
            table = build_report_table_fn(context)
            console.print(table)
        except ValueError as e:
            console.print(f"[red]Error: {e}![/red]")


def __load_context(options: BaseOptions) -> Context:
    config = load_config(options.journal_path)
    journal = load_journal(config, options.journal_path)

    return Context(config, journal, options)
