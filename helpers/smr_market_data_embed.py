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

# Functions
async def build_embed():
    """
    Build and save a Discord embed message containing Shimmer market data fetched from various sources.
    """
    logger.info("Building Discord embed message")

    try:
        # Get data from API calls
        # current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        coingecko_data = await get_coingecko_exchange_data()
        coingecko_24h_vol = await get_coingecko_24h_trading_volume()
        defillama_data = await get_defillama_data()
        # geckoterminal_data = await get_geckoterminal_data()
        shimmer_data = await get_shimmer_data()
        # total_defi_tx_24h = geckoterminal_data["total_defi_tx_24h"]
        iota_rank = defillama_data["iota_rank"]
        discord_timestamp = await generate_discord_timestamp()

        # Set up Bitfinex order book depth
        # bitfinex_order_book_data = await calculate_total_bitfinex_depth(coingecko_data['usd_price'])
        # logger.debug("Final bitfinex_order_book_data: %s", bitfinex_order_book_data)


        # positive_order_book_depth_str_2_percent = ""
        # negative_order_book_depth_str_2_percent = ""
        # positive_order_book_depth_str_5_percent = ""
        # negative_order_book_depth_str_5_percent = ""
        # positive_order_book_depth_str_10_percent = ""
        # negative_order_book_depth_str_10_percent = ""
        # positive_order_book_depth_str_20_percent = ""
        # negative_order_book_depth_str_20_percent = ""


        # # Iterate through the order book data and format the strings
        # for percentage, data in bitfinex_order_book_data['total_order_book_depth'].items():

        #     # Format the 'buy' data using format_currency() function
        #     if 'buy' in data:
        #         formatted_buy_data = await format_currency(data['buy'], "SMR")
        #         buy_data = f"Buy: {formatted_buy_data}\n\n"
        #     else:
        #         logger.error(f"Missing 'buy' key for percentage level {percentage}")

        #     # Format the 'sell' data using format_currency() function
        #     if 'sell' in data:
        #         formatted_sell_data = await format_currency(data['sell'], "SMR")
        #         sell_data = f"Sell: {formatted_sell_data}\n\n"
        #     else:
        #         logger.error(f"Missing 'sell' key for percentage level {percentage}")

        #     buy_sell_info = f"**{percentage}**:\n{buy_data if percentage.startswith('-') else sell_data}"

        #     if int(percentage[:-1]) == -2:
        #         negative_order_book_depth_str_2_percent += buy_sell_info
        #     elif int(percentage[:-1]) == -5:
        #         negative_order_book_depth_str_5_percent += buy_sell_info
        #     elif int(percentage[:-1]) == -10:
        #         negative_order_book_depth_str_10_percent += buy_sell_info
        #     elif int(percentage[:-1]) == -20:
        #         negative_order_book_depth_str_20_percent += buy_sell_info
        #     elif int(percentage[:-1]) == 2:
        #         positive_order_book_depth_str_2_percent += buy_sell_info
        #     elif int(percentage[:-1]) == 5:
        #         positive_order_book_depth_str_5_percent += buy_sell_info
        #     elif int(percentage[:-1]) == 10:
        #         positive_order_book_depth_str_10_percent += buy_sell_info
        #     elif int(percentage[:-1]) == 20:
        #         positive_order_book_depth_str_20_percent += buy_sell_info

        # Create an embed instance
        embed = discord.Embed(title="IOTA Market Data", color=0x00FF00)
        embed.add_field(name="Price (Coingecko)", value=f"{await format_currency(coingecko_data['usd_price'])}", inline=False)
        # embed.add_field(name="24h Volume (Bitfinex)", value=f"{await format_currency(coingecko_data['total_volume'])}", inline=False)
        embed.add_field(name="24h Volume (Coingecko)", value=f"{await format_currency(coingecko_24h_vol)}", inline=False)
        embed.add_field(name="\u200b", value="\u200b", inline=False)
        embed.add_field(name="Defi Data", value="\u200b", inline=False)
        embed.add_field(name="IOTA Rank (DefiLlama)", value=iota_rank, inline=True)
        embed.add_field(name="IOTA on-chain amount (IOTA API)", value=f"{await format_currency(await format_shimmer_amount(shimmer_data['shimmer_onchain_token_amount']), 'IOTA')}", inline=True)
        embed.add_field(name="Total Value Locked (DefiLlama)", value=f"{await format_currency(defillama_data['iota_tvl'])}", inline=True)
        # embed.add_field(name="24h DeFi Transactions (GeckoTerminal)", value=total_defi_tx_24h, inline=True)
        # embed.add_field(name="24h DeFi Volume (GeckoTerminal)", value=f"{await format_currency(geckoterminal_data['defi_total_volume'])}", inline=True)
        embed.add_field(name="\u200b", value="\u200b", inline=False)
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
        embed.add_field(name="Sources", value="Bitfinex, Coingecko, DefiLlama, GeckoTerminal, IOTA API", inline=False)
        embed.add_field(name="Last Data Update", value=f"{discord_timestamp}", inline=False)
        embed.set_footer(text="Data updated every 24h\nMade with IOTA-❤️ by Holger and Mido")

        # Save the embed to a pickle file
        with open("assets/embed_shimmer_market_data.pkl", "wb") as f:
            pickle.dump(embed, f)

    except Exception:
        logger.info(traceback.format_exc())


async def main():
    await build_embed()


if __name__ == "__main__":
    main()