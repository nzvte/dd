import random
import discord
import logging
import aiohttp
import asyncio
from discord.ext import commands
import motor.motor_asyncio as mongodb

logging.basicConfig(
    level=logging.INFO,
    format="\x1b[38;5;197m[\x1b[0m%(asctime)s\x1b[38;5;197m]\x1b[0m -> \x1b[38;5;197m%(message)s\x1b[0m",
    datefmt="%H:%M:%S",
)

class fun(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.color = 0x2f3136
        self.connection = mongodb.AsyncIOMotorClient("mongodb+srv://root:GJ2mG7wpJMuK1DlC@discord.zvth0.mongodb.net/reverb?retryWrites=true&w=majority")
        self.db = self.connection["reverb"]["servers"]

    @commands.command(name="tuck", description="Tuck someone in for bed", usage="tuck <user>")
    async def tuck(self, ctx, user: discord.Member = None):
        if user == None:
            await ctx.send("**`%s`** tucked themself in!.. loser..." % (ctx.author.name))
        else:
            await ctx.send("**`%s`** tucked **`%s`** in!" % (ctx.author.name, user.name))

    @commands.command(name="uwuify", description="Uwuifys the text", usage="uwuify <text>", aliases=["uwu"])
    async def uwuify(self, ctx, *, text):
        text = text.replace("@everyone", "<mention>")
        text = text.replace("@here", "<mention>")
        text = text.replace("@", "<mention>")
        await ctx.send("uwu %s" % (text.replace("l", "w")))

    @commands.command(name="yomama", description="Yomama joke", usage="yomama")
    async def yomama(self, ctx):
        async with aiohttp.ClientSession as session:
            async with session.get("https://api.yomomma.info/") as response:
                if "joke" in await response.text():
                    json = await response.json()
                    joke = json["joke"]
                    await ctx.send("Here is a joke for you: %s" % (joke))

    @commands.command(name="rps", description="Play rock paper scissors", usage="rps <rock/paper/scissors>", aliases=["rock-paper-scissors"])
    async def rps(self, ctx, choice):
        my_choice = random.choice(["rock", "paper", "scissors"])
        if not choice in ["rock", "paper", "scissors"]:
            return await ctx.send(embed=discord.Embed(title="rps", description="Invalid option you may only use rock, paper or scissors", color=self.color))
        if my_choice == "rock" and choice == "paper":
            return await ctx.send("You won!")
        if my_choice == "paper" and choice == "rock":
            return await ctx.send("You lost...")
        if my_choice == "paper" and choice == "scissors":
            return await ctx.send("You won!")
        if my_choice == "scissors" and choice == "paper":
            return await ctx.send("You lost...")
        if my_choice == "rock" and choice == "scissors":
            return await ctx.send("You lost...")
        if my_choice == "scissors" and choice == "rock":
            return await ctx.send("You won!")

    @commands.command(name="spank", description="Spanks a user", usage="spank <user>")
    async def spank(self, ctx, user: discord.Member = None):
        if user.id == ctx.author.id:
            await ctx.send("**`%s`** spanked themselves.. ew, how gross and pathetic.." % (ctx.author.name))
        else:
            await ctx.send("**`%s`** spanked **`%s`**" % (ctx.author.name, user.name))

    @commands.command(name="reverse", description="Reverses your message", usage="reverse <text>", aliases=["rev"])
    async def reverse(self, ctx, *, text):
        reversed = text[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
        await ctx.send("🔄 %s" % (reversed))

    @commands.command(name="randomcolor", description="Random hex color", usage="randomcolor", aliases=["clr"])
    async def randomcolour(self, ctx):
        color = "".join([random.choice("0123456789ABCDE") for x in range(6)])
        await ctx.send(embed=discord.Embed(title="randomcolor", description="hex: `#%s`" % (color), color=self.color).set_thumbnail(url="https://via.placeholder.com/150/%s/%s" % (color, color)))

    @commands.command(name="random", description="Random number", usage="random <start> <end>", aliases=["rand"])
    async def random(self, ctx, start: int = None, end: int = None):
        if start == None:
            start = 1
        if end == None:
            end = 150
        await ctx.send("Here is your random number: " % (random.randint(start, end)))

    @commands.command(name="kiss", description="Kiss a mentioned user", usage="kiss <user>")
    async def kiss(self, ctx, user: discord.Member = None):
        if user.id == ctx.author.id:
            await ctx.send("**`%s`** kisses themselves.. ew, how gross and pathetic.." % (ctx.author.name))
        else:
            await ctx.send("**`%s`** kisses **`%s`**" % (ctx.author.name, user.name))

    @commands.command(name="firstmsg", description="First message sent in the mentioned channel or current channel", usage="firstmsg", aliases=["fmsg", "first"])
    async def firstmsg(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel
        first_message = (await channel.history(limit=1, oldest_first=True).flatten())[0]
        embed = discord.Embed(color=self.color)
        embed.set_author(name=first_message.content, url=first_message.jump_url)
        await ctx.send(embed=embed)

    @commands.command(name="hug", description="Hug a mentioned user", usage="hug <user>")
    async def hug(self, ctx, user: discord.Member = None):
        if user.id == ctx.author.id:
            await ctx.send("**`%s`** hugs themselves.. ew, how gross and pathetic.." % (ctx.author.name))
        else:
            await ctx.send("**`%s`** hugs **`%s`**" % (ctx.author.name, user.name))

    @commands.command(name="clap", description="replaces spaces with a clap emoji", usage="clap <message>")
    async def clap(self, ctx, *, message):
        await ctx.send(message.replace(" ", "👏"))

    @commands.command(name="coinflip", description="Flips a coin", usage="coinflip", aliases=["flip"])
    async def conflip(self, ctx):
        msg = await ctx.send("flipping a coin...")
        await asyncio.sleep(2)
        coin = random.choice(["heads", "tails"])
        await msg.edit(content="it landed on %s" % (coin))

    @commands.command(name="bite", description="bite a person of choice. Watch out they might not like it", usage="bite <user>")
    async def bite(self, ctx, user: discord.Member = None):
        if user.id == ctx.author.id:
            await ctx.send("**`%s`** bites themselves.. ew, how gross and pathetic.." % (ctx.author.name))
        else:
            await ctx.send("**`%s`** bites **`%s`**" % (ctx.author.name, user.name))

    @commands.command(name="8ball", description="8ball, find out your future.", usage="8ball <question>", aliases=["ball"])
    async def ball(self, ctx, *, question):
        response = random.choice(["no", "as i see it, yes"])
        await ctx.reply("%s, %s" % (ctx.author.mention, response))

    @commands.command(name="poll", description="creates a poll", usage="poll <question>", aliases=["question"])
    async def poll(self, ctx, *, question):
        embed = discord.Embed(title="Poll", color=0x2f3136, description="```%s```" % (question))
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")

    @commands.command(name="pong", description="pong [useless]", usage="pong")
    async def pong(self, ctx):
        await ctx.send("🏓")

    @commands.command(name="nut", description="nut [useless]", usage="nut")
    async def nut(self, ctx):
        await ctx.send("🥜")

    @commands.command(name="no", description="no [useless]", usage="no")
    async def no(self, ctx):
        await ctx.send("⛔")

def setup(client):
    client.add_cog(fun(client))