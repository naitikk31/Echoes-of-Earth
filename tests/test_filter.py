"""
F. Crisis Filter Tests
Verify filter toggle behavior, active states, and that at least one filter stays active.
"""

import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.filter
class TestCrisisFilter:
    """Test suite for verifying crisis filter functionality."""

    FILTER_TYPES = ["Conflict", "Economic", "Disaster", "Health"]

    def test_all_filters_active_initially(self, loaded_page, wait):
        """All 4 filter buttons should be active (have filter-btn-active class) by default."""
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".crisis-filter"))
        )

        filter_buttons = loaded_page.find_elements(By.CSS_SELECTOR, ".filter-btn")
        assert len(filter_buttons) == 4, f"Expected 4 filter buttons, got {len(filter_buttons)}"

        for btn in filter_buttons:
            classes = btn.get_attribute("class")
            assert "filter-btn-active" in classes, (
                f"Filter button '{btn.text}' should be active by default"
            )

    def test_filter_labels_correct(self, loaded_page, wait):
        """Filter buttons should have correct labels."""
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".crisis-filter"))
        )

        filter_buttons = loaded_page.find_elements(By.CSS_SELECTOR, ".filter-btn")
        button_texts = [btn.text.strip().lower() for btn in filter_buttons]

        for expected_type in self.FILTER_TYPES:
            assert expected_type.lower() in " ".join(button_texts), (
                f"Filter '{expected_type}' should be present in filter buttons"
            )

    def test_filter_label_present(self, loaded_page, wait):
        """The 'FILTER' label should be present above the buttons."""
        filter_label = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".filter-label"))
        )
        assert "FILTER" in filter_label.text.upper(), (
            f"Expected 'FILTER' label, got '{filter_label.text}'"
        )

    def test_toggle_filter_off(self, loaded_page, wait):
        """Clicking an active filter button should deactivate it."""
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".crisis-filter"))
        )

        filter_buttons = loaded_page.find_elements(By.CSS_SELECTOR, ".filter-btn")
        first_btn = filter_buttons[0]

        # Verify it's active
        assert "filter-btn-active" in first_btn.get_attribute("class")

        # Click to deactivate
        first_btn.click()
        time.sleep(0.3)

        # Verify it's now inactive
        classes = first_btn.get_attribute("class")
        assert "filter-btn-active" not in classes, (
            "Filter button should be inactive after clicking"
        )

    def test_toggle_filter_on(self, loaded_page, wait):
        """Clicking an inactive filter button should reactivate it."""
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".crisis-filter"))
        )

        filter_buttons = loaded_page.find_elements(By.CSS_SELECTOR, ".filter-btn")
        first_btn = filter_buttons[0]

        # Deactivate first
        first_btn.click()
        time.sleep(0.3)
        assert "filter-btn-active" not in first_btn.get_attribute("class")

        # Reactivate
        first_btn.click()
        time.sleep(0.3)
        assert "filter-btn-active" in first_btn.get_attribute("class"), (
            "Filter button should be active after re-clicking"
        )

    def test_cannot_deactivate_all_filters(self, loaded_page, wait):
        """It should not be possible to deactivate all filters — at least one must remain."""
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".crisis-filter"))
        )

        filter_buttons = loaded_page.find_elements(By.CSS_SELECTOR, ".filter-btn")

        # Try to deactivate all 4 filters
        for btn in filter_buttons:
            btn.click()
            time.sleep(0.2)

        # Count how many are still active
        active_buttons = [
            btn for btn in filter_buttons
            if "filter-btn-active" in btn.get_attribute("class")
        ]

        assert len(active_buttons) >= 1, (
            "At least one filter must remain active — cannot deactivate all"
        )

    def test_multiple_filters_can_be_inactive(self, loaded_page, wait):
        """Multiple filters can be deactivated simultaneously (but not all)."""
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".crisis-filter"))
        )

        filter_buttons = loaded_page.find_elements(By.CSS_SELECTOR, ".filter-btn")

        # Deactivate first two
        filter_buttons[0].click()
        time.sleep(0.2)
        filter_buttons[1].click()
        time.sleep(0.2)

        # First two should be inactive
        assert "filter-btn-active" not in filter_buttons[0].get_attribute("class")
        assert "filter-btn-active" not in filter_buttons[1].get_attribute("class")

        # Last two should still be active
        assert "filter-btn-active" in filter_buttons[2].get_attribute("class")
        assert "filter-btn-active" in filter_buttons[3].get_attribute("class")
