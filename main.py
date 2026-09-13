import nextcord
from nextcord.ext import commands
import yaml
import os
from mongoengine import connect
from utils import InvalidModeLiveStock, data

if data["mode"] not in ["dropdown", "button"]:
    raise InvalidModeLiveStock

connect(
    db="auto_store",
    host=data["mongodb_url"],
)


bot = commands.Bot(
    intents=nextcord.Intents.all(),
    case_insensitive=True,
    default_guild_ids=data["guild_id"],
)

for ext in data["extensions"]:
    bot.load_extension(ext)


bot.run(data["token"])
