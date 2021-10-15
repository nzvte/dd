import time
import discord
import logging
import requests
from discord.ext import commands
import motor.motor_asyncio as mongodb

logging.basicConfig(
    level=logging.INFO,
    format="\x1b[38;5;197m[\x1b[0m%(asctime)s\x1b[38;5;197m]\x1b[0m -> \x1b[38;5;197m%(message)s\x1b[0m",
    datefmt="%H:%M:%S",
)

class general(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.color = 0x2f3136
        self.connection = mongodb.AsyncIOMotorClient("mongodb+srv://root:GJ2mG7wpJMuK1DlC@discord.zvth0.mongodb.net/reverb?retryWrites=true&w=majority")
        self.db = self.connection["reverb"]["servers"]

    @commands.command(name="membercount", description="Shows member stats", usage="membercount", aliases=["mc"])
    async def membercount(self, ctx):
        online = 0
        offline = 0
        dnd = 0
        idle = 0
        bots = 0
        for member in ctx.guild.members:
            if member.status == discord.Status.online:
                online += 1
            if member.status == discord.Status.offline:
                offline += 1
            if member.status == discord.Status.dnd:
                dnd += 1
            if member.status == discord.Status.idle:
                idle += 1
            if member.bot:
                bots += 1
        embed = discord.Embed(title=ctx.guild.name, description="Here is **`%s`**'s member information" % (ctx.guild.name), color=self.color)
        embed.add_field(name="*Online*", value="`%s`" % (online), inline=False)
        embed.add_field(name="*Offline*", value="`%s`" % (offline), inline=False)
        embed.add_field(name="*Idle*", value="`%s`" % (idle), inline=False)
        embed.add_field(name="*Do Not Disturb*", value="`%s`" % (dnd), inline=False)
        embed.add_field(name="*Bots*", value="`%s`" % (bots), inline=False)
        embed.add_field(name="*Total*", value="`%s`" % (len(ctx.guild.members)), inline=False)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed=embed)

    @commands.command(name="banner", description="Shows the banner", usage="banner")
    async def banner(self, ctx):
        if len(ctx.guild.banner_url) == 0:
            return await ctx.send(embed=discord.Embed(title="banner", description="There is no guild banner"), color=self.color)
        await ctx.send(embed=discord.Embed(title="**`%s`**'s server banner" % (ctx.guild.name), color=self.color).set_image(url=ctx.guild.banner_url))

    @commands.command(name="servericon", description="Shows server icon", usage="servericon", aliases=["serverpfp", "guildpfp", "spfp"])
    async def servericon(self, ctx):
        if ctx.guild.icon_url == None:
            return await ctx.send(embed=discord.Embed(title="guildicon", description="There is no guild icon"), color=self.color)
        await ctx.send(embed=discord.Embed(title="**`%s`**'s server icon" % (ctx.guild.name), color=self.color).set_image(url=ctx.guild.icon_url))

    @commands.command(name="serverinfo", description="Shows server information", usage="serverinfo", aliases=["sinfo"])
    async def serverinfo(self, ctx):
        embed = discord.Embed(title="**`%s`**" % (ctx.guild.name), color=self.color)
        embed.add_field(name="*Server ID*", value="`%s`" % (ctx.guild.id), inline=False)
        embed.add_field(name="*Server Name*", value="`%s`" % (ctx.guild.name), inline=False)
        embed.add_field(name="*Server Owner*", value="`%s`" % (ctx.guild.owner), inline=False)
        embed.add_field(name="*Creation Date*", value="`%s`" % (ctx.guild.created_at.strftime("%a, %d %B %Y, %I:%M %p")), inline=False)
        embed.add_field(name="*Members*", value="`%s`" % (len(ctx.guild.members)), inline=False)
        embed.add_field(name="*Roles*", value="`%s`" % (len(ctx.guild.roles)), inline=False)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed=embed)

    @commands.command(name="invite", description="Invite the bot", usage="invite", aliases=["add"])
    async def invite(self, ctx):
        await ctx.send(embed=discord.Embed(title="Invite", description="[Bot Invite](https://discord.com/oauth2/authorize?client_id=865143144269217825&permissions=2134207679&scope=bot)\n[Support Server](https://discord.gg/w2QC2AB9hP)", color=self.color).set_thumbnail(url=self.client.user.avatar_url))

    @commands.command(name="ping", description="Shows the latency", usage="ping", aliases=["latency"])
    async def ping(self, ctx):
        before = time.monotonic()
        await self.db.find_one({"ping": 1})
        db = round(time.monotonic() - before) * 1000
        shard = shard = self.client.get_shard(ctx.guild.shard_id)
        ping_ = int(shard.latency * 1000)
        if ping_ < 25:
            client_emoji = "<:connection:867971898460487680>"
        elif ping_ < 50:
            client_emoji = "<:good_connection:867971898208829440>"
        else:
            client_emoji = "<:bad_connection:867971898531782686>"
        if db < 25:
            db_emoji = "<:connection:867971898460487680>"
        elif db < 50:
            db_emoji = "<:good_connection:867971898208829440>"
        else:
            db_emoji = "<:bad_connection:867971898531782686>"
        await ctx.send(embed=discord.Embed(title="Ping", description="**%s Shard **`%s`** latency: `%sms`\n%s Database latency: `%sms`**" % (client_emoji, ctx.guild.shard_id, ping_, db_emoji, db), color=self.color))

    @commands.command(name="status", description="Shows users status", usage="status <member>")
    async def status(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author

        status = member.status
        if status == discord.Status.offline:
            status_location = "Not Applicable"
        elif member.mobile_status != discord.Status.offline:
            status_location = "Mobile"
        elif member.web_status != discord.Status.offline:
            status_location = "Browser"
        elif member.desktop_status != discord.Status.offline:
            status_location = "Desktop"
        else:
            status_location = "Not Applicable"
        await ctx.send(embed=discord.Embed(title="status", description="`%s`: `%s`" % (status_location, status), color=self.color))

    @commands.command(name="emoji", description="Shows emoji syntax", usage="emoji [emoji]")
    async def emoji(self, ctx, emoji: discord.Emoji):
        return await ctx.send(embed=discord.Embed(title="emoji", description="emoji: %s\nid: **`%s`**" % (emoji, emoji.id), color=self.color))

    @commands.command(name="user", description="Shows user syntax", usage="user [user]")
    async def user(self, ctx, user: discord.Member = None):
        return await ctx.send(embed=discord.Embed(title="user", description="user: %s\nid: **`%s`**" % (user.mention, user.id), color=self.color))

    @commands.command(name="role", description="Shows role syntax", usage="role [role]")
    async def role(self, ctx, role: discord.Role): 
        return await ctx.send(embed=discord.Embed(title="role", description="role: %s\nid: **`%s`**" % (role.mention, role.id), color=self.color))

    @commands.command(name="channel", description="Shows channel syntax", usage="channel [channel]")
    async def channel(self, ctx, channel: discord.TextChannel): 
        return await ctx.send(embed=discord.Embed(title="channel", description="channel: %s\nid: **`%s`**" % (channel.mention, channel.id), color=self.color))

    @commands.command(name="joined-at", description="Shows when a user joined", usage="joined-at [user]", aliases=["ja"])
    async def joined_at(self, ctx):
        joined = ctx.author.joined_at.strftime("%a, %d %b %Y %I:%M %p")
        await ctx.send(embed=discord.Embed(title="joined-at", description="**`%s`**" % (joined), color=self.color))

    @commands.command(name="invites", description="Shows the amount of invites", usage="invites <user>", aliases=["invs"])
    async def invites(self, ctx, member: discord.Member = None):
        totalInvites = 0
        if member == None:
            member = ctx.author
        for i in await ctx.guild.invites():
            if i.inviter == member:
                totalInvites += i.uses
        if member == ctx.author:
             embed = discord.Embed(title="invites", description="You've invited **`%s`** member(s) to the server!" % (totalInvites), color=self.color)
        else:
            embed = discord.Embed(title="invites", description="**`%s`** has invited **`%s`** member(s) to the server!" % (member.name, totalInvites), color=self.color)
        await ctx.send(embed=embed)

    @commands.command(name="boosts", description="Shows boosts count", usage="boosts", aliases=["bc"])
    async def boosts(self, ctx):
        await ctx.send(embed=discord.Embed(title="boosts", description="**`%s`**" % (ctx.guild.premium_subscription_count), color=self.color))

    @commands.command(name="emoji-add", description="Adds a emoji", usage="emoji-add [emoji]", aliases=["eadd"])
    @commands.has_permissions(manage_emojis=True)
    async def emojiadd(self, ctx, emote):
        try:
            if emote[0] == '<':
                name = emote.split(':')[1]
                emoji_name = emote.split(':')[2][:-1]
                anim = emote.split(':')[0]
                if anim == '<a':
                    url = f'https://cdn.discordapp.com/emojis/{emoji_name}.gif'
                else:
                    url = f'https://cdn.discordapp.com/emojis/{emoji_name}.png'
                try:
                    response = requests.get(url) 
                    img = response.content
                    emote = await ctx.guild.create_custom_emoji(name=name, image=img) 
                    return await ctx.send(embed=discord.Embed(title="emoji-add", description="added \"**`%s`**\"!" % (emote), color=self.color))
                except Exception:
                    return await ctx.send(embed=discord.Embed(title="emoji-add", description=f"failed to add emoji", color=self.color))
            else:
                return await ctx.send(embed=discord.Embed(title="emoji-add", description=f"invalid emoji", color=self.color))
        except Exception:
            return await ctx.send(embed=discord.Embed(title="emoji-add", description=f"failed to add emoji", color=self.color))

    @commands.command(name="emoji-delete", description="Deletes a emoji", usage="emoji-delete [emoji]", aliases=["edel"])
    @commands.has_permissions(manage_emojis=True)
    async def delete(self, ctx, emote: discord.Emoji):
        return await ctx.send(embed=discord.Embed(title="emoji-delete", description="deleted \"**`%s`**\"!" % (emote), color=self.color))

    @commands.command(name="userinfo", description="Shows user information", usage="userinfo <user>", aliases=["whois"])
    async def userinfo(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author
        if member == "":
            member = ctx.author
        embed = discord.Embed(title="User Information", color=self.color, timestamp=ctx.message.created_at)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.add_field(name="User ID", value="**`%s`**" % (member.id), inline=False)
        embed.add_field(name="Name", value="**`%s`**" % (member.display_name), inline=False)
        embed.add_field(name="Discriminator", value="**`%s`**" % (member.discriminator), inline=False)
        embed.add_field(name="Creation Date", value="**`%s`**" % (member.created_at.strftime("%a, %d %B %Y, %I:%M %p")), inline=False)
        embed.add_field(name="Bot Check", value="**`%s`**" % (member.bot), inline=False)
        embed.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="avatar", description="Shows users avatar", usage="avatar <user>", aliases=["pfp"])
    async def avatar(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author
        embed = discord.Embed(title=f"{member.name}\'s Avatar", color=self.color)
        embed.add_field(name="Avatar", value=f"[`Link`]({member.avatar_url})", inline=False)
        embed.set_image(url=member.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="info", description="Shows bot information", usage="info", aliases=["botinfo"])
    async def info(self, ctx):
        before = time.monotonic()
        await self.db.find_one({"ping": 1})
        db = f"{round(time.monotonic() - before) * 1000}ms"
        data = """**```yaml
Creator:
    Developer: Dropout#1337

Stats:
    Servers: %s
    Users: %s
    Shards: %s
    
Latencies:
    Database: %s
    Websocket: %s
    Shards:
""" % (len(self.client.guilds), len(set(self.client.get_all_members())), self.client.shard_count, db, int(self.client.latency * 1000))
        embed = discord.Embed(title="Information", color=self.color)
        for x in range(self.client.shard_count):
            shard = self.client.get_shard(x)
            #shard_servers = len([guild for guild in self.client.guilds if guild.shard_id == shard_id])
            data += "       Shard %s: %sms\n" % (x, int(shard.latency * 1000))
        embed.description = data
        embed.description += "```**"
        embed.set_thumbnail(url=self.client.user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="upvote", description="Upvote the bot", usage="upvote", aliases=["supportus"])
    async def upvote(self, ctx):
        await ctx.send(embed=discord.Embed(title="Upvote!", description="[Discord Bot List](https://discordbotlist.com/bots/reverb)\n[Discord.Bots.gg](https://discord.bots.gg/bots/865143144269217825)", color=self.color))

def setup(client):
    client.add_cog(general(client))
