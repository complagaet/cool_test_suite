import pytest
import os
from pytest_html import extras

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Execute all other hooks to obtain the report object
    outcome = yield
    report = outcome.get_result()

    # Check if the test failed
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")  # Get the WebDriver instance from the test
        if driver:
            # Ensure the screenshots directory exists
            screenshots_dir = os.path.join(os.getcwd(), "screenshots")
            os.makedirs(screenshots_dir, exist_ok=True)

            # Capture screenshot on failure
            screenshot_path = os.path.join(screenshots_dir, f"{item.name}.png")
            driver.save_screenshot(screenshot_path)

            # Attach the screenshot to the HTML report
            if hasattr(report, "extra"):
                report.extra.append(extras.image(screenshot_path))

# Add a hook to configure pytest-html
def pytest_configure(config):
    # Check if pytest-html is installed and add metadata
    if config.pluginmanager.hasplugin("html"):
        config._metadata = getattr(config, "_metadata", {})
        config._metadata["Project Name"] = "Cool Test Suite"
        config._metadata["Tester"] = "Your Name"