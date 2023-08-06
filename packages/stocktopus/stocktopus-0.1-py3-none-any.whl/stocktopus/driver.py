from collections.abc import Iterator
from contextlib import contextmanager

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .paramspec_from import paramspec_from
from .types import Condition, ConditionFnc, Driver, Locator, T

present: ConditionFnc[WebElement] = EC.presence_of_element_located
all_present: ConditionFnc[list[WebElement]] = EC.presence_of_all_elements_located
visible: ConditionFnc[WebElement | bool] = EC.visibility_of_element_located
clickable: ConditionFnc[WebElement | bool] = EC.element_to_be_clickable


@contextmanager
def driver() -> Iterator[WebDriver]:
    options = Options()
    with webdriver.Firefox(options=options) as driver:
        yield driver


def wait(driver: Driver, condition: Condition[T], timeout: float = 5, **kwargs) -> T:
    return WebDriverWait(driver, timeout=timeout, **kwargs).until(condition)


def find(driver: Driver, loc: Locator, **kwargs) -> WebElement:
    return wait(driver, present(loc), **kwargs)


def click(driver: Driver, loc: Locator, condition: ConditionFnc = clickable, **kwargs) -> None:
    elem = wait(driver, condition(loc), **kwargs)
    if not isinstance(elem, WebElement):
        raise ValueError("condition did not return valid element")
    elem.click()


@paramspec_from(find)
def is_present(*args, **kwargs) -> bool:
    try:
        find(*args, **kwargs, timeout=1)
        return True
    except TimeoutException:
        return False


def by_text(text: str, elem="*", relative: bool = False) -> Locator:
    return By.XPATH, f"{'.' if relative else ''}//{elem}[normalize-space(text())='{text}']"
