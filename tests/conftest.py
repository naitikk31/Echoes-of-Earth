"""
Shared pytest fixtures for Selenium E2E tests.
Provides WebDriver setup, teardown, screenshot-on-failure, and common helpers.
"""

import os
import pytest
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


# ─── Constants ───
DEFAULT_BASE_URL = "http://localhost:5173"
DEFAULT_WAIT_TIMEOUT = 15  # seconds
SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "screenshots")
REPORTS_DIR = os.path.join(os.path.dirname(__file__), "reports")


def pytest_addoption(parser):
    """Add custom CLI options for pytest."""
    parser.addoption(
        "--base-url",
        action="store",
        default=DEFAULT_BASE_URL,
        help="Base URL of the application under test",
    )


@pytest.fixture(scope="session")
def base_url(request):
    """Get the base URL from CLI option or default."""
    return request.config.getoption("--base-url")


@pytest.fixture(scope="function")
def driver(request, base_url):
    """
    Set up and tear down a Chrome WebDriver instance for each test.
    Supports headless mode via HEADLESS=1 environment variable.
    """
    chrome_options = Options()

    # Headless mode
    if os.environ.get("HEADLESS", "0") == "1":
        chrome_options.add_argument("--headless=new")

    # Common options for stability
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    # Suppress WebGL/GPU warnings in logs
    chrome_options.add_argument("--disable-logging")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    # Initialize WebDriver with webdriver-manager
    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service, options=chrome_options)
    browser.implicitly_wait(5)

    yield browser

    browser.quit()


@pytest.fixture(scope="function")
def wait(driver):
    """Provide a WebDriverWait instance with default timeout."""
    return WebDriverWait(driver, DEFAULT_WAIT_TIMEOUT)


@pytest.fixture(scope="function")
def loaded_page(driver, wait, base_url):
    """
    Navigate to the app and wait for the React app to fully render.
    Returns the driver with the page loaded and ready.
    """
    driver.get(base_url)

    # Wait for the Three.js canvas to appear (confirms React + R3F rendered)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "canvas")))

    # Wait for the overlay title to render (confirms React hydration)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))

    # Ensure the loading overlay has disappeared so it doesn't intercept clicks
    try:
        wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".loading-overlay")))
    except Exception:
        pass

    return driver


@pytest.fixture(scope="function")
def loaded_page_with_data(loaded_page, wait):
    """
    Wait for crisis data to load (stats panel appears when data is ready).
    Returns the driver with data loaded.
    """
    try:
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".stats-panel"))
        )
    except Exception:
        # Data may not load (e.g., API unavailable), tests should handle gracefully
        pass
    return loaded_page


# ─── Screenshot on Failure Hook ───


def pytest_runtest_makereport(item, call):
    """Capture screenshot on test failure."""
    if call.when == "call" and call.excinfo is not None:
        # Get the driver fixture if available
        driver = item.funcargs.get("driver") or item.funcargs.get("loaded_page")
        if driver is None:
            driver = item.funcargs.get("loaded_page_with_data")

        if driver is not None:
            # Ensure screenshot directory exists
            os.makedirs(SCREENSHOT_DIR, exist_ok=True)

            # Generate filename from test name + timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_name = item.name.replace("[", "_").replace("]", "_")
            filename = f"{test_name}_{timestamp}.png"
            filepath = os.path.join(SCREENSHOT_DIR, filename)

            try:
                driver.save_screenshot(filepath)
                print(f"\n📸 Screenshot saved: {filepath}")
            except Exception as e:
                print(f"\n⚠️ Failed to capture screenshot: {e}")


# ─── Helper Functions ───


def search_and_select_country(driver, wait, country_name):
    """
    Helper: Type a country name into the search bar and select the first result.
    Opens the news panel for that country.
    """
    # Find and click the search input
    search_input = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".search-input"))
    )
    search_input.clear()
    search_input.send_keys(country_name)

    # Wait for dropdown to appear
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".search-dropdown"))
    )

    # Click the first result
    first_result = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".search-result"))
    )
    first_result.click()

    # Wait for the news panel to appear
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".news-panel"))
    )


@pytest.fixture(scope="function")
def select_country(driver, wait):
    """
    Fixture that returns a callable to search and select a country.
    Usage in tests: select_country("India")
    """
    def _select(country_name):
        search_and_select_country(driver, wait, country_name)
    return _select
