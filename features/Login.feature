@feature
Feature: Login page
  This feature covers functional tests inside the login page of the Saucedemo site.

  Background:
    Given the saucedemo login page is displayed

  @positive @smoke
  Scenario: Log into the site using standard user credentials
    When I enter the 'standard_user' email address
    And I enter the password
    And I click the Login button
    Then the saucedemo products page is displayed

  @positive @smoke
  Scenario: Log out from the site
    Given I am logged into the site
    When I click the menu icon
    Then the menu sidebar is displayed
    When I click the Logout sidebar link
    Then the saucedemo login page is displayed

  @positive @smoke
  Scenario: Logging in using problem user credentials
    When I enter the 'problem_user' email address
    And I enter the password
    And I click the Login button
    Then the saucedemo products page is displayed


  @negative
  Scenario: Logging in with an incorrect password
    When I enter the 'standard_user' email address
    And I enter an incorrect password
    And I click the Login button
    Then this error message is displayed
    """
    Epic sadface: Username and password do not match any user in this service
    """
