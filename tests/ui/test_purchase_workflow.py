from playwright.sync_api import Page, expect
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.home_page import HomePage
import pytest


@pytest.mark.e2e
def test_add_product_to_cart_and_pay(logged_in_page: Page) -> None:
    home_page = HomePage(logged_in_page)
    product_page = ProductPage(logged_in_page)
    cart_page = CartPage(logged_in_page)

    home_page.open()
    home_page.products.nth(0).click()

    # Add the product to the cart
    product_page.add_to_cart()
    expect(product_page.cart_quantity).to_have_text("1")

    cart_page.open()
    expect(cart_page.cart_items).to_have_count(1)
    
    # Proceed to checkout
    cart_page.proceed_to_checkout()

    # Verify that the checkout page is displayed
    expect(logged_in_page).to_have_url("/checkout")

    expect(cart_page.app_login_msg.nth(0)).to_contain_text("You can proceed to checkout")

    cart_page.checkout_button_2.click()

    # Verify that the this is the Billing Address page
    expect(cart_page.billing_address_header).to_be_visible()

    cart_page.country_dropdown.select_option("SG")

    cart_page.postal_code_input.fill("486036")
    cart_page.house_number_input.fill("1")

    cart_page.checkout_button_3.click()

    cart_page.payment_method_dropdown.select_option("cash-on-delivery")
    cart_page.check_payment_button.click()

    expect(cart_page.payment_success_msg).to_contain_text("Payment was successful")




