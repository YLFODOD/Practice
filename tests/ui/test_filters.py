"""TC05 — Test filter functionality."""

import re
from urllib.parse import parse_qs, urlparse

from playwright.sync_api import Page, expect


def request_params(request) -> dict:
    """Params from the query string and/or JSON body, whichever the app uses."""
    params = {k: v[0] for k, v in parse_qs(urlparse(request.url).query).items()}
    if request.post_data:
        try:
            params.update(request.post_data_json)
        except Exception:
            pass
    return params


def products_response(**expected):
    """Predicate: a successful /products response whose request has these params."""

    def match(r) -> bool:
        if r.request.method == "OPTIONS" or not r.ok:
            return False
        if not urlparse(r.url).path.rstrip("/").endswith("/products"):
            return False
        params = request_params(r.request)
        return all(params.get(k) == v for k, v in expected.items())

    return match


def test_price_in_ascending_order(page: Page) -> None:
    """Products in the Hammer category are listed by price, lowest first."""
    page.goto("/", wait_until="domcontentloaded")

    hammer_category = page.get_by_role("checkbox", name=re.compile("hammer", re.IGNORECASE))
    hammer_id = hammer_category.get_attribute("value")

    with page.expect_response(products_response(by_category=hammer_id)):
        hammer_category.check()
    expect(hammer_category).to_be_checked()

    sort = page.get_by_test_id("sort")
    with page.expect_response(products_response(sort="price,asc", by_category=hammer_id)) as resp_info:
        sort.select_option("price,asc")

    products = resp_info.value.json()["data"]
    assert all(p["category"]["name"] == "Hammer" for p in products)

    prices = [p["price"] for p in products]
    assert prices == sorted(prices), f"API returned unsorted prices: {prices}"

    expect(page.get_by_test_id("product-price")).to_have_text([f"${p:.2f}" for p in prices])
