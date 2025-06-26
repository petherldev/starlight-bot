"""
Fun cog – /joke – now using Py-Cord slash decorators.
"""
from __future__ import annotations

import random

import discord
from discord.ext import commands
from starlight.utils import make_embed

JOKES = [
    "Why don't scientists trust atoms? They make up everything!",
    "Why did the scarecrow win an award? He was outstanding in his field!",
    "What do you call fake spaghetti? An impasta!",
    "Why don't skeletons fight each other? They don't have the guts!",
    "What do you call a bear with no teeth?  **A gummy bear!**",
]


class Fun(commands.Cog):
    """Entertainment commands."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.slash_command(name="joke", description="Hear a dad joke.")
    async def joke(self, ctx: discord.ApplicationContext) -> None:
        await ctx.respond(embed=make_embed("😂 Dad Joke", random.choice(JOKES)))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Fun(bot))
