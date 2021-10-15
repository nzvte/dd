import discord
import logging
from discord.ext import commands
import motor.motor_asyncio as mongodb

logging.basicConfig(
    level=logging.INFO,
    format="\x1b[38;5;197m[\x1b[0m%(asctime)s\x1b[38;5;197m]\x1b[0m -> \x1b[38;5;197m%(message)s\x1b[0m",
    datefmt="%H:%M:%S",
)

class welcome(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.color = 0x2f3136
        self.connection = mongodb.AsyncIOMotorClient("mongodb+srv://root:GJ2mG7wpJMuK1DlC@discord.zvth0.mongodb.net/reverb?retryWrites=true&w=majority")
        self.db = self.connection["reverb"]["servers"]

    @commands.group(invoke_without_command=True, name="reaction", description="Shows reaction commands", usage="reaction", aliases=["rr"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def reaction(self, ctx):
        return await ctx.send(embed=discord.Embed(title="Reaction", description="Please use `%shelp reaction` instead!\n— This command group does not require a detailed help" % (ctx.prefix)))

    @reaction.command(name="add", description="Setup a new reaction role", usage="reaction add <message id> <role> <emoji>")
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def add(self, ctx, message, role: discord.Role, emoji: discord.Emoji):
        try:
            msg = await ctx.fetch_message(message)
        except Exception:
            return await ctx.send(embed=discord.Embed(title="Add | Reaction", description="Invalid message ID", color=self.color))
        data = await self.db.find_one({"guild": ctx.guild.id})
        try:
            data["reaction"]["data"]
            await self.db.update_one(
                {
                    "guild": ctx.guild.id
                },
                {
                    "$set": {
                        "reaction": {
                            "data": {
                                message: {
                                    "role": role.id,
                                    "emoji": emoji.id
                                }
                            }
                        }
                    }
                }
            )
        except Exception:
            await self.db.update_one(
                {
                    "guild": ctx.guild.id
                },
                {
                    "$set": {
                        "reaction": {
                            "data": {
                                message: {
                                    "role": role.id,
                                    "emoji": emoji.id
                                }
                            }
                        }
                    }
                }
            )

        await msg.add_reaction(emoji)
        return await ctx.send(embed=discord.Embed(title="Add | Reaction", description="Successfully added reaction to message", color=self.color))

    @reaction.command(name="remove", description="Remove a reaction role", usage="reaction remove <message id>", aliases=["del"])
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def remove(self, ctx, message):
        try:
            await self.db.update_one(
                {
                    "guild": ctx.guild.id
                },
                {
                    "$pull": {
                        "reaction": {
                            "data": message
                        }
                    }
                }
            )
            return await ctx.send(embed=discord.Embed(title="Remove | Reaction", description="Successfully reaction role from message", color=self.color))
        except Exception:
            return await ctx.send(embed=discord.Embed(title="Remove | Reaction", description="Failed to remove reaction, are you sure there is reaction role for that message?\n— Try removing the reaction manually", color=self.color))

def setup(client):
    client.add_cog(welcome(client))
