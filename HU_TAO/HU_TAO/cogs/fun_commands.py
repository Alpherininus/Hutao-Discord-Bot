import random

import discord
from discord.ext import commands

queue = []

antworten = ['Ja', 'Nein']

gold = ['1808', 'Alles', '292', '300', '4129', '50', '68', '79', '809', 'Alles', '190', '41', '99', '455', 'kein']


class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["howhot", "hot"])
    async def hotcalc(self, ctx, *, user: discord.Member = None):
        user = user or ctx.author

        random.seed(user.id)
        r = random.randint(1, 100)
        hot = r / 1.17

        if hot > 25:
            emoji = "❤"
        elif hot > 50:
            emoji = "💖"
        elif hot > 75:
            emoji = "💞"
        else:
            emoji = "💔"

        await ctx.send(f"**{user.name}** is **{hot:.2f}%** hot {emoji}")

    #######################################################################################

    @commands.command(help='BAGUETTE')
    async def baguette(self, ctx):
        await ctx.send(
            '<a:BaguetteMarch:824002940330836008><a:BaguetteMarch:824002940330836008><a:BaguetteMarch:824002940330836008><a:BaguetteMarch:824002940330836008><a:BaguetteMarch:824002940330836008>')
        await ctx.message.delete()


def setup(client):
    client.add_cog(Fun(client))