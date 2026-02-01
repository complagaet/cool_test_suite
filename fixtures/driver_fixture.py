import os

from dotenv import load_dotenv
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()

_raw_browsers = os.getenv("BROWSER", "chrome")
_browser_list = [b.strip().lower() for b in _raw_browsers.split(",") if b.strip()]
if not _browser_list:
    _browser_list = ["chrome"]


@pytest.fixture(scope="function", params=_browser_list)
def driver(request):
    run_on = os.getenv("RUN_ON", "local").strip().lower()
    browser = request.param

    if run_on == "cloud":
        bs_user = os.getenv("BROWSERSTACK_USERNAME")
        bs_key = os.getenv("BROWSERSTACK_ACCESS_KEY")
        if not bs_user or not bs_key:
            raise RuntimeError("BrowserStack credentials are not set (BROWSERSTACK_USERNAME/BROWSERSTACK_ACCESS_KEY).")

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
        if browser != "chrome":
            raise RuntimeError("Local run supports only Chrome. Use RUN_ON=cloud for other browsers.")

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
    
