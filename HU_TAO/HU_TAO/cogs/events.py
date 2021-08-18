import asyncio

import discord
from discord.ext import commands


class Events(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Start | Login {self.client.user}")
        await asyncio.sleep(3)
        print(f"Start | Done {self.client.latency * 1000:,.0f}ms")
        self.client.remove_command("help")

        servers = len(self.client.guilds)
        members = 0
        for guild in self.client.guilds:
            members += guild.member_count - 1
        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                                    name=f'{servers} servers {members} members'))


def setup(client):
    client.add_cog(Events(client))
