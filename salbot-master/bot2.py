import os
import sys
import asyncio
import discord
import random
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from discord.utils import get
import logging
from dotenv import load_dotenv
from pathlib import Path
import aiosqlite
load_dotenv(dotenv_path="./salbot-secrets/.env")

logger = logging.getLogger("salc1bot")

client = commands.Bot(command_prefix = '!')

db_p = Path("./data/autorankup.db").resolve()


extensions = [
    "cogs.general",
    "cogs.logging",
    "cogs.user_info",
    "cogs.faq",
    "cogs.serverstatus",
    "cogs.badwords",
    "cogs.member_management",
    "cogs.tosbot",
    "salbot-secrets.autorankup"
]

@client.event
async def on_ready():
    client.remove_command("help")
    client.sql_conn = await aiosqlite.connect(db_p)
    for exten in extensions:
        client.load_extension(exten)
        logger.info(f"Loaded extension: {exten}")
    await client.change_presence(status=discord.Status.online, activity=discord.Game("Leaking salc\'s base in progress"))
    logger.info(f"{client.user} has connected to Discord!")


@client.command()
@commands.has_any_role("Moderator", "Administrator")
async def reload(ctx):
    """ Reload all extensions """
    for exten in extensions:
        client.reload_extension(exten)
        logger.info(f"Reloaded extension: {exten}")
    await ctx.send("Reload Succesfull")

@client.event
async def on_error(event, *args, **kwargs):
    logger.error(f"Error in event: {event} with args {args},{kwargs}", exc_info=sys.exc_info())


## ----------------------------------- DONT EDIT PAST THIS LINE UNLESS YOU KNOW WHAT YOU'RE DOING! --------------------------------------------
if __name__ == "__main__": # only run bot if this file wasn't imported
    try: 
        client.run(os.environ["TOKEN"])
    except discord.errors.LoginFailure as error:
        print("wrong token")
        logger.info(f"Error logging in! Error: {error}" )
