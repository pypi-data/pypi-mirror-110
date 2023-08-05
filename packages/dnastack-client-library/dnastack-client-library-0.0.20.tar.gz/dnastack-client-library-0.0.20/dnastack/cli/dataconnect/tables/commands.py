import click
from dnastack.client import *


@click.group()
@click.pass_context
def tables(ctx):
    pass


@tables.command(name="list")
@click.pass_context
def list_tables(ctx):
    click.echo(dataconnect_client.list_tables(ctx.obj["data-connect-url"]))


@tables.command()
@click.pass_context
@click.argument("table_name")
def get(ctx, table_name):
    click.echo(dataconnect_client.get_table(ctx.obj["data-connect-url"], table_name))
