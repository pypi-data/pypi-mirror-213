import typer
import yaml
from typing_extensions import Annotated

from ..parserlib.load import load_csv
from .parse import parse


def convert(
    portfolio: Annotated[str, typer.Option(help="path to Portfolio.csv input file")] = "Portfolio.csv",
    transactions: Annotated[str, typer.Option(help="path to Transactions.csv input file")] = "Transactions.csv",
    output: Annotated[str, typer.Option(help="path to trades.yml output file")] = "taxes.yml",
) -> None:
    portfolio2 = load_csv(portfolio)
    transactions2 = load_csv(transactions)
    data = parse(portfolio2, transactions2)
    with open(output, "w+") as fh:
        yaml.safe_dump(data, fh)
