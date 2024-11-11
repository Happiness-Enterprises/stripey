#!/usr/bin/env python
"""Stripe Payment Link code"""

import os
from argparse import ArgumentParser

import stripe
from dotenv import load_dotenv

STRIPE_KEY: str = ""
STRIPE_KWARGS = {}
STRIPE_ADJUSTABLE_QUANTITY = False
STRIPE_ALLOW_PROMOTION_CODES = False
STRIPE_APPLICATION_FEE_PERCENT = 0.0
STRIPE_AUTOMATIC_TAX = False
STRIPE_COLLECT_PHONE_NUMBERS = False
STRIPE_QUANTITY = 1


def set_globals_from_env(env_file):
    """Load environment and set global constants."""
    # pylint: disable=global-statement
    if env_file and os.path.exists(env_file):
        load_dotenv(env_file)

    global STRIPE_KEY
    global STRIPE_ADJUSTABLE_QUANTITY
    global STRIPE_ALLOW_PROMOTION_CODES
    global STRIPE_APPLICATION_FEE_PERCENT
    global STRIPE_AUTOMATIC_TAX
    global STRIPE_COLLECT_PHONE_NUMBERS
    global STRIPE_QUANTITY

    STRIPE_KEY = os.environ["STRIPE_KEY"]
    STRIPE_ADJUSTABLE_QUANTITY = bool(
        os.getenv("STRIPE_ADJUSTABLE_QUANTITY", "false").lower() == "true"
    )
    STRIPE_ALLOW_PROMOTION_CODES = bool(
        os.getenv("STRIPE_ALLOW_PROMOTION_CODES", "false").lower() == "true"
    )
    STRIPE_APPLICATION_FEE_PERCENT = float(
        os.getenv("STRIPE_APPLICATION_FEE_PERCENT", "0.0")
    )
    STRIPE_AUTOMATIC_TAX = bool(
        os.getenv("STRIPE_AUTOMATIC_TAX", "false").lower() == "true"
    )
    STRIPE_COLLECT_PHONE_NUMBERS = bool(
        os.getenv("STRIPE_COLLECT_PHONE_NUMBERS").lower() == "true"
    )
    STRIPE_QUANTITY = int(os.getenv("STRIPE_QUANTITY", "1"))

    stripe.api_key = STRIPE_KEY


def select_item_index(items: list) -> any:
    """Allow user to interactively select an item."""
    item_number = None
    while item_number is None:
        item_number = input(f"Select 1 - {len(items)}? ")
        try:
            item_number = int(item_number)
        except ValueError:
            item_number = None
            print("Invalid input detected; enter a number.")
            continue

        if item_number < 1 or item_number > len(items):
            item_number = None
            print(f"Valid values are between 1 and {len(items)}")
    return items[item_number - 1]


def choose_int(prompt: str, default: int = None) -> int:
    value = None
    if default is not None:
        prompt = f"{prompt} ({default})"
    while value is None:
        value = input(f"{prompt}? ") or str(default)
        try:
            value = int(value)
        except ValueError:
            value = None
            print("Invalid input detected; enter an integer.")
            continue
    return value


def choose_float(prompt: str, default: float = None) -> float:
    value = None
    if default is not None:
        prompt = f"{prompt} ({default})"
    while value is None:
        value = input(f"{prompt}? ") or str(default)
        try:
            value = float(value)
        except ValueError:
            value = None
            print("Invalid input detected; enter a decimal.")
            continue
    return value


def choose_bool(prompt: str, default: bool = False) -> bool:
    options = "[y]/n" if default else "y/[n]"
    value = input(f"{prompt} ({options})? ").lower()
    if not value:
        return default
    return value.startswith("y")


def choose_account(accounts: list[stripe.Account]) -> stripe.Account:
    """Allow user to interactively select an :class:`stripe.Account`."""
    print("Please select an account:")
    for idx, account in enumerate(accounts):
        print(f"  {idx+1}. {account.business_profile.name} ({account.id})\n")
    return select_item_index(accounts)


def choose_product(
    account: stripe.Account, products: list[stripe.Product]
) -> stripe.Product:
    """Allow user to interactively select a :class:`stripe.Product`."""
    print(f"Please select one of {account.business_profile.name}'s products:")
    for idx, product in enumerate(products):
        price = stripe.Price.retrieve(product.default_price, **STRIPE_KWARGS)
        livemode = "LIVE" if product.livemode else "TEST"
        print(
            f"  {idx+1}. {product.name} ({product.id}):"
            f" {price.unit_amount} {price.currency}"
        )
        print(f"      * mode: {livemode}")
        if price.recurring:
            for key, value in price.recurring.items():
                print(f"      * {key}: {value}")
        print()
    return select_item_index(products)


def create_payment_link(**kwargs) -> stripe.PaymentLink:
    """Create a :class:`stripe.PaymentLink`."""
    return stripe.PaymentLink.create(
        **STRIPE_KWARGS,
        line_items=[
            {
                "price": "price_1QJQweHhPlF00wZxeWF3Lh7p",
                "quantity": 1,
            }
        ],
        application_fee_percent=3.0,
    )


def main():
    """Main method"""
    parser = ArgumentParser()
    parser.add_argument(
        "-e",
        "--env",
        default=".env",
        help="ENV file with values.",
    )

    args = parser.parse_args()
    set_globals_from_env(env_file=args.env)

    accounts = stripe.Account.list()
    account = choose_account(accounts.data)
    STRIPE_KWARGS["stripe_account"] = account.id
    print(f"\nUsing connected account: {account.id}.\n")

    products = stripe.Product.list(**STRIPE_KWARGS)
    product = choose_product(account, products.data)
    quantity = choose_int("Quantity", STRIPE_QUANTITY)
    adjustable_quantity = choose_bool("Adjustable quantity", STRIPE_ADJUSTABLE_QUANTITY)
    application_fee_percent = choose_float(
        "Application fee percent",
        STRIPE_APPLICATION_FEE_PERCENT,
    )
    allow_promotion_codes = choose_bool(
        "Allow promotion codes", STRIPE_ALLOW_PROMOTION_CODES
    )
    collect_phone_numbers = choose_bool(
        "Collect phone numbers", STRIPE_COLLECT_PHONE_NUMBERS
    )
    automatic_tax = choose_bool(
        "Automatically collect taxes from customer", STRIPE_AUTOMATIC_TAX
    )
    payment_link = stripe.PaymentLink.create(
        **STRIPE_KWARGS,
        line_items=[
            {
                "price": product.default_price,
                "quantity": quantity,
                "adjustable_quantity": {
                    "enabled": adjustable_quantity,
                },
            },
        ],
        application_fee_percent=application_fee_percent,
        allow_promotion_codes=allow_promotion_codes,
        phone_number_collection={"enabled": collect_phone_numbers},
        automatic_tax={"enabled": automatic_tax},
    )

    mode = "LIVE" if payment_link.livemode else "TEST"
    print(f"Payment Link Created ({mode} mode): {payment_link.url}")
    view_details = choose_bool("View details")
    if view_details:
        print(payment_link)
