from datetime import date

from attrs import define
from pydash import py_
from rich import box
from rich.table import Table

from nutorious.config import ColumnConfig, Config
from nutorious.context import Context
from nutorious.model import Day, Meal, Food
from nutorious.report.base import BaseOptions, display_report
from nutorious.ui import create_tree_row


@define
class DailyReportOptions(BaseOptions):
    dt: date


def display_daily_report(options: DailyReportOptions):
    display_report(options, __build_daily_table)


def __build_daily_table(ctx: Context):
    config = ctx.config
    journal = ctx.journal
    options: DailyReportOptions = ctx.options
    columns = config.ui.daily.columns

    table = __create_report_table(config, options.dt)

    day = journal.closest_day(options.dt)

    traverse_report_node_fn = __travere_report_node(columns)

    day_row = create_tree_row(
        columns,
        root=day,
        traverse_fn=traverse_report_node_fn,
        extract_value_fn=__extract_column_value,
    )
    table.add_row(*day_row)

    for meal in day.meals:
        meal_row = create_tree_row(
            columns,
            root=meal,
            traverse_fn=traverse_report_node_fn,
            extract_value_fn=__extract_column_value,
        )
        table.add_row(*meal_row)

    return table


def __create_report_table(config: Config, dt: date):
    report_config = config.ui.daily

    table = Table(
        title=report_config.title.format(dt=dt),
        title_style="black on green",
        header_style="bold magenta",
        show_lines=True,
        box=box.MINIMAL_DOUBLE_HEAD,
    )

    for column in report_config.columns:
        # noinspection PyTypeChecker
        table.add_column(
            column.title,
            style=column.style,
            justify=column.justify,
            no_wrap=True,
        )

    return table


def __travere_report_node(report_columns: list[ColumnConfig]):
    report_column_names = py_.map(report_columns, lambda c: c.data)

    def traverse_fn(node):
        if isinstance(node, Day):
            return None
        if isinstance(node, Food):
            return py_.filter(node.ingredients, lambda i: i.name not in report_column_names)

    return traverse_fn


def __extract_column_value(column: ColumnConfig, node):
    if column.data == "title":
        return node.title

    if column.data == "amount":
        if isinstance(node, Meal) or isinstance(node, Day):
            return None
        return node.amount

    return node.amount_of(column.data)
