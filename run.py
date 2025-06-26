"""
─────────────────────────────────────────────────────────────────────────────
 Starlight-Bot • Launcher
─────────────────────────────────────────────────────────────────────────────
Running this file spins up the bot.  It imports `main()` from `starlight.core`
to keep *all* Discord-specific logic out of the entry-point, which helps with
unit-testing and avoids accidental Gateway connections when importing modules.
"""

# Import the synchronous wrapper for the async runner.
from starlight.core import main

###############################################################################
# Main guard
###############################################################################
if __name__ == "__main__":
    # Delegating everything to starlight/core.py keeps this file tiny,
    # but we still expose a single, obvious "python run.py" entry-point.
    main()
