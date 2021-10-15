import discord
import logging
import aiohttp
from discord.ext import commands
import motor.motor_asyncio as mongodb

logging.basicConfig(
    level=logging.INFO,
    format="\x1b[38;5;197m[\x1b[0m%(asctime)s\x1b[38;5;197m]\x1b[0m -> \x1b[38;5;197m%(message)s\x1b[0m",
    datefmt="%H:%M:%S",
)

class nsfw(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.color = 0x2f3136
        self.connection = mongodb.AsyncIOMotorClient("mongodb+srv://root:GJ2mG7wpJMuK1DlC@discord.zvth0.mongodb.net/reverb?retryWrites=true&w=majority")
        self.db = self.connection["reverb"]["servers"]

    async def get_image(self, type):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://nekobot.xyz/api/image?type=%s" % (type)) as response:
                json = await response.json()
                if json["success"]:
                    return json["message"]
                else:
                    return "Failed"

    @commands.group(invoke_without_command=True, name="nsfw", description="Shows nsfw command menu", usage="nsfw")
    async def nsfw(self, ctx):
        return await ctx.send(embed=discord.Embed(title="Nsfw", description="Please use `%shelp nsfw` instead!\n— This command group does not require a detailed help" % (ctx.prefix)))
    
    @nsfw.command(name="hass", description="NSFW", usage="nsfw hass")
    async def hass(self, ctx):
        url = await self.get_image(type="hass")
        if ctx.channel.is_nsfw(): await ctx.send(embed=discord.Embed(title="nsfw", color=self.color).set_image(url=url))
        if ctx.channel.is_nsfw() != True: return await ctx.send(embed=discord.Embed(title="NSFW", description="**`%s`** does not have nsfw mode enabled" % (ctx.channel.name), color=self.color))

    @nsfw.command(name="hmidriff", description="NSFW", usage="nsfw hmidriff")
    async def hmidriff(self, ctx):
        url = await self.get_image(type="hmidriff")
        if ctx.channel.is_nsfw(): await ctx.send(embed=discord.Embed(title="nsfw", color=self.color).set_image(url=url))
        if ctx.channel.is_nsfw() != True: return await ctx.send(embed=discord.Embed(title="NSFW", description="**`%s`** does not have nsfw mode enabled" % (ctx.channel.name), color=self.color))

    @nsfw.command(name="pgif", description="NSFW", usage="nsfw pgif")
    async def pgif(self, ctx):
        url = await self.get_image(type="pgif")
        if ctx.channel.is_nsfw(): await ctx.send(embed=discord.Embed(title="nsfw", color=self.color).set_image(url=url))
        if ctx.channel.is_nsfw() != True: return await ctx.send(embed=discord.Embed(title="NSFW", description="**`%s`** does not have nsfw mode enabled" % (ctx.channel.name), color=self.color))

    @nsfw.command(name="4k", description="NSFW", usage="nsfw 4k")
    async def fourk(self, ctx):
        url = await self.get_image(type="4k")
        if ctx.channel.is_nsfw(): await ctx.send(embed=discord.Embed(title="nsfw", color=self.color).set_image(url=url))
        if ctx.channel.is_nsfw() != True: return await ctx.send(embed=discord.Embed(title="NSFW", description="**`%s`** does not have nsfw mode enabled" % (ctx.channel.name), color=self.color))

    @nsfw.command(name="holo", description="NSFW", usage="nsfw holo")
    async def holo(self, ctx):
        url = await self.get_image(type="holo")
        if ctx.channel.is_nsfw(): await ctx.send(embed=discord.Embed(title="nsfw", color=self.color).set_image(url=url))
        if ctx.channel.is_nsfw() != True: return await ctx.send(embed=discord.Embed(title="NSFW", description="**`%s`** does not have nsfw mode enabled" % (ctx.channel.name), color=self.color))

    @nsfw.command(name="hneko", description="NSFW", usage="nsfw hneko")
    async def hneko(self, ctx):
        url = await self.get_image(type="hneko")
        if ctx.channel.is_nsfw(): await ctx.send(embed=discord.Embed(title="nsfw", color=self.color).set_image(url=url))
        if ctx.channel.is_nsfw() != True: return await ctx.send(embed=discord.Embed(title="NSFW", description="**`%s`** does not have nsfw mode enabled" % (ctx.channel.name), color=self.color))

    @nsfw.command(name="neko", description="NSFW", usage="nsfw neko")
    async def neko(self, ctx):
        url = await self.get_image(type="neko")
        if ctx.channel.is_nsfw(): await ctx.send(embed=discord.Embed(title="nsfw", color=self.color).set_image(url=url))
        if ctx.channel.is_nsfw() != True: return await ctx.send(embed=discord.Embed(title="NSFW", description="**`%s`** does not have nsfw mode enabled" % (ctx.channel.name), color=self.color))

    @nsfw.command(name="hkitsune", description="NSFW", usage="nsfw hkitsune")
    async def hkitsune(self, ctx):
        url = await self.get_image(type="hkitsune")
        if ctx.channel.is_nsfw(): await ctx.send(embed=discord.Embed(title="nsfw", color=self.color).set_image(url=url))
        if ctx.channel.is_nsfw() != True: return await ctx.send(embed=discord.Embed(title="NSFW", description="**`%s`** does not have nsfw mode enabled" % (ctx.channel.name), color=self.color))

    @nsfw.command(name="kemonomimi", description="NSFW", usage="nsfw kemonomimi")
    async def kemonomimi(self, ctx):
        url = await self.get_image(type="kemonomimi")
        if ctx.channel.is_nsfw(): await ctx.send(embed=discord.Embed(title="nsfw", color=self.color).set_image(url=url))
        if ctx.channel.is_nsfw() != True: return await ctx.send(embed=discord.Embed(title="NSFW", description="**`%s`** does not have nsfw mode enabled" % (ctx.channel.name), color=self.color))

    @nsfw.command(name="anal", description="NSFW", usage="nsfw anal")
    async def anal(self, ctx):
        url = await self.get_image(type="anal")
        if ctx.channel.is_nsfw(): await ctx.send(embed=discord.Embed(title="nsfw", color=self.color).set_image(url=url))
        if ctx.channel.is_nsfw() != True: return await ctx.send(embed=discord.Embed(title="NSFW", description="**`%s`** does not have nsfw mode enabled" % (ctx.channel.name), color=self.color))

    @nsfw.command(name="hanal", description="NSFW", usage="nsfw hanal")
    async def hanal(self, ctx):
        url = await self.get_image(type="hanal")
        if ctx.channel.is_nsfw(): await ctx.send(embed=discord.Embed(title="nsfw", color=self.color).set_image(url=url))
        if ctx.channel.is_nsfw() != True: return await ctx.send(embed=discord.Embed(title="NSFW", description="**`%s`** does not have nsfw mode enabled" % (ctx.channel.name), color=self.color))

    @nsfw.command(name="gonewild", description="NSFW", usage="nsfw gonewild")
    async def gonewild(self, ctx):
        url = await self.get_image(type="gonewild")
        if ctx.channel.is_nsfw(): await ctx.send(embed=discord.Embed(title="nsfw", color=self.color).set_image(url=url))
        if ctx.channel.is_nsfw() != True: return await ctx.send(embed=discord.Embed(title="NSFW", description="**`%s`** does not have nsfw mode enabled" % (ctx.channel.name), color=self.color))

    @nsfw.command(name="kanna", description="NSFW", usage="nsfw kanna")
    async def kanna(self, ctx):
        url = await self.get_image(type="kanna")
        if ctx.channel.is_nsfw(): await ctx.send(embed=discord.Embed(title="nsfw", color=self.color).set_image(url=url))
        if ctx.channel.is_nsfw() != True: return await ctx.send(embed=discord.Embed(title="NSFW", description="**`%s`** does not have nsfw mode enabled" % (ctx.channel.name), color=self.color))

    @nsfw.command(name="ass", description="NSFW", usage="nsfw ass")
    async def ass(self, ctx):
        url = await self.get_image(type="ass")
        if ctx.channel.is_nsfw(): await ctx.send(embed=discord.Embed(title="nsfw", color=self.color).set_image(url=url))
        if ctx.channel.is_nsfw() != True: return await ctx.send(embed=discord.Embed(title="NSFW", description="**`%s`** does not have nsfw mode enabled" % (ctx.channel.name), color=self.color))

    @nsfw.command(name="pussy", description="NSFW", usage="nsfw pussy")
    async def pussy(self, ctx):
        url = await self.get_image(type="pussy")
        if ctx.channel.is_nsfw(): await ctx.send(embed=discord.Embed(title="nsfw", color=self.color).set_image(url=url))
        if ctx.channel.is_nsfw() != True: return await ctx.send(embed=discord.Embed(title="NSFW", description="**`%s`** does not have nsfw mode enabled" % (ctx.channel.name), color=self.color))

    @nsfw.command(name="thigh", description="NSFW", usage="nsfw thigh")
    async def thigh(self, ctx):
        url = await self.get_image(type="thigh")
        if ctx.channel.is_nsfw(): await ctx.send(embed=discord.Embed(title="nsfw", color=self.color).set_image(url=url))
        if ctx.channel.is_nsfw() != True: return await ctx.send(embed=discord.Embed(title="NSFW", description="**`%s`** does not have nsfw mode enabled" % (ctx.channel.name), color=self.color))

    @nsfw.command(name="hthigh", description="NSFW", usage="nsfw hthigh")
    async def hthigh(self, ctx):
        url = await self.get_image(type="hthigh")
        if ctx.channel.is_nsfw(): await ctx.send(embed=discord.Embed(title="nsfw", color=self.color).set_image(url=url))
        if ctx.channel.is_nsfw() != True: return await ctx.send(embed=discord.Embed(title="NSFW", description="**`%s`** does not have nsfw mode enabled" % (ctx.channel.name), color=self.color))

    @nsfw.command(name="gah", description="NSFW", usage="nsfw gah")
    async def gah(self, ctx):
        url = await self.get_image(type="gah")
        if ctx.channel.is_nsfw(): await ctx.send(embed=discord.Embed(title="nsfw", color=self.color).set_image(url=url))
        if ctx.channel.is_nsfw() != True: return await ctx.send(embed=discord.Embed(title="NSFW", description="**`%s`** does not have nsfw mode enabled" % (ctx.channel.name), color=self.color))

    @nsfw.command(name="coffee", description="NSFW", usage="nsfw coffee")
    async def coffee(self, ctx):
        url = await self.get_image(type="coffe")
        if ctx.channel.is_nsfw(): await ctx.send(embed=discord.Embed(title="nsfw", color=self.color).set_image(url=url))
        if ctx.channel.is_nsfw() != True: return await ctx.send(embed=discord.Embed(title="NSFW", description="**`%s`** does not have nsfw mode enabled" % (ctx.channel.name), color=self.color))

    @nsfw.command(name="food", description="NSFW", usage="nsfw food")
    async def food(self, ctx):
        url = await self.get_image(type="food")
        if ctx.channel.is_nsfw(): await ctx.send(embed=discord.Embed(title="nsfw", color=self.color).set_image(url=url))
        if ctx.channel.is_nsfw() != True: return await ctx.send(embed=discord.Embed(title="NSFW", description="**`%s`** does not have nsfw mode enabled" % (ctx.channel.name), color=self.color))

    @nsfw.command(name="paizuri", description="NSFW", usage="nsfw paizuri")
    async def paizuri(self, ctx):
        url = await self.get_image(type="paizuri")
        if ctx.channel.is_nsfw(): await ctx.send(embed=discord.Embed(title="nsfw", color=self.color).set_image(url=url))
        if ctx.channel.is_nsfw() != True: return await ctx.send(embed=discord.Embed(title="NSFW", description="**`%s`** does not have nsfw mode enabled" % (ctx.channel.name), color=self.color))

    @nsfw.command(name="tentacle", description="NSFW", usage="nsfw tentacle")
    async def tentacle(self, ctx):
        url = await self.get_image(type="tentacle")
        if ctx.channel.is_nsfw(): await ctx.send(embed=discord.Embed(title="nsfw", color=self.color).set_image(url=url))
        if ctx.channel.is_nsfw() != True: return await ctx.send(embed=discord.Embed(title="NSFW", description="**`%s`** does not have nsfw mode enabled" % (ctx.channel.name), color=self.color))

    @nsfw.command(name="boobs", description="NSFW", usage="nsfw boobs")
    async def boobs(self, ctx):
        url = await self.get_image(type="boobs")
        if ctx.channel.is_nsfw(): await ctx.send(embed=discord.Embed(title="nsfw", color=self.color).set_image(url=url))
        if ctx.channel.is_nsfw() != True: return await ctx.send(embed=discord.Embed(title="NSFW", description="**`%s`** does not have nsfw mode enabled" % (ctx.channel.name), color=self.color))

    @nsfw.command(name="hboobs", description="NSFW", usage="nsfw hboobs")
    async def hboobs(self, ctx):
        url = await self.get_image(type="hboobs")
        if ctx.channel.is_nsfw(): await ctx.send(embed=discord.Embed(title="nsfw", color=self.color).set_image(url=url))
        if ctx.channel.is_nsfw() != True: return await ctx.send(embed=discord.Embed(title="NSFW", description="**`%s`** does not have nsfw mode enabled" % (ctx.channel.name), color=self.color))

    @nsfw.command(name="yaoi", description="NSFW", usage="nsfw yaoi")
    async def yaoi(self, ctx):
        url = await self.get_image(type="yaoi")
        if ctx.channel.is_nsfw(): await ctx.send(embed=discord.Embed(title="nsfw", color=self.color).set_image(url=url))
        if ctx.channel.is_nsfw() != True: return await ctx.send(embed=discord.Embed(title="NSFW", description="**`%s`** does not have nsfw mode enabled" % (ctx.channel.name), color=self.color))

def setup(client):
    client.add_cog(nsfw(client))
