import typer
from typing_extensions import Annotated

from ._version import __version__
from .degiro.main import convert as degiro
from .interactive_brokers.main import convert as ib
from .process import process as process_input

app = typer.Typer(no_args_is_help=True)


def version_callback(value: bool):
    if value:
        print(f"version: {__version__}")
        raise typer.Exit()


@app.callback()
def common(
    ctx: typer.Context,
    version: bool = typer.Option(None, "--version", callback=version_callback),
):
    pass


@app.command()
def process(
    _input: Annotated[str, typer.Option("--input", help="path to trades.yml input file")] = "taxes.yml"
) -> None:
    return process_input(_input)


app.command("degiro")(degiro)
app.command("ib")(ib)


def main():
    app()
