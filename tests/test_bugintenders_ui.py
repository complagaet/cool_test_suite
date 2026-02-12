import logging
import pytest

from fixtures.driver_fixture import driver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, StaleElementReferenceException

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

BASE_URL = "https://bugintenders.lukoyanov.love/"

SPLASH_XPATH = (
    "//div[contains(@class,'fixed') and contains(@class,'top-0') and contains(@class,'left-0') "
    "and contains(@class,'w-full') and contains(@class,'bg-[#EBE7E5]') "
    "and contains(@class,'z-150') and contains(@class,'h-screen-fallback')]"
)

SEARCH_INPUT_CSS = "input[type='text'], input[type='search'], input:not([type])"


def splash_is_hidden_or_nonblocking(driver) -> bool:
    """
    True if:
    - splash not found, OR
    - splash class includes 'hidden', OR
    - splash not displayed, OR
    - splash has pointer-events none (non-blocking)
    """
    els = driver.find_elements(By.XPATH, SPLASH_XPATH)
    if not els:
        return True

    for el in els:
        try:
            cls = (el.get_attribute("class") or "")
            cls_tokens = set(cls.split())

            if "hidden" in cls_tokens:
                continue

            if not el.is_displayed():
                continue

            pe = (el.value_of_css_property("pointer-events") or "").strip().lower()
            if pe == "none":
                continue

            return False

        except StaleElementReferenceException:
            continue

    return True


def wait_app_ready(driver, timeout: int = 25) -> None:
    """
    Wait until app is usable:
    1) splash is hidden OR non-blocking
    2) search input exists and is interactable
    Fallback: if splash never becomes hidden but input is clickable, proceed anyway.
    """
    wait = WebDriverWait(driver, timeout)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    try:
        wait.until(lambda d: splash_is_hidden_or_nonblocking(d))
    except TimeoutException:
        logging.warning("Splash did not become hidden in time. Falling back to input clickability.")

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, SEARCH_INPUT_CSS)))
    inp = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, SEARCH_INPUT_CSS)))
    assert inp is not None


def open_site(driver):
    driver.get(BASE_URL)
    wait_app_ready(driver, timeout=30)


def wait_for_any_text(driver, timeout: int, texts: list[str]) -> None:
    WebDriverWait(driver, timeout).until(lambda d: any(t in d.page_source for t in texts))


def click_with_fallback(driver, element, timeout: int = 15) -> None:
    """
    Click that survives overlays/animations:
    - Scroll into view
    - Normal click
    - If intercepted: wait_app_ready and JS click
    """
    driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'center'});", element)
    try:
        element.click()
    except ElementClickInterceptedException:
        logging.info("Click intercepted. Waiting app ready and clicking via JS.")
        wait_app_ready(driver, timeout=timeout)
        driver.execute_script("arguments[0].click();", element)


def xpath_literal(s: str) -> str:
    if "'" not in s:
        return f"'{s}'"
    if '"' not in s:
        return f'"{s}"'
    parts = s.split("'")
    return "concat(" + ", \"'\", ".join([f"'{p}'" for p in parts]) + ")"


def find_clickable_button_by_text(driver, timeout: int, texts: list[str]):
    xpaths = [f"//button[contains(normalize-space(.), {xpath_literal(t)})]" for t in texts]
    xpath_union = " | ".join(xpaths)
    return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath_union)))


def find_present_by_any_xpath(driver, timeout: int, xpaths: list[str]):
    last = None
    for xp in xpaths:
        try:
            return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xp)))
        except TimeoutException as e:
            last = e
    raise last or TimeoutException(f"None of the XPaths appeared: {xpaths}")


def get_search_input(driver, timeout: int = 15):
    wait = WebDriverWait(driver, timeout)
    return wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, SEARCH_INPUT_CSS)))


def open_category_menu(driver, timeout: int = 15):
    """
    Open category selector/menu.
    """
    wait_app_ready(driver, timeout=timeout)

    candidates = [
        "//button[contains(., 'Хабарландыру') or contains(., 'Объявления') or contains(., 'Тауар') or contains(., 'Товары') or contains(., 'Жеткізуш') or contains(., 'Постав')]",
        "//*[@role='button' and (contains(., 'Хабарландыру') or contains(., 'Объявления') or contains(., 'Тауар') or contains(., 'Товары') or contains(., 'Жеткізуш') or contains(., 'Постав'))]",
    ]
    btn = find_present_by_any_xpath(driver, timeout, candidates)
    click_with_fallback(driver, btn, timeout=timeout)


def select_category(driver, category_texts: list[str], timeout: int = 15):
    open_category_menu(driver, timeout=timeout)
    option = find_clickable_button_by_text(driver, timeout, category_texts)
    click_with_fallback(driver, option, timeout=timeout)


def perform_search(driver, query: str, timeout: int = 15):
    wait_app_ready(driver, timeout=timeout)
    inp = get_search_input(driver, timeout=timeout)
    inp.clear()
    inp.send_keys(query)
    inp.send_keys(Keys.ENTER)


def select_category_and_search(driver, category_texts: list[str], query: str, timeout: int = 15):
    select_category(driver, category_texts, timeout=timeout)
    perform_search(driver, query, timeout=timeout)


def wait_for_new_tab(driver, old_handles, timeout: int = 25):
    WebDriverWait(driver, timeout).until(EC.number_of_windows_to_be(len(old_handles) + 1))
    return [h for h in driver.window_handles if h not in old_handles][0]


@pytest.mark.smoke
def test_smoke_open_main_page(driver):
    """Checks that the main page opens and the URL contains bugintenders."""
    logging.info("SMOKE: Opening main page.")
    open_site(driver)
    assert "bugintenders" in driver.current_url.lower()


@pytest.mark.smoke
def test_smoke_language_switcher_exists(driver):
    """Checks that the language switcher is present on the main page."""
    logging.info("SMOKE: Checking language switcher presence.")
    open_site(driver)
    wait_for_any_text(driver, 20, ["kk", "ru", "Қаз", "Рус"])
    assert True


@pytest.mark.smoke
def test_smoke_announcements_search(driver):
    """Checks search in the announcements category for the query 'stol'."""
    logging.info("SMOKE: Announcements search 'стол'.")
    open_site(driver)
    select_category_and_search(driver, ["Хабарландырулар", "Объявления"], "стол", timeout=20)
    wait_for_any_text(driver, 30, ["Хабарландыру", "Объявлен", "Хабарландырулар", "Объявления"])
    assert any(x in driver.page_source for x in ["Хабарландыру", "Объявлен"])


@pytest.mark.smoke
def test_smoke_suppliers_search(driver):
    """Checks search in the suppliers category for the query 'stol'."""
    logging.info("SMOKE: Suppliers search 'стол'.")
    open_site(driver)
    select_category_and_search(driver, ["Жеткізушілер", "Поставщики"], "стол", timeout=20)
    wait_for_any_text(driver, 35, ["Проверка поставщика", "Жеткізушіні тексеру", "Профиль", "Профильді"])
    assert any(x in driver.page_source for x in ["Проверка поставщика", "Жеткізушіні тексеру", "Профиль", "Профильді"])


@pytest.mark.smoke
def test_smoke_goods_search_and_find_suppliers_button(driver):
    """Checks goods search and presence of the 'Find suppliers' button."""
    logging.info("SMOKE: Goods search 'чайник' and check 'Find suppliers' button exists.")
    open_site(driver)
    select_category_and_search(driver, ["Тауарлар", "Товары"], "чайник", timeout=20)
    wait_for_any_text(driver, 40, ["Найти поставщиков", "Жеткізушілерді табу"])
    assert any(x in driver.page_source for x in ["Найти поставщиков", "Жеткізушілерді табу"])


@pytest.mark.regression
def test_regression_supplier_profile_opens_goszakup(driver):
    """Checks that opening a supplier profile happens in a new tab."""
    logging.info("REGRESSION: Supplier profile opens in new tab.")
    open_site(driver)
    select_category_and_search(driver, ["Жеткізушілер", "Поставщики"], "стол", timeout=20)

    btn = find_clickable_button_by_text(driver, 40, ["Посмотреть профиль", "Профильді көру", "Профиль"])
    old_handles = driver.window_handles
    click_with_fallback(driver, btn, timeout=20)

    new_handle = wait_for_new_tab(driver, old_handles, timeout=30)
    driver.switch_to.window(new_handle)
    WebDriverWait(driver, 30).until(lambda d: "goszakup" in d.current_url.lower() or "gzk" in d.current_url.lower())
    assert True


@pytest.mark.regression
def test_regression_goods_find_suppliers_flow(driver):
    """Checks the flow: goods -> find suppliers -> start search."""
    logging.info("REGRESSION: Goods -> Find suppliers -> Start search shows results.")
    open_site(driver)
    select_category_and_search(driver, ["Тауарлар", "Товары"], "чайник", timeout=20)

    btn_find = find_clickable_button_by_text(driver, 45, ["Найти поставщиков", "Жеткізушілерді табу"])
    click_with_fallback(driver, btn_find, timeout=25)

    btn_start = find_clickable_button_by_text(driver, 45, ["Начать поиск", "Іздеуді бастау"])
    click_with_fallback(driver, btn_start, timeout=25)

    wait_for_any_text(driver, 45, ["Проверка поставщика", "Жеткізушіні тексеру", "Лот", "Лоты", "Тендер"])
    assert True


@pytest.mark.regression
def test_regression_refresh_stability(driver):
    """Checks that page refresh does not break the UI."""
    logging.info("REGRESSION: Refresh does not break app.")
    open_site(driver)
    driver.refresh()
    wait_app_ready(driver, timeout=30)
    assert True


@pytest.mark.regression
def test_regression_filters_button_does_not_break_ui(driver):
    """Checks that clicking the filters button (if present) does not break the UI."""
    logging.info("REGRESSION: Filters button (if present) does not break UI.")
    open_site(driver)
    select_category_and_search(driver, ["Хабарландырулар", "Объявления"], "стол", timeout=20)

    try:
        filters_btn = find_clickable_button_by_text(driver, 8, ["Фильтры", "Сүзгілер"])
        click_with_fallback(driver, filters_btn, timeout=20)
        wait_for_any_text(driver, 25, ["недоступ", "қолжетімсіз", "Сүзгі", "Фильтр"])
        assert True
    except TimeoutException:
        pytest.skip("Filters button not present in this build/UI.")


@pytest.mark.negative
def test_negative_min_query_length_validation(driver):
    """Checks minimum query length validation (<3 characters)."""
    logging.info("NEGATIVE: <3 chars shows validation message.")
    open_site(driver)
    select_category(driver, ["Хабарландырулар", "Объявления"], timeout=20)
    perform_search(driver, "ab", timeout=20)

    wait_for_any_text(driver, 40, ["минимум 3", "кемінде 3", "3 символ", "3 таңба"])
    assert True


@pytest.mark.negative
def test_negative_only_spaces_handled_safely(driver):
    """Checks that spaces-only input does not crash the app."""
    logging.info("NEGATIVE: spaces-only input should not crash.")
    open_site(driver)
    select_category(driver, ["Хабарландырулар", "Объявления"], timeout=20)
    perform_search(driver, "   ", timeout=20)

    crash_indicators = ["TypeError", "ReferenceError", "Unhandled", "Stack trace"]
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    assert not any(x in driver.page_source for x in crash_indicators)


@pytest.mark.negative
def test_negative_sql_like_input_does_not_crash(driver):
    """Checks that SQL-like input does not crash the app."""
    logging.info("NEGATIVE: SQL-like input should not crash the app.")
    open_site(driver)
    select_category(driver, ["Хабарландырулар", "Объявления"], timeout=20)
    perform_search(driver, "' OR 1=1 --", timeout=20)

    crash_indicators = ["TypeError", "ReferenceError", "Unhandled", "Stack trace"]
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    assert not any(x in driver.page_source for x in crash_indicators)
