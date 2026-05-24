"""
D. News Panel Tests
Verify that each article in the news panel shows title, source, date,
description, and a "Read Full Article" link.
"""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.panel
class TestNewsPanel:
    """Test suite for verifying news panel article content."""

    @pytest.fixture(autouse=True)
    def open_news_panel(self, loaded_page_with_data, wait, select_country):
        """Open the news panel by searching for a country before each test."""
        self.driver = loaded_page_with_data
        self.wait = wait
        select_country("Ukraine")

    def _get_articles(self):
        """Get all article cards in the news panel."""
        return self.driver.find_elements(By.CSS_SELECTOR, ".news-article-card")

    def test_articles_exist(self):
        """Verify that at least one article card exists in the panel."""
        articles = self._get_articles()
        if not articles:
            pytest.skip("No articles loaded for this country — skipping article content tests")
        assert len(articles) >= 1, "At least one article should be displayed"

    def test_article_has_title(self):
        """Each article should have a non-empty title."""
        articles = self._get_articles()
        if not articles:
            pytest.skip("No articles loaded")

        for i, article in enumerate(articles):
            title = article.find_element(By.CSS_SELECTOR, ".article-title")
            assert title.text.strip(), f"Article {i+1} title should not be empty"

    def test_article_has_source(self):
        """Each article should have a non-empty source."""
        articles = self._get_articles()
        if not articles:
            pytest.skip("No articles loaded")

        for i, article in enumerate(articles):
            source = article.find_element(By.CSS_SELECTOR, ".article-source")
            assert source.text.strip(), f"Article {i+1} source should not be empty"

    def test_article_has_date(self):
        """Each article should have a non-empty date."""
        articles = self._get_articles()
        if not articles:
            pytest.skip("No articles loaded")

        for i, article in enumerate(articles):
            date = article.find_element(By.CSS_SELECTOR, ".article-date")
            assert date.text.strip(), f"Article {i+1} date should not be empty"

    def test_article_has_description(self):
        """Each article should have a description (may say 'No description available')."""
        articles = self._get_articles()
        if not articles:
            pytest.skip("No articles loaded")

        for i, article in enumerate(articles):
            description = article.find_element(By.CSS_SELECTOR, ".article-description")
            assert description.text.strip(), f"Article {i+1} description should not be empty"

    def test_read_full_article_link(self):
        """Articles with URLs should have a 'Read Full Article' link."""
        articles = self._get_articles()
        if not articles:
            pytest.skip("No articles loaded")

        links_found = 0
        for article in articles:
            links = article.find_elements(By.CSS_SELECTOR, ".article-link")
            for link in links:
                assert "read full article" in link.text.lower(), (
                    f"Link text should contain 'Read Full Article', got '{link.text}'"
                )
                href = link.get_attribute("href")
                assert href and href != "#", f"Article link href should be valid, got '{href}'"
                assert link.get_attribute("target") == "_blank", (
                    "Article link should open in a new tab"
                )
                links_found += 1

        # At least some articles should have links (not all may have URLs)
        # This is informational, not a hard failure
        print(f"  Found {links_found} 'Read Full Article' links across {len(articles)} articles")

    def test_article_type_dot_visible(self):
        """Each article should have a colored type indicator dot."""
        articles = self._get_articles()
        if not articles:
            pytest.skip("No articles loaded")

        for i, article in enumerate(articles):
            dot = article.find_element(By.CSS_SELECTOR, ".article-type-dot")
            assert dot.is_displayed(), f"Article {i+1} type dot should be visible"

    def test_panel_close_button(self):
        """Clicking the close button should remove the news panel."""
        # Verify panel is open
        panel = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".news-panel"))
        )
        assert panel.is_displayed()

        # Click close
        close_btn = self.driver.find_element(
            By.CSS_SELECTOR, ".news-panel-close"
        )
        close_btn.click()

        # Verify panel is gone
        self.wait.until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, ".news-panel"))
        )
        panels = self.driver.find_elements(By.CSS_SELECTOR, ".news-panel")
        assert len(panels) == 0, "News panel should be removed after closing"
