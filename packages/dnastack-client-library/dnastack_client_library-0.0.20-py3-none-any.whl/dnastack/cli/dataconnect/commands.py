from .tables import commands as tables_commands
from dnastack.cli.utils import assert_config, get_config
from dnastack.client import *


@click.group()
@click.pass_context
def dataconnect(ctx):
    assert_config(ctx, "data-connect-url", str)


@dataconnect.command()
@click.pass_context
@click.argument("q")
@click.option("-d", "--download", is_flag=True)
@click.option("-r", "--raw", is_flag=True)
@click.option(
    "-f",
    "--format",
    type=click.Choice(["json", "csv"]),
    show_choices=True,
    default="json",
    show_default=True,
)
def query(ctx, q, download, raw, format="json"):
    click.echo(
        dataconnect_client.query(
            get_config(ctx, "data-connect-url", str),
            q,
            download,
            "csv"
            if raw
            else format,  # we need to make the -r/--raw command backwards compatible so override -f if -r is used
            raw,
        )
    )


dataconnect.add_command(tables_commands.tables)
