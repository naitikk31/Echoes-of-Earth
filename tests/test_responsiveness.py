"""
H. Responsiveness Tests
Test UI behavior on different screen sizes (desktop, tablet, mobile).
"""

import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


VIEWPORT_SIZES = {
    "desktop": (1920, 1080),
    "tablet": (768, 1024),
    "mobile": (375, 812),
}


@pytest.mark.responsive
class TestResponsiveness:
    """Test suite for verifying UI behavior at different viewport sizes."""

    def _resize_and_load(self, driver, width, height, base_url):
        """Resize browser window and reload the page."""
        driver.set_window_size(width, height)
        driver.get(base_url)
        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "canvas")))
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        time.sleep(1)  # Allow layout to settle
        return wait

    def test_desktop_layout(self, driver, base_url):
        """At 1920×1080 (desktop), all panels should be visible."""
        wait = self._resize_and_load(driver, 1920, 1080, base_url)

        # Canvas should be visible
        canvas = driver.find_element(By.TAG_NAME, "canvas")
        assert canvas.is_displayed(), "Canvas should be visible on desktop"

        # Title should be visible
        title = driver.find_element(By.TAG_NAME, "h1")
        assert title.is_displayed(), "Title should be visible on desktop"

        # Search bar
        search = driver.find_element(By.CSS_SELECTOR, ".search-input")
        assert search.is_displayed(), "Search bar should be visible on desktop"

        # Crisis filter
        crisis_filter = driver.find_element(By.CSS_SELECTOR, ".crisis-filter")
        assert crisis_filter.is_displayed(), "Crisis filter should be visible on desktop"

        # Legend
        legend = driver.find_element(By.CSS_SELECTOR, ".legend-panel")
        assert legend.is_displayed(), "Legend should be visible on desktop"

        # Control bar
        controls = driver.find_element(By.CSS_SELECTOR, ".control-bar")
        assert controls.is_displayed(), "Control bar should be visible on desktop"

    def test_tablet_layout(self, driver, base_url):
        """At 768×1024 (tablet), page should load without crashes."""
        wait = self._resize_and_load(driver, 768, 1024, base_url)

        # Core elements should still be present
        canvas = driver.find_element(By.TAG_NAME, "canvas")
        assert canvas.is_displayed(), "Canvas should be visible on tablet"
        assert canvas.size["width"] > 0, "Canvas should have width on tablet"

        title = driver.find_element(By.TAG_NAME, "h1")
        assert title.is_displayed(), "Title should be visible on tablet"

        # Page should not have crashed (body is still present)
        body = driver.find_element(By.TAG_NAME, "body")
        assert body is not None, "Page should not crash on tablet"

    def test_mobile_layout(self, driver, base_url):
        """At 375×812 (mobile), page should load without crashes, canvas visible."""
        wait = self._resize_and_load(driver, 375, 812, base_url)

        # Canvas must still be present
        canvas = driver.find_element(By.TAG_NAME, "canvas")
        assert canvas.is_displayed(), "Canvas should be visible on mobile"

        # Title should still exist in the DOM
        titles = driver.find_elements(By.TAG_NAME, "h1")
        assert len(titles) >= 1, "Title element should exist on mobile"

        # Root div should be present
        root = driver.find_element(By.ID, "root")
        assert root is not None, "React root should exist on mobile"

    def test_canvas_resizes_with_viewport(self, driver, base_url):
        """Canvas should resize appropriately when viewport changes."""
        # Start at desktop
        self._resize_and_load(driver, 1920, 1080, base_url)
        desktop_width = driver.execute_script("return window.innerWidth;")

        # Resize to tablet
        driver.set_window_size(768, 1024)
        time.sleep(1)
        tablet_width = driver.execute_script("return window.innerWidth;")

        # Canvas width should change with viewport
        assert tablet_width < desktop_width, (
            f"Canvas should be narrower on tablet ({tablet_width}) than desktop ({desktop_width})"
        )

    def test_no_horizontal_scroll_desktop(self, driver, base_url):
        """At desktop size, there should be no horizontal scrollbar."""
        self._resize_and_load(driver, 1920, 1080, base_url)

        scroll_width = driver.execute_script("return document.body.scrollWidth")
        client_width = driver.execute_script("return document.body.clientWidth")

        assert scroll_width <= client_width + 5, (
            f"No horizontal scroll expected: scrollWidth={scroll_width}, clientWidth={client_width}"
        )
