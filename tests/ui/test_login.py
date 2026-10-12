"""TC02 — login: valid, wrong password, empty fields.

Note: Toolshop locks a customer account after repeated failed logins, and the
demo accounts are shared by everyone. So the "wrong password" case uses an
email that doesn't exist — never fail logins against the real demo account.
"""

import re

import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage


def test_valid_login_opens_account(page: Page, credentials: dict[str, str]) -> None:
    LoginPage(page).open().login(credentials["email"], credentials["password"])

    expect(page).to_have_url(re.compile(r"/account"))
    expect(page.get_by_test_id("nav-menu")).to_be_visible()


@pytest.mark.parametrize(
    ("email", "password", "error_id"),
    [
        pytest.param("nobody@example.com", "wrong-pass", "login-error", id="unknown-user"),
        pytest.param("", "", "email-error", id="empty-fields"),
        pytest.param("not-an-email", "x", "email-error", id="bad-email-format"),
    ],
)
def test_invalid_login_shows_error(page: Page, email: str, password: str, error_id: str) -> None:
    login = LoginPage(page).open()
    login.login(email, password)

    expect(page.get_by_test_id(error_id)).to_be_visible()
    expect(page).to_have_url(re.compile(r"/auth/login"))
