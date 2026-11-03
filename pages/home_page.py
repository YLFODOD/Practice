from playwright.sync_api import Page


class HomePage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.products = page.locator("//h5[@data-test='product-name']")

    def open(self) -> "HomePage":
        self.page.goto("/")
        return self
