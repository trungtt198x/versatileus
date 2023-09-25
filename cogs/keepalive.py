""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.5.0
"""
import discord
from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks, db_manager


# Here we name the cog and create a new class for the cog.
class Keepalive(commands.Cog, name="keepalive"):
    def __init__(self, bot):
        self.bot = bot

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.
    
    @commands.hybrid_command(
        name="addthread",
        description="Keep the given thread ID alive",
    )
    # This will only allow owners of the bot to execute the command -> config.json
    @checks.is_owner()
    async def addthread(self, context: Context, thread_id: str):
        """
        This is a testing command that does nothing.

        :param context: The application command context.
        """
        # Do your stuff here
        # Connect to database
        thread_ids = await db_manager.get_keep_alive_thread()
        guild_id = int(context.guild.id)
        thread_id = int(thread_id) # This is needed because /commands do not like long ints in Discord

        if thread_id not in thread_ids:
            embed = discord.Embed(
                description=f"Thread {thread_id} is being kept alive now",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
            await db_manager.add_keep_alive_thread(thread_id, guild_id)
            return

        if thread_id in thread_ids:
            embed = discord.Embed(
                description=f"Thread {thread_id} is already being kept alive",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
            return

    @commands.hybrid_command(
        name="rmthread",
        description="Do not keep the given thread ID alive anymore",
    )
    # This will only allow owners of the bot to execute the command -> config.json
    @checks.is_owner()
    async def rmthread(self, context: Context, thread_id: str):
        """
        This is a testing command that does nothing.

        :param context: The application command context.
        """
        # Do your stuff here
        # Connect to database
        thread_ids = await db_manager.get_keep_alive_thread()
        guild_id = int(context.guild.id)
        thread_id = int(thread_id) # This is needed because /commands do not like long ints in Discord

        if thread_id not in thread_ids:
            embed = discord.Embed(
                description=f"Thread {thread_id} was not being kept alive anyway",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
            return

        await db_manager.remove_keep_alive_thread(thread_id, guild_id)
        embed = discord.Embed(
                description=f"Thread {thread_id} is not being kept alive anymore",
                color=0xE02B2B,
            )
        await context.send(embed=embed)
        return

    @commands.hybrid_command(
        name="lsthread",
        description="'List all monitored threads",
    )
    # This will only allow owners of the bot to execute the command -> config.json
    @checks.is_owner()
    async def lsthread(self, context: Context):
        thread_ids = await db_manager.get_keep_alive_thread()
        embed = discord.Embed(
            description=f"Thread {thread_ids} are being kept alive",
            color=0xE02B2B,
        )
        await context.send(embed=embed)
        return


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Keepalive(bot))
