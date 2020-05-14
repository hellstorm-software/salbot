from discord.ext import commands
import discord
from discord.utils import get
import logging
logger = logging.getLogger('salc1bot')
import os

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    #Ping Command (Ex: Pong! 93ms)
    @commands.command()
    @commands.has_any_role("Member", "Private Chat Access", "OG Role That Has No Purpose", "Moderator", "Administrator")
    async def ping(self, ctx):
        """ Get Discord API ping"""
        await ctx.message.delete()
        await ctx.send(f'> Pong! {round(self.bot.latency * 1000)}ms', delete_after=10)

    @commands.command()
    @commands.has_any_role("Moderator", "Administrator")
    async def restart(self, ctx):
        """ Restart the bot """
        await  self.bot.close()
        os.system('echo "sleep 10; kill $PPID" |at now')
        exit(69) # this should restart the bot if its started with start.sh

def setup(bot):
    bot.add_cog(General(bot))
