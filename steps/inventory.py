from behave import when, then

from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from expects import expect, equal

from sauce_demo_bdd.context import SauceDemoContext


@when("I sort the products by {sort_order} order")
def step_impl_1(context: SauceDemoContext, sort_order: str):
    sort_option = context.driver.find_element_by_xpath(
        "//option[contains(text(),'{}')]".format(sort_order)
    )
    sort_option.click()


@then("the products page is sorted in {sort_order} order")
def step_impl_2(context: SauceDemoContext, sort_order: str):
    product_sort_container = context.driver.find_element_by_xpath(
        "//span[contains(text(),'{}')]".format(sort_order)
    )
    expect(product_sort_container.text.lower()).to(equal(sort_order.lower()))


@when('I add the item "{item_name}" into the cart')
def step_impl_3(context: SauceDemoContext, item_name: str):
    inventory_list = context.wait.until(
        ec.presence_of_all_elements_located(
            (By.XPATH, "//div[@class='inventory_item_name']")
        )
    )
    item_element = [item for item in inventory_list if item.text == item_name][0]
    add_to_cart_button = context.browser.wait(
        parent_elem=item_element, timeout=5
    ).until(
        ec.presence_of_element_located(
            (By.XPATH, "//button[contains(text(), 'Add to cart')]")
        )
    )
    add_to_cart_button.click()
    context.item_added_to_cart = item_element


@then("the item is added to the cart")
def step_impl_4(context: SauceDemoContext):
    if context.item_added_to_cart is None:
        raise ValueError("No item was added to the cart")
    cart_button = context.browser.wait(
        parent_elem=context.item_added_to_cart, timeout=5
    ).until(
        ec.presence_of_element_located(
            (By.XPATH, "//button[contains(text(), 'Remove')]")
        )
    )
    expect(cart_button.text.lower()).to(equal("Remove".lower()))
