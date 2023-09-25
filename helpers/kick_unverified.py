""""
Copyright © antonionardella 2023 - https://github.com/antonionardella (https://antonionardella.it)
Description:
Kick Double Counter unverified group members that DCounter was not able to kick

Version: 5.5.0
"""
import discord
import logging
import helpers.configuration_manager as configuration_manager
import asyncio

logger = logging.getLogger("discord_bot")

# Load configuration
config = configuration_manager.load_config('config.json')
unverified_role_name = config["unverified_role_name"]
unverified_role_id = config["unverified_role_id"]
verified_role_id = config["verified_role_id"]

async def kick_unverified_accounts(bot):
    # Find the specific role by its name or ID
    specific_role = discord.utils.get(bot.guilds[0].roles, name=unverified_role_name) or bot.guilds[0].get_role(unverified_role_id)
    
    # Get all members with the specific role
    members_with_role = specific_role.members

    # Wait for 30 seconds for each member with the specific role and kick them
    for member in members_with_role:
        logger.debug(f"Member id: {member.id}")
        if discord.utils.get(member.roles, id=verified_role_id): # has Turing test passed
            # Member has verfied role, remove unverified role if present
            if discord.utils.get(member.roles, id=unverified_role_id):
                await member.remove_roles(bot.guilds[0].get_role(unverified_role_id))
        else:
            # Member does not have verified role, kick them
            await asyncio.sleep(5)
            await member.kick(reason="Verification not completed, please join again and verify your account. https://discord.gg/iota")
            logger.info(member, "kicked", member.id)