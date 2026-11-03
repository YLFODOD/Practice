from playwright.sync_api import Page, expect
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.home_page import HomePage


def test_add_product_to_cart(page: Page) -> None:
    home_page = HomePage(page)
    product_page = ProductPage(page)
    cart_page = CartPage(page)

    home_page.open()
    home_page.products.nth(0).click()

    # Add the product to the cart
    product_page.add_to_cart()
    expect(product_page.cart_quantity).to_have_text("1")

    cart_page.open()
    expect(cart_page.cart_items).to_have_count(1)

def test_set_product_quantity_in_cart(cart_page_with_items: Page) -> None:
    cart_page = CartPage(cart_page_with_items)

    cart_page.open()
    # Set the quantity of the first product in the cart to 3
    cart_page.set_product_quantity_by_index(0, 3)

    # Verify that the quantity has been updated
    expect(cart_page.product_quantity.nth(0)).to_have_value("3")