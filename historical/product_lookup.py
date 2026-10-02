"""
Historical prototype from a marketplace automation project.

This file has been sanitized for public release. Credentials and
account-specific configuration have been removed.

It is preserved to document the original implementation and development
process rather than as an example of production-ready code.
"""

import os
import requests
import json
from ebaysdk.trading import Connection as Trading
from ebaysdk.exception import ConnectionError
import yaml
import csv
from get_cards import get_card_info


# Paths and configurations
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
config_folder = os.path.join(project_root, '.config')
config_file = os.path.join(config_folder, 'ebay.yaml')

# CSV file path
csv_files_folder = os.path.join(project_root, 'csv_files')
csv_file_path = os.path.join(csv_files_folder, 'cards_from_pics.csv')


# Function to deploy a fixed-price item to eBay
def add_fixed_price_item(
    card_name,
    set_code,
    price,
    quantity,
    rarity=None,
    image_url=None
):
    """
    Creates a fixed-price listing on eBay for a specified Yu-Gi-Oh! card.
    """

    # Fetch card details dynamically using the helper function
    card_details = get_card_info(card_name, set_code, rarity)

    if not card_details:
        print(
            f"Failed to retrieve card details for {card_name} "
            f"with set code {set_code}"
        )
        return

    try:
        # Initialize eBay API connection (Canada site)
        api = Trading(
            config_file=config_file,
            warnings=True,
            debug=True,
            siteid='2'
        )

        # Create dynamic item specifics
        item_specifics = [
            {
                'Name': 'Game',
                'Value': 'Yu-Gi-Oh! TCG'
            },
            {
                'Name': 'Card Type',
                'Value': card_details.get('card_type', 'Trading Card')
            },
            {
                'Name': 'Card Name',
                'Value': card_details['name']
            },
            {
                'Name': 'Features',
                'Value': card_details['edition']
            },
            {
                'Name': 'Rarity',
                'Value': card_details['rarity']
            },
            {
                'Name': 'Attribute',
                'Value': card_details.get('attribute', 'N/A')
            },
            {
                'Name': 'Manufacturer',
                'Value': 'Konami'
            }
        ]

        # Dynamic description generation
        description = (
            f"This is a {card_details['rarity']} "
            f"{card_details['name']} from the "
            f"{card_details['set_name']} set. "
            f"Perfect for collectors!"
        )

        # Item data for eBay listing
        item = {
            'Title': (
                f"{card_details['name']} - "
                f"{set_code} - "
                f"{card_details['rarity']} - "
                f"{card_details['edition']} - Near Mint"
            ),
            'Description': description,
            'PrimaryCategory': {
                'CategoryID': '183454'
            },
            'StartPrice': price,
            'Currency': 'CAD',
            'Country': 'CA',
            'DispatchTimeMax': 3,
            'ListingDuration': 'GTC',
            'ListingType': 'FixedPriceItem',
            'Location': 'Ontario, Canada',
            'Quantity': quantity,
            'ConditionID': 4000,
            'ConditionDescriptors': {
                'ConditionDescriptor': {
                    'Name': '40001',
                    'Value': '400010'
                }
            },
            'SellerProfiles': {
                'SellerPaymentProfile': {
                    'PaymentProfileID': 'YOUR_PAYMENT_PROFILE_ID'
                },
                'SellerReturnProfile': {
                    'ReturnProfileID': 'YOUR_RETURN_PROFILE_ID'
                },
                'SellerShippingProfile': {
                    'ShippingProfileID': 'YOUR_SHIPPING_PROFILE_ID'
                }
            },
            'ItemSpecifics': {
                'NameValueList': item_specifics
            },
            'PictureDetails': {
                'PictureURL': image_url
            }
        }

        # Execute the AddFixedPriceItem API call to create the listing
        response = api.execute(
            'AddFixedPriceItem',
            {'Item': item}
        )

        # Print the response for debugging
        print(
            f"Listing Created for {card_name} "
            f"(Set Code: {set_code}): Response Dictionary:"
        )
        print(response.dict())

    except ConnectionError as e:
        print(f"Error: {e}")

        if e.response:
            print("Response Error Details:")
            print(e.response.dict())


# Function to read from CSV and create listings
def create_listings_from_csv(csv_file_path):
    """
    Reads a CSV file and creates eBay listings for each row.
    """

    with open(csv_file_path, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            # Extract data from the CSV row
            try:
                card_name = row['card_name']
                set_code = row['set_code']

                rarity = (
                    row['rarity']
                    if row['rarity'] != 'X'
                    else None
                )

                price = (
                    float(row['price'])
                    if row['price'] != 'X'
                    else 0.0
                )

                quantity = (
                    int(row['quantity'])
                    if row['quantity'] != 'X'
                    else 1
                )

                image_url = row['URL']

            except ValueError:
                print(
                    f"Skipping row with invalid price or quantity: {row}"
                )
                continue

            print(
                f"Preparing to list: {card_name}, "
                f"Set Code: {set_code}, "
                f"Price: {price}, "
                f"Quantity: {quantity}, "
                f"Rarity: {rarity}, "
                f"URL: {image_url}"
            )

            # Deploy listing for each card entry
            add_fixed_price_item(
                card_name,
                set_code,
                price,
                quantity,
                rarity,
                image_url
            )


# Example call to create listings from CSV
create_listings_from_csv(csv_file_path)
