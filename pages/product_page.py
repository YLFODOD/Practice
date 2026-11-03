from playwright.sync_api import Page


class ProductPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.product_name = page.get_by_test_id("product-name")
        self.product_price = page.get_by_test_id("unit-price")
        self.add_to_cart_button = page.get_by_test_id("add-to-cart")
        self.cart_quantity = page.get_by_test_id("cart-quantity")

    def open(self, product_id: str) -> "ProductPage":
        self.page.goto(f"/product/{product_id}")
        return self

    def add_to_cart(self) -> None:
        with self.page.expect_response(
            lambda r: "/carts" in r.url and r.request.method == "POST" and r.ok
        ) as response_info:
            self.add_to_cart_button.click()
