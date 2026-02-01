# Assignment 6 Report (Checklist)

Primary website: https://sultan-it-solutions-admin.vercel.app

## Data-Driven Testing (Excel)

- [x] Test data stored in `.xlsx` file  
  - File: `data/test_data.xlsx`
- [x] Excel contains input data and expected results  
  - Columns: `case_id`, `username`, `password`, `expected_result`, `expected_text`
- [x] Automated test reads Excel dynamically  
  - Test: `tests/test_ddt_login_excel.py`
- [x] Test runs multiple data sets  
- [x] Assertions compare actual vs expected  
- [x] Execution result logged per data set  
  - Output: `results/ddt_results.csv`

## Positive Test Cases

1) **Valid login**  
   - Input: correct username + password  
   - Expected: dashboard header contains "Заявки"  
   - Data row: `case_id=valid_login`

## Negative Test Cases

1) **Invalid password**  
   - Input: correct username + wrong password  
   - Expected: login page remains, header "Login"  
   - Data row: `case_id=invalid_password`

2) **Invalid username**  
   - Input: wrong username + correct password  
   - Expected: login page remains, header "Login"  
   - Data row: `case_id=invalid_username`

## Cross-Browser Cloud Testing

- Platform: BrowserStack  
- Mode: Automated (Selenium Remote WebDriver)  
- Browsers: Chrome + Firefox (latest)

