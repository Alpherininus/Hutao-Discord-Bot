import random

import discord
from discord.ext import commands
from discord.ext.commands import Greedy

zahl = ["1", "2", "3", "4", "5", "6", "7", "8"]

spam = ["SPAMING", "(:"]

weapon = ["AK47", "Speer", "Bogen", "Schwert", "Buch", "2Händer", "Magie", "Keule", "Heu", "Straw", "bow", "spear"]

antworten = ["ja", "nein", "definitv", "Ich bin mir nicht sicher"]

prefix = "t?"

gold = ['1808', 'Alles', '292', '300', '4129', '50', '68', '79', '809', 'Alles', '190', '41', '99', '455', 'kein']

gif = ["<a:qiqi_1:824002468584751165>\r\n<a:qiqi_2:824002468580556830>\r\n<a:qiqi_3:824002468748066867>",
       "<a:PaimonNomming:824002466378809385>",
       "<a:baron_dance:824002940132917318>",
       "<a:BaguetteMarch:824002940330836008>",
       "<a:zerotwo_phuthon:824603915702108170>",
       "<a:StressWarning:824616547011133470>",
       "<a:ultrafastparrot:824616546705735680>",
       "<a:genshinimpact:824719004441509899>",
       "<a:typingcat:824024351581143091>",
       "<a:HatsuneMiku_Happy:824604669837049886>",
       "<a:Hyped_ZeroTwo:824603913578872832>",
       "<a:fiatpl01:865864338057330698>"
       ]

symbols = ["<:emoji_7:856653955878092800>",
           "<:emoji_6:856653911481778186>",
           "<:emoji_5:856653868003622912>",
           "<:emoji_4:856653828106747944>",
           "<:emoji_3:856653779980779520>",
           "<:emoji_2:856653737385000970>",
           "<:emoji_1:856653701624365106>"
           ]


def caps_pls(text):
    return text.upper()


class SimpleCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###################################################################################################################
    # mathe

    @commands.command()
    async def math(self, ctx, a: int, x, b: int):
        if x == "+":
            await ctx.send(f"{a} + {b} = {a + b}")
        elif x == "-":
            await ctx.send(f"{a} - {b} = {a - b}")
        elif x == "*" or x == "x":
            await ctx.send(f"{a} * {b} = {a * b}")
        elif x == "/" or x == ":":
            await ctx.send(f"{a} / {b} = {a / b}")

    ###################################################################################################################
    # commands

    @commands.command(name="zahl", help="Random Zahl")
    async def zahl(self, ctx):
        await ctx.send(f"deine Zahl ist {random.choice(zahl)}")

    @commands.command()
    async def test(self, ctx, numbers: Greedy[int], reason: str):
        await ctx.message.delete()
        await ctx.send(f"numbers: {numbers}, reason: {reason}")

    @commands.command(name="kill", help="kill")
    async def kill(self, ctx, member: discord.Member):
        await ctx.send(f"{member.display_name} wurde mit {random.choice(weapon)} gekillt!")

    @commands.command()
    async def caps(self, ctx, *, arg: caps_pls):
        await ctx.message.delete()
        await ctx.send(arg)

    @commands.command()
    async def say(self, ctx, *, arg):
        await ctx.message.delete()
        await ctx.send(arg)

    @commands.command()
    async def txt(self, ctx, member: discord.Member, args):
        await ctx.message.delete()
        await ctx.send(f'{member.display_name} {args}')

    @commands.command(name='gif')
    async def gif_emotes(self, ctx):
        await ctx.send(content=f'{random.choice(gif)}')

    @commands.command(name="ping")
    async def ping(self, ctx):
        await ctx.channel.send(f"Pong {self.client.latency * 1000:,.0f}ms")

    ##################################################################################################################
    # Help

    @commands.command(name='hutao', help='Custom Help', aliases=["hhelp", "thelp"])
    async def help_hutao(self, ctx):
        embed = discord.Embed(title="**Command Help** <a:PaimonNomming:824002466378809385>",
                              url='https://youtu.be/iik25wqIuFo',
                              colour=discord.Colour(0x910000))
        embed.set_author(name="Hu Tao - Bot")
        embed.add_field(name="_Help_",
                        value=f"{prefix}hutao\r\n"
                              f"{prefix}game\r\n",
                        inline=False)
        embed.add_field(name="_Commands_",
                        value=f"{prefix}kill\r\n"
                              f"{prefix}zahl\r\n"
                              f"{prefix}math\r\n"
                              f"{prefix}txt\r\n"
                              f"{prefix}say\r\n"
                              f"{prefix}caps\r\n"
                              f"{prefix}rollen\r\n"
                              f"{prefix}userinfo\r\n"
                              f"{prefix}setprefix",
                        inline=True)
        embed.add_field(name="_Games_",
                        value=f"{prefix}slot\r\n",
                        inline=True)
        embed.add_field(name="_Fun_",
                        value=f"{prefix}8ball\r\n"
                              f"{prefix}pklee\r\n"
                              f"{prefix}phutao\r\n"
                              f"{prefix}baguette\r\n"
                              f"{prefix}gif\r\n"
                              f"{prefix}waifurate\r\n"
                              f"{prefix}howhot\r\n"
                              f"{prefix}pepeSchild\r\n"
                              f"{prefix}RIP\r\n"
                              f"{prefix}rotation",
                        inline=True)
        embed.add_field(name="_Channels_",
                        value=f"{prefix}create-channel\r\n"
                              f"{prefix}create-voice-channel\r\n"
                              f"{prefix}delete-channel\r\n"
                              f"~~{prefix}delete-voice-channel~~",
                        inline=True)
        embed.add_field(name="Info",
                        value="- Bot is not Bug Free\r\n"
                              "- Channels erstellen mit **Max.15** Buchstaben",
                        inline=False)
        embed.set_thumbnail(
            url="https://media.discordapp.net/attachments/823997811758202971/829727905151451155/iitw10f9rab61.jpg?width")
        embed.set_footer(text="Coded by STEVEN#7195")
        await ctx.send(embed=embed)

    @commands.command(name='game', help='Custom Help')
    async def help_game(self, ctx):
        embed = discord.Embed(title="**Command Help**",
                              url='https://youtu.be/iik25wqIuFo',
                              colour=discord.Colour(0xff06))

        embed.set_author(name="Game - Bot", url="https://discord.gg/fTde2f8")
        embed.add_field(name="_Commands_", value=f"{prefix}game\r\n",
                        inline=False)
        embed.add_field(name="_Tuniere (RL)_",
                        value=
                        f"{prefix}tunier/add\r\n"
                        f"{prefix}tunier/remove\r\n"
                        f"{prefix}tunier/liste\r\n"
                        f"{prefix}tunier/picker",
                        inline=True)
        embed.add_field(name="Info", value="- Bot is not Bug Free\r\n"
                                           "- `g?x1 @user` ist der Gewinner",
                        inline=False)
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/840335423582765136/842147248418717696"
                                "/1067332-200.png")
        embed.set_footer(text="Coded by STEVEN#7195")
        await ctx.send(embed=embed)
        await ctx.message.delete()


#######################################################################################################################


def setup(client):
    client.add_cog(SimpleCommands(client))
