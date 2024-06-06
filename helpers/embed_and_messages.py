""""
Copyright © antonionardella 2023 - https://github.com/antonionardella (https://linkfree.antonionardella.it)
Description:
This file contains functions for the IOTA data

Version: 5.4
"""

import pickle
import discord


async def create_empty_embed_and_messages():
    embed = discord.Embed(title="IOTA Market Data", color=0x00FF00)

    embed.add_field(name="Updates: ", value="Every 24h")
    embed.add_field(
        name="❌ Market Data not available yet: ",
        value="Please have patience, the data will be available soon.",
    )
    with open("assets/embed_shimmer_market_data.pkl", "wb") as f:
        pickle.dump(embed, f)