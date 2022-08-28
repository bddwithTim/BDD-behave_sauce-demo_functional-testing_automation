from urllib import parse

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options as ChromeOptions

from sauce_demo_bdd import get_config


def chrome_options():
    _chrome_options = ChromeOptions()
    config = get_config()

    extensions = (config["browser"]["extensions"],)
    gpu = (config["browser"]["gpu"],)
    headless = config["browser"]["headless"]
    window_size = config["browser"]["size"]

    if not extensions:
        _chrome_options.add_argument("--disable-extensions")
    if not gpu:
        _chrome_options.add_argument("--disable-gpu")
    if window_size:
        _chrome_options.add_argument(f"--window-size={window_size}")
    if headless:
        _chrome_options.add_argument("--headless")
        _chrome_options.add_argument("--load-images=no")
        _chrome_options.add_argument("--window-position=1,0")
        # driver.manage().window().maximize() doesn't work
        # in headless mode. Therefore setting the window size directly.
        # sample sizes: 1024x768, 1920x1080
        if not window_size:
            _chrome_options.add_argument("--window-size=1200,1100")
    else:
        if not window_size:
            _chrome_options.add_argument("--start-maximized")
        _chrome_options.add_argument("--disable-infobars")

    return _chrome_options


class Browser:
    """
    Utility class for handling Browser operations.
    """

    def __init__(self, driver: WebDriver, base_url: str) -> None:
        self.driver = driver
        self.base_url = base_url

    def wait(self, parent_elem: WebElement = None, timeout: int = 10) -> WebDriverWait:
        parent = parent_elem or self.driver
        return WebDriverWait(parent, timeout)

    def open(self, url: str, reopen: bool = False) -> None:
        """Open an absolute URL."""
        if self.driver.current_url == url and not reopen:
            return
        self.driver.get(url)

    def open_relative(self, url: str, reopen: bool = False) -> None:
        """Open a relative URL from the `base_url`."""
        target = parse.urljoin(self.base_url, url)
        if self.driver.current_url == target and not reopen:
            return
        self.driver.get(target)
        self.wait().until(ec.url_to_be(target))
