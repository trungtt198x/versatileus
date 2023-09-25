""""
Copyright © antonionardella 2023 - https://github.com/antonionardella (https://antonionardella.it)
Description:
Double Counter support bot to bain main accounts of banned alt accounts.

Version: 5.5.0
"""
import discord
import logging
import helpers.configuration_manager as configuration_manager
import re

logger = logging.getLogger("discord_bot")

# Load configuration
config = configuration_manager.load_config('config.json')
dc_bot_channel = config["dc_bot_channel"]

async def ban_main_account(message):
    # Define the message part input that triggers the bot
    dc_message_content = str(":small_red_triangle: Alt-account intrusion")

    # Read the mesage
    logger.debug("Reading the message")
    logger.debug(message.content)
    if message.content.startswith(dc_message_content):
        if message.author.bot == True:
            logger.info("User matched")
            dc_verify_message =  message.content.casefold()

            temp = re.findall(r'\d+', dc_verify_message)
            res = list(map(int, temp))
            for i in range(0, len(res)):
                if i == (len(res)-1):
                    continue
            res.reverse()
            
            await message.channel.send("Bye bye " + str(res[0]))
            userid_to_ban = int(res[0])
                    
            await message.guild.ban(discord.Object(id=userid_to_ban))
            print(str(userid_to_ban) + " gone")
        else:
            logger.info("It is not an ALT account message")