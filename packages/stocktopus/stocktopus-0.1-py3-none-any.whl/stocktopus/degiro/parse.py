from dateutil import parser

from ..parserlib.parse import combine
from ..types import Position, Trade, TradeType, _Position


def parse(portfolio: list[dict], transactions: list[dict]) -> list[Position]:
    positions: dict[str, _Position] = {
        x["ISIN"]: {
            "isin": x["ISIN"],
            "total": abs(float(x["Anzahl"])),
            "value": abs(float(x["Wert in CHF"])),
        }
        for x in portfolio
        if x["ISIN"]
    }
    trades: list[Trade] = [
        {
            "isin": x["ISIN"],
            "datetime": parser.parse(f'{x["Datum"]} {x["Uhrzeit"]}'),
            "price": abs(float(x["Wert in Lokalwährung"])),
            "quantity": abs(float(x["Anzahl"])),
            "type": TradeType.BUY if float(x["Anzahl"]) >= 0 else TradeType.SELL,
        }
        for x in transactions
    ]
    return combine(positions, trades)
