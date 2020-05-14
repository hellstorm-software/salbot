from discord.ext import commands
from mcstatus import MinecraftServer
import discord
import socket
import logging
logger = logging.getLogger('salc1bot')

class ServerStatus(commands.Cog):
    def __init__(self, bot, channel_server_mapping):
        self.bot = bot
        self.channel_server_mapping = {channel:MinecraftServer(server) for channel, server in channel_server_mapping.items()}
    
    @commands.command()
    @commands.cooldown(1, 20, type=commands.BucketType.channel)
    @commands.has_any_role("Member", "Private Chat Access", "OG Role That Has No Purpose", "Moderator", "Administrator")
    async def server(self, ctx):
        """ Get status for the server associated with the channel the command is run in."""
        await ctx.message.delete()
        server = self.channel_server_mapping.get(ctx.channel.id)
        if server:
            try:
                status = server.status()
            except (socket.timeout, ConnectionRefusedError, ConnectionResetError, OSError):
                await ctx.send("Could not fetch server status, it may be down or unreachable.")
            else:
                version = status.version.name
                ping = status.latency
                maxP = status.players.max
                curP = status.players.online
                motd = status.description['text']
                embed = discord.Embed(title="Sever status for {}".format(server.host), description="{}".format(motd))
                embed.add_field(name="Players", value="{}/{}".format(curP,maxP), inline=True)
                embed.add_field(name="Ping", value="{0:.1f}ms (to this bot)".format(ping), inline=True)
                embed.add_field(name="Version", value="{}".format(version), inline=True)
                await ctx.send(embed=embed, delete_after=10)
        else:
            await ctx.send("No server linked to this channel", delete_after=10)

def setup(bot):
    channel_server_mapping = {
        588040378188431486: "2b2t.org",
    }
    bot.add_cog(ServerStatus(bot, channel_server_mapping))
