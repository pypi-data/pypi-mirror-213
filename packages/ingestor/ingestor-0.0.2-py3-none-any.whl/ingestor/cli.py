import click

from ingest import ingest
from load import load


@click.group()
def cli():
    pass


cli.add_command(ingest)
cli.add_command(load)
