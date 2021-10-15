import discord
import logging
from discord.ext import commands
import motor.motor_asyncio as mongodb

logging.basicConfig(
    level=logging.INFO,
    format="\x1b[38;5;197m[\x1b[0m%(asctime)s\x1b[38;5;197m]\x1b[0m -> \x1b[38;5;197m%(message)s\x1b[0m",
    datefmt="%H:%M:%S",
)

class configuration(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.color = 0x2f3136
        self.connection = mongodb.AsyncIOMotorClient("mongodb+srv://root:GJ2mG7wpJMuK1DlC@discord.zvth0.mongodb.net/reverb?retryWrites=true&w=majority")
        self.db = self.connection["reverb"]["servers"]

    @commands.group(invoke_without_command=True, name="help", description="Shows the help menu", usage="help", aliases=["helpme"])
    async def help(self, ctx, sub=None):
        if sub == None:
            embed = discord.Embed(title="%s" % (self.client.user.name), color=self.color)
            embed.description = "Join our support server by clicking [here](https://discord.gg/w2QC2AB9hP)"
            embed.add_field(name="*Categorys*", value="""**```
• general                 | Shows general commands
• moderation              | Shows moderation commands
• configuration           | Shows configuration commands
• welcome-message         | Shows welcome commands
• utility                 | Shows utility commands
• reaction                | Shows reaction commands
• hentai                  | Shows hentai commands
• fun                     | Shows fun commands
• nsfw                    | Shows nsfw commands
```**""", inline=False)
            embed.add_field(name="*Usage*", value="`%shelp [category/command]`" % (ctx.prefix), inline=False)
            embed.set_footer(text="Total commands: 118")
            await ctx.send(embed=embed)
        else:
            for cmd in self.client.commands:
                if str(cmd) == sub or sub in cmd.aliases:
                    return await ctx.send(embed=discord.Embed(title="**`%s`** Help" % (cmd), description="""**```
• description             | %s
• usage                   | %s```**""" % (cmd.description, cmd.usage)))
            return await ctx.send(embed=discord.Embed(title="help", description="this isn't a command, use `help` for a list of commands", color=self.color))


    @help.command(name="general", description="Shows the general menu", usage="help general")
    async def general(self, ctx):
        embed = discord.Embed(title="Help | General", color=self.color)
        embed.description = """**```
• membercount            | Shows the guilds member count
• banner                 | Shows the guilds banner
• servericon             | Shows the guilds icon
• serverinfo             | Shows the guilds information
• invite                 | Invite the bot
• ping                   | Check the bots latency
• info                   | Bot information
• status [user]          | Checks the users status
• emoji [emoji]          | Returns the emojis id
• user [user]            | Returns the users id
• role [role]            | Returns the roles id
• channel [channel]      | Returns the channels id
• invites [user]         | Returns the amount of invites
• boosts                 | Shows the amount of boosts
• emoji-add [emoji]      | Adds a emoji to the guild 
• emoji-delete [emoji]   | Deletes a emoji
• avatar [user]          | Shows the users avatar
```**"""
        await ctx.send(embed=embed)

    @help.command(name="configuration", description="Shows the configuration menu", usage="help configuration", aliases=["config"])
    async def configuration(self, ctx):
        embed = discord.Embed(title="Help | Configuration", color=self.color)
        embed.description = """**```
• whitelist add [user]    | Whitelists a user
• whitelist remove [user] | Unwhitelists a user
• whitelisted             | Shows all whitelisted users
• config status           | Shows the guilds config
• config enable [module]  | Enables a module
• config disable [module] | Disables a module
• prefix set [prefix]     | Sets the guilds prefix
• log set [channel]       | Set the logs
• log remove              | Remove the logs
• punishment [kick/ban]   | Set the punishment
```**"""
        await ctx.send(embed=embed)

    @help.command(name="moderation", description="Shows the moderation menu", usage="help moderation", aliases=["mod"])
    async def moderation(self, ctx):
        embed = discord.Embed(title="Help | Moderation", color=self.color)
        embed.description = """**```
• nuke                   | Nukes the channel
• unbanall               | Unbans all users
• ban [user]             | Bans a user
• unban [user]           | Unbans a user
• purge [amount]         | Purges messages
• kick [user]            | Kicks a user
• lock [channel]         | Locks a channel
• unlock [channel]       | Unlocks the channel
• slowmode [time]        | Changes the channels slowmode
• unslowmode             | Disables slowmode
```**"""
        await ctx.send(embed=embed)

    @help.command(name="welcome-message", description="Shows the welcome menu", usage="help welcome-message")
    async def welcome_message(self, ctx):
        embed = discord.Embed(title="Help | Welcome", color=self.color)
        embed.description = """**```
• wlc channel [channel] | Sets the welcome channel
• wlc message [message] | Sets the welcome message
• wlc disable           | Disables welcome messages
• wlc enable            | Enables welcome messages
• wlc test              | Tests the welcome message
```**"""
        await ctx.send(embed=embed)

    @help.command(name="utility", description="Shows the utility menu", usage="help utility", aliases=["util", "utils"])
    async def welcome(self, ctx):
        embed = discord.Embed(title="Help | Utility", color=self.color)
        embed.description = """**```
• snipe                | Snipes a deleted message
• roleall [role]       | Adds a role to everyone
• dump members         | Dumps the members
• dump channels        | Dumps the channels
• dump roles           | Dumps the roles
• jail [user]          | Jails a user
• unjail [user]        | Unjails a user
• cleanup [amount]     | Deletes the bots messages
```**"""
        await ctx.send(embed=embed)

    @help.command(name="reaction", description="Shows the reaction menu", usage="help reaction")
    async def welcome(self, ctx):
        embed = discord.Embed(title="Help | Reaction Role", color=self.color)
        embed.description = """**```
• rr add <message> <role> <emoji> | Adds reaction role
• rr remove <message>             | Removes reaction
```**"""
        await ctx.send(embed=embed)

    @help.command(name="hentai", description="Shows the hentai menu", usage="help hentai")
    async def hentai(self, ctx):
        embed = discord.Embed(title="Help | Hentai", color=self.color)
        embed.description = """**```
• hentai random      | Shows random hentai
• hentai pussy       | Shows pussy hentai
• hentai lesbian     | Shows lesbian hentai
• hentai nudes       | Shows nudes hentai
• hentai blowjob     | Shows blowjob hentai
• hentai tits        | Shows tits hentai
• hentai boobs       | Shows boobs hentai
• hentai feet        | Shows feet hentai
• hentai anal        | Shows anal hentai
```**"""
        await ctx.send(embed=embed)

    @help.command(name="fun", description="Shows the fun menu", usage="help fun")
    async def fun(self, ctx):
        embed = discord.Embed(title="Help | Fun", color=self.color)
        embed.description = """**```
• tuck [user]        | Tuck in a user
• uwuify [text]      | Uwuifys the text
• rps [rock/etc]     | Play rps
• spank [user]       | Spanks user
• reverse [text]     | Reverses text
• randomcolor        | Shows a random color
• random             | Shows random number
• kiss [user]        | Kisses a user
• hug [user]         | Hugs a user
• clap [text]        | Clap some text
• coinflip           | Flips a coin
• bite [user]        | Bites a user
• 8ball [question]   | Use a magic 8ball
• poll [question]    | Yes or no?
• pong               | Pong!
• nut                | Nut
• no                 | Just no
```**"""
        await ctx.send(embed=embed)

    @help.command(name="nsfw", description="Shows the nsfw menu", usage="help nsfw")
    async def nsfw(self, ctx):
        embed = discord.Embed(title="Help | NSFW", color=self.color)
        embed.description = """**```
• nsfw hass         | NSFW command
• nsfw hmidriff     | NSFW command
• nsfw pgif         | NSFW command
• nsfw 4k           | NSFW command
• nsfw holo         | NSFW command
• nsfw hneko        | NSFW command
• nsfw neko         | NSFW command
• nsfw hkitsune     | NSFW command
• nsfw kemonomimi   | NSFW command
• nsfw anal         | NSFW command
• nsfw hanal        | NSFW command
• nsfw gonewild     | NSFW command
• nsfw kanna        | NSFW command
• nsfw ass          | NSFW command
• nsfw pussy        | NSFW command
• nsfw thigh        | NSFW command
• nsfw hthigh       | NSFW command
• nsfw gah          | NSFW command
• nsfw coffee       | NSFW command
• nsfw food         | NSFW command
• nsfw paizuri      | NSFW command
• nsfw tentacle     | NSFW command
• nsfw boobs        | NSFW command
• nsfw hboobs       | NSFW command
• nsfw yaoi         | NSFW command
```**"""
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(configuration(client))
