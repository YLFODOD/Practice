"""Shared fixtures. pytest loads this file automatically for every test."""

import os

import pytest
from dotenv import load_dotenv
from playwright.sync_api import APIRequestContext, Playwright

load_dotenv()  # reads a local .env if present; harmless in CI

API_URL = os.getenv("API_URL", "https://api.practicesoftwaretesting.com")


@pytest.fixture(scope="session", autouse=True)
def use_data_test_ids(playwright: Playwright) -> None:
    """Toolshop marks elements with data-test="...", so make get_by_test_id() use it."""
    playwright.selectors.set_test_id_attribute("data-test")


@pytest.fixture(scope="session")
def credentials() -> dict[str, str]:
    """Customer login. Locally from .env, in CI from repository secrets."""
    email = os.getenv("TEST_USER_EMAIL")
    password = os.getenv("TEST_USER_PASSWORD")
    if not email or not password:
        pytest.skip("Set TEST_USER_EMAIL and TEST_USER_PASSWORD (see .env.example)")
    return {"email": email, "password": password}


@pytest.fixture(scope="session")
def api(playwright: Playwright):
    """An HTTP client for API tests (TC09). No browser is launched for these."""
    context: APIRequestContext = playwright.request.new_context(base_url=API_URL)
    yield context
    context.dispose()
