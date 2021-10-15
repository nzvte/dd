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
        self.aliases = {
            "anti-ban": "Anti Ban",
            "anti-kick": "Anti Kick",
            "anti-role-create": "Anti Role Creation",
            "anti-role-delete": "Anti Role Deletion",
            "anti-channel-create": "Anti Channel Creation",
            "anti-channel-delete": "Anti Channel Deletion",
            "anti-webhook-create": "Anti Webhook Creation"
        }

    @commands.command(name="punishment", description="Changes the punishment", usage="punishment [ban/kick]", aliases=["action"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def punishment(self, ctx, punishment):
        if not ctx.guild.owner.id == ctx.author.id:
            return await ctx.send(embed=discord.Embed(title="Missing Permissions", description="You must be the **`Server Owner`** to run this command", color=self.color))
        if punishment.lower() in ("kick", "ban"):
            await self.db.update_one(
                {
                    "guild": ctx.guild.id
                },
                {
                    "$set": {
                        "action": punishment.lower()
                    }
                }
            )
            return await ctx.send(embed=discord.Embed(title="Punishment | Success", description="Successfully changed the punishment to %s" % (punishment), color=self.color))
        else:
            return await ctx.send(embed=discord.Embed(title="Punishment | Failed", description="Invalid punishment, you can either change it to `ban` or `kick`", color=self.color))

    @commands.group(invoke_without_command=True, name="whitelist", description="Shows whitelist menu", usage="whitelist", aliases=["wl"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def whitelist(self, ctx):
        if not ctx.guild.owner.id == ctx.author.id:
            return await ctx.send(embed=discord.Embed(title="Missing Permissions", description="You must be the **`Server Owner`** to run this command", color=self.color))
        embed = discord.Embed(title="Whitelist | Help", color=self.color)
        embed.add_field(name="usage", value="— `%swhitelisted` - Shows all the current users in the whitelist\n— `%swhitelist add <user>` - Adds a user to the whitelist\n— `%swhitelist remove <user>` - Removes a user from the whitelist" % (ctx.prefix, ctx.prefix, ctx.prefix), inline=False)
        embed.add_field(name="description", value="— `Warning` - By whitelisting a user the bot will completely ignore all the users actions. This may allow the user to nuke or make changes to your server", inline=False)
        embed.add_field(name="permissions", value="— `Server Owner` - You must have server ownership to use this group of commands", inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="whitelisted", description="Shows whitelisted users", usage="whitelisted", aliases=["wls"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def whitelisted(self, ctx):
        if not ctx.guild.owner.id == ctx.author.id:
            return await ctx.send(embed=discord.Embed(title="Missing Permissions", description="You must be the **`Server Owner`** to run this command", color=self.color))
        data = await self.db.find_one({"guild": ctx.guild.id})
        whitelist = data["whitelisted"]
        embed = discord.Embed(title="Whitelisted", color=self.color)
        embed.description = "```"
        for id in whitelist:
            user = self.client.get_user(id)
            embed.description += "— %s (%s)\n" % (user, user.id)
        if embed.description == "```":
            embed.description += "No users inside the whitelist"
        embed.description += "```"
        await ctx.send(embed=embed)

    @whitelist.command(name="add", description="Add user to whitelist", usage="whitelist add [user]", aliases=["a"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def add_whitelist(self, ctx, user: discord.Member):
        if not ctx.guild.owner.id == ctx.author.id:
            return await ctx.send(embed=discord.Embed(title="Missing Permissions", description="You must be the **`Server Owner`** to run this command", color=self.color))
        await self.db.update_one(
            {
                "guild": ctx.guild.id
            },
            {
                "$push": {
                    "whitelisted": user.id
                }
            }
        )
        await ctx.send(embed=discord.Embed(title="Whitelist | Add", description="Successfully added %s to the guilds whitelist" % (user), color=self.color))

    @whitelist.command(name="remove", description="Remove user from whitelist", usage="whitelist remove [user]", aliases=["r"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def remove_whitelist(self, ctx, user: discord.Member):
        if not ctx.guild.owner.id == ctx.author.id:
            return await ctx.send(embed=discord.Embed(title="Missing Permissions", description="You must be the **`Server Owner`** to run this command", color=self.color))
        await self.db.update_one(
            {
                "guild": ctx.guild.id
            },
            {
                "$pull": {
                    "whitelisted": user.id
                }
            }
        )
        await ctx.send(embed=discord.Embed(title="Whitelist | Remove", description="Successfully removed %s from the guilds whitelist" % (user), color=self.color))

    @commands.group(invoke_without_command=True, name="config", description="Shows config menu", usage="config")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def config(self, ctx):
        if not ctx.guild.owner.id == ctx.author.id:
            return await ctx.send(embed=discord.Embed(title="Missing Permissions", description="You must be the **`Server Owner`** to run this command", color=self.color))
        embed = discord.Embed(title="Config | Help", color=self.color)
        embed.add_field(name="usage", value="— `%sconfig status` - Shows all the event status\n— `%sconfig enable <module>` - Enables the specified module\n— `%sconfig disable <module>`" % (ctx.prefix, ctx.prefix, ctx.prefix), inline=False)
        embed.add_field(name="description", value="— `Warning` - Enabling or disabling modules may leave your server in danger of nukers ", inline=False)
        embed.add_field(name="permissions", value="— `Server Owner` - You must have server ownership to use this group of commands", inline=False)
        embed.add_field(name="modules", value="— `anti-ban`\n— `anti-kick`\n— `anti-role-create`\n— `anti-role-delete`\n— `anti-role-create`\n— `anti-channel-create`\n— `anti-channel-delete`\n— `anti-webhook-create`", inline=False)
        await ctx.send(embed=embed)

    @config.command(name="status", description="Shows module status", usage="config status", aliases=["stat"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def status(self, ctx):
        if not ctx.guild.owner.id == ctx.author.id:
            return await ctx.send(embed=discord.Embed(title="Missing Permissions", description="You must be the **`Server Owner`** to run this command", color=self.color))
        data = await self.db.find_one({"guild": ctx.guild.id})
        embed = discord.Embed(title="Config | Status", color=self.color)
        for module in self.aliases:
            status = data["events"][module]
            if status == True:
                status = "Enabled"
            else:
                status = "Disabled"
            embed.add_field(name="%s" % (self.aliases.get(module)), value="— `%s`" % (status), inline=False)
        await ctx.send(embed=embed)
    
    @config.command(name="enable", description="Enables a module", usage="config enable [module]")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def enable(self, ctx, module):
        if not ctx.guild.owner.id == ctx.author.id:
            return await ctx.send(embed=discord.Embed(title="Missing Permissions", description="You must be the **`Server Owner`** to run this command", color=self.color))
        if not module in self.aliases:
            return await ctx.send(embed=discord.Embed(title="Invalid Module", description="The specified module is invalid", color=self.color))
        data = await self.db.find_one({"guild": ctx.guild.id})
        status = data["events"][module]
        if status == True:
            return await ctx.send(embed=discord.Embed(title="Enable | Config", description="**`%s`** is already enabled" % (module), color=self.color))
        else:
            await self.db.update_one(
                {
                    "guild": ctx.guild.id
                },
                {
                    "$set": {
                        "events.%s" % (module): True
                    }
                }
            )
            return await ctx.send(embed=discord.Embed(title="Enable | Config", description="Successfully enabled module", color=self.color))

    @config.command(name="disable", description="Disables a module", usage="config disable [module]")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def disable(self, ctx, module):
        if not ctx.guild.owner.id == ctx.author.id:
            return await ctx.send(embed=discord.Embed(title="Missing Permissions", description="You must be the **`Server Owner`** to run this command", color=self.color))
        if not module in self.aliases:
            return await ctx.send(embed=discord.Embed(title="Invalid Module", description="The specified module is invalid", color=self.color))
        data = await self.db.find_one({"guild": ctx.guild.id})
        status = data["events"][module]
        if status == False:
            return await ctx.send(embed=discord.Embed(title="Disable | Config", description="**`%s`** is already disabled" % (module), color=self.color))
        else:
            await self.db.update_one(
                {
                    "guild": ctx.guild.id
                },
                {
                    "$set": {
                        "events.%s" % (module): False
                    }
                }
            )
            return await ctx.send(embed=discord.Embed(title="Disable | Config", description="Successfully disabled module", color=self.color))

    @commands.group(invoke_without_command=True, name="log", description="Shows the log menu", usage="log")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def log(self, ctx):
        embed = discord.Embed(title="Log | Help", color=self.color)
        embed.add_field(name="usage", value="— log set <channel>\n— log remove", inline=False)
        embed.add_field(name="description", value="— `log set` - Will set the specified channel as the log channel\n— `log remove` - Will remove the log channel", inline=False)
        embed.add_field(name="permissions", value="— `log set` - Requires you to have administrator permissions\n— `log remove` - Requires you to have administrator permissions", inline=False)
        await ctx.send(embed=embed)

    @log.command(name="set", description="Sets the log channel", usage="log set [channel]")
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def log_set(self, ctx, channel: discord.TextChannel):
        await self.db.update_one(
            {
                "guild": ctx.guild.id
            },
            {
                "$set": {
                    "log-channel": channel.id
                }
            }
        )
        await ctx.send(embed=discord.Embed(title="Set | Log", description="Successfully set the log channel to **`%s`**" % (channel.name), color=self.color))

    @log.command(name="remove", description="Removes logging", usage="log remove")
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def log_remove(self, ctx):
        await self.db.update_one(
            {
                "guild": ctx.guild.id
            },
            {
                "$set": {
                    "log-channel": None
                }
            }
        )
        await ctx.send(embed=discord.Embed(title="Remove | Log", description="Successfully removed the log channel", color=self.color))

    @commands.group(invoke_without_command=True, name="prefix", description="Shows prefix menu", usage="prefix")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def prefix(self, ctx):
        embed = discord.Embed(title="Prefix | Help", color=self.color)
        embed.add_field(name="usage", value="— prefix set <prefix>", inline=False)
        embed.add_field(name="description", value="— `prefix set` - Will set the event action to the specified action", inline=False)
        embed.add_field(name="permissions", value="— `prefix set` - Requires you to have administrator permissions", inline=False)
        await ctx.send(embed=embed)

    @prefix.command(name="set", description="Sets the prefix", usage="prefix set [prefix]")
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def set_prefix(self, ctx, prefix):
        await self.db.update_one(
            {
                "guild": ctx.guild.id
            },
            {
                "$set": {
                    "prefix": prefix
                }
            }
        )
        await ctx.send(embed=discord.Embed(title="Set | Prefix", description="Successfully set the prefix to **`%s`**" % (prefix), color=self.color))

def setup(client):
    client.add_cog(configuration(client))
