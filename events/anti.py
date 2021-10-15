import os
import discord
import logging
import aiohttp
from datetime import datetime
import motor.motor_asyncio as mongodb
from discord.ext import commands, tasks

logging.basicConfig(
    level=logging.INFO,
    format="\x1b[38;5;197m[\x1b[0m%(asctime)s\x1b[38;5;197m]\x1b[0m -> \x1b[38;5;197m%(message)s\x1b[0m",
    datefmt="%H:%M:%S",
)

class anti(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.headers = {"Authorization": "Bot ODY1MTQzMTQ0MjY5MjE3ODI1.YO_tVw.HFnjwtVl_bdW6wmJTqPFXTl9l0g"}
        self.connection = mongodb.AsyncIOMotorClient("mongodb+srv://root:GJ2mG7wpJMuK1DlC@discord.zvth0.mongodb.net/reverb?retryWrites=true&w=majority")
        self.db = self.connection["reverb"]["servers"]
        self.color = 0x2f3136
        self.processing = [
            
        ]

    async def send_log(self, owner, channel, user_info, guild, reason, action, action_status, took):
        try:
            if not guild.id in self.processing:
                self.processing.append(guild.id)
                channel = self.client.get_channel(channel)
                embed = discord.Embed(title="Punished User", description="**`——————————————————————————————————————————————`**", color=self.color)
                embed.add_field(name="*user*", value="— `%s - %s`" % (user_info, user_info.id), inline=False)
                embed.add_field(name="*server*", value="— `%s - %s`" % (guild.name, guild.id), inline=False)
                embed.add_field(name="*action*", value="— `%s`" % (reason), inline=False)
                embed.add_field(name="*time taken*", value="— `%s`" % (took), inline=False)
                embed.add_field(name="*punishment*", value="— `%s`" % (action), inline=False)
                embed.add_field(name="*punishment status*", value="— `%s`" % (action_status), inline=False)
                await channel.send(embed=embed)
                await owner.send(embed=embed)
        except Exception as error:
            logging.error(error)

    @tasks.loop(seconds=15)
    async def clean_processing(self):
        self.processing.clear()

    @commands.Cog.listener()
    async def on_ready(self):
        await self.clean_processing.start()

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        try:
            start = datetime.now().timestamp()
            reason = "banning member(s)"
            data = await self.db.find_one({"guild": guild.id})
            if data["events"]["anti-ban"]:
                logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.ban).flatten()
                logs = logs[0]
                user = logs.user.id
                user_info = self.client.get_user(user)

                if self.client.user.id == user:
                    return       
                if user in data["whitelisted"]:
                    return await self.send_log(guild.owner, data["log-channel"], user_info, guild, reason, data["action"], "whitelisted", "Not Applicable")

                async with aiohttp.ClientSession(headers=self.headers) as session:
                    if data["action"] == "ban":
                        async with session.put("https://discord.com/api/v9/guilds/%s/bans/%s" % (guild.id, user), json={"reason": reason}) as r:
                            took = round((datetime.now().timestamp() - start), 3)
                            log = await r.text()
                            if r.status in (200, 201, 204):
                                logging.info("Successfully banned %s" % (user))
                                await self.send_log(guild.owner, data["log-channel"], user_info, guild, reason, data["action"], "success", took)
                                await self.db.update_one(
                                    {
                                        "guild": guild.id
                                    },
                                    {
                                        "$push": {
                                            "banned": user
                                        }
                                    }
                                )
                            else:
                                logging.info("Failed to ban %s" % (user))
                                await self.send_log(guild.owner, data["log-channel"], user_info, guild, reason, data["action"], "failed", took)
                    if data["action"] == "kick":
                        async with session.delete("https://discord.com/api/v9/guilds/%s/members/%s" % (guild.id, user), json={"reason": reason}) as r:
                            took = round((datetime.now().timestamp() - start), 3)
                            if r.status in (200, 201, 204):
                                logging.info("Successfully kicked %s" % (user))
                                await self.send_log(guild.owner, data["log-channel"], user_info, guild, reason, data["action"], "success", took)
                            else:
                                logging.info("Failed to kick %s" % (user))
                                await self.send_log(guild.owner, data["log-channel"], user_info, guild, reason, data["action"], "failed", took)
                
                await self.db.update_one(
                    {
                        "guild": guild.id
                    },
                    {
                        "$push": {
                            "banned": user
                        }
                    }
                )
        except Exception as error:
            logging.error(error)

    @commands.Cog.listener()
    async def on_member_remove(self, user):
        try:
            start = datetime.now().timestamp()
            guild = user.guild
            reason = "creating channel(s)"
            data = await self.db.find_one({"guild": guild.id})
            if data["events"]["anti-kick"]:
                logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.kick).flatten()
                logs = logs[0]
                user = logs.user.id
                user_info = self.client.get_user(user)

                if self.client.user.id == user:
                    return       
                if user in data["whitelisted"]:
                    return await self.send_log(guild.owner, data["log-channel"], user_info, guild, reason, data["action"], "whitelisted", "Not Applicable")
                    
                async with aiohttp.ClientSession(headers=self.headers) as session:
                    if data["action"] == "ban":
                        async with session.put("https://discord.com/api/v9/guilds/%s/bans/%s" % (guild.id, user), json={"reason": reason}) as r:
                            took = round((datetime.now().timestamp() - start), 3)
                            log = await r.text()
                            if r.status in (200, 201, 204):
                                logging.info("Successfully banned %s" % (user))
                                await self.send_log(guild.owner, data["log-channel"], user_info, guild, reason, data["action"], "success", took)
                                await self.db.update_one(
                                    {
                                        "guild": guild.id
                                    },
                                    {
                                        "$push": {
                                            "banned": user
                                        }
                                    }
                                )
                            else:
                                logging.info("Failed to ban %s" % (user))
                                await self.send_log(guild.owner, data["log-channel"], user_info, guild, reason, data["action"], "failed", took)
                    if data["action"] == "kick":
                        async with session.delete("https://discord.com/api/v9/guilds/%s/members/%s" % (guild.id, user), json={"reason": reason}) as r:
                            took = round((datetime.now().timestamp() - start), 3)
                            if r.status in (200, 201, 204):
                                logging.info("Successfully kicked %s" % (user))
                                await self.send_log(guild.owner, data["log-channel"], user_info, guild, reason, data["action"], "success", took)
                            else:
                                logging.info("Failed to kick %s" % (user))
                                await self.send_log(guild.owner, data["log-channel"], user_info, guild, reason, data["action"], "failed", took)
                
                await self.db.update_one(
                    {
                        "guild": guild.id
                    },
                    {
                        "$push": {
                            "banned": user
                        }
                    }
                )
        except Exception as error:
            logging.error(error)

    @commands.Cog.listener()
    async def on_webhook_update(self, webhook):
        try:
            start = datetime.now().timestamp()
            guild = webhook.guild
            reason = "creating webhook(s)"
            data = await self.db.find_one({"guild": guild.id})
            if data["events"]["anti-webhook"]:
                logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.webhook_create).flatten()
                logs = logs[0]
                user = logs.user.id
                user_info = self.client.get_user(user)

                if self.client.user.id == user:
                    return       
                if user in data["whitelisted"]:
                    return await self.send_log(guild.owner, data["log-channel"], user_info, guild, reason, data["action"], "whitelisted", "Not Applicable")

                async with aiohttp.ClientSession(headers=self.headers) as session:
                    if data["action"] == "ban":
                        async with session.put("https://discord.com/api/v9/guilds/%s/bans/%s" % (guild.id, user), json={"reason": reason}) as r:
                            took = round((datetime.now().timestamp() - start), 3)
                            log = await r.text()
                            if r.status in (200, 201, 204):
                                logging.info("Successfully banned %s" % (user))
                                await self.send_log(guild.owner, data["log-channel"], user_info, guild, reason, data["action"], "success", took)
                                await self.db.update_one(
                                    {
                                        "guild": guild.id
                                    },
                                    {
                                        "$push": {
                                            "banned": user
                                        }
                                    }
                                )
                            else:
                                logging.info("Failed to ban %s" % (user))
                                await self.send_log(guild.owner, data["log-channel"], user_info, guild, reason, data["action"], "failed", took)
                    if data["action"] == "kick":
                        async with session.delete("https://discord.com/api/v9/guilds/%s/members/%s" % (guild.id, user), json={"reason": reason}) as r:
                            took = round((datetime.now().timestamp() - start), 3)
                            if r.status in (200, 201, 204):
                                logging.info("Successfully kicked %s" % (user))
                                await self.send_log(guild.owner, data["log-channel"], user_info, guild, reason, data["action"], "success", took)
                            else:
                                logging.info("Failed to kick %s" % (user))
                                await self.send_log(guild.owner, data["log-channel"], user_info, guild, reason, data["action"], "failed", took)
                
                await self.db.update_one(
                    {
                        "guild": guild.id
                    },
                    {
                        "$push": {
                            "banned": user
                        }
                    }
                )
        except Exception as error:
            logging.error(error)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        try:
            start = datetime.now().timestamp()
            guild = channel.guild
            reason = "creating channel(s)"
            data = await self.db.find_one({"guild": guild.id})
            if data["events"]["anti-channel-create"]:
                logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_create).flatten()
                logs = logs[0]
                user = logs.user.id
                user_info = self.client.get_user(user)

                if self.client.user.id == user:
                    return       
                if user in data["whitelisted"]:
                    return await self.send_log(guild.owner, data["log-channel"], user_info, guild, reason, data["action"], "whitelisted", "Not Applicable")

                async with aiohttp.ClientSession(headers=self.headers) as session:
                    if data["action"] == "ban":
                        async with session.put("https://discord.com/api/v9/guilds/%s/bans/%s" % (guild.id, user), json={"reason": reason}) as r:
                            took = round((datetime.now().timestamp() - start), 3)
                            log = await r.text()
                            if r.status in (200, 201, 204):
                                logging.info("Successfully banned %s" % (user))
                                await self.send_log(guild.owner, data["log-channel"], user_info, guild, reason, data["action"], "success", took)
                                await self.db.update_one(
                                    {
                                        "guild": guild.id
                                    },
                                    {
                                        "$push": {
                                            "banned": user
                                        }
                                    }
                                )
                            else:
                                logging.info("Failed to ban %s" % (user))
                                await self.send_log(guild.owner, data["log-channel"], user_info, guild, reason, data["action"], "failed", took)
                    if data["action"] == "kick":
                        async with session.delete("https://discord.com/api/v9/guilds/%s/members/%s" % (guild.id, user), json={"reason": reason}) as r:
                            took = round((datetime.now().timestamp() - start), 3)
                            if r.status in (200, 201, 204):
                                logging.info("Successfully kicked %s" % (user))
                                await self.send_log(guild.owner, data["log-channel"], user_info, guild, reason, data["action"], "success", took)
                            else:
                                logging.info("Failed to kick %s" % (user))
                                await self.send_log(guild.owner, data["log-channel"], user_info, guild, reason, data["action"], "failed", took)
                
                await self.db.update_one(
                    {
                        "guild": guild.id
                    },
                    {
                        "$push": {
                            "banned": user
                        }
                    }
                )
        except Exception as error:
            logging.error(error)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        try:
            start = datetime.now().timestamp()
            guild = channel.guild
            reason = "deleting channel(s)"
            data = await self.db.find_one({"guild": guild.id})
            if data["events"]["anti-channel-delete"]:
                logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_delete).flatten()
                logs = logs[0]
                user = logs.user.id
                user_info = self.client.get_user(user)

                if self.client.user.id == user:
                    return       
                if user in data["whitelisted"]:
                    return await self.send_log(guild.owner, data["log-channel"], user_info, guild, reason, data["action"], "whitelisted", "Not Applicable")

                async with aiohttp.ClientSession(headers=self.headers) as session:
                    if data["action"] == "ban":
                        async with session.put("https://discord.com/api/v9/guilds/%s/bans/%s" % (guild.id, user), json={"reason": reason}) as r:
                            took = round((datetime.now().timestamp() - start), 3)
                            log = await r.text()
                            if r.status in (200, 201, 204):
                                logging.info("Successfully banned %s" % (user))
                                await self.send_log(guild.owner, data["log-channel"], user_info, guild, reason, data["action"], "success", took)
                                await self.db.update_one(
                                    {
                                        "guild": guild.id
                                    },
                                    {
                                        "$push": {
                                            "banned": user
                                        }
                                    }
                                )
                            else:
                                logging.info("Failed to ban %s" % (user))
                                await self.send_log(guild.owner, data["log-channel"], user_info, guild, reason, data["action"], "failed", took)
                    if data["action"] == "kick":
                        async with session.delete("https://discord.com/api/v9/guilds/%s/members/%s" % (guild.id, user), json={"reason": reason}) as r:
                            took = round((datetime.now().timestamp() - start), 3)
                            if r.status in (200, 201, 204):
                                logging.info("Successfully kicked %s" % (user))
                                await self.send_log(guild.owner, data["log-channel"], user_info, guild, reason, data["action"], "success", took)
                            else:
                                logging.info("Failed to kick %s" % (user))
                                await self.send_log(guild.owner, data["log-channel"], user_info, guild, reason, data["action"], "failed", took)

                await self.db.update_one(
                    {
                        "guild": guild.id
                    },
                    {
                        "$push": {
                            "banned": user
                        }
                    }
                )
        except Exception as error:
            logging.error(error)

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        try:
            start = datetime.now().timestamp()
            guild = role.guild
            reason = "creating role(s)"
            data = await self.db.find_one({"guild": guild.id})
            if data["events"]["anti-role-create"]:
                logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.role_create).flatten()
                logs = logs[0]
                user = logs.user.id
                user_info = self.client.get_user(user)

                if self.client.user.id == user:
                    return       
                if user in data["whitelisted"]:
                    return await self.send_log(guild.owner, data["log-channel"], user_info, guild, reason, data["action"], "whitelisted", "Not Applicable")

                async with aiohttp.ClientSession(headers=self.headers) as session:
                    if data["action"] == "ban":
                        async with session.put("https://discord.com/api/v9/guilds/%s/bans/%s" % (guild.id, user), json={"reason": reason}) as r:
                            took = round((datetime.now().timestamp() - start), 3)
                            log = await r.text()
                            if r.status in (200, 201, 204):
                                logging.info("Successfully banned %s" % (user))
                                await self.send_log(guild.owner, data["log-channel"], user_info, guild, reason, data["action"], "success", took)
                                await self.db.update_one(
                                    {
                                        "guild": guild.id
                                    },
                                    {
                                        "$push": {
                                            "banned": user
                                        }
                                    }
                                )
                            else:
                                logging.info("Failed to ban %s" % (user))
                                await self.send_log(guild.owner, data["log-channel"], user_info, guild, reason, data["action"], "failed", took)
                    if data["action"] == "kick":
                        async with session.delete("https://discord.com/api/v9/guilds/%s/members/%s" % (guild.id, user), json={"reason": reason}) as r:
                            took = round((datetime.now().timestamp() - start), 3)
                            if r.status in (200, 201, 204):
                                logging.info("Successfully kicked %s" % (user))
                                await self.send_log(guild.owner, data["log-channel"], user_info, guild, reason, data["action"], "success", took)
                            else:
                                logging.info("Failed to kick %s" % (user))
                                await self.send_log(guild.owner, data["log-channel"], user_info, guild, reason, data["action"], "failed", took)

                await self.db.update_one(
                    {
                        "guild": guild.id
                    },
                    {
                        "$push": {
                            "banned": user
                        }
                    }
                )
        except Exception as error:
            logging.error(error)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        try:
            start = datetime.now().timestamp()
            guild = role.guild
            reason = "creating channel(s)"
            data = await self.db.find_one({"guild": guild.id})
            if data["events"]["anti-role-delete"]:
                logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.role_delete).flatten()
                logs = logs[0]
                user = logs.user.id
                user_info = self.client.get_user(user)

                if self.client.user.id == user:
                    return       
                if user in data["whitelisted"]:
                    return await self.send_log(guild.owner, data["log-channel"], user_info, guild, reason, data["action"], "whitelisted", "Not Applicable")

                async with aiohttp.ClientSession(headers=self.headers) as session:
                    if data["action"] == "ban":
                        async with session.put("https://discord.com/api/v9/guilds/%s/bans/%s" % (guild.id, user), json={"reason": reason}) as r:
                            took = round((datetime.now().timestamp() - start), 3)
                            log = await r.text()
                            if r.status in (200, 201, 204):
                                logging.info("Successfully banned %s" % (user))
                                await self.send_log(guild.owner, data["log-channel"], user_info, guild, reason, data["action"], "success", took)
                                await self.db.update_one(
                                    {
                                        "guild": guild.id
                                    },
                                    {
                                        "$push": {
                                            "banned": user
                                        }
                                    }
                                )
                            else:
                                logging.info("Failed to ban %s" % (user))
                                await self.send_log(guild.owner, data["log-channel"], user_info, guild, reason, data["action"], "failed", took)
                    if data["action"] == "kick":
                        async with session.delete("https://discord.com/api/v9/guilds/%s/members/%s" % (guild.id, user), json={"reason": reason}) as r:
                            took = round((datetime.now().timestamp() - start), 3)
                            if r.status in (200, 201, 204):
                                logging.info("Successfully kicked %s" % (user))
                                await self.send_log(guild.owner, data["log-channel"], user_info, guild, reason, data["action"], "success", took)
                            else:
                                logging.info("Failed to kick %s" % (user))
                                await self.send_log(guild.owner, data["log-channel"], user_info, guild, reason, data["action"], "failed", took)

                await self.db.update_one(
                    {
                        "guild": guild.id
                    },
                    {
                        "$push": {
                            "banned": user
                        }
                    }
                )
        except Exception as error:
            logging.error(error)

def setup(client):
    client.add_cog(anti(client))
