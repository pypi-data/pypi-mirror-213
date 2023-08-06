import pathlib
import sys

import click

try:
    from ingestor.ingest import ingest
    from ingestor.load import load
except (ImportError, ModuleNotFoundError):
    sys.path.insert(0, pathlib.Path(__file__).parent.parent.as_posix())
    from ingestor.ingest import ingest
    from ingestor.load import load


@click.group()
def cli():
    pass


cli.add_command(ingest)
cli.add_command(load)


if __name__ == "__main__":
    cli()
