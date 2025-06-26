"""
Core – creates `StarlightBot`, configures logging, loads cogs, syncs commands.

Why so many comments?
─────────────────────
• New contributors grok the flow instantly.
• Future-you will thank past-you for the context.
"""

from __future__ import annotations

import asyncio
import logging
import logging.config
import os
from pathlib import Path
from typing import Final, Self

import discord
from dotenv import load_dotenv

from starlight import __version__
from starlight.utils import console

###############################################################################
# Environment & logging bootstrap
###############################################################################
BASE_DIR: Final[Path] = Path(__file__).resolve().parent
load_dotenv(BASE_DIR.parent / ".env")  # reads TOKEN from sibling .env

logging.config.fileConfig(BASE_DIR / "logging.cfg", disable_existing_loggers=False)
log: Final[logging.Logger] = logging.getLogger(__name__)

###############################################################################
# StarlightBot subclass
###############################################################################
class StarlightBot(discord.Bot):
    """
    Thin wrapper around `discord.Bot` that:

    1. Enables minimal but useful intents.
    2. Auto-loads every *.py file in ./cogs.
    3. Syncs application commands once per boot.
    """

    def __init__(self: Self) -> None:
        intents = discord.Intents.default()
        intents.message_content = True         # you might need this for future AI
        intents.members = True                 # required by /server
        super().__init__(intents=intents)

    # ────────────────────────────────────────────────────────────────────
    # Lifecycle hooks
    # ────────────────────────────────────────────────────────────────────
    async def setup_hook(self: Self) -> None:
        """Runs *once* before login – perfect for cog discovery."""
        for cog in (BASE_DIR / "cogs").glob("*.py"):
            await self.load_extension(f"starlight.cogs.{cog.stem}")
            log.debug("Loaded cog %s", cog.stem)

        # Register slash-commands globally.  Guild-scoped would be faster, but
        # global is simpler once you leave testing.
        synced = await self.tree.sync()
        log.info("Synced %d application commands.", len(synced))

    async def on_ready(self: Self) -> None:
        """Gateway READY – the bot is fully connected."""
        console.rule("[bold magenta]🌟  Starlight-Bot Online! 🌟")
        log.info("User: %s • ID: %s", self.user, self.user.id)
        log.info("Connected to %d guild(s).", len(self.guilds))


###############################################################################
# Async runner & thin synchronous façade
###############################################################################
async def _runner() -> None:
    """Async entrypoint – creates bot and starts the gateway."""
    token: str | None = os.getenv("TOKEN")
    if not token:
        console.print("[bold red]❌  TOKEN missing in .env – aborting![/]")
        raise SystemExit(1)

    bot = StarlightBot()
    try:
        await bot.start(token)
    finally:
        await bot.close()
        log.info("Graceful shutdown complete.")


def main() -> None:
    """
    Public entry-point imported by run.py.

    Uses asyncio.run to guarantee a fresh event loop (important on Windows).
    """
    console.print(f":rocket: Launching Starlight-Bot v{__version__} …")
    try:
        asyncio.run(_runner())
    except KeyboardInterrupt:
        console.print("\n[italic]Exiting via Ctrl-C…[/]")
