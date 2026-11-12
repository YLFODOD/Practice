"""TC09 — REST API tests with Playwright's request context (no browser)."""

import pytest
from playwright.sync_api import APIRequestContext


@pytest.mark.api
def test_products_list_is_paginated(api: APIRequestContext) -> None:
    response = api.get("/products")

    assert response.ok, f"{response.status} {response.status_text}"
    body = response.json()
    assert body["data"], "expected at least one product"
    first = body["data"][0]
    assert {"id", "name", "price"} <= first.keys()


@pytest.mark.api
def test_login_returns_access_token(api: APIRequestContext, credentials: dict[str, str]) -> None:
    response = api.post("/users/login", data=credentials)

    assert response.status == 200
    assert response.json().get("access_token")


@pytest.mark.api
def test_bad_login_returns_401(api: APIRequestContext) -> None:
    response = api.post("/users/login", data={"username": "invalid", "password": "invalid"})

    assert response.status == 401


@pytest.mark.api
def test_search_product_by_name(api: APIRequestContext) -> None:
    response = api.get("/products/search", params={"q": "hammer"})

    assert response.ok, f"{response.status} {response.status_text}"
