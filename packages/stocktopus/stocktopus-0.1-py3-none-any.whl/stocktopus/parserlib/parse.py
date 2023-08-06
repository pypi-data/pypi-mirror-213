from ..types import Position, Trade, _Position


def combine(positions: dict[str, _Position], trades: list[Trade]) -> list[Position]:
    shares = set(positions.keys()) | {x["isin"] for x in trades}
    return [
        {
            "isin": x,
            "total": positions[x]["total"] if x in positions else 0,
            "value": positions[x]["value"] if x in positions else 0,
            "trades": [y for y in trades if y["isin"] == x],
        }
        for x in shares
    ]
