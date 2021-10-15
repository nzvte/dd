import os
import pymongo
import discord
import logging
from discord.ext import commands

client = pymongo.MongoClient("xx")
db = client.get_database("reverb").get_collection("servers")

logging.basicConfig(
    level=logging.INFO,
    format="\x1b[38;5;197m[\x1b[0m%(asctime)s\x1b[38;5;197m]\x1b[0m -> \x1b[38;5;197m%(message)s\x1b[0m",
    datefmt="%H:%M:%S",
)

token = "ODk4NDcyMDA3MTExNDI2MDcw.YWktQw.jO0d8hDfZpC9CA2xZrRgAlnR1ws"
cogs = ["events.ready", "events.anti", "commands.configuration", "commands.general", "commands.moderation", "commands.help", "commands.jishaku", "commands.welcome", "events.welcome", "commands.utility", "events.reaction", "commands.reaction", "commands.hentai", "commands.fun", "commands.nsfw"]

def prefix(client, message):
    try:
        prefix = db.find_one({"guild": message.guild.id})["prefix"]
        return commands.when_mentioned_or(*prefix)(client, message)
    except Exception:
        return commands.when_mentioned_or(">")(client, message)

client = commands.AutoShardedBot(
    command_prefix=prefix,
    case_insensitive=True,
    help_command=None,
    intents=discord.Intents.all(),
    #shard_count=3
)

os.system("clear")
for cog in cogs:
    try:
        client.load_extension(cog)
        logging.info("Successfully loaded the \"%s\" cog" % (cog))
    except Exception as e:
        logging.error("Failed to load \"%s\" with error: %s" % (cog, e))

client.run("ODk4NDcyMDA3MTExNDI2MDcw.YWktQw.jO0d8hDfZpC9CA2xZrRgAlnR1ws")
