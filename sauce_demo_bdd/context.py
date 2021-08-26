from typing import Mapping, Sequence
from behave.runner import Context

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from sauce_demo_bdd.browser import Browser


class SauceDemoContext(Context):
    """Dummy type used for assistance with static analysis."""

    driver: WebDriver
    wait: WebDriverWait
    browser: Browser
    browser_data: dict
    scenario_start_time: float
    users: Sequence[Mapping]
    user: Mapping
    item_added_to_cart: WebElement
