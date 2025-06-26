"""
Utility helpers used across the bot.

Content
───────
• console        – a pre-configured Rich Console for colourful stdout.
• random_colour  – pastel discord.Colour generator (HSV → RGB).
• make_embed     – centralised embed factory with automatic timestamp & footer.
• clamp          – tiny maths helper for future colour utilities.

Adding shared helpers here keeps cogs clean and avoids circular imports.
"""

from __future__ import annotations

import datetime as _dt
import random
from typing import Final, TypeAlias

import discord
from rich.console import Console

# ────────────────────────────────────────────────────────────────────────────
# Public re-exports
# ────────────────────────────────────────────────────────────────────────────
__all__: tuple[str, ...] = ("console", "random_colour", "make_embed", "clamp")

# Type alias for hex-int colours if you ever call make_embed(colour=0xFFAA00)
HexInt: TypeAlias = int

# ────────────────────────────────────────────────────────────────────────────
# Rich console – singletons are fine; Rich handles thread-safety.
# ────────────────────────────────────────────────────────────────────────────
console: Final[Console] = Console(
    highlight=False,  # disable syntax highlighting for raw strings
    emoji=True,       # enable :sparkles: etc.
    width=120,        # wider line-wrap for large messages
)

# ────────────────────────────────────────────────────────────────────────────
# Helper functions
# ────────────────────────────────────────────────────────────────────────────
def clamp(value: float, /, lo: float = 0.0, hi: float = 1.0) -> float:
    """Clamp *value* into the inclusive range [lo, hi]."""
    return max(lo, min(value, hi))


def random_colour(*, pastel: bool = True) -> discord.Colour:
    """
    Return a pleasant random colour.

    Args
    ----
    pastel:
        If *True* (default) generates bright pastel tones by locking V=0.95 and
        S≈0.7.  If *False* generates fully random discord.Colour values.
    """
    if pastel:
        hue = random.randint(0, 360)
        sat = random.uniform(0.6, 0.8)   # 60–80 %
        val = 0.95                       # 95 %
        return discord.Colour.from_hsv(hue / 360, sat, val)

    # Completely random 24-bit colour
    return discord.Colour(random.randint(0, 0xFFFFFF))


def make_embed(
    title: str,
    description: str | None = None,
    *,
    colour: discord.Colour | HexInt | None = None,
) -> discord.Embed:
    """
    Unified embed builder so all embeds share timestamp & footer.

    • *title* – short, one-line heading.
    • *description* – longer body text. Markdown supported by Discord.
    • *colour* – discord.Colour or 0xRRGGBB int.  Defaults to random pastel.
    """
    if isinstance(colour, int):
        colour = discord.Colour(colour)

    embed = discord.Embed(
        title=title,
        description=description or "",
        colour=colour or random_colour(),
        timestamp=_dt.datetime.now(_dt.UTC),
    )
    # Footer is only populated once the client is connected (self.user exists).
    embed.set_footer(text="✨ Powered by Starlight-Bot")
    return embed
