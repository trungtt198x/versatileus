""""
Copyright © antonionardella 2023 - https://github.com/antonionardella (https://antonionardella.it)
Description:
Get API data for IOTA from CoinGecko API
Version: 5.5.0
"""
import requests
import logging
import helpers.configuration_manager as configuration_manager

logger = logging.getLogger("discord_bot")

# Load configuration
config = configuration_manager.load_config('config.json')

# IOTA data
coingecko_coin_id = config["coingecko_coin_id"]
coingecko_exchange_id = config["coingecko_exchange_id"]
coingecko_api_key = config["coingecko_api_key"]


async def get_coingecko_exchange_data():
    """
    Get Coingecko exchange data for IOTA cryptocurrency.

    Returns:
        dict: A dictionary containing the latest USD price and 24h total volume for IOTA.
              Example: {"usd_price": 0.1234, "total_volume": 1234567.89}
    Raises:
        requests.exceptions.RequestException: If there is an issue with the HTTP request to the Coingecko API.
    """
    logger.info("Getting the Coingecko Exchange data")
    coingecko_exchange_url = f"https://api.coingecko.com/api/v3/exchanges/{coingecko_exchange_id}/tickers?coin_ids={coingecko_coin_id}"
    headers = {"accept": "application/json"}

    try:
        exchange_response = requests.get(coingecko_exchange_url, headers=headers, timeout=10)
        exchange_response.raise_for_status()  # Raise HTTPError for bad requests (4xx and 5xx status codes)
        logger.debug("Coingecko exchange response: %s", exchange_response.text)

        if exchange_response.status_code == 200:
            tickers = exchange_response.json().get("tickers", [])
            usd_volume = sum(ticker["converted_volume"]["usd"] for ticker in tickers if ticker["target"] == "USD")
            usdt_volume = sum(ticker["converted_volume"]["usd"] for ticker in tickers if ticker["target"] == "USDT")
            usd_price = next(ticker["last"] for ticker in tickers if ticker["target"] == "USD")
            twentyfourh_volume = usd_volume + usdt_volume

            logger.debug("Last USD Price: %s", usd_price)
            logger.debug("Total USD Converted Volume for IOTA: %s", twentyfourh_volume)

            return {"usd_price": usd_price, "total_volume": twentyfourh_volume}

        else:
            logger.debug("Error: Unable to fetch data from the API.")

    except requests.exceptions.Timeout:
        logger.error("Coingecko API request timed out.")
    except requests.exceptions.HTTPError as errh:
        logger.error("HTTP Error occurred: %s", errh)
    except requests.exceptions.RequestException as err:
        logger.error("Request Exception occurred: %s", err)

async def get_coingecko_24h_trading_volume():
    """
    Get Coingecko 24h trading volume for IOTA cryptocurrency.

    Returns:
        dict: A dictionary containing the 24h trading volume for IOTA.

    Raises:
        requests.exceptions.RequestException: If there is an issue with the HTTP request to the Coingecko API.
    """
    logger.info("Getting Coingecko 24h trading volume")
    coingecko_exchange_url = f"https://api.coingecko.com/api/v3/simple/price?ids={coingecko_coin_id}&vs_currencies=usd&include_24hr_vol=true"
    headers = {"accept": "application/json", "x-cg-demo-api-key": coingecko_api_key}

    try:
        coingecko_response = requests.get(coingecko_exchange_url, headers=headers, timeout=10)
        coingecko_response.raise_for_status()  # Raise HTTPError for bad requests (4xx and 5xx status codes)
        logger.debug("Coingecko 24h trading volume response: %s", coingecko_response.text)

        if coingecko_response.status_code == 200:
            coingecko_response_data = coingecko_response.json().get(coingecko_coin_id, {})
            usd_24h_vol = coingecko_response_data["usd_24h_vol"]
            logger.debug("usd_24h_vol: %s", usd_24h_vol)

            return usd_24h_vol

        else:
            logger.debug("Error: Unable to fetch data from the API.")

    except requests.exceptions.Timeout:
        logger.error("Coingecko API request timed out.")
    except requests.exceptions.HTTPError as errh:
        logger.error("HTTP Error occurred: %s", errh)
    except requests.exceptions.RequestException as err:
        logger.error("Request Exception occurred: %s", err)
