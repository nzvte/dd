import discord
import logging
from discord.ext import commands
import motor.motor_asyncio as mongodb

logging.basicConfig(
    level=logging.INFO,
    format="\x1b[38;5;197m[\x1b[0m%(asctime)s\x1b[38;5;197m]\x1b[0m -> \x1b[38;5;197m%(message)s\x1b[0m",
    datefmt="%H:%M:%S",
)

class reaction_event(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.color = 0x2f3136
        self.connection = mongodb.AsyncIOMotorClient("mongodb+srv://root:GJ2mG7wpJMuK1DlC@discord.zvth0.mongodb.net/reverb?retryWrites=true&w=majority")
        self.db = self.connection["reverb"]["servers"]

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id == self.client.user.id:
            return
        message = str(payload.message_id)
        guild = self.client.get_guild(payload.member.guild.id)
        data = await self.db.find_one({"guild": guild.id})
        if message in data["reaction"]["data"]:
            if payload.emoji.id == data["reaction"]["data"][message]["emoji"]:
                role = guild.get_role(data["reaction"]["data"][message]["role"])
                await payload.member.add_roles(role)

def setup(client):
    client.add_cog(reaction_event(client))
