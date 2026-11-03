"""Shared fixtures. pytest loads this file automatically for every test."""

import os, re

import pytest
from dotenv import load_dotenv
from playwright.sync_api import APIRequestContext, Browser, Page, Playwright, expect
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.product_page import ProductPage

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


@pytest.fixture(scope="function")
def cart_page_with_items(page: Page) -> Page:
    home_page = HomePage(page)

    # Open the home page and add a product to the cart
    home_page.open()
    home_page.products.nth(0).click()
    product_page = ProductPage(page)
    product_page.add_to_cart()

    return page


@pytest.fixture(scope="session")
def auth_state(browser: Browser, base_url: str, credentials: dict[str, str], tmp_path_factory) -> None:
    path = tmp_path_factory.mktemp("auth") / "state.json"
    context = browser.new_context(base_url=base_url)
    page = context.new_page()
    LoginPage(page).open().login(credentials["email"], credentials["password"])
    expect(page).to_have_url(re.compile(r"/account"))
    context.storage_state(path=path)
    context.close()
    return str(path)


@pytest.fixture
def logged_in_page(new_context, auth_state: str) -> Page:
    return new_context(storage_state=auth_state).new_page()
