"""
E. Search Functionality Tests
Verify the search bar, dropdown, result matching, and country selection.
"""

import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.search
class TestSearch:
    """Test suite for verifying search functionality."""

    def test_search_input_accepts_text(self, loaded_page_with_data, wait):
        """Verify that the search input accepts text input."""
        search_input = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".search-input"))
        )
        search_input.click()
        search_input.send_keys("Ind")

        assert search_input.get_attribute("value") == "Ind", (
            "Search input should accept typed text"
        )

    def test_search_opens_dropdown(self, loaded_page_with_data, wait):
        """Typing a country name should open the search dropdown."""
        search_input = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".search-input"))
        )
        search_input.click()
        search_input.send_keys("Ind")

        dropdown = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".search-dropdown"))
        )
        assert dropdown.is_displayed(), "Search dropdown should appear"

    def test_search_results_match_query(self, loaded_page_with_data, wait):
        """Search results should contain the query text."""
        search_input = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".search-input"))
        )
        search_input.click()
        search_input.send_keys("Ind")

        wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".search-dropdown"))
        )

        results = loaded_page_with_data.find_elements(By.CSS_SELECTOR, ".search-result-name")
        assert len(results) > 0, "Should have at least one search result"

        for result in results:
            assert "ind" in result.text.lower(), (
                f"Result '{result.text}' should contain the search query 'ind'"
            )

    def test_search_results_show_coordinates(self, loaded_page_with_data, wait):
        """Each search result should show coordinates."""
        search_input = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".search-input"))
        )
        search_input.click()
        search_input.send_keys("Japan")

        wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".search-dropdown"))
        )

        coords = loaded_page_with_data.find_elements(By.CSS_SELECTOR, ".search-result-coords")
        assert len(coords) > 0, "Results should show coordinates"
        for coord in coords:
            assert "°" in coord.text, f"Coordinates should contain degree symbol, got '{coord.text}'"

    def test_search_results_show_map_pin(self, loaded_page_with_data, wait):
        """Each search result should have a map pin icon."""
        search_input = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".search-input"))
        )
        search_input.click()
        search_input.send_keys("Brazil")

        wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".search-dropdown"))
        )

        icons = loaded_page_with_data.find_elements(By.CSS_SELECTOR, ".search-result-icon")
        assert len(icons) > 0, "Results should have map pin icons"

    def test_select_country_opens_panel(self, loaded_page_with_data, wait):
        """Clicking a search result should open the news panel for that country."""
        search_input = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".search-input"))
        )
        search_input.click()
        search_input.send_keys("France")

        wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".search-dropdown"))
        )

        first_result = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".search-result"))
        )
        first_result.click()

        # News panel should appear
        panel = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".news-panel"))
        )
        assert panel.is_displayed(), "News panel should open after selecting a country"

        # Search input should be cleared after selection
        search_input_after = loaded_page_with_data.find_element(
            By.CSS_SELECTOR, ".search-input"
        )
        assert search_input_after.get_attribute("value") == "", (
            "Search input should be cleared after selection"
        )

    def test_search_clear_button(self, loaded_page_with_data, wait):
        """Clicking the clear button should empty the search and close dropdown."""
        search_input = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".search-input"))
        )
        search_input.click()
        search_input.send_keys("Germany")

        # Wait for dropdown
        wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".search-dropdown"))
        )

        # Click clear button
        clear_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".search-clear"))
        )
        clear_btn.click()

        # Input should be empty
        assert search_input.get_attribute("value") == "", (
            "Search input should be empty after clearing"
        )

        # Dropdown should be gone
        time.sleep(0.3)
        dropdowns = loaded_page_with_data.find_elements(By.CSS_SELECTOR, ".search-dropdown")
        assert len(dropdowns) == 0, "Dropdown should be hidden after clearing"

    def test_search_escape_closes(self, loaded_page_with_data, wait):
        """Pressing Escape should close the search dropdown."""
        search_input = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".search-input"))
        )
        search_input.click()
        search_input.send_keys("China")

        wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".search-dropdown"))
        )

        # Press Escape
        search_input.send_keys(Keys.ESCAPE)

        time.sleep(0.3)
        dropdowns = loaded_page_with_data.find_elements(By.CSS_SELECTOR, ".search-dropdown")
        assert len(dropdowns) == 0, "Dropdown should close on Escape"

    def test_search_keyboard_navigation(self, loaded_page_with_data, wait):
        """Arrow keys should navigate through search results."""
        search_input = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".search-input"))
        )
        search_input.click()
        search_input.send_keys("United")

        wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".search-dropdown"))
        )

        # Press ArrowDown to highlight first result
        search_input.send_keys(Keys.ARROW_DOWN)
        time.sleep(0.2)

        highlighted = loaded_page_with_data.find_elements(
            By.CSS_SELECTOR, ".search-result-highlight"
        )
        assert len(highlighted) >= 1, "ArrowDown should highlight a result"

    def test_search_no_results_for_gibberish(self, loaded_page_with_data, wait):
        """Searching for nonsense should show no dropdown."""
        search_input = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".search-input"))
        )
        search_input.click()
        search_input.send_keys("xyzxyzxyz123")

        time.sleep(0.5)
        dropdowns = loaded_page_with_data.find_elements(By.CSS_SELECTOR, ".search-dropdown")
        assert len(dropdowns) == 0, "No dropdown should appear for invalid search"
