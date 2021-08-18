import asyncio
import os

import discord
import youtube_dl
from discord.ext import commands

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


async def from_url(cls, url, *, loop=None, stream=False):
    loop = loop or asyncio.get_event_loop()
    data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

    if 'entries' in data:
        # take first item from a playlist
        data = data['entries'][0]

    filename = data['url'] if stream else ytdl.prepare_filename(data)
    return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


def is_connected(ctx):
    voice_client = ctx.message.guild.voice_client
    return voice_client and voice_client.is_connected()


#
queue = []
loop = False


class MusicCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='join', help='Tells the bot to join the voice channel')
    async def join(self, ctx):
        if not ctx.message.author.voice:
            await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
            return
        else:
            channel = ctx.message.author.voice.channel
        await channel.connect()
        embed = discord.Embed(title="**Join**",
                              colour=discord.Colour(0x4fff))
        embed.add_field(name="Hallo !",
                        value="Bitte die Play Commands eingeben :)",
                        inline=False)
        await ctx.send(embed=embed, delete_after=20.1)
        await ctx.message.delete()

    @commands.command(name='leave', help='To make the bot leave the voice channel')
    async def leave(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_connected():
            await voice_client.disconnect()
            embed = discord.Embed(title="**Leave**",
                                  colour=discord.Colour(0x4fff))
            embed.add_field(name="Ich geh", value="Viel Spaß weiterhin", inline=False)
            await ctx.send(embed=embed, delete_after=20.1)
            await ctx.message.delete()
        else:
            await ctx.send("The bot is not connected to a voice channel.")

    @commands.command(name="play")
    async def play(self, ctx, url: str):
        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
        except PermissionError:
            embed = discord.Embed(title="**Play**",
                                  colour=discord.Colour(0xff0000))
            embed.add_field(name="Error", value="Wait for the current playing music to end or use the 'stop' command",
                            inline=False)
            await ctx.send(embed=embed, delete_after=15.1)
            return

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")
        voice_channel = ctx.author.voice.channel
        voice = ctx.channel.guild.voice_client
        if voice is None:
            voice = await voice_channel.connect()
        elif voice.channel != voice_channel:
            voice = await voice.move_to(voice_channel)
        if voice.is_playing:
            voice.stop()
            #
            voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print('Song zuende.'))
            embed = discord.Embed(title="**Play** <:speaker_on:861282451270795264>", description=f" ",
                                  colour=discord.Colour(0x4fff))
            embed.add_field(name="Was Spielt gerade", value=f"{url}", inline=True)
            await ctx.send(embed=embed)
            await ctx.message.delete()

    @commands.command(name='pause', help='This command pauses the song')
    async def pause(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            await voice_client.pause()
            embed = discord.Embed(title="**Pause** <:speaker_mute:861282451359137792>",
                                  colour=discord.Colour(0x4fff))
            embed.add_field(name="ist Pausiert",
                            value="Mit ``t?resume`` wird Es wider abgespielt",
                            inline=False)
            await ctx.send(embed=embed, delete_after=20.1)
            await ctx.message.delete()
        else:
            await ctx.send("The bot is not playing anything at the moment.")

    @commands.command(name='resume', help='Resumes the song')
    async def resume(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_paused():
            await voice_client.resume()
            await ctx.message.delete()
        else:
            await ctx.send("The bot was not playing anything before this. Use play_song command")

    @commands.command(name='stop', help='Stops the song')
    async def stop(self, ctx):
        await ctx.message.delete()
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            await voice_client.stop()
            embed = discord.Embed(title="**Stop**",
                                  colour=discord.Colour(0x4fff))
            embed.add_field(name="Ist gestopt <:speaker_off:861282450613469204>",
                            value="Du hast denn Bot gestopt. ``t?leave``", inline=False)
            await ctx.send(embed=embed, delete_after=20.1)
        else:
            await ctx.send("The bot is not playing anything at the moment.")

    @commands.command(name='qplay', help='This command plays music')
    async def queueplay(self, ctx):
        global queue

        if not ctx.message.author.voice:
            await ctx.send("You are not connected to a voice channel <:speaker1600:861282451309330442>")
            return

        else:
            channel = ctx.message.author.voice.channel

        try:
            await channel.connect()
        except:
            pass

        server = ctx.message.guild
        voice_channel = server.voice_client

        try:
            async with ctx.typing():
                player = await YTDLSource.from_url(queue[0], loop=self.client.loop)
                voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

                if loop:
                    queue.append(queue[0])

                del (queue[0])

            embed = discord.Embed(title="**Play** <:speaker_off:861282450613469204>",
                                  colour=discord.Colour(0x4fff))
            embed.add_field(name="Now playing from queue", value=f"{player.title}",
                            inline=False)
            await ctx.send(embed=embed)

        except:
            await ctx.send('Nothing in your queue! Use `?queue` to add a song! <:speaker1600:861282451309330442>')
        await ctx.message.delete()

    @commands.command(name='queue')
    async def queue_(self, ctx, url):
        global queue

        queue.append(url)
        embed = discord.Embed(title="**Queue** <:speaker_off:861282450613469204>",
                              colour=discord.Colour(0x4fff))
        embed.add_field(name="Added to queue!", value=f"`{url}`",
                        inline=False)
        await ctx.send(embed=embed)
        await ctx.message.delete()

    @commands.command(name='remove')
    async def remove(self, ctx, number):
        global queue
        try:
            del (queue[int(number)])
            embed = discord.Embed(title="**Queue View** <:speaker_off:861282450613469204>",
                                  colour=discord.Colour(0x4fff))
            embed.add_field(name="Queue", value=f"Your queue is now\r\n`{queue}`",
                            inline=False)
            await ctx.send(embed=embed)
        except:
            await ctx.send('Your queue is either **empty** or the index is **out of range** <:speaker1600:861282451309330442>')
        await ctx.message.delete()

    @commands.command(name='view', help='This command shows the queue')
    async def view(self, ctx):
        embed = discord.Embed(title="**Queue View** <:speaker_off:861282450613469204>",
                              colour=discord.Colour(0x4fff))
        embed.add_field(name="Queue", value=f"`{queue}`",
                        inline=False)
        await ctx.send(embed=embed)

    class NoMoreTracks(commands.CommandError):
        pass

    #################################################################################################################


def setup(client):
    client.add_cog(MusicCommands(client))
