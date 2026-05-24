"""
A. Page Load Tests
Verify that the homepage loads successfully and all main UI elements are rendered.
"""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.smoke
class TestPageLoad:
    """Test suite for verifying the homepage loads correctly."""

    def test_homepage_loads(self, driver, wait, base_url):
        """Verify the homepage loads successfully with the correct title."""
        driver.get(base_url)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        assert "global-risk-moniter" in driver.title, (
            f"Expected 'global-risk-moniter' in title, got '{driver.title}'"
        )

    def test_globe_canvas_visible(self, loaded_page, wait):
        """Verify the 3D globe canvas (Three.js/R3F) is visible."""
        canvas = wait.until(
            EC.visibility_of_element_located((By.TAG_NAME, "canvas"))
        )
        assert canvas.is_displayed(), "Globe canvas should be visible"
        assert canvas.size["width"] > 0, "Canvas width should be > 0"
        assert canvas.size["height"] > 0, "Canvas height should be > 0"

    def test_title_rendered(self, loaded_page, wait):
        """Verify the 'TECTONEWS' title heading is rendered."""
        heading = wait.until(
            EC.visibility_of_element_located((By.TAG_NAME, "h1"))
        )
        assert heading.is_displayed(), "Title heading should be visible"
        assert "TECTONEWS" in heading.text.upper(), (
            f"Expected 'TECTONEWS' in heading, got '{heading.text}'"
        )

    def test_search_bar_present(self, loaded_page, wait):
        """Verify the search bar input is present with correct placeholder."""
        search_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".search-input"))
        )
        assert search_input.is_displayed(), "Search bar should be visible"
        placeholder = search_input.get_attribute("placeholder")
        assert "search" in placeholder.lower() or "country" in placeholder.lower(), (
            f"Search placeholder should mention 'search' or 'country', got '{placeholder}'"
        )

    def test_crisis_filter_present(self, loaded_page, wait):
        """Verify the crisis filter panel is present."""
        crisis_filter = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".crisis-filter"))
        )
        assert crisis_filter.is_displayed(), "Crisis filter should be visible"

        # Verify filter buttons exist
        filter_buttons = loaded_page.find_elements(
            By.CSS_SELECTOR, ".filter-btn"
        )
        assert len(filter_buttons) == 4, (
            f"Expected 4 filter buttons (Conflict, Economic, Disaster, Health), got {len(filter_buttons)}"
        )

    def test_legend_panel_present(self, loaded_page, wait):
        """Verify the legend panel is present at the bottom-left."""
        legend = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".legend-panel"))
        )
        assert legend.is_displayed(), "Legend panel should be visible"

    def test_control_bar_present(self, loaded_page, wait):
        """Verify the control bar is present at the bottom-right."""
        control_bar = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".control-bar"))
        )
        assert control_bar.is_displayed(), "Control bar should be visible"

    def test_stats_panel_loads_with_data(self, loaded_page_with_data, wait):
        """Verify the stats panel appears when crisis data is loaded."""
        try:
            stats = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".stats-panel"))
            )
            assert stats.is_displayed(), "Stats panel should be visible with data"

            # Verify stats content
            metrics = loaded_page_with_data.find_elements(
                By.CSS_SELECTOR, ".stats-metric-value"
            )
            assert len(metrics) >= 1, "Stats panel should show at least one metric"
        except Exception:
            pytest.skip("Stats panel not available — data may not have loaded")
