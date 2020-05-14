from discord.ext import commands
import discord
from discord.utils import get
import logging
logger = logging.getLogger('salc1bot')

class MemberManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_memeber_join(self, member):
        logger.info(f'{member} ({member.id}) has joined the server.')

    @commands.Cog.listener()
    async def on_memeber_remove(self, member):
        logger.info(f'{member} ({member.id}) has left the server.')
    
    @commands.command()
    @commands.has_any_role("Moderator","Private Chat Access","Administrator")
    async def addmember(self, ctx, member : discord.Member = None):
        """ Gives someone the member role"""
        #await ctx.message.delete()
        role = get(member.guild.roles, name="Member")
        await member.add_roles(role)
        logmsg = f'> Added member role for {member}'
        await ctx.send(logmsg)
        logger.info(f"{ctx.author} {logmsg[1:]}")

    @commands.command()
    @commands.has_any_role("Moderator","Private Chat Access","Administrator")
    async def removemember(self, ctx, member : discord.Member = None):
        """ Removes the member role from someone """
        #await ctx.message.delete()
        role = get(member.guild.roles, name="Member")
        await member.remove_roles(role)
        logmsg = f'> Removed member role for {member}'
        await ctx.send(logmsg)
        logger.info(f"{ctx.author} {logmsg[1:]}")

def setup(bot):
    bot.add_cog(MemberManagement(bot))