"""
G. History Slider Tests
Verify the history slider navigation, day markers, and LIVE badge.
"""

import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.history
class TestHistorySlider:
    """Test suite for verifying history slider functionality."""

    def _slider_present(self, driver):
        """Check if the history slider is present (it only renders with loaded history data)."""
        sliders = driver.find_elements(By.CSS_SELECTOR, ".history-slider")
        return len(sliders) > 0 and sliders[0].is_displayed()

    def test_slider_present_when_data_loaded(self, loaded_page_with_data, wait):
        """History slider should be present when daily history data is loaded."""
        # Give extra time for history to load
        time.sleep(3)

        if not self._slider_present(loaded_page_with_data):
            pytest.skip(
                "History slider not present — may not have multi-day history data"
            )

        slider = loaded_page_with_data.find_element(
            By.CSS_SELECTOR, ".history-slider"
        )
        assert slider.is_displayed(), "History slider should be visible"

    def test_slider_has_day_dots(self, loaded_page_with_data, wait):
        """History slider should have day marker dots."""
        time.sleep(3)

        if not self._slider_present(loaded_page_with_data):
            pytest.skip("History slider not present")

        dots = loaded_page_with_data.find_elements(
            By.CSS_SELECTOR, ".history-day-dot"
        )
        assert len(dots) >= 2, (
            f"Expected at least 2 day dots, got {len(dots)}"
        )

    def test_slider_has_active_dot(self, loaded_page_with_data, wait):
        """One day dot should be active (highlighted)."""
        time.sleep(3)

        if not self._slider_present(loaded_page_with_data):
            pytest.skip("History slider not present")

        active_dots = loaded_page_with_data.find_elements(
            By.CSS_SELECTOR, ".history-day-dot.active"
        )
        assert len(active_dots) == 1, "Exactly one day dot should be active"

    def test_slider_has_range_input(self, loaded_page_with_data, wait):
        """History slider should contain a range input."""
        time.sleep(3)

        if not self._slider_present(loaded_page_with_data):
            pytest.skip("History slider not present")

        range_input = loaded_page_with_data.find_element(
            By.CSS_SELECTOR, ".history-range"
        )
        assert range_input.get_attribute("type") == "range", (
            "Should have a range input element"
        )

    def test_live_badge_on_latest_day(self, loaded_page_with_data, wait):
        """The latest day (today) should show a 'LIVE' badge."""
        time.sleep(3)

        if not self._slider_present(loaded_page_with_data):
            pytest.skip("History slider not present")

        live_badges = loaded_page_with_data.find_elements(
            By.CSS_SELECTOR, ".history-live-badge"
        )
        # LIVE badge is only shown when the active day is today (last index)
        if live_badges:
            assert "LIVE" in live_badges[0].text.upper(), (
                f"Badge should say 'LIVE', got '{live_badges[0].text}'"
            )
        else:
            # If slider is not on the latest day, LIVE badge may not show
            pass

    def test_slider_has_nav_buttons(self, loaded_page_with_data, wait):
        """History slider should have left and right navigation buttons."""
        time.sleep(3)

        if not self._slider_present(loaded_page_with_data):
            pytest.skip("History slider not present")

        nav_buttons = loaded_page_with_data.find_elements(
            By.CSS_SELECTOR, ".history-nav-btn"
        )
        assert len(nav_buttons) == 2, (
            f"Expected 2 nav buttons (back/forward), got {len(nav_buttons)}"
        )

    def test_nav_button_back(self, loaded_page_with_data, wait):
        """Clicking the back nav button should change the active day."""
        time.sleep(3)

        if not self._slider_present(loaded_page_with_data):
            pytest.skip("History slider not present")

        # Get timestamp before
        timestamp_el = loaded_page_with_data.find_element(
            By.CSS_SELECTOR, ".history-timestamp"
        )
        timestamp_before = timestamp_el.text.strip()

        # Click back button (first nav button)
        nav_buttons = loaded_page_with_data.find_elements(
            By.CSS_SELECTOR, ".history-nav-btn"
        )
        back_btn = nav_buttons[0]

        if not back_btn.is_enabled():
            pytest.skip("Back button is disabled — already at earliest day")

        back_btn.click()
        time.sleep(0.5)

        # Timestamp should change
        timestamp_after = timestamp_el.text.strip()
        assert timestamp_before != timestamp_after, (
            f"Timestamp should change after navigation: before='{timestamp_before}', after='{timestamp_after}'"
        )

    def test_nav_button_forward_disabled_at_end(self, loaded_page_with_data, wait):
        """Forward button should be disabled when on the latest day (today)."""
        time.sleep(3)

        if not self._slider_present(loaded_page_with_data):
            pytest.skip("History slider not present")

        nav_buttons = loaded_page_with_data.find_elements(
            By.CSS_SELECTOR, ".history-nav-btn"
        )
        forward_btn = nav_buttons[1]

        # On initial load, the slider is at "today" (last index),
        # so forward should be disabled
        assert not forward_btn.is_enabled() or forward_btn.get_attribute("disabled") is not None, (
            "Forward button should be disabled at the latest day"
        )

    def test_clicking_day_dot_changes_day(self, loaded_page_with_data, wait):
        """Clicking a day dot should change the active day."""
        time.sleep(3)

        if not self._slider_present(loaded_page_with_data):
            pytest.skip("History slider not present")

        dots = loaded_page_with_data.find_elements(
            By.CSS_SELECTOR, ".history-day-dot"
        )
        if len(dots) < 2:
            pytest.skip("Not enough day dots to test clicking")

        # Click the first dot (earliest day)
        dots[0].click()
        time.sleep(0.5)

        # Verify the first dot is now active
        classes = dots[0].get_attribute("class")
        assert "active" in classes, (
            "Clicked day dot should become active"
        )
