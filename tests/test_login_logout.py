import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from fixtures.driver_fixture import driver

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_login_logout(driver):
    logging.info("Opening Sultan IT Solutions Admin website.")
    driver.get("https://sultan-it-solutions-admin.vercel.app")
    wait = WebDriverWait(driver, 10)

    logging.info("Locating and entering username.")
    username_input = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Username']"))
    )
    username_input.clear()
    username_input.send_keys("complagaet")

    logging.info("Locating and entering password.")
    password_input = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Password']"))
    )
    password_input.clear()
    password_input.send_keys("123")

    logging.info("Clicking the login button.")
    login_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Login!')]"))
    )
    login_button.click()

    logging.info("Verifying the header text after login.")
    header = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//h1[contains(text(),'Заявки')]")
        )
    )

    assert "Заявки" in header.text

    logging.info("Locating and clicking the menu button for logout.")
    menu_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button:has(svg.lucide-menu)"))
    )
    menu_button.click()


    logging.info("Locating and clicking the logout button.")
    logout_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[.//span[text()='Выход']]")
        )
    )
    logout_button.click()

    logging.info("Verifying the login header text after logout.")
    login_header = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//h2[text()='Login']"))
    )

    assert "Login" in login_header.text

def test_always_fail(driver):
    driver.get("https://sultan-it-solutions-admin.vercel.app")
    wait = WebDriverWait(driver, 10)

    # Login first
    username_input = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Username']"))
    )
    username_input.clear()
    username_input.send_keys("complagaet")

    password_input = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Password']"))
    )
    password_input.clear()
    password_input.send_keys("123")

    login_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Login!')]")
    ))
    login_button.click()

    menu_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button:has(svg.lucide-menu)"))
    )

    actions = ActionChains(driver)
    actions.move_to_element(menu_button).perform()
    menu_button.click()       

    sidebar = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "div.text-card-foreground")
        )
    )

    #assert sidebar.is_displayed()
    assert False
