import disnake
from disnake.ext import commands

from app.utils.nats_handler import NATSHandler

import os 

bot = commands.InteractionBot(
    test_guilds=[1331517665210269776],
    owner_id=213890615883202560,
    )

@bot.event
async def on_ready():
    await bot._sync_application_commands() # I had severe issues with commands disappearing. Not sure is it applicable for production
    print(f"{bot.user} rdy")

def load_cogs(nats_handler):
    for filename in os.listdir("./bot/cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
            cog_name = filename[:-3]
            if cog_name == 'broadcast':
                from app.cogs.broadcast import setup_broadcast # Had to use this workaround, as I couldnt pass nats_handler with default load_extension
                setup_broadcast(bot,nats_handler)
            else:
                bot.load_extension(f"bot.cogs.{cog_name}")

async def run_bot(BOT_TOKEN, nats_handler):
    load_cogs(nats_handler)
    await bot.start(BOT_TOKEN)
