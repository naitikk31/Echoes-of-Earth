"""
B. Globe Interaction Tests
Simulate mouse drag to rotate the globe and verify UI stability.
"""

import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.interaction
class TestGlobeInteraction:
    """Test suite for verifying globe interactions don't break the UI."""

    def test_globe_drag_rotate(self, loaded_page_with_data, wait):
        """Simulate mouse drag on the globe canvas to rotate it."""
        canvas = wait.until(
            EC.visibility_of_element_located((By.TAG_NAME, "canvas"))
        )

        # Perform a click-and-drag action on the canvas
        actions = ActionChains(loaded_page_with_data)
        actions.move_to_element(canvas)
        actions.click_and_hold()
        actions.move_by_offset(200, 0)   # Drag right
        actions.release()
        actions.perform()

        # Small wait for any animation
        time.sleep(0.5)

        # Verify canvas is still visible and intact
        canvas_after = loaded_page_with_data.find_element(By.TAG_NAME, "canvas")
        assert canvas_after.is_displayed(), (
            "Canvas should still be visible after drag interaction"
        )

        # Verify overlay is still intact
        heading = loaded_page_with_data.find_element(By.TAG_NAME, "h1")
        assert heading.is_displayed(), (
            "Title should still be visible after drag interaction"
        )

    def test_globe_drag_vertical(self, loaded_page_with_data, wait):
        """Simulate vertical drag on the globe canvas."""
        canvas = wait.until(
            EC.visibility_of_element_located((By.TAG_NAME, "canvas"))
        )

        actions = ActionChains(loaded_page_with_data)
        actions.move_to_element(canvas)
        actions.click_and_hold()
        actions.move_by_offset(0, 150)   # Drag down
        actions.release()
        actions.perform()

        time.sleep(0.5)

        # Verify UI elements are still present
        assert loaded_page_with_data.find_element(By.TAG_NAME, "canvas").is_displayed()
        assert loaded_page_with_data.find_element(By.CSS_SELECTOR, ".search-input").is_displayed()

    def test_globe_drag_diagonal(self, loaded_page_with_data, wait):
        """Simulate diagonal drag on the globe canvas."""
        canvas = wait.until(
            EC.visibility_of_element_located((By.TAG_NAME, "canvas"))
        )

        actions = ActionChains(loaded_page_with_data)
        actions.move_to_element(canvas)
        actions.click_and_hold()
        actions.move_by_offset(-50, -50)     # Drag up-left
        actions.move_by_offset(100, 100)     # Then drag down-right
        actions.release()
        actions.perform()

        time.sleep(0.5)

        # Verify the entire page is still functional
        canvas_after = loaded_page_with_data.find_element(By.TAG_NAME, "canvas")
        assert canvas_after.is_displayed(), "Canvas survived diagonal drag"
        assert canvas_after.size["width"] > 0

    def test_globe_zoom_scroll(self, loaded_page_with_data, wait):
        """Simulate scroll wheel zoom on the globe canvas."""
        canvas = wait.until(
            EC.visibility_of_element_located((By.TAG_NAME, "canvas"))
        )

        # Scroll to zoom in
        actions = ActionChains(loaded_page_with_data)
        actions.move_to_element(canvas)
        actions.scroll_by_amount(0, -300)  # Scroll up = zoom in
        actions.perform()

        time.sleep(0.5)

        # Scroll to zoom out
        actions = ActionChains(loaded_page_with_data)
        actions.move_to_element(canvas)
        actions.scroll_by_amount(0, 300)  # Scroll down = zoom out
        actions.perform()

        time.sleep(0.5)

        # Verify canvas is still intact
        canvas_after = loaded_page_with_data.find_element(By.TAG_NAME, "canvas")
        assert canvas_after.is_displayed(), (
            "Canvas should still be visible after zoom interaction"
        )

    def test_rapid_interactions(self, loaded_page_with_data, wait):
        """Perform rapid successive interactions to stress-test stability."""
        canvas = wait.until(
            EC.visibility_of_element_located((By.TAG_NAME, "canvas"))
        )

        actions = ActionChains(loaded_page_with_data)
        actions.move_to_element(canvas)

        # Rapid successive drags
        for _ in range(5):
            actions.click_and_hold()
            actions.move_by_offset(50, 30)
            actions.release()

        actions.perform()
        time.sleep(0.5)

        # Verify everything is still working
        assert loaded_page_with_data.find_element(By.TAG_NAME, "canvas").is_displayed()
        assert loaded_page_with_data.find_element(By.TAG_NAME, "h1").is_displayed()
        assert loaded_page_with_data.find_element(By.CSS_SELECTOR, ".crisis-filter").is_displayed()
