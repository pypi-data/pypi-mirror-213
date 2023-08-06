"""cli"""
import click
from humanity_etl.tables.timeclocks import timeclocks


@click.command()
@click.option("--table")
def main(table: str) -> None:
    """program"""
    if table == "timeclocks":
        timeclocks()
    elif table == "ALL":
        timeclocks()
    else:
        raise ValueError("Invalid table selection")
