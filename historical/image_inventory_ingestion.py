"""
Historical prototype from a marketplace automation project.

This file has been sanitized for public release. Credentials,
account-specific configuration, and storage identifiers have been removed.

It is preserved to document the original implementation and development
process rather than as an example of production-ready code.
"""

import os
import csv
import logging

from google.cloud import storage
from google.oauth2 import service_account


# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Project and configuration paths
project_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

config_folder = os.path.join(project_root, ".config")

# Sanitized placeholder for the original service-account file
credentials_file = os.path.join(
    config_folder,
    "google-service-account.json"
)

csv_files_folder = os.path.join(
    project_root,
    "csv_files"
)

csv_file_path = os.path.join(
    csv_files_folder,
    "cards_from_pics.csv"
)

# Sanitized placeholder for the original Google Cloud Storage bucket
BUCKET_NAME = "YOUR_BUCKET_NAME"


# Initialize Google Cloud Storage client with explicit credentials
try:
    credentials = service_account.Credentials.from_service_account_file(
        credentials_file
    )

    storage_client = storage.Client(
        credentials=credentials
    )

    bucket = storage_client.bucket(
        BUCKET_NAME
    )

    logging.info(
        "Connected to Google Cloud Storage successfully."
    )

except Exception as e:
    logging.error(
        f"Failed to connect to Google Cloud Storage: {e}"
    )
    exit(1)


def extract_data_from_filename(filename):
    """
    Extracts card name and set code from the filename.

    Expected format:
    CARDNAME_SETCODE.jpg

    Example:
    DARK_RENEWAL_SBC1-ENG19.jpg
    """

    try:
        base_name = filename.rsplit(".", 1)[0]

        # Split from the final underscore
        name_parts = base_name.rsplit("_", 1)

        # Convert underscores in the card name back to spaces
        card_name = name_parts[0].replace("_", " ")
        set_code = name_parts[1]

        logging.info(
            f"Extracted data - Card Name: {card_name}, "
            f"Set Code: {set_code} from filename: {filename}"
        )

        return card_name, set_code

    except IndexError:
        logging.warning(
            f"Incorrect filename format: {filename}"
        )

        return None, None


def generate_csv_from_images():
    """
    Generates a CSV file containing information derived from
    image files stored in Google Cloud Storage.
    """

    # Retrieve objects from the bucket
    try:
        blobs = bucket.list_blobs()

        logging.info(
            f"Retrieved list of blobs from bucket: {BUCKET_NAME}"
        )

    except Exception as e:
        logging.error(
            f"Failed to list blobs in bucket {BUCKET_NAME}: {e}"
        )

        return

    # Open CSV file for writing
    try:
        os.makedirs(
            csv_files_folder,
            exist_ok=True
        )

        with open(
            csv_file_path,
            mode="w",
            newline=""
        ) as csvfile:

            fieldnames = [
                "card_name",
                "set_code",
                "rarity",
                "price",
                "quantity",
                "URL"
            ]

            writer = csv.DictWriter(
                csvfile,
                fieldnames=fieldnames
            )

            writer.writeheader()

            logging.info(
                f"Opened CSV file {csv_file_path} for writing."
            )

            # Process each image in the bucket
            for blob in blobs:

                logging.info(
                    f"Processing blob: {blob.name}"
                )

                card_name, set_code = extract_data_from_filename(
                    blob.name
                )

                if not card_name or not set_code:
                    logging.warning(
                        f"Skipping blob {blob.name} "
                        "due to incorrect format."
                    )

                    continue

                # Construct the inventory row
                row = {
                    "card_name": card_name,
                    "set_code": set_code,
                    "rarity": "X",
                    "price": "X",
                    "quantity": 1,
                    "URL": (
                        f"https://storage.googleapis.com/"
                        f"{BUCKET_NAME}/{blob.name}"
                    )
                }

                writer.writerow(row)

                logging.info(
                    f"Added row to CSV: {row}"
                )

    except Exception as e:
        logging.error(
            f"Error writing to CSV file {csv_file_path}: {e}"
        )

        return

    logging.info(
        f"CSV file {csv_file_path} generated successfully."
    )


# Run the script to generate the CSV
generate_csv_from_images()
