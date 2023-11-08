""""
Copyright © antonionardella 2023 - https://github.com/antonionardella (https://antonionardella.it)
Description:
Get API data for Shimmer from Shimmer API
Version: 5.5.0
"""
import requests
import logging
import helpers.configuration_manager as configuration_manager

logger = logging.getLogger("discord_bot")

# Load configuration
config = configuration_manager.load_config('config.json')

# Shimmer data
shimmer_onchain_deposit_alias = config["shimmer_onchain_deposit_alias"]

async def get_shimmer_data():
    """Get Shimmer Explorer API data"""
    shimmer_explorer_api_url = f"https://api.shimmer.network/api/indexer/v1/outputs/alias/{shimmer_onchain_deposit_alias}"
    headers = {"accept": "application/json"}
    try:
        shimmer_api_response = requests.get(shimmer_explorer_api_url, headers=headers, timeout=10)
        shimmer_api_response.raise_for_status()
        logger.debug("Shimmer Explorer API response: %s", shimmer_api_response.text)

        if shimmer_api_response.status_code == 200:
            # Extract and parse the JSON response
            shimmer_api_response = shimmer_api_response.json()
            
            response_output_id = shimmer_api_response.get("items", [])[0]
            shimmer_onchain_token_amount = None

            if response_output_id:
                output_url = f"https://api.shimmer.network/api/core/v2/outputs/{response_output_id}"
                while True:
                    response_output_id = requests.get(output_url)
                    output_id_data = response_output_id.json()

                    if output_id_data.get("metadata", {}).get("isSpent"):
                        item_content = output_id_data.get("metadata", {}).get("transactionIdSpent")
                        output_url = f"https://api.shimmer.network/api/core/v2/outputs/{item_content}"
                    else:
                        shimmer_onchain_token_amount = output_id_data.get("output", {}).get("amount")
                        break
            
            if shimmer_onchain_token_amount is not None:
                logger.debug("Shimmer On Chain Amount: %s", shimmer_onchain_token_amount)
                return {"shimmer_onchain_token_amount":  shimmer_onchain_token_amount}
            else:
                logger.debug("Shimmer TVL Value not found in the response.")

        else:
            logger.debug("Error: Unable to fetch data from the API.")

    except requests.exceptions.Timeout:
        logger.error("Shimmer API request timed out.")
    except requests.exceptions.HTTPError as errh:
        logger.error("HTTP Error occurred: %s", errh)
    except requests.exceptions.RequestException as err:
        logger.error("Request Exception occurred: %s", err)