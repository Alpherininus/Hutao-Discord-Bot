import os

import discord
from discord.ext import commands

# words
tem = ["hoi"]
badwordslist = ["k"]

# prefix
custom_prefixes = {}
default_prefixes = ['t?']


async def determine_prefix(bot, message):
    guild = message.guild
    if guild:
        return custom_prefixes.get(guild.id, default_prefixes)
    else:
        return default_prefixes


client = commands.Bot(case_insensitive=True, command_prefix=determine_prefix)


#######################################################################################################################

@client.event
async def on_message(message):
    if message.author.bot:
        return
    for badword in message.content.lower().split():
        if badword in badwordslist:
            await message.channel.send(f'Hey! {message.author.mention} ! Don\'t be a knecht!')
            await message.delete()
            print(f'{message.author} Said A Bad Word.')
            break

    for word in message.content.lower().split():
        if word in tem:
            await message.channel.send(f'**Hoi** <:TemmieSmug:868792284634820628> **!**')
            print(f'{message.author} Said A HOi.')
            break
    await client.process_commands(message)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        print(ctx.message.content, error)
        embed = discord.Embed(title="**ERROR** <a:emoji_21:856654949337006111>",
                              description=f'`{ctx.message.content}` | {ctx.author} Du kannst denn Command nochmal in `{round(error.retry_after, 2)} Sek` benutzen!',
                              colour=discord.Colour(0xff0000))
        await ctx.send(embed=embed, delete_after=120)
    if isinstance(error, commands.MissingRole):
        print(ctx.message.content, error)
        embed = discord.Embed(title="**ERROR** <a:emoji_21:856654949337006111>",
                              description=f'`{ctx.message.content}` | {ctx.author} Du hast nicht die benötigte Rolle!',
                              colour=discord.Colour(0xff0000))
        await ctx.send(embed=embed, delete_after=120)
    if isinstance(error, commands.BadArgument):
        print(ctx.message.content, error)
        embed = discord.Embed(title="**ERROR** <a:emoji_23:856655090239537173>",
                              description=f'`{ctx.message.content}` | {ctx.author} Falsche Argumente\r\n'
                                          f'{error}',
                              colour=discord.Colour(0xff0000))
        await ctx.send(embed=embed, delete_after=120)
    if isinstance(error, commands.MissingRequiredArgument):
        print(ctx.message.content, error)
        embed = discord.Embed(title="**ERROR** <a:emoji_23:856655090239537173>",
                              description=f'`{ctx.message.content}` | {ctx.author} Dir fehlen die benötigten Argumente um denn Command auszuführen zu können!\r\n'
                                          f'{error}',
                              colour=discord.Colour(0xff0000))
        await ctx.send(embed=embed, delete_after=120)
    if isinstance(error, commands.CheckFailure):
        print(ctx.message.content, error)
        embed = discord.Embed(title="**ERROR** <a:emoji_21:856654949337006111>",
                              description=f'`{ctx.message.content}` | {ctx.author} | {error}',
                              colour=discord.Colour(0xff0000))
        await ctx.send(embed=embed, delete_after=120)
    if isinstance(error, commands.MessageNotFound):
        print(ctx.message.content, error)
        embed = discord.Embed(title="**ERROR** <a:emoji_21:856654949337006111>",
                              description=f'`{ctx.message.content}` | {ctx.author} Keine Message gefunden!\r\n'
                                          f'{error}',
                              colour=discord.Colour(0xff0000))
        await ctx.send(embed=embed, delete_after=120)
    if isinstance(error, commands.CommandError):
        print(ctx.message.content, error)
        embed = discord.Embed(title="**ERROR** <a:emoji_23:856655090239537173>",
                              description=f'`{ctx.message.content}` | {ctx.author} Dieser Command existiert nicht!\r\n'
                                          f'{error}',
                              colour=discord.Colour(0xff0000))
        await ctx.send(embed=embed, delete_after=120)


@client.command()
@commands.guild_only()
async def setprefix(ctx, *, prefixes=""):
    custom_prefixes[ctx.guild.id] = prefixes.split() or default_prefixes
    await ctx.send(f"Prefixes set!")


@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    print(f'Prodokoll | {ctx.author} hat: Load eingegeben.')


@client.command()
async def unload(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    print(f'Prodokoll | {ctx.author} hat: Unload eingegeben.')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

#######################################################################################################################


client.run("###TOKEN###")
