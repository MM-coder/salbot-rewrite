"""
Created by vcokltfre at 2020-07-08
"""
from discord.ext import commands
from discord.ext.commands import has_any_role
import discord
import logging
import time
from datetime import timedelta, datetime


class BotInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("salbot.botinfo")
        self.stats = {
            "session_messages":0,
            "session_uptime_start":round(time.time()),
            "session_commands_completed":0
        }

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        self.stats["session_messages"] += 1

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        self.stats["session_commands_completed"] += 1

    @commands.command(name="stats", aliases=["botinfo"])
    @has_any_role("Administrator", "Moderator", "Private Chat Access", "Member")
    async def stats_cmd(self, ctx):
        uptime = str(timedelta(seconds=round(time.time() - self.stats["session_uptime_start"])))

        stats_embed = discord.Embed(title="SalBot Statistics", color=0x3AE12B, timestamp=datetime.now())

        stats_embed.add_field(name="Uptime", value=uptime, inline=False)
        stats_embed.add_field(name="Messages this Session", value=str(self.stats["session_messages"]), inline=True)
        stats_embed.add_field(name="Commands this Session", value=str(self.stats["session_commands_completed"]), inline=True)

        await ctx.channel.send(embed=stats_embed)


def setup(bot):
    bot.add_cog(BotInfo(bot))