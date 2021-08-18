import discord

from discord.ext import commands


class UserCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def userinfo(self, ctx, *, user: discord.Member):
        embed = discord.Embed(title="USER INFO", description=f"Here is the info we retrieved about {user.display_name}",
                              colour=user.colour)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="NAME", value=user.name, inline=True)
        embed.add_field(name="NICKNAME", value=user.nick, inline=True)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="STATUS", value=user.status, inline=True)
        embed.add_field(name="TOP ROLE", value=user.top_role.name, inline=True)
        embed.add_field(name='JOIN THIS SERVER', value=user.joined_at.strftime('%d/%m/%Y, %H:%M:%S'), inline=True)
        embed.add_field(name='CREATED ACCOUNT', value=user.created_at.strftime('%d/%m/%Y, %H:%M:%S'), inline=True)
        await ctx.send(embed=embed)

    class MemberRoles(commands.MemberConverter):
        async def convert(self, ctx, argument):
            member = await super().convert(ctx, argument)
            return [role.name for role in member.roles[1:]]  # Remove everyone role!

    @commands.command(name="rollen", help="rollen anzeigen")
    async def roles(self, ctx, *, member: MemberRoles):
        """Tells you a member's roles."""
        embed = discord.Embed(title="**Rollen!**",
                              colour=discord.Colour(0x910000))
        embed.add_field(name="I see the following roles:", value='' + ', '.join(member),
                        inline=True)
        embed.set_footer(text="Info")
        await ctx.send(embed=embed)

    @commands.command()
    async def lol(self, ctx):
        await ctx.send("test")


def setup(client):
    client.add_cog(UserCommands(client))
