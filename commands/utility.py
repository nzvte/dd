import os
import discord
import logging
from discord.ext import commands
import motor.motor_asyncio as mongodb

logging.basicConfig(
    level=logging.INFO,
    format="\x1b[38;5;197m[\x1b[0m%(asctime)s\x1b[38;5;197m]\x1b[0m -> \x1b[38;5;197m%(message)s\x1b[0m",
    datefmt="%H:%M:%S",
)

class utility(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.color = 0x2f3136
        self.connection = mongodb.AsyncIOMotorClient("mongodb+srv://root:GJ2mG7wpJMuK1DlC@discord.zvth0.mongodb.net/reverb?retryWrites=true&w=majority")
        self.db = self.connection["reverb"]["servers"]
        self.tasks = []
        self.dump_tasks = []
        self.sniped = {}
        self.afk = {}

    @commands.Cog.listener()
    async def on_message_delete(self, message): 
        if message.guild == None: 
            return
        if message.author.bot: 
            return
        if not message.content: 
            return 
        self.sniped[message.channel.id] = message

    @commands.command(name="snipe", description="Snipes the most reecent deleted message", usage="snipe", aliases=["s"])
    async def snipe(self, ctx):
        message = self.sniped.get(ctx.channel.id)
        if message == None:
            return await ctx.send(embed=discord.Embed(title="snipe", description="There are no reecently deleted messages", color=self.color))
        embed = discord.Embed(title="Message sent by %s" % (message.author), description=message.content, color=self.color, timestamp=message.created_at)
        await ctx.send(embed=embed)

    @commands.command(name="roleall", description="Gives a role to all members", usage="roleall <role>", aliases=["role-all", "rall"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def role_all(self, ctx, *, role: discord.Role):
        if ctx.guild.id in self.tasks:
            return await ctx.send(embed=discord.Embed(title="roleall", description="There is a roleall task already running, please wait for it to finish", color=self.color))
        await ctx.message.add_reaction("✅")
        num = 0
        failed = 0
        for user in list(ctx.guild.members):
            try:
                await user.add_roles(role)
                num += 1
            except Exception:
                failed += 1
        await ctx.send(embed=discord.Embed(title="roleall", description="Successfully added **`%s`** to **`%s`** users, failed to add it to **`%s`** users" % (role.name, num, failed), color=self.color))

    @commands.group(invoke_without_command=True, name="dump", description="Shows dump commands", usage="dump")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def dump(self, ctx):
        return await ctx.send(embed=discord.Embed(title="Dump", description="Please use `%shelp dump` instead!\n— This command group does not require a detailed help" % (ctx.prefix)))

    @dump.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_guild=True)
    async def members(self, ctx):
        if ctx.guild.id in self.dump_tasks:
            return await ctx.send(embed=discord.Embed(title="Members | Dump", description="There is a dump task already running, please wait for it to finish", color=self.color))
        with open(f"{ctx.guild.id}_members_dump.txt", "a+", encoding="utf-8") as f:
            for member in ctx.guild.members:
                f.write(f"{member} ({member.id})\n")
            f.close()
        await ctx.send(file=discord.File(f"{ctx.guild.id}_members_dump.txt"))
        os.remove(f"{ctx.guild.id}_members_dump.txt")

    @dump.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_guild=True)
    async def channels(self, ctx):
        if ctx.guild.id in self.dump_tasks:
            return await ctx.send(embed=discord.Embed(title="Channels | Dump", description="There is a dump task already running, please wait for it to finish", color=self.color))
        with open(f"{ctx.guild.id}_channels_dump.txt", "a+", encoding="utf-8") as f:
            for channel in ctx.guild.text_channels:
                f.write(f"[text_channel] {channel} ({channel.id})\n")
            for voice in ctx.guild.voice_channels:
                f.write(f"[voice_channel] {voice} ({voice.id})\n")
            f.close()
        await ctx.send(file=discord.File(f"{ctx.guild.id}_channels_dump.txt"))
        os.remove(f"{ctx.guild.id}_channels_dump.txt")

    @dump.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_guild=True)
    async def roles(self, ctx):
        if ctx.guild.id in self.dump_tasks:
            return await ctx.send(embed=discord.Embed(title="Roles | Dump", description="There is a dump task already running, please wait for it to finish", color=self.color))
        with open(f"{ctx.guild.id}_roles_dump.txt", "a+", encoding="utf-8") as f:
            for role in ctx.guild.roles:
                f.write(f"[role] {role} ({role.id})\n")
            f.close()
        await ctx.send(file=discord.File(f"{ctx.guild.id}_roles_dump.txt"))
        os.remove(f"{ctx.guild.id}_roles_dump.txt")

    @commands.command(name="jail", description="Jails a user", usage="jail <user>")
    @commands.has_permissions(administrator=True)
    async def jail(self, ctx, member: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="jailed")
        if not role:
            await ctx.guild.create_role(name="jailed")

        jail = discord.utils.get(ctx.guild.text_channels, name="jail")
        if not jail:
            try:
                overwrites = {
                    ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
                    ctx.guild.me: discord.PermissionOverwrite(read_messages=True)
                }            
                jail = await ctx.guild.create_text_channel("jail", overwrites=overwrites)
                await ctx.send(embed=discord.Embed(title="jail", description="Your server has no jail channel, I created one for you %s" % (jail.mention), color=self.color))
            except discord.Forbidden:
                return await ctx.send(embed=discord.Embed(title="jail", description="Please give me permissions, I am unable to create the jailed channel", color=self.color))

        for channel in ctx.guild.channels:
            if channel.name == "jail":
                perms = channel.overwrites_for(member)
                perms.send_messages = True
                perms.read_messages = True
                await channel.set_permissions(member, overwrite=perms)
            else:
                perms = channel.overwrites_for(member)
                perms.send_messages = False
                perms.read_messages = False
                perms.view_channel = False
                await channel.set_permissions(member, overwrite=perms)

        role = discord.utils.get(ctx.guild.roles, name="jailed")
        await member.add_roles(role)

        await jail.send(content=member.mention, embed=discord.Embed(title="jail", description="Please live out your jail sentence until the court lets you free.", color=self.color))
        await ctx.send(embed=discord.Embed(title="jail", description="Successfully jailed **`%s`**" % (member.name), color=self.color))
        await member.send(embed=discord.Embed(title="jail", description="You have been jailed in **`%s`** by **`%s`**" % (ctx.guild.name, ctx.author.name), color=self.color))

    @commands.command(name="unjail", description="Unjails a user", usage="unjail <user>",  aliases=["free"])
    @commands.has_permissions(administrator=True)
    async def unjail(self, ctx, member: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="jailed")
        for channel in ctx.guild.channels:
            if channel.name == "jail":
                perms = channel.overwrites_for(member)
                perms.send_messages = None
                perms.read_messages = None
                await channel.set_permissions(member, overwrite=perms)
            else:
                perms = channel.overwrites_for(member)
                perms.send_messages = None
                perms.read_messages = None
                perms.view_channel = None
                await channel.set_permissions(member, overwrite=perms)

        await ctx.send(embed=discord.Embed(title="unjail", description="Successfully unjailed **`%s`**" % (member.name), color=self.color))
        await member.send(embed=discord.Embed(title="unjail", description="you have been unjailed in **`%s`** by **`%s`**" % (ctx.guild.name, ctx.author.name), color=self.color))

    @commands.command(name="cleanup", description="deletes the bots messages", aliases=["cu"], usage="cleanup <amount>")
    @commands.has_permissions(administrator=True)
    async def cleanup(self, ctx, amount: int):
        msg = await ctx.send("cleaning...")
        async for message in ctx.message.channel.history(limit=amount).filter(lambda m: m.author == self.client.user).map(lambda m: m):
            try:
                if message.id == msg.id:
                    pass
                else:
                    await message.delete()
            except:
                pass
        await msg.edit(content="cleaned up 👍")

def setup(client):
    client.add_cog(utility(client))
