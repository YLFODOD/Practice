from playwright.sync_api import Page


class CartPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.cart_items = page.locator("//span[@data-test='product-title']")
        self.checkout_button = page.get_by_test_id("proceed-1")
        self.checkout_button_2 = page.get_by_test_id("proceed-2")
        self.checkout_button_3 = page.get_by_test_id("proceed-3")
        self.product_quantity = page.locator("//input[@data-test='product-quantity']")
        self.app_login_msg = page.locator("//app-login")
        self.billing_address_header = page.get_by_role("heading", name="Billing Address")
        self.country_dropdown = page.get_by_test_id("country")
        self.postal_code_input = page.get_by_test_id("postal_code")
        self.house_number_input = page.get_by_test_id("house_number")
        self.state_input = page.get_by_test_id("state")
        self.payment_method_dropdown = page.get_by_test_id("payment-method")
        self.check_payment_button = page.get_by_test_id("finish")
        self.payment_success_msg = page.get_by_test_id("payment-success-message")

    def open(self) -> "CartPage":
        self.page.goto("/checkout")
        return self

    def proceed_to_checkout(self) -> None:
        self.checkout_button.click()

    def set_product_quantity_by_index(self, index: int, quantity: int) -> None:
        self.product_quantity.nth(index).fill(str(quantity))
