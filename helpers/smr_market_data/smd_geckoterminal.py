""""
Copyright © antonionardella 2023 - https://github.com/antonionardella (https://antonionardella.it)
Description:
Get API data for Shimmer from GeckoTerminal API
Version: 5.5.0
"""
import requests
import logging
import helpers.configuration_manager as configuration_manager

logger = logging.getLogger("discord_bot")

# Load configuration
config = configuration_manager.load_config('config.json')

# Shimmer data
geckoterminal_ticker = config["geckoterminal_ticker"]


async def get_geckoterminal_data():
    """
    Get GeckoTerminal Defi Volume data for ShimmerEVM.

    Returns:
        dict: Dictionary containing ShimmerEVM's total 24h volume and total 24h transactions.
    """
    logger.info("Getting GeckoTerminal Defi Volume data for ShimmerEVM")
    geckoterminal_url = f"https://api.geckoterminal.com/api/v2/networks/{geckoterminal_ticker}/pools"
    headers = {"accept": "application/json"}
    total_defi_volume_usd_h24 = 0
    total_defi_tx_24h = 0
    page = 1

    try:
        while True:
            # Make a request to the GeckoTerminal API with the current page number
            defi_volume = requests.get(geckoterminal_url + f"?page={page}", headers=headers, timeout=10)
            defi_volume.raise_for_status()

            if defi_volume.status_code == 200:
                defi_volume_json = defi_volume.json()
                # Extract and parse the JSON response
                defi_volume_data = defi_volume_json.get("data", [])

                for entry in defi_volume_data:
                    h24_volume = float(entry["attributes"]["volume_usd"]["h24"])
                    total_defi_volume_usd_h24 += h24_volume

                    # Extract transactions data for h24
                    transactions_h24 = entry["attributes"]["transactions"]["h24"]
                    buys_h24 = transactions_h24.get("buys", 0)
                    sells_h24 = transactions_h24.get("sells", 0)
                    # Perform operations with buys_h24 and sells_h24 as needed
                    total_defi_tx_24h += buys_h24 + sells_h24

                logger.debug("Total USD 24h Volume for all pools: %s", total_defi_volume_usd_h24)
                logger.debug("Total 24h Defi Transactions for ShimmerEVM: %s", total_defi_tx_24h)

                if total_defi_volume_usd_h24 > 0 and total_defi_tx_24h > 0:
                    return {"defi_total_volume": total_defi_volume_usd_h24, "total_defi_tx_24h": total_defi_tx_24h}
                else:
                    logger.debug("Shimmer Total Volume or Total Transactions not found in the response.")
            elif defi_volume.status_code == 404:
                logger.error("404 Client Error: Not Found for URL: %s", defi_volume.url)
            else:
                logger.error("Unexpected status code: %s", defi_volume.status_code)

            page += 1

    except requests.exceptions.Timeout:
        logger.error("GeckoTerminal API request timed out.")
    except requests.exceptions.HTTPError as errh:
        logger.error("HTTP Error occurred: %s", errh)
    except requests.exceptions.RequestException as err:
        logger.error("Request Exception occurred: %s", err)
    except Exception as e:
        logger.error("An unexpected error occurred: %s", e)