"""Page Object for /auth/login (Day 4 / TC06 — start here, then add more pages)."""

from playwright.sync_api import Page


class LoginPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.email = page.get_by_test_id("email")
        self.password = page.get_by_test_id("password")
        self.submit = page.get_by_test_id("login-submit")
        self.login_error = page.get_by_test_id("login-error")
        self.email_error = page.get_by_test_id("email-error")
        self.password_error = page.get_by_test_id("password-error")

    def open(self) -> "LoginPage":
        self.page.goto("/auth/login")
        return self

    def login(self, email: str, password: str) -> None:
        self.email.fill(email)
        self.password.fill(password)
        self.submit.click()
