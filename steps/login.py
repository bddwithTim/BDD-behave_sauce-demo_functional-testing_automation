import time

from urllib import parse
from behave import given, when, then

from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from expects import expect, equal

from sauce_demo_bdd.context import SauceDemoContext


@given("the saucedemo {page_name} page is displayed")
def step_impl_1(context: SauceDemoContext, page_name: str):
    page_dict = {"login": "", "products": "inventory.html", "cart": "cart.html"}
    context.browser.open_relative(page_dict[page_name.lower()])


@when("I enter the '{user_account}' email address")
def step_impl_2(context: SauceDemoContext, user_account: str):
    user_name = context.wait.until(
        ec.presence_of_element_located((By.XPATH, "//input[@id='user-name']"))
    )
    user_name.send_keys(user_account)


@when("I enter the password")
def step_impl_3(context: SauceDemoContext):
    password = context.driver.find_element_by_xpath("//input[@id='password']")
    password.send_keys(context.user["password"])


@when("I click the Login button")
def step_impl_4(context: SauceDemoContext):
    login_button = context.driver.find_element_by_xpath("//input[@id='login-button']")
    login_button.click()


@then("the saucedemo {page_name} page is displayed")
def step_impl_5(context: SauceDemoContext, page_name: str):
    # create a dictionary for relative url reference
    page_dict = {"login": "", "products": "inventory.html", "cart": "cart.html"}
    expected_url = parse.urljoin(
        context.browser_data["url"], f"{page_dict[page_name.lower()]}"
    )

    context.wait.until(ec.url_matches(expected_url))


@given("I am logged into the site")
def step_impl_6(context: SauceDemoContext):
    if context.driver.current_url is not parse.urljoin(
        context.browser_data["url"], "inventory"
    ):
        context.execute_steps(
            """
            Given the saucedemo login page is displayed
            When I enter the 'standard_user' email address
            And I enter the password
            And I click the Login button
            """
        )


@when("I click the menu icon")
def step_impl_7(context: SauceDemoContext):
    menu_sidebar_icon = context.driver.find_element_by_xpath(
        "//button[@id='react-burger-menu-btn']"
    )
    menu_sidebar_icon.click()


@then("the menu sidebar is displayed")
def step_impl_8(context: SauceDemoContext):
    context.wait.until(
        ec.presence_of_element_located((By.XPATH, "//nav[@class='bm-item-list']"))
    )


@when("I click the {sidebar_link} sidebar link")
def step_impl_9(context: SauceDemoContext, sidebar_link: str):
    menu_sidebar = context.wait.until(
        ec.visibility_of_element_located((By.XPATH, "//div[@aria-hidden='false']"))
    )
    selected_sidebar_link = context.browser.wait(
        parent_elem=menu_sidebar, timeout=5
    ).until(
        ec.visibility_of_element_located(
            (
                By.XPATH,
                f"//a[@class='bm-item menu-item' and contains(text(),'{sidebar_link}')]",
            )
        )
    )

    selected_sidebar_link.click()


@when("I enter an incorrect password")
def step_impl_10(context: SauceDemoContext):
    password = context.driver.find_element_by_xpath("//input[@id='password']")
    password.send_keys(f'{context.user["password"]}{time.time()}')


@then("this error message is displayed")
def step_impl_11(context: SauceDemoContext):
    error_message = context.wait.until(
        ec.presence_of_element_located(
            (By.XPATH, f'//h3[contains(text(),"{context.text.strip()}")]')
        )
    )

    expect(error_message.text).to(equal(context.text.strip()))
