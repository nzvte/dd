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

class hentai(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.color = 0x2f3136
        self.connection = mongodb.AsyncIOMotorClient("mongodb+srv://root:GJ2mG7wpJMuK1DlC@discord.zvth0.mongodb.net/reverb?retryWrites=true&w=majority")
        self.db = self.connection["reverb"]["servers"]

    @commands.group(invoke_without_command=True)
    async def hentai(self, ctx):
        return await ctx.send(embed=discord.Embed(title="Hentai", description="Please use `%shelp reaction` instead!\n— This command group does not require a detailed help" % (ctx.prefix)))

    @hentai.command(name="random", description="Gathers random hentai", usage="hentai random")
    async def random(self, ctx):
        if ctx.channel.is_nsfw():
            async with aiohttp.ClientSession() as session:
                async with session.get("https://nekos.life/api/v2/img/Random_hentai_gif") as response:
                    if not "url" in await response.text():
                        return await ctx.send(embed=discord.Embed(title="Random Hentai", description="Failed to gather some random hentai", color=self.color))
                    else:
                        json = await response.json()
                        hentai_url = json["url"]
                        return await ctx.send(embed=discord.Embed(title="Random Hentai", color=self.color).set_image(url=hentai_url))
        else:
            return await ctx.send(embed=discord.Embed(title="Random Hentai", description="**`%s`** does not have nsfw mode enabled" % (ctx.channel.name), color=self.color))

    @hentai.command(name="pussy", description="Gathers pussy hentai", usage="hentai pussy")
    async def pussy(self, ctx):
        if ctx.channel.is_nsfw():
            async with aiohttp.ClientSession() as session:
                async with session.get("https://nekos.life/api/v2/img/pussy") as response:
                    if not "url" in await response.text():
                        return await ctx.send(embed=discord.Embed(title="Pussy Hentai", description="Failed to gather some pussy hentai", color=self.color))
                    else:
                        json = await response.json()
                        hentai_url = json["url"]
                        return await ctx.send(embed=discord.Embed(title="Pussy Hentai", color=self.color).set_image(url=hentai_url))
        else:
            return await ctx.send(embed=discord.Embed(title="Pussy Hentai", description="**`%s`** does not have nsfw mode enabled" % (ctx.channel.name), color=self.color))

    @hentai.command(name="lesbian", description="Gathers lesbian hentai", usage="hentai lesbian")
    async def lesbian(self, ctx):
        if ctx.channel.is_nsfw():
            async with aiohttp.ClientSession() as session:
                async with session.get("https://nekos.life/api/v2/img/les") as response:
                    if not "url" in await response.text():
                        return await ctx.send(embed=discord.Embed(title="Lesbian Hentai", description="Failed to gather some lesbian hentai", color=self.color))
                    else:
                        json = await response.json()
                        hentai_url = json["url"]
                        return await ctx.send(embed=discord.Embed(title="Lesbian Hentai", color=self.color).set_image(url=hentai_url))
        else:
            return await ctx.send(embed=discord.Embed(title="Lesbian Hentai", description="**`%s`** does not have nsfw mode enabled" % (ctx.channel.name), color=self.color))

    @hentai.command(name="nudes", description="Gathers nude hentai", usage="hentai nudes")
    async def nudes(self, ctx):
        if ctx.channel.is_nsfw():
            async with aiohttp.ClientSession() as session:
                async with session.get("https://nekos.life/api/v2/img/nsfw_neko_gif") as response:
                    if not "url" in await response.text():
                        return await ctx.send(embed=discord.Embed(title="Nudes Hentai", description="Failed to gather some nudes hentai", color=self.color))
                    else:
                        json = await response.json()
                        hentai_url = json["url"]
                        return await ctx.send(embed=discord.Embed(title="Nudes Hentai", color=self.color).set_image(url=hentai_url))
        else:
            return await ctx.send(embed=discord.Embed(title="Nudes Hentai", description="**`%s`** does not have nsfw mode enabled" % (ctx.channel.name), color=self.color))

    @hentai.command(name="blowjob", description="Gathers blowjob hentai", usage="hentai blowjob")
    async def blowjob(self, ctx):
        if ctx.channel.is_nsfw():
            async with aiohttp.ClientSession() as session:
                async with session.get("https://nekos.life/api/v2/img/blowjob") as response:
                    if not "url" in await response.text():
                        return await ctx.send(embed=discord.Embed(title="Blowjob Hentai", description="Failed to gather some blowjob hentai", color=self.color))
                    else:
                        json = await response.json()
                        hentai_url = json["url"]
                        return await ctx.send(embed=discord.Embed(title="Blowjob Hentai", color=self.color).set_image(url=hentai_url))
        else:
            return await ctx.send(embed=discord.Embed(title="Blowjob Hentai", description="**`%s`** does not have nsfw mode enabled" % (ctx.channel.name), color=self.color))

    @hentai.command(name="tits", description="Gathers tits hentai", usage="hentai tits")
    async def tits(self, ctx):
        if ctx.channel.is_nsfw():
            async with aiohttp.ClientSession() as session:
                async with session.get("https://nekos.life/api/v2/img/Random_hentai_gif") as response:
                    if not "url" in await response.text():
                        return await ctx.send(embed=discord.Embed(title="Tits Hentai", description="Failed to gather some tits hentai", color=self.color))
                    else:
                        json = await response.json()
                        hentai_url = json["url"]
                        return await ctx.send(embed=discord.Embed(title="Tits Hentai", color=self.color).set_image(url=hentai_url))
        else:
            return await ctx.send(embed=discord.Embed(title="Tits Hentai", description="**`%s`** does not have nsfw mode enabled" % (ctx.channel.name), color=self.color))

    @hentai.command(name="boobs", description="Gathers boobs hentai", usage="hentai boobs")
    async def boobs(self, ctx):
        if ctx.channel.is_nsfw():
            async with aiohttp.ClientSession() as session:
                async with session.get("https://nekos.life/api/v2/img/boobs") as response:
                    if not "url" in await response.text():
                        return await ctx.send(embed=discord.Embed(title="Boobs Hentai", description="Failed to gather some boobs hentai", color=self.color))
                    else:
                        json = await response.json()
                        hentai_url = json["url"]
                        return await ctx.send(embed=discord.Embed(title="Boobs Hentai", color=self.color).set_image(url=hentai_url))
        else:
            return await ctx.send(embed=discord.Embed(title="Boobs Hentai", description="**`%s`** does not have nsfw mode enabled" % (ctx.channel.name), color=self.color))

    @hentai.command(name="feet", description="Gathers feet hentai", usage="hentai feet")
    async def random(self, ctx):
        if ctx.channel.is_nsfw():
            async with aiohttp.ClientSession() as session:
                async with session.get("https://nekos.life/api/v2/img/feetg") as response:
                    if not "url" in await response.text():
                        return await ctx.send(embed=discord.Embed(title="Feet Hentai", description="Failed to gather some feet hentai", color=self.color))
                    else:
                        json = await response.json()
                        hentai_url = json["url"]
                        return await ctx.send(embed=discord.Embed(title="Feet Hentai", color=self.color).set_image(url=hentai_url))
        else:
            return await ctx.send(embed=discord.Embed(title="Feet Hentai", description="**`%s`** does not have nsfw mode enabled" % (ctx.channel.name), color=self.color))

    @hentai.command(name="anal", description="Gathers anal hentai", usage="hentai anal")
    async def anal(self, ctx):
        if ctx.channel.is_nsfw():
            async with aiohttp.ClientSession() as session:
                async with session.get("https://nekos.life/api/v2/img/anal") as response:
                    if not "url" in await response.text():
                        return await ctx.send(embed=discord.Embed(title="Anal Hentai", description="Failed to gather some anal hentai", color=self.color))
                    else:
                        json = await response.json()
                        hentai_url = json["url"]
                        return await ctx.send(embed=discord.Embed(title="Anal Hentai", color=self.color).set_image(url=hentai_url))
        else:
            return await ctx.send(embed=discord.Embed(title="Anal Hentai", description="**`%s`** does not have nsfw mode enabled" % (ctx.channel.name), color=self.color))

def setup(client):
    client.add_cog(hentai(client))