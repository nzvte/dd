import discord
import logging
from discord.ext import commands
import motor.motor_asyncio as mongodb

logging.basicConfig(
    level=logging.INFO,
    format="\x1b[38;5;197m[\x1b[0m%(asctime)s\x1b[38;5;197m]\x1b[0m -> \x1b[38;5;197m%(message)s\x1b[0m",
    datefmt="%H:%M:%S",
)

class moderation(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.color = 0x2f3136
        self.client.tasks = []
        self.connection = mongodb.AsyncIOMotorClient("mongodb+srv://root:GJ2mG7wpJMuK1DlC@discord.zvth0.mongodb.net/reverb?retryWrites=true&w=majority")
        self.db = self.connection["reverb"]["servers"]

    @commands.command(name="nuke", description="Nukes a channel", usage="nuke", aliases=["n"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def nuke(self, ctx, channel: discord.TextChannel = None):
        channel = channel if channel else ctx.channel
        newchannel = await channel.clone()
        await newchannel.edit(position=channel.position)
        await channel.delete()
        embed = discord.Embed(title="nuke", description="Channel has been nuked by **`%s`**" % (ctx.author), color=self.color)
        embed.set_image(url="https://media2.giphy.com/media/HhTXt43pk1I1W/giphy.gif")
        await newchannel.send(embed=embed, delete_after=5)

    @commands.command(name="unbanall", description="Unbans all users", usage="unbanall", aliases=["massunban", "unbaneveryone"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(ban_members=True)
    async def unbanall(self, ctx):
        if ctx.guild.id in self.client.tasks:
            await ctx.send(embed=discord.Embed(title="unbanall", description="There is a massunban task already running, please wait for it to finish", color=self.color))
        else:
            await ctx.message.add_reaction("✅")
            self.client.tasks.append(ctx.guild.id)
            unbanned = 0
            ignored = 0
            data = await self.db.find_one({"guild": ctx.guild.id})
            ignore = data["banned"]
            for users in await ctx.guild.bans():
                if users.user.id in ignore:
                    ignored += 1
                else:
                    await ctx.guild.unban(user=users.user)
                    unbanned += 1
            self.client.tasks.remove(ctx.guild.id)
            await ctx.send(embed=discord.Embed(title="unbanall", description="Successfully unbanned **`%s`** members, did not unban **`%s`** members because they were banned by %s" % (unbanned, ignored, self.client.user.name), color=self.color))

    @commands.command(name="ban", description="Bans a user", usage="ban [user] <reason>")
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if ctx.guild.owner.id != ctx.author.id:
            if member.top_role >= ctx.author.top_role:
                return await ctx.send(embed=discord.Embed(title="ban", description="**`%s`**'s role is higher than yours, you cannot ban that user." % (member.name), color=self.color))
        await member.ban(reason=reason)
        await ctx.send(embed=discord.Embed(title="ban", description="Successfully banned **`%s`**" % (member.name), color=self.color))

    @commands.command(name="unban", description="Unbans a user", usage="unban [user id]", aliases=["uban"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user):
        try:
            await ctx.guild.unban(discord.Object(id=user))
            await ctx.send(embed=discord.Embed(title="unban", description="Successfully unbanned **`%s`**" % (user), color=self.color))
        except Exception:
            await ctx.send(embed=discord.Embed(title="unban", description="Failed to unban **`%s`**" % (user), color=self.color))

    @commands.command(name="purge", description="Purges messages", usage="purge [amount]", aliases=["clear", "p"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount+1)
        await ctx.send(embed=discord.Embed(title="purge", description="Successfully purged messages", color=self.color), delete_after=3)

    @commands.command(name="kick", description="Kicks a user", usage="kick [user] <reason>")
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        try:
            await member.kick(reason=reason)
            await ctx.send(embed=discord.Embed(title="kick", description="Successfully kicked **`%s`**" % (member.name), color=self.color))
        except Exception:
            await ctx.send(embed=discord.Embed(title="kick", description="Failed to kick **`%s`**" % (member.name), color=self.color))

    @commands.command(name="lock", description="Locks down a channel", usage="lock <channel> <reason>", aliases=["lockdown"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx, channel: discord.TextChannel = None, *, reason=None):
        if channel is None: channel = ctx.channel
        try:
            await channel.set_permissions(ctx.guild.default_role, overwrite=discord.PermissionOverwrite(send_messages = False), reason=reason)
            await ctx.send(embed=discord.Embed(title="lockdown", description="Successfully locked **`%s`**" % (channel.mention), color=self.color))
        except:
            await ctx.send(embed=discord.Embed(title="lockdown", description="Failed to lockdown **`%s`**" % (channel.mention), color=self.color))
        else:
            pass

    @commands.command(name="unlock", description="Unlocks a channel", usage="unlock <channel> <reason>", aliases=["unlockdown"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx, channel: discord.TextChannel=None, *, reason=None):
        if channel is None: channel = ctx.channel
        try:
            await channel.set_permissions(ctx.guild.default_role, overwrite=discord.PermissionOverwrite(send_messages = True), reason=reason)
            await ctx.send(embed=discord.Embed(title="unlockdown", description="Successfully unlocked **`%s`**" % (channel.mention), color=self.color))
        except:
            await ctx.send(embed=discord.Embed(title="unlockdown", description="Failed to lock **`%s`**" % (channel.mention), color=self.color))
        else:
            pass

    @commands.command(name="slowmode", description="Changes the slowmode", usage="slowmode [seconds]", aliases=["slow"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def slowmode(self, ctx, seconds: int=0):
        if seconds > 120:
            return await ctx.send(embed=discord.Embed(title="slowmode", description="Slowmode can not be over 2 minutes", color=self.color))
        if seconds == 0:
            await ctx.channel.edit(slowmode_delay=seconds)
            await ctx.send(embed=discord.Embed(title="slowmode", description="Slowmode is disabled", color=self.color))
        else:
            await ctx.channel.edit(slowmode_delay=seconds)
            await ctx.send(embed=discord.Embed(title="slowmode", description="Set slowmode to **`%s`**" % (seconds), color=self.color))

    @commands.command(name="unslowmode", description="Disables slowmode", usage="unslowmode", aliases=["unslow"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def unslowmode(self, ctx):
        await ctx.channel.edit(slowmode_delay=0)
        await ctx.send(embed=discord.Embed(title="unslowmode", description="Disabled slowmode", color=self.color))

def setup(client):
    client.add_cog(moderation(client))
