# 🗂️ Project Structure: Starlight-Bot

This document explains the complete file and folder layout for the `Starlight-Bot` project.

It is designed to guide contributors and new developers through how each part of the bot works, where logic resides, and how the components are wired together.


## Root Directory

```bash
starlight-bot/
├── README.md            # Project overview, features, setup instructions, usage examples
├── LICENSE              # Legal license file (e.g. GPLv3, AGPL, etc.)
├── .env.example         # Example env file — copy to `.env` and insert your bot TOKEN=
├── pyproject.toml       # Poetry-based package manager config (dependencies, metadata)
├── requirements.txt     # Optional pip-based dependency list for non-Poetry users
├── run.py               # Tiny launcher file that runs `main()` from core.py
└── starlight/           # Main source package for the bot
```


## `starlight/` (Bot Source Code)

```bash
starlight/
├── __init__.py          # Package marker, defines bot version for logging and packaging
├── core.py              # Startup logic: class StarlightBot, token loading, cog loading
├── utils.py             # Reusable utilities (console printer, embed builder, colour tools)
├── logging.cfg          # Logging configuration using RichHandler for coloured output
└── cogs/                # Modular command handlers (slash-commands live here)
```


## `starlight/cogs/` (Command Modules)

Each file here is a self-contained group of related commands (called **cogs** in discord.py).

```bash
cogs/
├── general.py           # Informational commands: /ping, /hello, /server, /uptime, /botinfo
├── fun.py               # Light-hearted fun: /joke, /roll, /choose, /8ball
└── errors.py            # Global error handler (shows user-friendly messages for failed commands)
```


## Breakdown of Core Files

### `run.py`

```py
# run.py
from starlight.core import main

if __name__ == "__main__":
    main()  # Entry point for launching the bot
```

> \[!TIP]
> Keeps the top-level script minimal and testable by delegating startup logic to `core.py`.


### `core.py`

* Initializes the bot (`discord.Bot` subclass)
* Loads `.env` and logging configuration
* Loads all cogs in `/cogs`
* Starts the event loop and connects to Discord

```py
class StarlightBot(discord.Bot):
    async def setup_hook(self):
        for cog in (BASE_DIR / "cogs").glob("*.py"):
            await self.load_extension(f"starlight.cogs.{cog.stem}")
        await self.tree.sync()  # Registers slash-commands
```


### `utils.py`

* Rich console instance: `console.print()`
* `make_embed()`: Easy and uniform embed creation
* `random_colour()`: Bright pastels for visual appeal

```py
def make_embed(title: str, description: str = "", *, colour=None) -> discord.Embed:
    ...
```


### `logging.cfg`

Rich-logging setup via `RichHandler`:

* Timestamped logs
* Color-coded levels (INFO, WARNING, etc.)
* Styled output

```ini
[handler_console]
class=rich.logging.RichHandler
formatter=rich
```


### `cogs/general.py`

Contains all informational slash-commands:

| Command    | Description                     |
| ---------- | ------------------------------- |
| `/ping`    | Check bot latency               |
| `/hello`   | Personalized greeting           |
| `/server`  | Show server info and stats      |
| `/uptime`  | Show how long bot has run       |
| `/botinfo` | Python and library version info |


### `cogs/fun.py`

Entertainment and games:

| Command   | Description                            |
| --------- | -------------------------------------- |
| `/joke`   | Send a random dad joke                 |
| `/roll`   | Roll N dice with X sides               |
| `/choose` | Pick one option from a list            |
| `/8ball`  | Ask the magic 8-ball a yes/no question |


### `cogs/errors.py`

Global command error handler:

* Catches and logs all command errors
* Sends clean, embed-based user messages
* Covers both prefix and slash command exceptions

```py
@commands.Cog.listener()
async def on_app_command_error(self, interaction, error):
    ...
```

## Dependencies

### From `pyproject.toml` or `requirements.txt`

* `discord.py >=2.3` – Main library for Discord interaction
* `python-dotenv` – Load `.env` config file
* `rich` – Logging + pretty terminal output

## Development Environment

| Tool      | Version                                          |
| --------- | ------------------------------------------------ |
| Python    | 3.11+                                            |
| OS        | Windows 10+ / Linux / macOS                      |
| IDE       | VSCode / PyCharm                                 |
| Formatter | [Black](https://github.com/psf/black) (optional) |
| Linter    | Ruff / Flake8 (optional)                         |
