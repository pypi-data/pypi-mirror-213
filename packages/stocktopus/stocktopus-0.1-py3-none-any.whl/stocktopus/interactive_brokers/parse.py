from dateutil import parser

from ..parserlib.parse import combine
from ..types import Position, Trade, _Position


def parse(data: dict) -> list[Position]:
    data = data["FlexQueryResponse"]["FlexStatements"]["FlexStatement"]
    positions: dict[str, _Position] = {
        x["@isin"]: {
            "isin": x["@isin"],
            "total": abs(float(x["@position"])),
            "value": abs(float(x["@positionValue"])),
        }
        for x in data["OpenPositions"]["OpenPosition"]
    }
    trades: list[Trade] = [
        {
            "isin": x["@isin"],
            "datetime": parser.parse(x["@dateTime"]),
            "price": abs(float(x["@tradePrice"])),
            "quantity": abs(float(x["@quantity"])),
            "type": x["@buySell"],
        }
        for x in data["Trades"]["Trade"]
        if x["@assetCategory"] == "STK"
    ]
    return combine(positions, trades)
