from typing import Any

import click

journal_path_param_type = click.Path(resolve_path=True, exists=True, file_okay=False)
date_param_type = click.DateTime(formats=["%Y-%m-%d"])


def option_journal_path():
    return click.option(
        "--journal_path",
        "--j",
        type=journal_path_param_type,
        default="./",
        help="Path to the journal directory. Default: current directory.",
    )


def option_watch():
    return click.option(
        "--watch",
        "--w",
        is_flag=True,
        default=False,
        show_default=True,
        help="Show live view of the report and update it, when journal files change.",
    )


def option_date(*names: str, **attrs: Any):
    return click.option(*names, type=date_param_type, **attrs)
