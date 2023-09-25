""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.5.0
"""
import discord
from discord.ext import commands
from discord.ext.commands import Context
import re

from helpers import checks, db_manager
                      


class Dcsupport(commands.Cog, name="dcsupport"):
    def __init__(self, bot):
        self.bot = bot

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.

    async def ban_main_account(message):
        # Define the message part input that triggers the bot
        dc_message_content = str(":small_red_triangle: Alt-account intrusion")

        # Read the mesage
        print(message.content)
        if message.content.startswith(dc_message_content) and message.channel.id in bot.config["dc_bot_channel"]:
            if message.author.bot == True:
                bot.logger.info("User matched")
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
                bot.logger.info("It is not an ALT account message")

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Dcsupport(bot))
