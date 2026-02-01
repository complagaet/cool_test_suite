# README for Cool Test Suite

This project contains a suite of automated tests for a software quality assurance assignment. The tests are written in Python and utilize the pytest framework for execution. Below is an overview of the project structure and instructions on how to set up and run the tests.

## Project Structure

- **`conftest.py`**: Contains shared fixtures and configurations for pytest.
- **`main.py`**: The main script for running the application.
- **`report.html`**: The test report generated after running the tests.
- **`requirements.txt`**: Lists the Python dependencies required for the project.
- **`fixtures/`**: Contains reusable fixtures for the tests.
  - `__init__.py`: Marks the directory as a Python package.
  - `driver_fixture.py`: Contains the fixture for setting up the web driver.
- **`screenshots/`**: Stores screenshots taken during test execution.
- **`tests/`**: Contains all the test cases.
  - `__init__.py`: Marks the directory as a Python package.
  - `search_test.py`: Contains test cases related to the search functionality.
  - `test_book_flight.py`: Contains test cases for booking a flight.
  - `test_login_logout.py`: Contains test cases for login and logout functionality.

## Setup Instructions

1. Clone the repository to your local machine.
2. Ensure you have Python 3 installed on your system.
3. Install the required dependencies by running the following command in the project directory:

   ```bash
   pip install -r requirements.txt
   ```

## Running the Tests

1. Navigate to the project directory in your terminal.
2. Run the following command to execute all the tests:

   ```bash
   pytest
   ```

3. To generate an HTML report of the test results, use the following command:

   ```bash
   pytest --html=report.html
   ```

4. After the tests are executed, you can find the test report in the `report.html` file in the project directory.

## Additional Notes

- Ensure that the necessary drivers (e.g., for Selenium) are installed and properly configured.
- Screenshots of failed tests will be saved in the `screenshots/` directory for debugging purposes.
- You can add more test cases in the `tests/` directory and define additional fixtures in the `fixtures/` directory as needed.

Happy Testing!

## Assignment 6: Data-Driven + Cross-Browser Testing

### Selected Website (Primary)

- `https://sultan-it-solutions-admin.vercel.app`

### Data-Driven Testing (Excel)

- Excel file: `data/test_data.xlsx`
- Test: `tests/test_ddt_login_excel.py`
- The test reads multiple rows from Excel, runs the same login flow, and asserts expected results per row.

Run only the DDT test:

```bash
pytest -v -k ddt_login_excel
```

### Cross-Browser Cloud Testing (BrowserStack)

Set credentials:

```bash
export BROWSERSTACK_USERNAME="your_username"
export BROWSERSTACK_ACCESS_KEY="your_access_key"
```

Run on BrowserStack (choose browser):

```bash
RUN_ON=cloud BROWSER=chrome pytest -v -k ddt_login_excel
RUN_ON=cloud BROWSER=firefox pytest -v -k ddt_login_excel
```

### Submission Checklist

- Source code (tests + fixtures).
- Excel file (`data/test_data.xlsx`) with input data and expected results.
- Screenshots, video recording, and logs from BrowserStack dashboard.
- Report (README/PDF/DOC) with positive and negative test cases.
