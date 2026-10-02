"""
Historical prototype from a marketplace automation project.

This file has been sanitized for public release. Credentials,
account-specific configuration, and identifying information have
been removed.

It is preserved to document the original implementation and development
process rather than as an example of production-ready code.
"""

import os

from ebaysdk.trading import Connection as Trading
from ebaysdk.exception import ConnectionError


# Paths and configuration
project_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

config_folder = os.path.join(project_root, ".config")
config_file = os.path.join(config_folder, "ebay.yaml")


def verify_and_submit(item):
    """
    Verifies an eBay listing payload before attempting submission.

    The listing is submitted only when eBay's verification response
    returns a successful acknowledgement.
    """

    try:
        api = Trading(
            config_file=config_file,
            warnings=True,
            debug=True,
            siteid="2"
        )

        # Validate the listing with eBay before creating it
        verification_response = api.execute(
            "VerifyAddFixedPriceItem",
            {"Item": item}
        )

        verification_result = verification_response.dict()
        acknowledgement = verification_result.get("Ack")

        print(
            f"Verification result: {acknowledgement}"
        )

        # Only perform the actual listing operation after
        # successful verification.
        if acknowledgement == "Success":

            print(
                "Verification successful. "
                "Submitting listing..."
            )

            submission_response = api.execute(
                "AddFixedPriceItem",
                {"Item": item}
            )

            print("Listing submitted.")
            print(submission_response.dict())

            return submission_response

        print(
            "Verification failed. "
            "Listing was not submitted."
        )

        print(verification_result)

        return None

    except ConnectionError as e:
        print(f"eBay API error: {e}")

        if e.response:
            print("Response Error Details:")
            print(e.response.dict())

        return None
