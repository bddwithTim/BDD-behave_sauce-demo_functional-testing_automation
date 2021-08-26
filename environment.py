import time
import re

from pathlib import Path
from behave.model import Scenario
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver

from sauce_demo_bdd import get_config
from sauce_demo_bdd.browser import Browser, chrome_options
from sauce_demo_bdd.context import SauceDemoContext


def before_all(context: SauceDemoContext):
    data = get_config()

    context.driver = webdriver.Chrome(chrome_options=chrome_options())
    context.users = data["users"]
    context.user = data["users"][0]
    context.browser_data = data["browser"]
    context.browser = Browser(context.driver, context.browser_data["url"])
    context.wait = WebDriverWait(context.driver, 10)


def after_all(context: SauceDemoContext):
    context.driver.quit()


def before_scenario(context: SauceDemoContext, scenario: Scenario):
    context.scenario_start_time = time.time()


def after_scenario(context: SauceDemoContext, scenario: Scenario):
    if scenario.status == "failed":
        scenario_error_dir = Path("logs")
        scenario_error_dir.mkdir(exist_ok=True)
        base_name = time.strftime(
            "%Y-%m-%d_%H%M%S_{}".format(re.sub(r'[/\\:*?"<>#]', "", scenario.name)[:60])
        )
        log_file_path = scenario_error_dir / "{}.txt".format(base_name)
        for step in scenario.steps:
            if step.status in ["failed", "undefined"]:
                log_file_path.write_text(
                    "Scenario: {}\nStep: {} {}\nError Message: {}".format(
                        scenario.name, step.keyword, step.name, step.error_message
                    )
                )
                break
        else:
            log_file_path.write_text("Scenario: {}\nStep: N/A".format(scenario.name))
