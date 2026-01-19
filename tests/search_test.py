import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fixtures.driver_fixture import driver
from selenium.webdriver.support.wait import TimeoutException

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_open_bugintenders(driver):
    logging.info("Opening Bugintenders website.")
    driver.get("https://bugintenders.lukoyanov.love")
    wait = WebDriverWait(driver, 5) 

    logging.info("Checking if the page title contains 'Bügın’ Tenders'.")
    assert "Bügın’ Tenders" in driver.title

def test_search_product(driver):
    logging.info("Opening Bugintenders website.")
    driver.get("https://bugintenders.lukoyanov.love")
    wait = WebDriverWait(driver, 5) 

    logging.info("Locating the search input field.")
    search_input = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'input[placeholder="Асхана үстелі..."]')
        )
    )

    logging.info("Clearing and entering search term: 'стол'.")
    search_input.clear()
    search_input.send_keys("стол")
    search_input.send_keys(Keys.ENTER)

    logging.info("Waiting for search results to appear.")
    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//h1[contains(text(),'Хабарландырулар')]")
        )
    )

    logging.info("Waiting for the notification button to be clickable.")
    wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(., 'Хабарландыруды ашу')]")
        )
    )

    assert "Хабарландыруды ашу" in driver.page_source
