# Starlight-Bot

> **Sleek, pastel-themed Discord slash-command assistant built with Py-Cord 2.5 and Python 3.12.**

## Feature Matrix

| Feature                           | Status | Notes |
|----------------------------------|:------:|-------|
| Slash commands (`/ping`, `/hello`, `/joke`, `/server`) | ✅ | Global sync |
| Rich logging (emojis + colours)   | ✅ | See `logging.cfg` |
| Pastel embeds + timestamp/footer  | ✅ | `utils.make_embed()` |
| Plug-and-play cogs                | ✅ | Drop files into `starlight/cogs/` |
| Graceful shutdown                 | ✅ | Ctrl-C safe |
| Active-Developer badge helper     | 🟡 | See guide below |
| Buttons, selects, mod tools       | 🚧 | Planned |

> [!NOTE]  
> All commands are **global** by default. First propagation can take up to an hour; guild-scoped testing is snappier.


## Quick-start

### Option A – `pip` + `venv` (works everywhere)

```bash
git clone https://github.com/petherldev/starlight-bot.git
cd starlight-bot
python -m venv venv
# Win:
venv\Scripts\activate
# macOS/Linux:
# source venv/bin/activate
pip install -r requirements.txt
copy .env.example .env        # or: cp .env.example .env
notepad .env                  # TOKEN=PASTE_YOUR_TOKEN_HERE
python run.py
```

### Option B – Poetry (auto-creates venv)

```bash
git clone https://github.com/petherldev/starlight-bot.git
cd starlight-bot
poetry install
cp .env.example .env          # add TOKEN=
poetry run python run.py
```

> \[!TIP]
> `poetry config virtualenvs.in-project true` keeps the venv in a local `.venv/` folder—handy for VS Code.


## Commands

| Command   | Purpose                       | Ephemeral? |
| --------- | ----------------------------- | :--------: |
| `/ping`   | Returns websocket latency     |      ✅     |
| `/hello`  | Greets user + shows UTC time  |      ❌     |
| `/joke`   | Sends a random dad-joke       |      ❌     |
| `/server` | Stats about the current guild |      ❌     |


## Getting Your Discord Bot Token

> \[!WARNING]
> **Never commit a token.** Regenerate immediately if leaked.

1. Go to **[https://discord.com/developers/applications](https://discord.com/developers/applications)**
2. New Application → **Bot** tab → *Reset Token* → **Copy**
3. Paste into `.env`:

```env
TOKEN=YOUR_SUPER_SECRET_TOKEN
```

4. Generate an invite link:

```
https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=277025508352&scope=bot%20applications.commands
```

Check the **applications.commands** scope; without it, slash-commands won’t register.


## 🏅 Active Developer Badge Guide

> \[!IMPORTANT]
> Discord awards the badge after **20 distinct days** of successfully invoked slash-commands.

1. Deploy Starlight-Bot and run **any** command daily (`/ping` is fine).
2. Visit *Developer Portal → Your App → Rewards → Active Developer* and claim.
3. Profit! 🎉


## Examples Snip

<details>
<summary><strong>1 · Minimal custom cog (8-Ball)</strong></summary>

```python
# starlight/cogs/8ball.py
import random
import discord
from discord import app_commands
from discord.ext import commands
from starlight.utils import make_embed

ANSWERS = [
    "Yes!", "No!", "Ask again later…", "Absolutely!", "Definitely not."
]

class EightBall(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @app_commands.command(name="8ball", description="Magic 8-Ball answers.")
    async def eight_ball(self, interaction: discord.Interaction, question: str):
        await interaction.response.send_message(
            embed=make_embed("🎱 8-Ball", random.choice(ANSWERS))
        )

async def setup(bot):  # required by Py-Cord
    await bot.add_cog(EightBall(bot))
```

</details>

<details>
<summary><strong>2 · Reply with buttons</strong></summary>

```python
# inside any cog
from discord.ui import Button, View

@app_commands.command(name="pressme", description="Button demo")
async def pressme(self, interaction: discord.Interaction):
    btn = Button(label="Click!", style=discord.ButtonStyle.primary)

    async def on_click(btn_inter: discord.Interaction):
        await btn_inter.response.send_message("✨ Button pressed!")

    btn.callback = on_click
    view = View()
    view.add_item(btn)
    await interaction.response.send_message("Press the shiny button:", view=view)
```

</details>

<details>
<summary><strong>3 · Querying bot latency elsewhere</strong></summary>

```python
# util example (can be imported by other modules)
from starlight.utils import make_embed
from discord.ext import commands

async def send_latency(channel: commands.Cog, bot: commands.Bot) -> None:
    latency = round(bot.latency * 1000)
    await channel.send(embed=make_embed("🏓 Latency", f"{latency} ms"))
```

</details>


## Development Checklist

* [x] Clone repository
* [x] Add `.env` with TOKEN
* [x] Run `python run.py`
* [ ] Add more cogs (music, moderation, AI, …)
* [ ] Write unit tests (`pytest`)


## Further Reading

| Topic                    | Docs Link                                                                              |
| ------------------------ | -------------------------------------------------------------------------------------- |
| Py-Cord API              | [https://docs.pycord.dev/](https://docs.pycord.dev/)                                   |
| Rich logging             | [https://rich.readthedocs.io/](https://rich.readthedocs.io/)                           |
| Discord Developer Portal | [https://discord.com/developers/docs/intro](https://discord.com/developers/docs/intro) |


## Licence

Starlight-Bot is released under the **Apache License 2.0**.
See [`LICENSE`](./LICENSE) for the full text.


## Contact

* GitHub — [https://github.com/petherldev](https://github.com/petherldev)
* Email  — [petherl@protonmail.com](mailto:petherl@protonmail.com)

*Made with \:sparkling\_heart: and too much coffee.*
