""""
Copyright © antonionardella 2023 - https://github.com/antonionardella (https://antonionardella.it)
Description:
Get API data for Shimmer from different sources

Version: 5.5.0
"""
import logging
import discord
import datetime
import pickle
import traceback
import requests
import json
import datetime
import os.path
import helpers.configuration_manager as configuration_manager
from helpers.formatting import format_currency, format_shimmer_amount, generate_discord_timestamp
from helpers.smr_market_data.smd_bitfinex import calculate_total_bitfinex_depth
from helpers.smr_market_data.smd_coingecko import get_coingecko_exchange_data
from helpers.smr_market_data.smd_coingecko import get_coingecko_24h_trading_volume
from helpers.smr_market_data.smd_shimmer import get_shimmer_data
from helpers.smr_market_data.smd_geckoterminal import get_geckoterminal_data
from helpers.smr_market_data.smd_defillama import get_defillama_data


logger = logging.getLogger("discord_bot")

# Load configuration
config = configuration_manager.load_config('config.json')

slack_channel = config["slack_channel"]

market_data_current_week_file_path = "assets/market_data_current_week.pkl"
market_data_last_week_file_path = "assets/market_data_last_week.pkl"

# Static data if the file does not exist
def get_market_data_last_week():
    return {
        # monday
        0: {
            "iota-price-coingecko": 0.17112,
            "24h-volume-coingecko": 15409685.01,
            "tvl-defilama": 227364.37,
            "tvl-geckoterminal": 227364.37,
            "24h-defi-txs": 249,
            "24h-defi-volume": 10271.84
        },
        # tuesday
        1: {
            "iota-price-coingecko": 0.17112,
            "24h-volume-coingecko": 15409685.01,
            "tvl-defilama": 227364.37,
            "tvl-geckoterminal": 227364.37,
            "24h-defi-txs": 249,
            "24h-defi-volume": 10271.84
        },
        # wednesday
        2: {
            "iota-price-coingecko": 0.17112,
            "24h-volume-coingecko": 15409685.01,
            "tvl-defilama": 227364.37,
            "tvl-geckoterminal": 227364.37,
            "24h-defi-txs": 249,
            "24h-defi-volume": 10271.84
        },
        # thursday
        3: {
            "iota-price-coingecko": 0.17583,
            "24h-volume-coingecko": 11092023.27,
            "tvl-defilama": 357441.75,
            "tvl-geckoterminal": 227364.37,
            "24h-defi-txs": 249,
            "24h-defi-volume": 10556.71
        },
        # friday
        4: {
            "iota-price-coingecko": 0.17721,
            "24h-volume-coingecko": 11526929.93,
            "tvl-defilama": 354708.34,
            "tvl-geckoterminal": 227364.37,
            "24h-defi-txs": 116,
            "24h-defi-volume": 11000
        },
        # saturday
        5: {
            "iota-price-coingecko": 0.17249,
            "24h-volume-coingecko": 10855710.61,
            "tvl-defilama": 361149.08,
            "tvl-geckoterminal": 227364.37,
            "24h-defi-txs": 199,
            "24h-defi-volume": 10814.00
        },
        # sunday
        6: {
            "iota-price-coingecko": 0.17117,
            "24h-volume-coingecko": 6617140.13,
            "tvl-defilama": 330935.81,
            "tvl-geckoterminal": 227364.37,
            "24h-defi-txs": 160,
            "24h-defi-volume": 3133.20
        }
    }

# Static data if the file does not exist
def get_market_data_current_week():
    return {
        # monday
        0: {
            "iota-price-coingecko": 0.17159,
            "24h-volume-coingecko": 8582530.23,
            "tvl-defilama": 341339.69,
            "tvl-geckoterminal": 227364.37,
            "24h-defi-txs": 262,
            "24h-defi-volume": 10271.84
        },
        # tuesday
        1: {
            "iota-price-coingecko": 0.16962,
            "24h-volume-coingecko": 9395325.27,
            "tvl-defilama": 338453.06,
            "tvl-geckoterminal": 227364.37,
            "24h-defi-txs": 260,
            "24h-defi-volume": 12556.71
        },
        # wednesday
        2: {
            "iota-price-coingecko": 0.16915,
            "24h-volume-coingecko": 10086899.93,
            "tvl-defilama": 322733.01,
            "tvl-geckoterminal": 227364.37,
            "24h-defi-txs": 472,
            "24h-defi-volume": 24685.36
        },
        # thursday
        3: {
            "iota-price-coingecko": 0.16915,
            "24h-volume-coingecko": 10086899.93,
            "tvl-defilama": 322733.01,
            "tvl-geckoterminal": 227364.37,
            "24h-defi-txs": 472,
            "24h-defi-volume": 24685.36
        },
        # friday
        4: {
            "iota-price-coingecko": 0.16915,
            "24h-volume-coingecko": 10086899.93,
            "tvl-defilama": 322733.01,
            "tvl-geckoterminal": 227364.37,
            "24h-defi-txs": 472,
            "24h-defi-volume": 24685.36
        },
        # saturday
        5: {
            "iota-price-coingecko": 0.16915,
            "24h-volume-coingecko": 10086899.93,
            "tvl-defilama": 322733.01,
            "tvl-geckoterminal": 227364.37,
            "24h-defi-txs": 472,
            "24h-defi-volume": 24685.36
        },
        # sunday
        6: {
            "iota-price-coingecko": 0.16915,
            "24h-volume-coingecko": 10086899.93,
            "tvl-defilama": 322733.01,
            "tvl-geckoterminal": 227364.37,
            "24h-defi-txs": 472,
            "24h-defi-volume": 24685.36
        }
    }

def get_current_weekday():
    today = datetime.datetime.today()
    return today.weekday()

def get_last_weekday():
    today = datetime.datetime.today()
    current_week_day = today.weekday() 
    if (current_week_day == 0):
        return 6
    else:
        return current_week_day - 1

def calc_change_percent(current_value, last_day_value, last_week_value):
    
    try:
        current_value_float = float(current_value)
        last_day_value_float = float(last_day_value)
        last_week_value_float = float(last_week_value)

        change_percent_daily = round((((current_value_float - last_day_value_float) / current_value_float) * 100), 2)
        change_percent_weekly = round((((current_value_float - last_week_value_float) / current_value_float) * 100), 2)

        sign_daily = ""
        if (change_percent_daily > 0):
            sign_daily = "+"
        
        sign_weekly = ""
        if (change_percent_weekly > 0):
            sign_weekly = "+"

        return {
            "daily": "Daily change: " + sign_daily + str(change_percent_daily) + " %",
            "weekly": "Weekly change: " + sign_weekly + str(change_percent_weekly) + " %" 
        }
    except Exception:
        return {
            "daily": "Daily change: N/A",
            "weekly": "Weekly change: N/A" 
        }

# If not exist, 2 files of market data for current week and last week will be created with dump data
def create_market_data_files():
    if (not os.path.isfile(market_data_current_week_file_path)):
        past_data = get_market_data_current_week()
        with open(market_data_current_week_file_path, "wb") as f:
            pickle.dump(json.dumps(past_data), f)
            f.close()

    if (not os.path.isfile(market_data_last_week_file_path)):
        past_data = get_market_data_last_week()
        with open(market_data_last_week_file_path, "wb") as f:
            pickle.dump(json.dumps(past_data), f)
            f.close()

def get_market_data():
    market_data_current_week = ""
    with open(market_data_current_week_file_path, "rb") as f:
        market_data_current_week = json.loads(pickle.load(f))
        f.close()

    market_data_last_week = ""
    with open(market_data_last_week_file_path, "rb") as f:
        market_data_last_week = json.loads(pickle.load(f))
        f.close()

    return {
        "current_week": market_data_current_week,
        "last_week": market_data_last_week
    }

# Update whenever the bot restarts
def update_market_data_current_week_file(market_data_current_week, current_weekday, market_data_current_day_latest):
    # Update market_data_current_week for the current day with latest values
    market_data_current_week[current_weekday] = market_data_current_day_latest
    
    with open(market_data_current_week_file_path, "wb") as f:
        pickle.dump(json.dumps(market_data_current_week), f)
        f.close()

# Update only on every monday
def update_market_data_last_week_file(market_data_current_week, current_weekday):
    if (current_weekday != 0):
        return
    
    with open(market_data_last_week_file_path, "wb") as f:
        pickle.dump(json.dumps(market_data_current_week), f)
        f.close()

async def commented_out_func():
    # Set up Bitfinex order book depth
    bitfinex_order_book_data = await calculate_total_bitfinex_depth(coingecko_data['usd_price'])
    logger.debug("Final bitfinex_order_book_data: %s", bitfinex_order_book_data)


    positive_order_book_depth_str_2_percent = ""
    negative_order_book_depth_str_2_percent = ""
    positive_order_book_depth_str_5_percent = ""
    negative_order_book_depth_str_5_percent = ""
    positive_order_book_depth_str_10_percent = ""
    negative_order_book_depth_str_10_percent = ""
    positive_order_book_depth_str_20_percent = ""
    negative_order_book_depth_str_20_percent = ""


    # Iterate through the order book data and format the strings
    for percentage, data in bitfinex_order_book_data['total_order_book_depth'].items():

        # Format the 'buy' data using format_currency() function
        if 'buy' in data:
            formatted_buy_data = await format_currency(data['buy'], "SMR")
            buy_data = f"Buy: {formatted_buy_data}\n\n"
        else:
            logger.error(f"Missing 'buy' key for percentage level {percentage}")

        # Format the 'sell' data using format_currency() function
        if 'sell' in data:
            formatted_sell_data = await format_currency(data['sell'], "SMR")
            sell_data = f"Sell: {formatted_sell_data}\n\n"
        else:
            logger.error(f"Missing 'sell' key for percentage level {percentage}")

        buy_sell_info = f"**{percentage}**:\n{buy_data if percentage.startswith('-') else sell_data}"

        if int(percentage[:-1]) == -2:
            negative_order_book_depth_str_2_percent += buy_sell_info
        elif int(percentage[:-1]) == -5:
            negative_order_book_depth_str_5_percent += buy_sell_info
        elif int(percentage[:-1]) == -10:
            negative_order_book_depth_str_10_percent += buy_sell_info
        elif int(percentage[:-1]) == -20:
            negative_order_book_depth_str_20_percent += buy_sell_info
        elif int(percentage[:-1]) == 2:
            positive_order_book_depth_str_2_percent += buy_sell_info
        elif int(percentage[:-1]) == 5:
            positive_order_book_depth_str_5_percent += buy_sell_info
        elif int(percentage[:-1]) == 10:
            positive_order_book_depth_str_10_percent += buy_sell_info
        elif int(percentage[:-1]) == 20:
            positive_order_book_depth_str_20_percent += buy_sell_info

# Functions
async def build_embed():
    """
    Build and save a Discord embed message containing Shimmer market data fetched from various sources.
    """
    logger.info("Building Discord embed message")

    try:
        # Get market-related data
        create_market_data_files()
        current_weekday = str(get_current_weekday())
        last_weekday = str(get_last_weekday())
        market_data = get_market_data()
        market_data_current_week = market_data["current_week"]
        market_data_last_week = market_data["last_week"]
        
        logger.info("market_data_current_week")
        logger.info(market_data_current_week)
        logger.info("market_data_last_week")
        logger.info(market_data_last_week)
        logger.info("current_weekday")
        logger.info(current_weekday)
        logger.info("last_weekday")
        logger.info(last_weekday)
        #############################

        # Get data from API calls
        # current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        coingecko_data = await get_coingecko_exchange_data()
        coingecko_24h_vol = await get_coingecko_24h_trading_volume()
        defillama_data = await get_defillama_data()
        geckoterminal_data = await get_geckoterminal_data()
        shimmer_data = await get_shimmer_data()
        total_defi_tx_24h = geckoterminal_data["total_defi_tx_24h"]
        defi_total_volume = geckoterminal_data['defi_total_volume']
        geckoterminal_tvl = geckoterminal_data['total_reserve_in_usd']
        iota_rank = defillama_data["iota_rank"]
        discord_timestamp = await generate_discord_timestamp()

        # await commented_out_func()

        # Create an embed instance
        embed = discord.Embed(title="IOTA Market Data", color=0x00FF00)
        slack_data = [{"type": "header", "text": {"type": "plain_text", "text": "IOTA Market Data"}}]

        my_coin_gecko_usd_price = await format_currency(coingecko_data['usd_price'])

        current_value = coingecko_data['usd_price']
        last_day_value = market_data_current_week[last_weekday]["iota-price-coingecko"]
        last_week_value = market_data_last_week[current_weekday]["iota-price-coingecko"]
        change_percent = calc_change_percent(current_value, last_day_value, last_week_value)

        embed.add_field(name="Price (Coingecko)", value=f"{my_coin_gecko_usd_price}", inline=False)
        slack_data.append({"type": "section", "text": {"type": "mrkdwn", "text": "*Price (Coingecko)*\n" + my_coin_gecko_usd_price + "\n" + change_percent["daily"] + "\n" + change_percent["weekly"]}})

        # embed.add_field(name="24h Volume (Bitfinex)", value=f"{await format_currency(coingecko_data['total_volume'])}", inline=False)
        
        my_coingecko_24h_vol = await format_currency(coingecko_24h_vol)

        current_value = coingecko_24h_vol
        last_day_value = market_data_current_week[last_weekday]["24h-volume-coingecko"]
        last_week_value = market_data_last_week[current_weekday]["24h-volume-coingecko"]
        change_percent = calc_change_percent(current_value, last_day_value, last_week_value)

        embed.add_field(name="24h Volume (Coingecko)", value=f"{my_coingecko_24h_vol}", inline=False)
        slack_data.append({"type": "section", "text": {"type": "mrkdwn", "text": "*24h Volume (Coingecko)*\n" + my_coingecko_24h_vol + "\n" + change_percent["daily"] + "\n" + change_percent["weekly"]}})

        embed.add_field(name="\u200b", value="\u200b", inline=False)
        # slack_data.append({"type": "section", "text": {"type": "mrkdwn", "text": "\n" }})
        slack_data.append({"type": "divider"})

        embed.add_field(name="DeFi Data", value="\u200b", inline=False)
        slack_data.append({"type": "section", "text": {"type": "mrkdwn", "text": "*DeFi Data*\n" }})

        embed.add_field(name="IOTA EVM Rank (DefiLlama)", value=iota_rank, inline=True)
        slack_data.append({"type": "section", "text": {"type": "mrkdwn", "text": "*IOTA EVM Rank (DefiLlama)*\n" + str(iota_rank) }})

        try:
            my_shimmer_onchain_token_amount = await format_currency(await format_shimmer_amount(shimmer_data['shimmer_onchain_token_amount']), 'IOTA')
            embed.add_field(name="IOTA on-chain amount (IOTA API)", value=f"{my_shimmer_onchain_token_amount}", inline=True)
            slack_data.append({"type": "section", "text": {"type": "mrkdwn", "text": "*IOTA on-chain amount (IOTA API)*\n" + my_shimmer_onchain_token_amount }})
        except Exception:
            logger.info(traceback.format_exc())

        my_iota_tvl = await format_currency(defillama_data['iota_tvl'])

        current_value = defillama_data['iota_tvl']
        last_day_value = market_data_current_week[last_weekday]["tvl-defilama"]
        last_week_value = market_data_last_week[current_weekday]["tvl-defilama"]
        change_percent = calc_change_percent(current_value, last_day_value, last_week_value)

        embed.add_field(name="Total Value Locked (DefiLlama)", value=f"{my_iota_tvl}", inline=True)
        slack_data.append({"type": "section", "text": {"type": "mrkdwn", "text": "*Total Value Locked (DefiLlama)*\n" + str(my_iota_tvl) + "\n" + change_percent["daily"] + "\n" + change_percent["weekly"]}})

        current_value = geckoterminal_tvl
        last_day_value
        last_week_value
        try:
            last_day_value = market_data_current_week[last_weekday]["tvl-geckoterminal"]
            last_week_value = market_data_last_week[current_weekday]["tvl-geckoterminal"]
        except Exception:
            last_day_value = None
            last_week_value = None
        
        change_percent = calc_change_percent(current_value, last_day_value, last_week_value)

        my_iota_tvl_geckoterminal = await format_currency(geckoterminal_tvl)
        embed.add_field(name="Total Value Locked (Geckoterminal)", value=f"{my_iota_tvl_geckoterminal}", inline=True)
        slack_data.append({"type": "section", "text": {"type": "mrkdwn", "text": "*Total Value Locked (Geckoterminal)*\n" + str(my_iota_tvl_geckoterminal) + "\n" + change_percent["daily"] + "\n" + change_percent["weekly"]}})

        current_value = total_defi_tx_24h
        last_day_value = market_data_current_week[last_weekday]["24h-defi-txs"]
        last_week_value = market_data_last_week[current_weekday]["24h-defi-txs"]
        change_percent = calc_change_percent(current_value, last_day_value, last_week_value)

        embed.add_field(name="24h DeFi Transactions (GeckoTerminal)", value=total_defi_tx_24h, inline=True)
        slack_data.append({"type": "section", "text": {"type": "mrkdwn", "text": "*24h DeFi Transactions (GeckoTerminal)*\n" + str(total_defi_tx_24h) + "\n" + change_percent["daily"] + "\n" + change_percent["weekly"]}})

        my_defi_total_volume = await format_currency(defi_total_volume)

        current_value = defi_total_volume
        last_day_value = market_data_current_week[last_weekday]["24h-defi-volume"]
        last_week_value = market_data_last_week[current_weekday]["24h-defi-volume"]
        change_percent = calc_change_percent(current_value, last_day_value, last_week_value)

        embed.add_field(name="24h DeFi Volume (GeckoTerminal)", value=f"{my_defi_total_volume}", inline=True)
        slack_data.append({"type": "section", "text": {"type": "mrkdwn", "text": "*24h DeFi Volume (GeckoTerminal)*\n" + str(my_defi_total_volume) + "\n" + change_percent["daily"] + "\n" + change_percent["weekly"]}})

        embed.add_field(name="\u200b", value="\u200b", inline=False)
        # slack_data.append({"type": "section", "text": {"type": "mrkdwn", "text": "\n" }})
        slack_data.append({"type": "divider"})

        # embed.add_field(name="ShimmerEVM Order Books", value="\u200b", inline=False)
        # embed.add_field(name="Order Book depth ±2%", value=f"{negative_order_book_depth_str_2_percent} {positive_order_book_depth_str_2_percent}", inline=True)
        # embed.add_field(name="\u200b", value="\u200b", inline=False)
        # embed.add_field(name="Order Book depth ±5%", value=f"{negative_order_book_depth_str_5_percent} {positive_order_book_depth_str_5_percent}", inline=True)
        # embed.add_field(name="\u200b", value="\u200b", inline=False)
        # embed.add_field(name="Order Book depth ±10%", value=f"{negative_order_book_depth_str_10_percent} {positive_order_book_depth_str_10_percent}", inline=True)
        # embed.add_field(name="\u200b", value="\u200b", inline=False)
        # embed.add_field(name="Order Book depth ±20%", value=f"{negative_order_book_depth_str_20_percent} {positive_order_book_depth_str_20_percent}", inline=True)
        # embed.add_field(name="\u200b", value="\u200b", inline=False)

        # Add additional information
        # my_source = "Bitfinex, Coingecko, DefiLlama, GeckoTerminal, IOTA API"
        # embed.add_field(name="Sources", value=f"{my_source}", inline=False)
        # slack_data.append({"type": "section", "text": {"type": "mrkdwn", "text": "*Sources*\n" + my_source }})

        embed.add_field(name="Last Data Update", value=f"{discord_timestamp}", inline=False)
        slack_data.append({"type": "section", "text": {"type": "mrkdwn", "text": "*Last Data Update*\n" + datetime.datetime.now().strftime("%d/%m/%Y %H:%M")}})

        embed.set_footer(text="Data updated every 24h\nMade with IOTA-❤️ by Holger and Mido")
        # slack_data.append({"type": "divider"})
        slack_data.append({"type": "section", "text": {"type": "plain_text", "text": "Data updated every 24h\n" }})

        # Save the embed to a pickle file
        with open("assets/embed_shimmer_market_data.pkl", "wb") as f:
            pickle.dump(embed, f)

        # Post data to slack channel
        slack_data = '{"blocks": ' + json.dumps(slack_data) + '}'
        # logger.info(slack_data)
        res = requests.post(url=slack_channel, data=slack_data)
        # logger.info(res)

        market_data_current_day_latest = {
            "iota-price-coingecko": coingecko_data['usd_price'],
            "24h-volume-coingecko": coingecko_24h_vol,
            "tvl-defilama": defillama_data['iota_tvl'],
            "tvl-geckoterminal": geckoterminal_tvl,
            "24h-defi-txs": total_defi_tx_24h,
            "24h-defi-volume": defi_total_volume
        }
        
        logger.info("market_data_current_day_latest")
        logger.info(market_data_current_day_latest)

        update_market_data_current_week_file(market_data_current_week, current_weekday, market_data_current_day_latest)
        update_market_data_last_week_file(market_data_current_week, current_weekday)
    except Exception:
        logger.info(traceback.format_exc())


async def main():
    await build_embed()


if __name__ == "__main__":
    main()