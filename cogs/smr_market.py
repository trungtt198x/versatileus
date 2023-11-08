""""
Copyright © antonionardella 2023 - https://github.com/antonionardella (https://antonionardella.it)
Description:
Shimmer market data

Version: 5.5.0
"""

from discord.ext import commands
from discord.ext.commands import Context
from helpers import checks
import helpers.configuration_manager as configuration_manager
import logging
import pickle
import traceback

logger = logging.getLogger("discord_bot")

# Load configuration
config = configuration_manager.load_config('config.json')
bot_reply_channel_id = config["bot_reply_channel"]


# Here we name the cog and create a new class for the cog.
class Tokens(commands.Cog, name="tokens"):
    def __init__(self, bot):
        self.bot = bot

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.

    @commands.cooldown(1, 3600, commands.BucketType.user)
    @commands.hybrid_command(
        name="smr-market",
        description="Shares the Shimmer market data",
    )
    # This will only allow non-blacklisted members to execute the command
    @checks.not_blacklisted()
    async def shimmer_market_data(self, context: Context):
        """
        This command prints an embed with the Shimmer Market data

        :param context: The application command context.
        """
        global bot_reply_channel_id
        # Do your stuff here

        if context.message.channel.id != int(bot_reply_channel_id):
            await context.send(
                f"This command can only be used in the <#{bot_reply_channel_id}> channel."
            )
            return

        try:
            with open("assets/embed_shimmer_market_data.pkl", "rb") as f:
                embed = pickle.load(f)
            await context.send(embed=embed)

        except Exception:
            print(traceback.format_exc())


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Tokens(bot))
