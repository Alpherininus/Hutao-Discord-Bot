import random
from io import BytesIO

import aiohttp
import discord
from PIL import ImageFont, ImageDraw, Image
from discord.ext import commands

pepe = "hi", "hey", "hallo", "morgen", "moin"
hallo = "hi", "hey", "hallo", "morgen", "moin"

pro = ["10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%", "No", "Ultimate", "Trap", "10%",
       "20%",
       "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"]

musli = ["Shiish", "Crunchy", "Crispy", "Breakfast"]

ses = aiohttp.ClientSession()


class PillowCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###############################################################################################################
    # PIL / pictures.jpeg
    # py -m pip install --upgrade pip
    # py -m pip install --upgrade Pillow

    @commands.command(name="pklee", help="Discord.Pillow.Image - Picture Klee")
    async def kleePIL(self, ctx, *, user: discord.Member = None):
        if user is None:
            user = ctx.author

        genshin = Image.open("cogs/pictures/PIL/Genshin/klee/klee.jpeg")

        asset = user.avatar_url_as(size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)

        pfp = pfp.resize((285, 285))

        genshin.paste(pfp, (332, 470))

        genshin.save("cogs/pictures/PIL/Genshin/klee/profile.jpeg")

        await ctx.send(file=discord.File("cogs/pictures/PIL/Genshin/klee/profile.jpeg"))
        print("Bot | PIL: Hat das bild geschickt")

    @commands.command(name="waifurate", help="Discord.Pillow.Image - Picture Klee")
    async def apicturesPIL(self, ctx, *, a: discord.Member = None, text="No text entered"):
        if a is None:
            a = ctx.author

        img = Image.open("cogs/pictures/PIL/wcard/wcard.png")

        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", 32)

        text = f"You are {random.choice(pro)} Waifu"

        draw.text((245, 100), text, (0, 0, 0), font=font)

        img.save("cogs/pictures/PIL/wcard/profile.png")

        a_asset = a.avatar_url_as(size=128)
        a_data = BytesIO(await a_asset.read())

        apfp = Image.open(a_data)

        apfp = apfp.resize((183, 183))

        img.paste(apfp, (42, 37))

        img.save("cogs/pictures/PIL/wcard/profile.png")

        await ctx.send(file=discord.File("cogs/pictures/PIL/wcard/profile.png"))
        print("Bot | PIL: Hat das bild geschickt")

        #

    @commands.command(name="phutao", help="Discord.Pillow.Image")
    async def hutaoPIL(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        hutao = Image.open("cogs/pictures/PIL/Genshin/hutao/hu.png")

        asset = user.avatar_url_as(size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)

        pfp = pfp.resize((177, 177))

        hutao.paste(pfp, (164, 337))

        hutao.save("cogs/pictures/PIL/Genshin/hutao/profile.png")

        await ctx.send(file=discord.File("cogs/pictures/PIL/Genshin/hutao/profile.png"))
        print("Bot | PIL: Hat das bild geschickt")

    ##################################################################################################################

    @commands.command(name="pepeSchild", help="Discord.Pillow.Image")
    async def bpicturesPIL(self, ctx, *, text="No text entered"):
        if len(text) <= 15:
            img = Image.open("cogs/pictures/PIL/pepe/pepeSchild.png")

            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype("arial.ttf", 13)

            draw.text((2, 2), text, (0, 0, 0), font=font)
            # draw.text((2, 16), text, (0, 0, 0), font=font)
            # draw.text((2, 30), text, (0, 0, 0), font=font)

            img.save("cogs/pictures/PIL/pepe/profile.png")

            await ctx.send(file=discord.File("cogs/pictures/PIL/pepe/profile.png"))
            print("Bot | PIL: Hat das bild geschickt")

    @commands.command(name="hallo", help="Discord.Pillow.Image")
    async def cpicturesPIL(self, ctx, *, member: discord.Member = None, text="No text entered"):

        img = Image.open("cogs/pictures/PIL/pepe/pS.png")

        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", 13)

        text = f"{random.choice(hallo)}\n{ctx.author}"

        draw.text((2, 2), text, (0, 0, 0), font=font)
        # draw.text((2, 16), text, (0, 0, 0), font=font)
        # draw.text((2, 30), text, (0, 0, 0), font=font)

        img.save("cogs/pictures/PIL/pepe/pS1.png")

        await ctx.send(file=discord.File("cogs/pictures/PIL/pepe/pS1.png"))
        await ctx.message.delete()
        print("Bot | PIL: Hat das bild geschickt")


    @commands.command(name="rotation")
    async def rotate(self, ctx, url: str, deegrees: int):
        async with ses.get(url) as r:
            if r.status in range(200, 299):
                img = Image.open(BytesIO(await r.read()), mode="r")
                img_rotated = img.rotate(angle=deegrees)
                b = BytesIO()
                img_rotated.save(b, format=f"{img.format}")
                b_im = b.getvalue()
                file = discord.File(filename=f"rotated.{img.format}", fp=BytesIO(b_im))
                mbed = discord.Embed()
                mbed.set_image(url=f"attachment://rotated.{img.format}")
                await ctx.send(embed=mbed, file=file)
                await ctx.message.delete()
                print("Bot | PIL: Hat das bild geschickt")
            else:
                await ctx.send(f"Error occured when trying to make request. Response: {r.status}")

    @commands.command(name="RIP", help="Discord.Pillow.Image")
    async def CoffinDanceHutao(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        hutao = Image.open("cogs/pictures/PIL/Genshin/coffin/coffin.png")

        asset = user.avatar_url_as(size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)

        pfp = pfp.resize((300, 300))

        hutao.paste(pfp, (322, 199))

        hutao.save("cogs/pictures/PIL/Genshin/coffin/profile.png")

        await ctx.send(file=discord.File("cogs/pictures/PIL/Genshin/coffin/profile.png"))
        print("Bot | PIL: Hat das bild geschickt")

    @commands.command(name="müsli", help="Discord.Pillow.Image")
    async def muesli(self, ctx, text="No text entered"):

        img = Image.open("cogs/pictures/PIL/müsli/muesli.png")

        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", 45)

        text = f"{random.choice(musli)}"

        draw.text((270, 190), text, (0, 0, 0), font=font)
        # draw.text((2, 16), text, (0, 0, 0), font=font)
        # draw.text((2, 30), text, (0, 0, 0), font=font)

        img.save("cogs/pictures/PIL/müsli/profile.png")

        await ctx.send(file=discord.File("cogs/pictures/PIL/müsli/profile.png"))
        print("Bot | PIL: Hat das bild geschickt")

    @commands.command(name="nudel", help="Discord.Pillow.Image")
    async def nudel(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        hutao = Image.open("cogs/pictures/PIL/nudel/nudel.png")

        asset = user.avatar_url_as(size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)

        pfp = pfp.resize((333, 333))

        hutao.paste(pfp, (578, 72))

        hutao.save("cogs/pictures/PIL/nudel/profile.png")

        await ctx.send(file=discord.File("cogs/pictures/PIL/nudel/profile.png"))
        print("Bot | PIL: Hat das bild geschickt")


def setup(client):
    client.add_cog(PillowCommands(client))
