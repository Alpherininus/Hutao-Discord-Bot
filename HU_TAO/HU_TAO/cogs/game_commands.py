import asyncio
import random

import discord

from discord.ext import commands


class GameCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["slots", "bet"])
    @commands.cooldown(rate=1, per=3.0, type=commands.BucketType.user)
    async def slot(self, ctx):
        emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
        a = random.choice(emojis)
        b = random.choice(emojis)
        c = random.choice(emojis)

        slotmachine = f"**[ {a} {b} {c} ]\n{ctx.author.name}**,"

        if (a == b == c):
            await ctx.send(f"{slotmachine} All matching, you won! 🎉")
        elif (a == b) or (a == c) or (b == c):
            await ctx.send(f"{slotmachine} 2 in a row, you won! 🎉")
        else:
            await ctx.send(f"{slotmachine} No match, you lost 😢")

    @commands.command(name='8ball', help='a Magic Ball')
    async def game_command(self, ctx, *, frage):
        mess = await ctx.channel.send(f'Ich versuche deine Frage `{frage}` zu beantworten.')
        await asyncio.sleep(2)
        await mess.edit(content='Ich kontaktiere das Orakel...<:Primogem:824002465673510980>')
        await asyncio.sleep(2)
        await mess.edit(content=f'Deine Antwort zur Frage `{frage}` lautet: `{antworten}`')
        await mess.add_reaction('<:PaimonNani:824002466831925340>')


def setup(client):
    client.add_cog(GameCommands(client))
