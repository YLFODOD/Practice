from playwright.sync_api import Page


class CartPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.cart_items = page.locator("//span[@data-test='product-title']")
        self.checkout_button = page.get_by_test_id("proceed-1")
        self.product_quantity = page.locator("//input[@data-test='product-quantity']")

    def open(self) -> "CartPage":
        self.page.goto("/checkout")
        return self

    def proceed_to_checkout(self) -> None:
        self.checkout_button.click()

    def set_product_quantity_by_index(self, index: int, quantity: int) -> None:
        self.product_quantity.nth(index).fill(str(quantity))
