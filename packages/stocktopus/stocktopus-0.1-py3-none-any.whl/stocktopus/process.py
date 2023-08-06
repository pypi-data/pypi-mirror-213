from time import sleep

import yaml
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from tipsy import cast_to_type

from .driver import Driver, by_text, click, driver, find, is_present, present
from .types import Position, Trade


def find_via_label(driver: Driver, text: str) -> WebElement:
    relative = isinstance(driver, WebElement)
    label = find(driver, by_text(text, elem="label", relative=relative))
    identifier = label.get_attribute("for")
    if identifier is None:
        raise ValueError(f"label {text} did not define a 'for' attribute")
    return find(driver, (By.ID, identifier))


def click_button(driver: Driver, text: str, elem="button/span") -> None:
    relative = isinstance(driver, WebElement)
    click(driver, by_text(text, elem=elem, relative=relative))


def get_driver(driver: Driver) -> WebDriver:
    return driver.parent if isinstance(driver, WebElement) else driver


def click_dropdown(driver: Driver, text: str) -> None:
    elem = find_via_label(driver, text)
    get_driver(driver).execute_script("arguments[0].scrollIntoView()", elem)
    _id = elem.get_attribute("id")
    if _id is None:
        raise ValueError(f"dropdown {text} did not define a 'id' attribute")
    # somehow this element is never 'visible' nor 'clickable'
    # so we just wait for it to be 'present'
    # unfortunately it is present already before we scrolled down,
    # we cannot wait for 'scrollIntoView' to complete
    # so we just wait for a second here
    sleep(1)
    click(driver, (By.ID, _id), condition=present)


def repr_number(n: float) -> str:
    # after 1000, the browser is 'smart' and humanizes the input
    # in the process it drops the '.' character.
    # this means that numbers like 1'234.56, will actually
    # be inputted as 123'456 instead, leading to wrong results
    # hitting the '.' again avoids this issue
    # this is simulated here by duplicating the character.
    return "..".join(f"{n}".split(".")) if n >= 1000 else f"{n}"


def enter_trade(d: Driver, trade: Trade) -> None:
    click_button(d, "Art/Grund")
    click_dropdown(d, ("Kauf" if trade["type"] == "BUY" else "Verkauf"))
    find_via_label(d, "Datum").send_keys(trade["datetime"].strftime("%d.%m.%Y"))
    find_via_label(d, "Stückzahl").send_keys(repr_number(trade["quantity"]))
    click_button(d, "Schliessen")


def enter_stock(d: Driver, stock: Position) -> None:
    find_via_label(d, "ISIN").send_keys(stock["isin"])
    click_button(d, "Wertschrift suchen")
    if is_present(
        d,
        by_text(
            "Der steuerbare Ertrag konnte bis zum Zeitpunkt "
            "der Drucklegung nicht ermittelt werden "
            "und wird später festgesetzt."
        ),
    ):
        # disclaimer modal opens which informs you that
        # this stock might not be correctly tracked
        click_button(d, "OK")
    find_via_label(d, "Stückzahl").send_keys(repr_number(stock["total"]))
    if is_present(d, by_text("Steuerwert")):
        # value of that stock was not known
        # needs to be manually entered
        find_via_label(d, "Steuerwert").send_keys(repr_number(stock["value"]))


def process(path: str):
    with open(path) as fh:
        data = yaml.safe_load(fh)
        positions = cast_to_type(data, list[Position])
    with driver() as d:
        d.get("https://www.services.zh.ch/app/ZHprivateTax2022/#/demo/home")
        if is_present(d, by_text("Willkommen zu ZHprivateTax, der papierlosen Steuererklärung")):
            click(d, (By.CLASS_NAME, "close-icon"))
        d.get("https://www.services.zh.ch/app/ZHprivateTax2022/#/demo/tax-assistant/securities/securities")
        click_button(d, "Andere Wertschrift hinzufügen", elem="button")
        for idx, stock in enumerate(positions):
            if idx > 0:
                click_button(d, "Übernehmen & nächster Eintrag")
            if is_present(d, by_text("Überprüfen Sie Ihre Eingabe")):
                # disclaimer modal opens which informs you that
                # the trades dont match up with the total value
                # at the end of the year
                input("Press Enter to continue...")
            if is_present(d, by_text("Deklaration im DA-1")):
                # disclaimer modal opens which informs you that
                # you could declare this stock in DA-1 form
                # to get your US tax on dividends back
                input("Press Enter to continue...")
            enter_stock(d, stock)
            for trade in stock["trades"]:
                click_button(d, "Weitere Zeile hinzufügen")
                modal = find(d, (By.CLASS_NAME, "zhp-modal"))
                enter_trade(modal, trade)
        click_button(d, "Übernehmen & schliessen")
