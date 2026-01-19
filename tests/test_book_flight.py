from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from fixtures.driver_fixture import driver
import pytest
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def test_book_flight(driver):
    logging.info("Navigating to BlazeDemo homepage.")
    driver.get("https://blazedemo.com/")

    logging.info("Checking if the page title contains 'BlazeDemo'.")
    assert "BlazeDemo" in driver.title, "Page title does not contain 'BlazeDemo'"

    logging.info("Selecting departure city: Paris.")
    from_port = Select(driver.find_element(By.NAME, "fromPort"))
    from_port.select_by_visible_text("Paris")

    logging.info("Selecting destination city: Buenos Aires.")
    to_port = Select(driver.find_element(By.NAME, "toPort"))
    to_port.select_by_visible_text("Buenos Aires")

    logging.info("Clicking on Find Flights button.")
    driver.find_element(By.CSS_SELECTOR, "input.btn.btn-primary").click()

    logging.info("Verifying the page title after searching for flights.")
    assert "BlazeDemo" in driver.title, "Page title does not contain 'BlazeDemo' after searching for flights."

    logging.info("Selecting the first available flight.")
    choose_buttons = driver.find_elements(By.CSS_SELECTOR, "input.btn.btn-small")
    choose_buttons[0].click()

    logging.info("Verifying the page title after selecting a flight.")
    assert "BlazeDemo" in driver.title, "Page title does not contain 'BlazeDemo' after selecting a flight."

    logging.info("Filling out passenger details.")
    driver.find_element(By.ID, "inputName").send_keys("Pavel Lukoyanov")
    driver.find_element(By.ID, "address").send_keys("123 Qabanbay Ave")
    driver.find_element(By.ID, "city").send_keys("Astana")
    driver.find_element(By.ID, "state").send_keys("Kazakhstan")
    driver.find_element(By.ID, "zipCode").send_keys("010000")

    logging.info("Selecting card type: Visa.")
    card_type = Select(driver.find_element(By.ID, "cardType"))
    card_type.select_by_value("visa")

    logging.info("Filling out payment details.")
    driver.find_element(By.ID, "creditCardNumber").send_keys("4111111111111111")
    driver.find_element(By.ID, "creditCardMonth").clear()
    driver.find_element(By.ID, "creditCardMonth").send_keys("12")
    driver.find_element(By.ID, "creditCardYear").clear()
    driver.find_element(By.ID, "creditCardYear").send_keys("2077")
    driver.find_element(By.ID, "nameOnCard").send_keys("Pavel Lukoyanov")

    logging.info("Clicking on Remember Me checkbox.")
    driver.find_element(By.ID, "rememberMe").click()

    logging.info("Submitting the purchase form.")
    driver.find_element(By.CSS_SELECTOR, "input.btn.btn-primary").click()

    logging.info("Verifying the page title after submitting the purchase form.")
    assert "BlazeDemo" in driver.title, "Page title does not contain 'BlazeDemo' after submitting the purchase form."

    logging.info("Checking the confirmation message.")
    confirmation_text = driver.find_element(By.TAG_NAME, "h1").text
    assert "Thank you for your purchase" in confirmation_text or "Your flight" in confirmation_text, "Confirmation message is incorrect."
