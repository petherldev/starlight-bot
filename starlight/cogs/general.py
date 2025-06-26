"""
General info slash-commands – /ping, /hello, /server – using Py-Cord decorators.
"""
from __future__ import annotations

import datetime as _dt

import discord
from discord.ext import commands
from starlight.utils import make_embed


class General(commands.Cog):
    """Informational slash-commands."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # /ping ──────────────────────────────────────────────────────────────
    @commands.slash_command(name="ping", description="Show bot latency.")
    async def ping(self, ctx: discord.ApplicationContext) -> None:
        latency = round(self.bot.latency * 1000)
        await ctx.respond(
            embed=make_embed("🏓 Pong!", f"Latency: `{latency} ms`"),
            ephemeral=True,
        )

    # /hello ─────────────────────────────────────────────────────────────
    @commands.slash_command(name="hello", description="Receive a friendly greeting.")
    async def hello(self, ctx: discord.ApplicationContext) -> None:
        now_utc = _dt.datetime.now(_dt.UTC).strftime("%Y-%m-%d %H:%M UTC")
        await ctx.respond(
            embed=make_embed(
                "👋 Hello there!",
                f"Greetings {ctx.author.mention}! It’s **{now_utc}**.",
            )
        )

    # /server ────────────────────────────────────────────────────────────
    @commands.slash_command(name="server", description="Information about this server.")
    async def server_info(self, ctx: discord.ApplicationContext) -> None:
        guild = ctx.guild
        if guild is None:  # DM
            return await ctx.respond("Not in a guild!", ephemeral=True)

        emb = make_embed(
            f"🌐 {guild.name}",
            f"ID • `{guild.id}`\nOwner • {guild.owner.mention if guild.owner else 'Unknown'}",
        )
        emb.add_field("👥 Members", f"{guild.member_count:,}")
        emb.add_field("🗓️ Created", guild.created_at.strftime("%Y-%m-%d"))
        if guild.icon:
            emb.set_thumbnail(url=guild.icon.url)

        await ctx.respond(embed=emb)


async def setup(bot: commands.Bot) -> None:  # loader hook for Py-Cord
    await bot.add_cog(General(bot))
