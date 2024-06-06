""""
Copyright © antonionardella 2023 - https://github.com/antonionardella (https://antonionardella.it)
Description:
IOTA market data

Version: 5.5.0
"""

from discord.ext import commands
from discord.ext.commands import Context
from helpers import checks
import helpers.configuration_manager as configuration_manager
from helpers.smr_market_data_embed import build_embed
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

    @commands.cooldown(1, 360, commands.BucketType.user)
    @commands.hybrid_command(
        name="smr-market",
        description="Shares the IOTA market data",
    )
    # This will only allow non-blacklisted members to execute the command
    @checks.not_blacklisted()
    async def shimmer_market_data(self, context: Context) -> None:
        """
        This command prints an embed with the IOTA Market data

        :param context: The application command context.
        """
        global bot_reply_channel_id

        if context.message.channel.id != int(bot_reply_channel_id):
            await context.send(
                f"This command can only be used in the <#{bot_reply_channel_id}> channel.", ephemeral=True
            )
            return

        try:
            with open("assets/embed_shimmer_market_data.pkl", "rb") as f:
                embed = pickle.load(f)
            await context.send(embed=embed)

        except Exception:
            print(traceback.format_exc())

    @commands.cooldown(1, 360, commands.BucketType.user)
    @commands.hybrid_command(
        name="updatesmd",
        description="Force updates the IOTA market data (Admin only)",
    )
    # This will only allow owners to execute the command
    @checks.is_owner()
    async def updatesmd(self, context: Context) -> None:
        """
        This command forces an update of IOTA Market data

        :param context: The application command context.
        """
        try:
            await context.send(
                "Hello! IOTA Market Data update launced...", ephemeral=True
            )
            await build_embed()

        except Exception:
            print(traceback.format_exc())

        await context.send(
                "Hello! IOTA Market Data update finished.", ephemeral=True
            )

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Tokens(bot))
