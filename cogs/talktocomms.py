""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.5.0
"""
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from discord.app_commands import Choice
from helpers import checks
import helpers.configuration_manager as configuration_manager

import logging

logger = logging.getLogger("discord_bot")

# Load configuration
config = configuration_manager.load_config('config.json')
tea_comms_channel = config["tea_comms_channel"]

# Here we name the cog and create a new class for the cog.


class Talktocomms(commands.Cog, name="talktocomms"):
    def __init__(self, bot):
        self.bot = bot

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.
    @commands.hybrid_group(name="talktotea", description="Submit Tweet information to TEA")
    @checks.not_blacklisted()
    async def talktotea(self, context: Context) -> None:
        """
        Lets you send relevant tweet information to TEA members.

        :param context: The hybrid command context.
        """
        if context.invoked_subcommand is None:
            embed = discord.Embed(
                title="Send Tweet",
                description="You need to specify a subcommand.\n\n**Subcommands:**\n`sendtweet` - \
                    Forward tweet information to TEA.\n`test` - Remove an address from your profile.\n`list` - \
                        List the address saved in your profile.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)

    @talktotea.command(
        base="talktotea",
        name="sendtweet",
        description="Lets you forward a Tweet information.",
    )
    @app_commands.choices(
        tweet_categories=[  # param name
            Choice(name="News/Announcements", value="news"),
            Choice(name="Tech Update", value="tech"),
            Choice(name="Educational", value="edu"),
            Choice(name="Campaign", value="camp"),
        ]
)
    @app_commands.describe(
        tweet_categories="Tweet category selection.",
        tweet_url="Tweet URL on X.com",
    )
    @checks.not_blacklisted()
    async def setup_send_tweet(
            self,
            context: Context,
            tweet_categories: Choice[str],
            tweet_url: str,
        ) -> None:
        submitted_by_user_id = context.author.id
        submitted_by_user_name = context.author.name
        channel = self.bot.get_channel(tea_comms_channel)
        logger.info(channel)
        await context.send(f"<@{submitted_by_user_id}>!\nThanks for submitting {tweet_url} in {tweet_categories.name}\n\n \
                        \n**CONTENT GUIDELINES REMINDER**\nRemember, we won't engage or reshare posts containing: \
                        \n- Investment & financial content *(advice, promises of returns, ISC token sales, price pumping, speculation, coin value, staking & rewards, TVL...)* \
                        \n- Unsubstantiated or misleading claims *(audits without proof, implying potential partnerships by tagging high profile accounts, unlikely ETAs...)* \
                        \n- General inappropriate content in a professional setting *(like sexualized imagery/language, trolling/insulting, harassement, private information, drama...)*", ephemeral=True)
        await channel.send(f"Hello <@105306128761503744>\nTweet Category:\n{tweet_categories.value}\nURL:\n{tweet_url}\nSubmitted_by:\n@{submitted_by_user_name}\n\n------\n")
        logger.debug(f"URL: {tweet_url}, category: {tweet_categories.value}, submitted_by: @{submitted_by_user_name}, submitter_id: {submitted_by_user_id}")

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Talktocomms(bot))
