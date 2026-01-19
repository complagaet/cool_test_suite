import pytest
import os
from pytest_html import extras

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver") 
        if driver:
            screenshots_dir = os.path.join(os.getcwd(), "screenshots")
            os.makedirs(screenshots_dir, exist_ok=True)

            screenshot_path = os.path.join(screenshots_dir, f"{item.name}.png")
            driver.save_screenshot(screenshot_path)

            if hasattr(report, "extra"):
                report.extra.append(extras.image(screenshot_path))

def pytest_configure(config):
    if config.pluginmanager.hasplugin("html"):
        config._metadata = getattr(config, "_metadata", {})
        config._metadata["Project Name"] = "Cool Test Suite"
        config._metadata["Tester"] = "Pasha"