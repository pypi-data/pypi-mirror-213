from collections.abc import Callable
from datetime import datetime
from enum import Enum
from typing import TypeAlias, TypedDict, TypeVar

from selenium.webdriver import Chrome, Edge, Firefox, Ie, Safari
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

T = TypeVar("T")
AnyDriver = Chrome | Firefox | Safari | Ie | Edge
Driver: TypeAlias = WebDriver | WebElement
Condition: TypeAlias = Callable[[AnyDriver], T]
Locator: TypeAlias = tuple[str, str]
ConditionFnc: TypeAlias = Callable[[Locator], Condition[T]]


class TradeType(Enum):
    BUY = "BUY"
    SELL = "SELL"


Trade = TypedDict(
    "Trade",
    {
        "isin": str,
        "datetime": datetime,
        "price": float | int,
        "quantity": float | int,
        # "type" is a keyword, so the functional syntax is necessary
        "type": TradeType,
    },
)


class _Position(TypedDict):
    isin: str
    total: float | int
    value: float | int


class Position(_Position):
    trades: list[Trade]
