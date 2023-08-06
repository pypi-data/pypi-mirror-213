from datetime import datetime

import click

from nutorious.cli import option_date, option_journal_path, option_watch
from nutorious.report.daily import DailyReportOptions, display_daily_report


@click.group()
def main():
    pass


@main.command()
@option_journal_path()
@option_date("--date", "--d", help="Date of the report. Default is 'today'.")
@option_watch()
def report(journal_path, date, watch):
    """
    Shows report on a date, closest to specified date.
    """

    date = datetime.today().date() if date is None else date.date()

    display_daily_report(DailyReportOptions(journal_path, watch, date))


@main.command()
@option_journal_path()
@option_date("--date1", "--d1", help="Date1 of the diff report. Default: yesterday.")
@option_date("--date2", "--d2", help="Date2 of the diff report. Default: today.")
@option_watch()
def diff(journal_path, date1, date2, watch):
    """Shows difference report between two dates"""

    click.echo(f"Diff report:")
    click.echo(f"  Journal: {journal_path}")
    click.echo(f"    Date1: {date1}")
    click.echo(f"    Date2: {date2}")
    click.echo(f"    Watch: {watch}")


if __name__ == "__main__":
    main()
