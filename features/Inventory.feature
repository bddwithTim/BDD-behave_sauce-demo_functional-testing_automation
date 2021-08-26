@feature
Feature: Inventory page
  This feature covers functional tests inside the Inventory page of the Saucedemo site.

  Background:
    Given I am logged into the site
    And the saucedemo products page is displayed

  @positive @smoke
  Scenario Outline: Sorting the products
    When I sort the products by <sort_order> order
    Then the products page is sorted in <sort_order> order

  Examples: Sort the products
    | sort_order          |
    | Name (A to Z)       |
    | Name (Z to A)       |
    | Price (low to high) |
    | Price (high to low) |


  @positive @smoke
  Scenario: Adding items and resetting the application state
    When I add the item "Sauce Labs Backpack" into the cart
    Then the item is added to the cart
    When I click the menu icon
    And I click the Logout sidebar link
    Then the saucedemo Login page is displayed
