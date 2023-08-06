from __future__ import annotations

from attrs import define
from rich.console import Console

from nutorious.config import load_config
from nutorious.context import Context
from nutorious.journal import load_journal


@define
class BaseOptions:
    journal_path: str
    watch: bool


def display_report(options: BaseOptions, build_report_table_fn):
    console = Console()

    config = load_config(options.journal_path)
    journal = load_journal(config, options.journal_path)

    context = Context(config, journal, options)
    if options.watch:
        # TODO: implement the watch/update loop
        build_report_table_fn(context)
    else:
        try:
            table = build_report_table_fn(context)
            console.print(table)
        except ValueError as e:
            console.print(f"[red]Error: {e}![/red]")
