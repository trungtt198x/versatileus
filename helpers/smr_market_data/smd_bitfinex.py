""""
Copyright © antonionardella 2023 - https://github.com/antonionardella (https://antonionardella.it)
Description:
Get API data for Shimmer from Bitfinex V2 API
Version: 5.5.0
"""
import requests
import logging
import helpers.configuration_manager as configuration_manager

logger = logging.getLogger("discord_bot")

# Load configuration
config = configuration_manager.load_config('config.json')

# Shimmer data
bitfinex_tickers = config["bitfinex_tickers"]
percentage_levels = [-2, 2, -5, 5, -10, 10, -20, 20]

# Functions
async def get_bitfinex_order_book_data(ticker):
    """
    Get Bitfinex order book data for a specific ticker from the API.
    
    Args:
        ticker (str): The Bitfinex ticker symbol for the cryptocurrency pair.
        
    Returns:
        dict: A dictionary containing order book data for the specified ticker.
              The dictionary includes price, quantity, and other relevant information
              for both buy and sell orders in the order book.
    Raises:
        requests.exceptions.RequestException: If there is an issue with the HTTP request to the Bitfinex API.
    """
    # Make the API request to get order book data
    url = f"https://api-pub.bitfinex.com/v2/book/{ticker}/R0?len=100"
    headers = {"accept": "application/json"}
    book_response = None

    try:
        book_response = requests.get(url, headers=headers, timeout=10)
        book_response.raise_for_status()  # Raise HTTPError for bad requests (4xx and 5xx status codes)
        logger.debug("Bitfinex book response: %s", book_response.text)

        if book_response.status_code == 200:
            order_book_data = book_response.json()
            return order_book_data

    except requests.exceptions.Timeout:
        logger.error("Bitfinex API request timed out.")
    except requests.exceptions.HTTPError as errh:
        logger.error("HTTP Error occurred: %s", errh)
    except requests.exceptions.RequestException as err:
        logger.error("Request Exception occurred: %s", err)


async def combine_bitfinex_order_book_data():
    """
    Combine order book data for multiple Bitfinex tickers into a dictionary.
    
    Returns:
        dict: A dictionary where keys are Bitfinex tickers, and values are dictionaries containing
              order book data for each ticker. Each inner dictionary includes price, quantity,
              and other relevant information for both buy and sell orders in the order book.
    Raises:
        requests.exceptions.RequestException: If there is an issue with the HTTP request to the Bitfinex API.
    """
    order_books_data = {}

    try:
        logger.debug("Bitfinex tickers: %s", bitfinex_tickers)

        for ticker in bitfinex_tickers:
            order_book_data = await get_bitfinex_order_book_data(ticker)

            if order_book_data is not None:
                order_books_data[ticker] = order_book_data
                logger.debug("Order book data %s", order_book_data) 

        return order_books_data

    except requests.exceptions.RequestException as err:
        logger.error("Request Exception occurred: %s", err)


async def get_bitfinex_order_book_depth(usd_price):
    """
    Get the order book depth for a list of Bitfinex tickers at various percentage levels.
    
    Args:
        tickers (list): A list of Bitfinex tickers for which order book depth is to be calculated.
        usd_price (float): The current USD price of the cryptocurrency.
        
    Returns:
        dict: A dictionary containing order book depth for each ticker at different percentage levels.
              The keys are tickers, and the values are dictionaries with buy and sell quantities
              for each specified percentage level.
    Raises:
        requests.exceptions.RequestException: If there is an issue with the HTTP request to the Bitfinex API.
    """
    order_book = await combine_bitfinex_order_book_data()
    order_book_depth = {}

    try:

        # Iterate through tickers
        for ticker, orders in order_book.items():
            ticker_depth = {}

            # Iterate percentage levels
            for percentage in percentage_levels:
                price_level = usd_price * (1 + percentage / 100)
                # price_level = round(price_level, 2)  # Round to 2 decimal places to match order book granularity
                buy_quantity = 0
                sell_quantity = 0
                logger.debug("Order book in function: %s", order_book)

                # Iterate through the entries and collect order book values
                for order in orders:
                    price = order[1]
                    amount = order[2]

                    # If the order price is within the specified percentage range
                    if price >= price_level and amount > 0:
                        buy_quantity += amount
                    elif price <= price_level and amount < 0:
                        sell_quantity -= amount  # Convert negative amount to positive for sell orders

                ticker_depth[f'{percentage}%'] = {'buy': buy_quantity, 'sell': sell_quantity}
                logger.debug("Depth after for loop: %s", ticker_depth)
            
            order_book_depth[ticker] = ticker_depth

        logger.debug(f"Order book depth: %s", order_book_depth)
        return order_book_depth
    
    except requests.exceptions.RequestException as err:
        logger.error("Request Exception occurred: %s", err)


async def calculate_total_bitfinex_depth(usd_price):
    """
    Calculate the total Bitfinex order book depth by summing buy and sell quantities
    for each percentage level across multiple tickers.
    
    Args:
        tickers (list): A list of Bitfinex tickers for which total order book depth is to be calculated.
        usd_price (float): The current USD price of the cryptocurrency.
        
    Returns:
        dict: A dictionary containing the total order book depth for each percentage level.
              The keys are percentage levels, and the values are dictionaries with total buy
              and sell quantities across all specified tickers.
    """
    logger.info("Calculating the total Bitfinex Order Book Depth")
    order_book_depth = await get_bitfinex_order_book_depth(usd_price)
    logger.debug("order_book_depth for calculate total: %s", order_book_depth)
    total_order_book_depth = {}

    # Iterate through percentage levels
    for percentage, data in order_book_depth[list(order_book_depth.keys())[0]].items():
        total_buy = 0
        total_sell = 0

        # Iterate through tickers and sum the buy and sell quantities for the current percentage level
        for ticker, ticker_data in order_book_depth.items():
            total_buy += ticker_data[percentage]['buy']
            total_sell += ticker_data[percentage]['sell']
            
        # Add the total buy and sell quantities for the current percentage level to the result dictionary
        total_order_book_depth[percentage] = {'buy': total_buy, 'sell': total_sell}
    return {"total_order_book_depth":  total_order_book_depth}