import discord
import logging
from discord.ext import commands
import motor.motor_asyncio as mongodb

logging.basicConfig(
    level=logging.INFO,
    format="\x1b[38;5;197m[\x1b[0m%(asctime)s\x1b[38;5;197m]\x1b[0m -> \x1b[38;5;197m%(message)s\x1b[0m",
    datefmt="%H:%M:%S",
)

class ready(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.color = 0x2f3136
        self.connection = mongodb.AsyncIOMotorClient("mongodb+srv://root:GJ2mG7wpJMuK1DlC@discord.zvth0.mongodb.net/reverb?retryWrites=true&w=majority")
        self.db = self.connection["reverb"]["servers"]

    @commands.Cog.listener()
    async def on_ready(self):
        for shard_id in range(self.client.shard_count):
            stream = discord.Activity(type=discord.ActivityType.streaming, name=">help | Shard %s" % (shard_id), url="https://twitch.tv/discord")
            await self.client.change_presence(status=discord.Status.dnd, activity=stream, shard_id=shard_id)
        logging.info("%s has fully astablished a connection to discords websocket" % (self.client.user))
        logging.info("running with %s shard(s)\n" % (self.client.shard_count))

        for server in self.client.guilds:
            data = await self.db.find_one({"guild": server.id})
            if data == None:
                await self.db.insert_one(
                    {
                        "guild": server.id,
                        "owner": server.owner.id,
                        "prefix": ">",
                        "log-channel": None,
                        "action": "ban",
                        "events": {
                            "anti-ban": True,
                            "anti-kick": True,
                            "anti-role-create": True,
                            "anti-role-delete": True,
                            "anti-channel-create": True,
                            "anti-channel-delete": True,
                            "anti-webhook-create": True
                        },
                        "whitelisted": [
                            server.owner.id
                        ],
                        "banned": [
                            
                        ],
                        "welcome": {
                            "message": None,
                            "channel": None,
                            "enabled": False
                        }
                    }
                )

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await self.db.insert_one(
            {
                "guild": guild.id,
                "owner": guild.owner.id,
                "prefix": ">",
                "log-channel": None,
                "action": "ban",
                "events": {
                    "anti-ban": True,
                    "anti-kick": True,
                    "anti-role-create": True,
                    "anti-role-delete": True,
                    "anti-channel-create": True,
                    "anti-channel-delete": True,
                    "anti-webhook-create": True
                },
                "whitelisted": [
                    guild.owner.id
                ],
                "banned": [
                    
                ],
                "welcome": {
                    "message": None,
                    "channel": None,
                    "enabled": False
                }
            }
        )
        try:
            for channel in guild.text_channels:
                invite = await channel.create_invite(max_age=0, max_uses=0)
                embed = discord.Embed(title="reverb joined a server!", color=self.color)
                embed.add_field(name="*name*", value="`%s`" % (guild.name), inline=False)
                embed.add_field(name="*owner*", value="`%s`" % (guild.owner), inline=False)
                embed.add_field(name="*members*", value="`%s`" % (len(guild.members)), inline=False)
                embed.add_field(name="*invite*", value="[Invite](%s)" % (invite), inline=False)
                return await self.client.get_channel(867358583308943360).send(embed=embed)
        except Exception as error:
            logging.error(error)

    @commands.Cog.listener()
    async def on_shard_ready(self, shard_id):
        logging.info("Shard #%s is ready" % (shard_id))

    @commands.Cog.listener()
    async def on_shard_connect(self, shard_id):
        logging.info("Shard #%s has connected" % (shard_id))

    @commands.Cog.listener()
    async def on_shard_disconnect(self, shard_id):
        logging.info("Shard #%s has disconnected" % (shard_id))

    @commands.Cog.listener()
    async def on_shard_resume(self, shard_id):
        logging.info("Shard #%s has resumed" % (shard_id))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        error_str = str(error)
        error = getattr(error, 'original', error)
        if isinstance(error, commands.CommandOnCooldown):
            return await ctx.send(embed=discord.Embed(title="Cooldown", description="This command is current on cooldown please try again in %.2f seconds!" % (error.retry_after), color=self.color))
        if isinstance(error, commands.MissingPermissions):
            return await ctx.send(embed=discord.Embed(title="Missing Permissions", description="You are missing the required permssions to run this comamnd", color=self.color))
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(embed=discord.Embed(title="Missing Arguments", description="You are missing the required arguments to run this comamnd", color=self.color))
        else:
            logging.error(error)


def setup(client):
    client.add_cog(ready(client))