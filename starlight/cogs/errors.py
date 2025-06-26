"""
Global error handler – keeps ugly tracebacks out of chat but logs them server-side.
"""

from __future__ import annotations

import logging

import discord
from discord import app_commands
from discord.ext import commands

from starlight.utils import make_embed

log = logging.getLogger(__name__)


class Errors(commands.Cog):
    """Intercept and prettify command errors."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Prefix-style command errors (if you add any legacy commands later)
    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        log.exception("Prefix command error", exc_info=error)
        await ctx.reply(embed=make_embed("❌ Error", str(error)), mention_author=False)

    # Slash command errors
    @commands.Cog.listener()
    async def on_app_command_error(self, interaction: discord.Interaction,
                                   error: app_commands.AppCommandError):
        log.exception("Slash command error", exc_info=error)
        embed = make_embed("❌ Something went wrong.",
                           "If this keeps happening please ping the developer.",
                           colour=discord.Colour.red())
        # Respect original interaction state.
        if interaction.response.is_done():
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Errors(bot))
