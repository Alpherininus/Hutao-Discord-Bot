import discord
import contextlib
import io

from discord.ext import commands


class Dev(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def eval(self, ctx, *, code):
        str_obj = io.StringIO()  # Retrieves a stream of data
        try:
            with contextlib.redirect_stdout(str_obj):
                exec(code)
        except Exception as e:
            return await ctx.send(f"```{e.__class__.__name__}: {e}```")
        await ctx.send(f'```{str_obj.getvalue()}```')

    @commands.command(name="cogload", hidden=True)
    @commands.is_owner()
    async def load(self, *, module: str):
        """Loads a module."""
        try:
            self.client.load_extension(module)
        except Exception as e:
            await self.client.say('\N{PISTOL}')
            await self.client.say('{}: {}'.format(type(e).__name__, e))
        else:
            await self.client.say('\N{OK HAND SIGN}')

    @commands.command(name="cogunload", hidden=True)
    @commands.is_owner()
    async def unload(self, *, module: str):
        """Unloads a module."""
        try:
            self.client.unload_extension(module)
        except Exception as e:
            await self.client.say('\N{PISTOL}')
            await self.client.say('{}: {}'.format(type(e).__name__, e))
        else:
            await self.client.say('\N{OK HAND SIGN}')

    @commands.command(name='cogreload', hidden=True)
    @commands.is_owner()
    async def _reload(self, *, module: str):
        """Reloads a module."""
        try:
            self.client.unload_extension(module)
            self.client.load_extension(module)
        except Exception as e:
            await self.client.say('\N{PISTOL}')
            await self.client.say('{}: {}'.format(type(e).__name__, e))
        else:
            await self.client.say('\N{OK HAND SIGN}')


def setup(client):
    client.add_cog(Dev(client))
