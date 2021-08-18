import datetime
import json
import os
import typing

import discord
from discord.ext import commands

#######################################################################################################################

author_msg_times = {}
# Struct:
# {
#    "<author_id>": ["<msg_time", "<msg_time>", ...],
#    "<author_id>": ["<msg_time"],
# }

with open('config.json') as configFile:
    data = json.load(configFile)
    for value in data["details"]:
        bot_token = value['token']
    for value in data["details"]:
        prefix = value['prefix']

    for value in data["words"]:
        tem = value['tem']

    for value in data["antispam"]:
        time_window_milliseconds = value['timewm']
    for value in data["antispam"]:
        max_msg_per_window = value["msgpw"]
    for value in data["antispam"]:
        deletepw = value["delete"]

client = commands.Bot(command_prefix=commands.when_mentioned_or(prefix))


#######################################################################################################################

@client.event
async def on_message(ctx, amount: int = deletepw):
    if ctx.channel.id == 836676954295763055:
        return

    if ctx.author.bot:
        return
    for word in ctx.content.lower().split():
        if word in tem:
            await ctx.channel.send(f'**Hoi** <:TemmieSmug:868792284634820628> **!**')
            print(f'{ctx.author} Said A HOi.')
            break

    # antispam
    # time_window_milliseconds = 5000
    # max_msg_per_window = 5
    global author_msg_counts

    author_id = ctx.author.id
    curr_time = datetime.datetime.now().timestamp() * 1000
    if not author_msg_times.get(author_id, False):
        author_msg_times[author_id] = []
    author_msg_times[author_id].append(curr_time)
    expr_time = curr_time - time_window_milliseconds
    expired_msgs = [
        msg_time for msg_time in author_msg_times[author_id]
        if msg_time < expr_time
    ]
    for msg_time in expired_msgs:
        author_msg_times[author_id].remove(msg_time)

    if len(author_msg_times[author_id]) > max_msg_per_window:
        await ctx.channel.purge(limit=amount)
        print(f"{ctx.author} Spamt in {ctx.channel}")

        spam = discord.Embed(title="**SPAM!**", description=f"Stop Spamming | {amount} Words Deleted",
                             color=discord.Colour.random())
        await ctx.channel.send(embed=spam)
        #

        await client.process_commands(ctx)


#######################################################################################################################

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')


@client.command()
async def unload(ctx, extension):
    client.load_extension(f'cogs.{extension}')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

#######################################################################################################################


client.run(bot_token)
