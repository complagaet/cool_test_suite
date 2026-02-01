import csv
import logging
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fixtures.driver_fixture import driver


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def _load_test_data():
    data_path = Path(__file__).resolve().parents[1] / "data" / "test_data.xlsx"
    df = pd.read_excel(data_path)
    return df.to_dict(orient="records")

def _write_result(row, status, actual_text=""):
    results_dir = Path(__file__).resolve().parents[1] / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    results_path = results_dir / "ddt_results.csv"

    file_exists = results_path.exists()
    with results_path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(
                [
                    "timestamp_utc",
                    "case_id",
                    "username",
                    "password",
                    "expected_result",
                    "expected_text",
                    "actual_text",
                    "status",
                ]
            )
        writer.writerow(
            [
                datetime.now(timezone.utc).isoformat(timespec="seconds"),
                row.get("case_id", ""),
                row.get("username", ""),
                row.get("password", ""),
                row.get("expected_result", ""),
                row.get("expected_text", ""),
                actual_text,
                status,
            ]
        )

@pytest.mark.parametrize("row", _load_test_data())
def test_login_ddt_excel(driver, row):
    base_url = "https://sultan-it-solutions-admin.vercel.app"
    wait = WebDriverWait(driver, 12)

    logging.info("Opening login page. case_id=%s", row["case_id"])
    driver.get(base_url)

    username_input = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Username']"))
    )
    password_input = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Password']"))
    )
    username_input.clear()
    username_input.send_keys(str(row["username"]))
    password_input.clear()
    password_input.send_keys(str(row["password"]))

    login_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Login!')]"))
    )
    login_button.click()

    expected_result = str(row["expected_result"]).strip().lower()
    expected_text = str(row["expected_text"])

    if expected_result == "success":
        header = wait.until(
            EC.presence_of_element_located((By.XPATH, "//h1[contains(text(),'Заявки')]"))
        )
        assert expected_text in header.text
        _write_result(row, "PASSED", actual_text=header.text)
        logging.info("PASSED case_id=%s (success)", row["case_id"])
    else:
        login_header = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//h2[text()='Login']"))
        )
        assert expected_text in login_header.text
        _write_result(row, "PASSED", actual_text=login_header.text)
        logging.info("PASSED case_id=%s (failure)", row["case_id"])
