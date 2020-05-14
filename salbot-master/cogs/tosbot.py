import json
import os
from discord.ext import commands
import discord
from discord.utils import get
import logging
logger = logging.getLogger('salc1bot')


class TosCommand:
    def __init__(self, name, content):
        self.name = name
        self.content = f"The following is against the Discord Community Guidelines and may result in account termination: '{content}'"

    async def __call__(self, ctx):
        embed = discord.Embed(title=self.name, description=self.content)
        await ctx.send(embed=embed)


class Tos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("data/dgl.json") as f:
            self.json_data = json.load(f)
        for item in self.json_data:
            command = TosCommand(item["names"][0], item["content"])
            print(command.name, command.content)
            self.dgl.command(item["names"][0], aliases=item["names"][1:])(command.__call__)

    @commands.group(name="dgl")
    @commands.has_any_role("Member", "Private Chat Access", "OG Role That Has No Purpose", "Moderator", "Administrator")
    async def dgl(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title="Discord Guidelines Commands")
            for command in self.dgl.commands:
                embed.add_field(
                    name=command.name, value=f"Aliases: {', '.join(command.aliases)}", inline=False)
            await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Tos(bot))
