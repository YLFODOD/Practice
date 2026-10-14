"""TC01 — home page loads and shows products."""

import re

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.smoke
def test_home_page_shows_products(page: Page) -> None:
    page.goto("/")  # relative to base_url in pytest.ini

    expect(page).to_have_title(re.compile("Practice Software Testing"))
    # expect() auto-waits until the Angular app has rendered the grid
    expect(page.get_by_test_id("product-name").first).to_be_visible()


@pytest.mark.smoke
def test_search_shows_matching_products(page: Page) -> None:
    """TC04 starter — search, then check every result matches."""
    page.goto("/")
    page.get_by_test_id("search-query").fill("pliers")
    page.get_by_test_id("search-submit").click()

    expect(page.get_by_test_id("search-term")).to_have_text("pliers")
    names = page.get_by_test_id("product-name")
    expect(names.filter(has_not_text=re.compile("pliers", re.IGNORECASE))).to_have_count(0)
    expect(names.first).to_be_visible()
