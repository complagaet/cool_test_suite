from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from fixtures.driver_fixture import driver
import pytest


def test_book_flight(driver):
    driver.get("https://blazedemo.com/")

    assert "BlazeDemo" in driver.title

    from_port = Select(driver.find_element(By.NAME, "fromPort"))
    from_port.select_by_visible_text("Paris")

    to_port = Select(driver.find_element(By.NAME, "toPort"))
    to_port.select_by_visible_text("Buenos Aires")

    driver.find_element(By.CSS_SELECTOR, "input.btn.btn-primary").click()

    assert "BlazeDemo" in driver.title

    choose_buttons = driver.find_elements(By.CSS_SELECTOR, "input.btn.btn-small")
    choose_buttons[0].click()

    assert "BlazeDemo" in driver.title

    driver.find_element(By.ID, "inputName").send_keys("Pavel Lukoyanov")
    driver.find_element(By.ID, "address").send_keys("123 Qabanbay Ave")
    driver.find_element(By.ID, "city").send_keys("Astana")
    driver.find_element(By.ID, "state").send_keys("Kazakhstan")
    driver.find_element(By.ID, "zipCode").send_keys("010000")

    card_type = Select(driver.find_element(By.ID, "cardType"))
    card_type.select_by_value("visa")

    driver.find_element(By.ID, "creditCardNumber").send_keys("4111111111111111")
    driver.find_element(By.ID, "creditCardMonth").clear()
    driver.find_element(By.ID, "creditCardMonth").send_keys("12")
    driver.find_element(By.ID, "creditCardYear").clear()
    driver.find_element(By.ID, "creditCardYear").send_keys("2077")
    driver.find_element(By.ID, "nameOnCard").send_keys("Pavel Lukoyanov")

    driver.find_element(By.ID, "rememberMe").click()

    driver.find_element(By.CSS_SELECTOR, "input.btn.btn-primary").click()

    assert "BlazeDemo" in driver.title

    confirmation_text = driver.find_element(By.TAG_NAME, "h1").text
    assert "Thank you for your purchase" in confirmation_text or "Your flight" in confirmation_text
