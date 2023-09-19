""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.5.0
"""

import os

import aiosqlite

DATABASE_PATH = f"{os.path.realpath(os.path.dirname(__file__))}/../database/database.db"


async def get_blacklisted_users() -> list:
    """
    This function will return the list of all blacklisted users.

    :param user_id: The ID of the user that should be checked.
    :return: True if the user is blacklisted, False if not.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            "SELECT user_id, strftime('%s', created_at) FROM blacklist"
        ) as cursor:
            result = await cursor.fetchall()
            return result


async def is_blacklisted(user_id: int) -> bool:
    """
    This function will check if a user is blacklisted.

    :param user_id: The ID of the user that should be checked.
    :return: True if the user is blacklisted, False if not.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            "SELECT * FROM blacklist WHERE user_id=?", (user_id,)
        ) as cursor:
            result = await cursor.fetchone()
            return result is not None


async def add_user_to_blacklist(user_id: int) -> int:
    """
    This function will add a user based on its ID in the blacklist.

    :param user_id: The ID of the user that should be added into the blacklist.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("INSERT INTO blacklist(user_id) VALUES (?)", (user_id,))
        await db.commit()
        rows = await db.execute("SELECT COUNT(*) FROM blacklist")
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] if result is not None else 0


async def remove_user_from_blacklist(user_id: int) -> int:
    """
    This function will remove a user based on its ID from the blacklist.

    :param user_id: The ID of the user that should be removed from the blacklist.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("DELETE FROM blacklist WHERE user_id=?", (user_id,))
        await db.commit()
        rows = await db.execute("SELECT COUNT(*) FROM blacklist")
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] if result is not None else 0


async def add_keep_alive_thread(thread_id: int, guild_id: int) -> int:
    """
    This function will add a thread to the database.

    :param thread_id: The ID of the thread that should be kept alive.
    :param guild_id: The ID of the server where the thread has been added.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("INSERT INTO threads(thread_id, guild_id) VALUES (?, ?)", (thread_id, guild_id))
        await db.commit()
        
        rows = await db.execute("SELECT COUNT(*) FROM threads")
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] if result is not None else 0

async def remove_keep_alive_thread(thread_id: int, guild_id: int) -> int:
    """
    This function will remove a warn from the database.

    :param thread_id: The ID of the thread.
    :param guild_id: The ID of the server where the thread has been added.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "DELETE FROM threads WHERE thread_id=? AND guild_id=?",
            (
                thread_id,
                guild_id,
            ),
        )
        await db.commit()
        rows = await db.execute(
            "SELECT COUNT(*) FROM threads WHERE thread_id=? AND guild_id=?",
            (
                thread_id,
                guild_id,
            ),
        )
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] if result is not None else 0


async def get_keep_alive_thread() -> list:
    """
    This function will get all the threads to be kept alive.

    :param thread_id: The ID of the thread that should be kept checked.
    :param guild_id: The ID of the server that should be checked.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        rows = await db.execute(
            "SELECT thread_id FROM threads",
        )
        async with rows as cursor:
            result = await cursor.fetchall()
            result_list = []
            for row in result:
                result_list.append(row[0])
            return result_list


async def get_all_guild_ids() -> list:
    """
    This function will get a list of all guild IDs.

    :return: A list of all guild IDs.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        rows = await db.execute(
          "SELECT guild_id FROM threads",
        )
        async with rows as cursor:
            result = await cursor.fetchall()
            result_list = []
            for row in result:
                result_list.append(row[1])
            return result_list
