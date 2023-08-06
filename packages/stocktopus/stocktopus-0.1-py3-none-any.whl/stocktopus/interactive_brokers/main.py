import typer
import yaml
from typing_extensions import Annotated

from ..parserlib.load import load_xml
from .parse import parse

app = typer.Typer(no_args_is_help=True)


@app.command()
def convert(
    _input: Annotated[str, typer.Option("--input", help="path to trades.xml input file")] = "tax.xml",
    output: Annotated[str, typer.Option(help="path to trades.yml output file")] = "taxes.yml",
) -> None:
    data = load_xml(_input)
    data2 = parse(data)
    with open(output, "w+") as fh:
        yaml.safe_dump(data2, fh)
