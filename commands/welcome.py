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

    @commands.group(invoke_without_command=True, name="welcome", description="Shows welcome commands", usage="welcome", aliases=["wlc"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def welcome(self, ctx):
        embed = discord.Embed(title="Welcome | Help", color=self.color)
        embed.add_field(name="usage", value="— welcome message <message>\n— welcome channel <channel>\n— welcome disable\n— welcome enable\n— welcome test", inline=False)
        embed.add_field(name="description", value="— `welcome message` - Sets the welcome to a message\n— `welcome channel` - Sets the welcome channel\n— `welcome disable` - Disables the welcome message\n— `welcome enable` - Enables the welcome message\n— `welcome test` - Test the welcome message", inline=False)
        embed.add_field(name="permissions", value="— `Manage Channels` - Requires you to have manage channels permissions for all commands", inline=False)
        embed.add_field(name="variables", value="— `{user.id}`\n— `{user.name}`\n— `{user.mention}`\n— `{user.tag}`\n— `{server.name}`\n— `{server.membercount}`\n— `{server.icon}`", inline=False)
        await ctx.send(embed=embed)
 
    @welcome.command(name="message", description="Sets the welcome message", usage="welcome message <message>", aliases=["msg"])
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def message(self, ctx, *, message):
        await self.db.update_one(
            {
                "guild": ctx.guild.id
            },
            {
                "$set": {
                    "welcome.message": message
                }
            }
        )
        return await ctx.send(embed=discord.Embed(title="Message | Welcome", description="Successfully set the welcome message", color=self.color))

    @welcome.command(name="channel", description="Sets the welcome channel", usage="welcome channel <channel>", aliases=["chan"])
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def channel(self, ctx, channel: discord.TextChannel = None):
        if channel == None:
            channel = ctx.channel
        await self.db.update_one(
            {
                "guild": ctx.guild.id
            },
            {
                "$set": {
                    "welcome.channel": channel.id
                }
            }
        )
        return await ctx.send(embed=discord.Embed(title="Channel | Welcome", description="Successfully set the welcome channel", color=self.color))

    @welcome.command(name="disable", description="Disables the welcome event", usage="welcome disable", aliases=["off"])
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def disable(self, ctx):
        await self.db.update_one(
            {
                "guild": ctx.guild.id
            },
            {
                "$set": {
                    "welcome.enabled": False
                }
            }
        )
        return await ctx.send(embed=discord.Embed(title="Disable | Welcome", description="Successfully disabled the welcome event", color=self.color))

    @welcome.command(name="enable", description="Enables the welcome event", usage="welcome enable", aliases=["on"])
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def enable(self, ctx):
        await self.db.update_one(
            {
                "guild": ctx.guild.id
            },
            {
                "$set": {
                    "welcome.enabled": True
                }
            }
        )
        return await ctx.send(embed=discord.Embed(title="Enable | Welcome", description="Successfully enabled the welcome event", color=self.color))

    @welcome.command(name="test", description="Tests the welcome event", usage="welcome test", aliases=["try"])
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def test(self, ctx):
        data = await self.db.find_one({"guild": ctx.guild.id})
        if data["welcome"]["enabled"] != True:
            return await ctx.send(embed=discord.Embed(title="Test | Welcome", description="The welcome event is not enabled, please run `welcome enable` to enable it", color=self.color))
        if data["welcome"]["message"] == None:
            return await ctx.send(embed=discord.Embed(title="Test | Welcome", description="No welcome message is set, please run `welcome message <message>` to set it", color=self.color))
        if data["welcome"]["channel"] == None:
            return await ctx.send(embed=discord.Embed(title="Test | Welcome", description="No welcome channel is set, please run `welcome channel` to set it", color=self.color))

        channel = self.client.get_channel(data["welcome"]["channel"])
        message = data["welcome"]["message"]
        user = ctx.author
        if "{user.id}" in message:
                message = message.replace("{user.id}", "%s" % (user.id))

        if "{user.mention}" in message:
            message = message.replace("{user.mention}", "%s" % (user.mention))

        if "{user.tag}" in message:
            message = message.replace("{user.tag}", "%s" % (user.discriminator))

        if "{user.name}" in message:
            message = message.replace("{user.name}", "%s" % (user.name))
            
        if "{user.avatar}" in message:
            message = message.replace("{user.avatar}", "%s" % (user.avatar_url))

        if "{server.name}" in message:
            message = message.replace("{server.name}", "%s" % (user.guild.name))
            
        if "{server.membercount}" in message:
            message = message.replace("{server.membercount}", "%s" % (user.guild.member_count))
            
        if "{server.icon}" in message:
            message = message.replace("{server.icon}", "%s" % (user.guild.icon_url))

        try:
            await channel.send(message)
            await ctx.send(embed=discord.Embed(title="Test | Welcome", description="Successfully tested the welcome message", color=self.color))
        except Exception:
            await ctx.send(embed=discord.Embed(title="Test | Welcome", description="Failed to send the welcome message, does the bot have permissions to send it in that channel?", color=self.color))

def setup(client):
    client.add_cog(welcome(client))