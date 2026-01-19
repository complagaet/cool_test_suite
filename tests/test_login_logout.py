import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from fixtures.driver_fixture import driver

def test_login_logout(driver):
    driver.get("https://sultan-it-solutions-admin.vercel.app")
    wait = WebDriverWait(driver, 10)

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
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Login!')]"))
    )
    login_button.click()

    header = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//h1[contains(text(),'Заявки')]")
        )
    )

    assert "Заявки" in header.text

    # --- Logout ---
    menu_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button:has(svg.lucide-menu)"))
    )
    menu_button.click()


    logout_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[.//span[text()='Выход']]")
        )
    )
    logout_button.click()

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
