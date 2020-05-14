from discord.ext import commands
import logging
import discord
import aiosqlite
import re
import json

logger = logging.getLogger('salc1bot')
automation_logger = logging.getLogger('salc1bot.automated')

class Badwords(commands.Cog):
    def __init__(self, bot, badwords):
        self.bot = bot
        self.badwords = list(map(re.compile, badwords))
    
    async def deluser(self, id):
        await self.bot.sql_conn.execute(f"DELETE FROM messagecount WHERE user_id = {id};")
        logger.debug(f"Deleted database entry for {id}")
        
    def isExempt(self, author: discord.User):
        for role in ["Administrator", "Moderator"]:
            if role in map(str, author.roles):
                return True
        return False

    @commands.Cog.listener()
    async def on_message(self, message):
        if isinstance(message.author, discord.User) or message.author.bot:
            return

        if not self.isExempt(message.author) and any(re.search(pattern, message.content) for pattern in self.badwords):
            # Remove the message which triggered the bot
            await message.delete()
            await message.author.send("There are some words discord doesn't like, we have to filter them out.")
            await self.deluser(message.author.id)
            automation_logger.info(f"user {message.author} ({message.author.id}) sent bad word in channel {message.channel.name}, message: \"{message.content[0:1500]}\" ")


def setup(bot):
    with open("data/badwords.json") as f:
        badwords = json.load(f)
    print(badwords)
    bw = Badwords(bot, badwords)
    bot.add_cog(bw)
