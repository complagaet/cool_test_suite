import os

from dotenv import load_dotenv
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="function")
def driver():
    load_dotenv()
    run_on = os.getenv("RUN_ON", "local").strip().lower()

    if run_on == "cloud":
        bs_user = os.getenv("BROWSERSTACK_USERNAME")
        bs_key = os.getenv("BROWSERSTACK_ACCESS_KEY")
        if not bs_user or not bs_key:
            raise RuntimeError("BrowserStack credentials are not set (BROWSERSTACK_USERNAME/BROWSERSTACK_ACCESS_KEY).")

        browser = os.getenv("BROWSER", "chrome").strip().lower()
        if browser not in {"chrome", "firefox", "edge", "safari"}:
            raise RuntimeError("Unsupported BROWSER. Use chrome, firefox, edge, or safari.")

        options = Options()
        options.set_capability("browserName", browser)
        options.set_capability("browserVersion", "latest")
        options.set_capability(
            "bstack:options",
            {
                "os": "Windows",
                "osVersion": "11",
                "sessionName": "Assignment 6 DDT",
                "projectName": "Cool Test Suite",
            },
        )

        driver = webdriver.Remote(
            command_executor=f"https://{bs_user}:{bs_key}@hub-cloud.browserstack.com/wd/hub",
            options=options,
        )
    else:
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-infobars")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.implicitly_wait(10)
    driver.set_page_load_timeout(30)

    yield driver

    driver.quit()
    
