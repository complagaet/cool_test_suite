import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fixtures.driver_fixture import driver
from selenium.webdriver.support.wait import TimeoutException


def test_open_bugintenders(driver):
    driver.get("https://bugintenders.lukoyanov.love")
    wait = WebDriverWait(driver, 5) 

    assert "Bügın’ Tenders" in driver.title

def test_search_product(driver):
    driver.get("https://bugintenders.lukoyanov.love")
    wait = WebDriverWait(driver, 5) 

    search_input = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'input[placeholder="Асхана үстелі..."]')
        )
    )

    search_input.clear()
    search_input.send_keys("стол")
    search_input.send_keys(Keys.ENTER)

    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//h1[contains(text(),'Хабарландырулар')]")
        )
    )

    wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(., 'Хабарландыруды ашу')]")
        )
    )

    assert "Хабарландыруды ашу" in driver.page_source
