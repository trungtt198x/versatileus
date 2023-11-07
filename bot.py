"""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.5.0
"""

import asyncio

import os
import platform
import random
import logging
import asyncio
import time
import multiprocessing
import aiosqlite
import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot, Context
from helpers import configuration_manager, db_manager, dcsupport, kick_unverified, smr_market_data, embed_and_messages
from helpers.logger import setup_logger
import exceptions

# Set up the logger
setup_logger()

# Load configuration
config = configuration_manager.load_config('config.json')
prefix = config["prefix"]
token = config["token"]
sync_commands_globally = config["sync_commands_globally"]
dc_bot_channel = config["dc_bot_channel"]
tea_comms_channel = config["tea_comms_channel"]

"""
Setup bot intents (events restrictions)
For more information about intents, please go to the following websites:
https://discordpy.readthedocs.io/en/latest/intents.html
https://discordpy.readthedocs.io/en/latest/intents.html#privileged-intents


Default Intents:
intents.bans = True
intents.dm_messages = True
intents.dm_reactions = True
intents.dm_typing = True
intents.emojis = True
intents.emojis_and_stickers = True
intents.guild_messages = True
intents.guild_reactions = True
intents.guild_scheduled_events = True
intents.guild_typing = True
intents.guilds = True
intents.integrations = True
intents.invites = True
intents.messages = True # `message_content` is required to get the content of the messages
intents.reactions = True
intents.typing = True
intents.voice_states = True
intents.webhooks = True

Privileged Intents (Needs to be enabled on developer portal of Discord), please use them only if you need them:
intents.members = True
intents.message_content = True
intents.presences = True
"""

intents = discord.Intents.default()
intents.message_content = True
"""
Uncomment this if you want to use prefix (normal) commands.
It is recommended to use slash commands and therefore not use prefix commands.

If you want to use prefix commands, make sure to also enable the intent below in the Discord developer portal.
"""
# intents.message_content = True

bot = Bot(
    command_prefix=commands.when_mentioned_or(prefix),
    intents=intents,
    help_command=None,
)

bot.logger = logging.getLogger("discord_bot")


def background_task():
    """Launched background tasks"""
    bot.logger.info("Starting background tasks for the DLT ledger data")
    asyncio.run(smr_market_data.main())
    time.sleep(24 * 60 * 60)
    background_task()


def run_bot():
    """Starts the discord bot"""
    asyncio.run(init_db())
    asyncio.run(load_cogs())
    asyncio.run(embed_and_messages.create_empty_embed_and_messages())
    bot.run(token)


async def init_db():
    async with aiosqlite.connect(
        f"{os.path.realpath(os.path.dirname(__file__))}/database/database.db"
    ) as db:
        with open(
            f"{os.path.realpath(os.path.dirname(__file__))}/database/schema.sql"
        ) as file:
            await db.executescript(file.read())
        await db.commit()


async def keep_them_all_alive():
    """
    Function that keeps all threads alive
    """
    bot.logger.info("Looking for threads to keep alive")
    thread_ids = await db_manager.get_keep_alive_thread()
    for thread_id in thread_ids:
        await keep_alive(thread_id)


async def keep_alive(thread_id):
    """
    Function that sends a 'ping' message in the thread and deletes it
    """
    
    bot.logger.info(f'Keeping thread {thread_id} alive')
    try:
        channel = await bot.fetch_channel(int(thread_id))
        msg = await channel.send('ping')
        await msg.delete()
    except discord.NotFound:
        print(f'Thread not found for thread_id: {thread_id}. Consider removing it from the list.')
    except discord.Forbidden:
        print(f'Permission denied for thread_id: {thread_id}. Consider checking bot permissions.')
    except discord.HTTPException as e:
        print(f'An error occurred for thread_id: {thread_id}. Details: {e}')
    except ValueError:
        print(f'Invalid thread_id format: {thread_id}. Consider removing it from the list.')
    except Exception as e:
        print(f'An unexpected error occurred: {e}')
"""
Create a bot variable to access the config file in cogs so that you don't need to import it every time.

The config is available using the following code:
- bot.config # In this file
- self.bot.config # In cogs
"""
bot.configuration_manager = configuration_manager


@bot.event
async def on_ready() -> None:
    """
    The code in this event is executed when the bot is ready.
    """
    bot.logger.info(f"Logged in as {bot.user.name}")
    bot.logger.info(f"discord.py API version: {discord.__version__}")
    bot.logger.info(f"Python version: {platform.python_version()}")
    bot.logger.info(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    bot.logger.info("-------------------")
    status_task.start()
    loop_keep_alive.start()
    kick_users.start()
    if sync_commands_globally:
        bot.logger.info("Syncing commands globally...")
        await bot.tree.sync()


@tasks.loop(minutes=5.0)
async def status_task() -> None:
    """
    Setup the game status task of the bot.
    """
    bot.logger.info("Started change status task")
    statuses = ["with you!", "with Skip!", "with humans!"]
    await bot.change_presence(activity=discord.Game(random.choice(statuses)))
    bot.logger.info("Changes bot status")

@tasks.loop(hours=168.0)
async def loop_keep_alive() -> None:
    """
    Setup the keep alive loop
    """
    bot.logger.info("Started keep alive task")
    await keep_them_all_alive()

@tasks.loop(hours=8.0)
async def kick_users() -> None:
    """
    Setup the kick unverified users loop
    """
    bot.logger.info("Started kick unverified users task")
    await kick_unverified.kick_unverified_accounts(bot)


@bot.event
async def on_message(message: discord.Message) -> None:
    """
    The code in this event is executed every time someone sends a message, with or without the prefix

    :param message: The message that was sent.
    """
    for dc_channel_id in dc_bot_channel:
        if message.channel.id == int(dc_channel_id):
            await dcsupport.ban_main_account(message)
    await bot.process_commands(message)

    if message.author == bot.user or message.author.bot:
        return


@bot.event
async def on_command_completion(context: Context) -> None:
    """
    The code in this event is executed every time a normal command has been *successfully* executed.

    :param context: The context of the command that has been executed.
    """
    full_command_name = context.command.qualified_name
    split = full_command_name.split(" ")
    executed_command = str(split[0])
    if context.guild is not None:
        bot.logger.info(
            f"Executed {executed_command} command in {context.guild.name} (ID: {context.guild.id}) by {context.author} (ID: {context.author.id})"
        )
    else:
        bot.logger.info(
            f"Executed {executed_command} command by {context.author} (ID: {context.author.id}) in DMs"
        )


@bot.event
async def on_command_error(context: Context, error) -> None:
    """
    The code in this event is executed every time a normal valid command catches an error.

    :param context: The context of the normal command that failed executing.
    :param error: The error that has been faced.
    """
    if isinstance(error, commands.CommandOnCooldown):
        minutes, seconds = divmod(error.retry_after, 60)
        hours, minutes = divmod(minutes, 60)
        hours = hours % 24
        embed = discord.Embed(
            description=f"**Please slow down** - You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
            color=0xE02B2B,
        )
        await context.send(embed=embed)
    elif isinstance(error, exceptions.UserBlacklisted):
        """
        The code here will only execute if the error is an instance of 'UserBlacklisted', which can occur when using
        the @checks.not_blacklisted() check in your command, or you can raise the error by yourself.
        """
        embed = discord.Embed(
            description="You are blacklisted from using the bot!", color=0xE02B2B
        )
        await context.send(embed=embed)
        if context.guild:
            bot.logger.warning(
                f"{context.author} (ID: {context.author.id}) tried to execute a command in the guild {context.guild.name} (ID: {context.guild.id}), but the user is blacklisted from using the bot."
            )
        else:
            bot.logger.warning(
                f"{context.author} (ID: {context.author.id}) tried to execute a command in the bot's DMs, but the user is blacklisted from using the bot."
            )
    elif isinstance(error, exceptions.UserNotOwner):
        """
        Same as above, just for the @checks.is_owner() check.
        """
        embed = discord.Embed(
            description="You are not the owner of the bot!", color=0xE02B2B
        )
        await context.send(embed=embed)
        if context.guild:
            bot.logger.warning(
                f"{context.author} (ID: {context.author.id}) tried to execute an owner only command in the guild {context.guild.name} (ID: {context.guild.id}), but the user is not an owner of the bot."
            )
        else:
            bot.logger.warning(
                f"{context.author} (ID: {context.author.id}) tried to execute an owner only command in the bot's DMs, but the user is not an owner of the bot."
            )
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            description="You are missing the permission(s) `"
            + ", ".join(error.missing_permissions)
            + "` to execute this command!",
            color=0xE02B2B,
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(
            description="I am missing the permission(s) `"
            + ", ".join(error.missing_permissions)
            + "` to fully perform this command!",
            color=0xE02B2B,
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="Error!",
            # We need to capitalize because the command arguments have no capital letter in the code.
            description=str(error).capitalize(),
            color=0xE02B2B,
        )
        await context.send(embed=embed)
    else:
        raise error


async def load_cogs() -> None:
    """
    The code in this function is executed whenever the bot will start.
    """
    for file in os.listdir(f"{os.path.realpath(os.path.dirname(__file__))}/cogs"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                await bot.load_extension(f"cogs.{extension}")
                bot.logger.info(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                bot.logger.error(f"Failed to load extension {extension}\n{exception}")

# Create processing for the bot and the background tasks
process_one = multiprocessing.Process(target=run_bot)
process_two = multiprocessing.Process(target=background_task)

# Start the processes
process_one.start()
process_two.start()