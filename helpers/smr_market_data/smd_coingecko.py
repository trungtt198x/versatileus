""""
Copyright © antonionardella 2023 - https://github.com/antonionardella (https://antonionardella.it)
Description:
Get API data for Shimmer from CoinGecko API
Version: 5.5.0
"""
import requests
import logging
import helpers.configuration_manager as configuration_manager

logger = logging.getLogger("discord_bot")

# Load configuration
config = configuration_manager.load_config('config.json')

# Shimmer data
coingecko_coin_id = config["coingecko_coin_id"]
coingecko_exchange_id = config["coingecko_exchange_id"]


async def get_coingecko_exchange_data():
    """Get Coingecko exchange data"""
    coingecko_exchange_url = f"https://api.coingecko.com/api/v3/exchanges/{coingecko_exchange_id}/tickers?coin_ids={coingecko_coin_id}"
    headers = {"accept": "application/json"}
    try:
        exchange_response = requests.get(coingecko_exchange_url, headers=headers, timeout=10)  # Set a timeout of 10 seconds
        exchange_response.raise_for_status()  # Raise HTTPError for bad requests (4xx and 5xx status codes)
        logger.debug("Coingecko exchange response: %s", exchange_response.text)
    
        if exchange_response.status_code == 200:
            # Extract and parse the JSON response
            exchange_response = exchange_response.json()

            # Extract and sum the respective USD converted volumes for USD and USDT
            usd_volume = 0
            usd_price = 0
            usdt_volume = 0
            twentyfourh_volume = 0

            for ticker in exchange_response["tickers"]:
                if ticker["target"] == "USD":
                    usd_volume += ticker["converted_volume"]["usd"]
                    usd_price += ticker["last"]
                elif ticker["target"] == "USDT":
                    usdt_volume += ticker["converted_volume"]["usd"]

            logger.debug("Last USD Price: %s", usd_price)
            logger.debug("Total USD Converted Volume for USD: %s", usd_volume)
            logger.debug("Total USD Converted Volume for USDT: %s", usdt_volume)
            twentyfourh_volume = usd_volume + usdt_volume
            logger.debug("Total USD Converted 24h Volume for Shimmer: %s", twentyfourh_volume)
            return {"usd_price": usd_price, "total_volume": twentyfourh_volume}

        else:
            logger.debug("Error: Unable to fetch data from the API.")

    except requests.exceptions.Timeout:
        logger.error("Coingecko API request timed out.")
    except requests.exceptions.HTTPError as errh:
        logger.error("HTTP Error occurred: %s", errh)
    except requests.exceptions.RequestException as err:
        logger.error("Request Exception occurred: %s", err)