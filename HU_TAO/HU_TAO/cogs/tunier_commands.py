import random

import discord
from discord.ext import commands

queue = []


class Anmeldung(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command(name='tunier/add', aliases=["t/a"])
    async def queue_(self, ctx, name):
        global queue

        queue.append(name)
        embed = discord.Embed(title="**Tunierliste**",
                              colour=discord.Colour(0x4fff))
        embed.add_field(name="Hinzugefügt:",
                        value=f"`{name}`",
                        inline=False)
        await ctx.send(embed=embed)

    @commands.command(name='tunier/remove', aliases=["t/r"])
    async def remove_(self, ctx, number):
        global queue
        try:
            del (queue[int(number)])
            embed = discord.Embed(title="**Tunierliste**",
                                  colour=discord.Colour(0x4fff))
            embed.add_field(name="Rausgenommen:",
                            value=f"Jetzt `{queue}`",
                            inline=False)
            await ctx.send(embed=embed)
        except:
            await ctx.send('Your queue is either **empty** or the index is **out of range**')

    @commands.command(name='tunier/liste', help='This command shows the queue', aliases=["t/l"])
    async def view_(self, ctx):
        embed = discord.Embed(title="**Tunierliste View**",
                              colour=discord.Colour(0x4fff))

        embed.add_field(name="Teilnehmer:",
                        value=f"`{', '.join(queue)}`",
                        inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="tunier/picker", aliases=["t/p"])
    async def tpicker(self, ctx):
        try:
            embed = discord.Embed(title="**Picker**",
                                  colour=discord.Colour(0x4fff))

            embed.add_field(name="Teilnehmer:",
                            value=f"{random.choice(queue)} gegen {random.choice(queue)}",
                            inline=False)
            await ctx.send(embed=embed)
        except:
            embed = discord.Embed(title="**ERROR** <:PaimonNani:824002466831925340>",
                                  description=f'Es sind keine Teilnehmer in der Liste',
                                  colour=discord.Colour(0xff06))
            await ctx.send(embed=embed)

    ###################################################################################################################


def setup(client):
    client.add_cog(Anmeldung(client))
