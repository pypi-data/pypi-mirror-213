from rich import box
from rich.console import Console
from rich.table import Table

table = Table(
    title="TheT",
    title_style="bold magenta",
    header_style="bold magenta",
    box=box.MINIMAL_DOUBLE_HEAD,
    show_lines=False,
)
table.add_column("title", style="cyan", no_wrap=True)
table.add_column("amount", justify="right", style="green", no_wrap=True)

table.add_row("t1", "a1")
table.add_row("t2", "a2")
table.add_row("t3", "a3")

console = Console()
console.print()
console.print(table)
