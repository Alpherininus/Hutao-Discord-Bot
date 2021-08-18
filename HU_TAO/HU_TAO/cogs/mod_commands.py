import discord

from discord.ext import commands

bad = [] # queue of Badwords
default_bad = ["Badwordlol"]


class ModCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###################################################################################################################

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def clear(self, ctx, amount: int = 10):
        await ctx.message.delete()  # Löscht den Command
        await ctx.channel.purge(limit=amount)  # Löscht die Anzahl die man angibt aus dem Channel
        embed = discord.Embed(title="**SERVERBOT**",
                              colour=discord.Colour(0x4fff))
        embed.add_field(name="Clear", value=f"Es wurden {amount} Nachrichten gelöscht!",
                        inline=True)
        await ctx.send(embed=embed, delete_after=5)

    @commands.command(name="mute")
    @commands.has_permissions(manage_channels=True)
    async def giverole(self, ctx, arg: discord.Member = None):
        await ctx.send(f"{ctx.author} hat {arg.display_name} Gemutet.")
        role = discord.utils.get(ctx.guild.roles, name='Muted')
        await arg.add_roles(role)
        await ctx.message.delete()

    @commands.command(name="unmute")
    @commands.has_permissions(manage_channels=True)
    async def removerole(self, ctx, arg: discord.Member = None):
        await ctx.send(f"{ctx.author} hat {arg.display_name} Endmutet.")
        role = discord.utils.get(ctx.guild.roles, name='Muted')
        await arg.remove_roles(role)
        await ctx.message.delete()

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        embed = discord.Embed(title="**Kick**",
                              colour=discord.Colour(0x4fff))
        embed.add_field(name="User", value=f"{member} was kicked!",
                        inline=True)
        await ctx.send(embed=embed)
        await ctx.message.delete()

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        await ctx.message.delete()
        bannedUsers = await ctx.guild.bans()
        name, discriminator = member.split("#")

        for ban in bannedUsers:
            user = ban.user

            if (user.name, user.discriminator) == (name, discriminator):
                await ctx.guild.unban(user)
                embed = discord.Embed(title="**Unban**",
                                      colour=discord.Colour(0x4fff))
                embed.add_field(name="User", value=f"{user.mention} was unbanned!",
                                inline=True)
                await ctx.send(embed=embed)
                return

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        global queue

        queue.append(member.display_name)
        await member.ban(reason=reason)
        embed = discord.Embed(title="**Ban**",
                              colour=discord.Colour(0x4fff))
        embed.add_field(name="User", value=f"{member} was banned!",
                        inline=True)
        await ctx.send(embed=embed)
        await ctx.message.delete()

    @commands.command(name='banlist')
    async def banlist_(self, ctx):
        embed = discord.Embed(title="**Ban List**",
                              colour=discord.Colour(0x4fff))
        embed.add_field(name="List", value=f"`{', '.join(queue)}`",
                        inline=False)
        await ctx.send(embed=embed)

    ###################################################################################################################

    @commands.command(name='badword/add')
    async def bqueue_(self, ctx, name):
        global bad

        bad.append(name)
        embed = discord.Embed(title="**Badwords**",
                              colour=discord.Colour(0x4fff))
        embed.add_field(name="Hinzugefügt:",
                        value=f"`{bad}`",
                        inline=False)
        await ctx.send(embed=embed)

    @commands.command(name='badword/remove')
    async def bremove_(self, ctx, number):
        global bad
        try:
            del (bad[int(number)])
            embed = discord.Embed(title="**Badwords**",
                                  colour=discord.Colour(0x4fff))
            embed.add_field(name="Rausgenommen:",
                            value=f"Jetzt `{bad}`",
                            inline=False)
            await ctx.send(embed=embed)
        except:
            await ctx.send('Your queue is either **empty** or the index is **out of range**')

    @commands.command(name='badword/liste', help='This command shows the queue')
    async def bview_(self, ctx):
        embed = discord.Embed(title="**Badwordsliste View**",
                              colour=discord.Colour(0x4fff))
        embed.add_field(name="Badwords:",
                        value=f"`{', '.join(bad)}`",
                        inline=False)
        await ctx.send(embed=embed)

    ###################################################################################################################

    @commands.command(name='create-channel')
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def create_channel(self, ctx, *, channel_name='name-angeben'):
        if len(channel_name) <= 15:
            guild = ctx.guild
            category_channel = self.client.get_channel(###############)
            existing_channel = discord.utils.get(guild.channels, name=channel_name, category=category_channel)
            if not existing_channel:
                print(f'Bot | Creating a new channel: {channel_name}')
                await guild.create_text_channel(str(channel_name), category=category_channel)
        else:
            embed = discord.Embed(title="**ERROR** <a:emoji_21:856654949337006111>",
                                  description=f'`{ctx.message.content}` | Name zu lang, maximal 15 Zeichen erlaubt!',
                                  colour=discord.Colour(0xff0000))
            await ctx.channel.send(embed=embed, delete_after=60)

    @commands.command(name="delete-channel")
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def del_channel(self, ctx, channel: discord.TextChannel):
        guild = ctx.guild
        category_channel = self.client.get_channel(#################)
        existing_channel = discord.utils.get(guild.channels, name=channel, category=category_channel)
        if not existing_channel:
            print(f'Bot | Delete a channel: {channel}')
            await channel.delete()
        else:
            embed = discord.Embed(title="**ERROR** <a:emoji_21:856654949337006111>",
                                  description=f'`{ctx.message.content}` | {ctx.author} CategoryID not Hexisting here',
                                  colour=discord.Colour(0xff0000))
            await ctx.channel.send(embed=embed, delete_after=60)

    ###################################################################################################################

    @commands.command(name='create-voicechannel')
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def create_voice_channel(self, ctx, *, channel_name='name-angeben'):
        if len(channel_name) <= 15:
            guild = ctx.guild
            category_channel = self.client.get_channel(##################)
            existing_channel = discord.utils.get(guild.channels, name=channel_name, category=category_channel)
            if not existing_channel:
                print(f'Bot | Creating a new Voicechannel: {channel_name}')
                await guild.create_voice_channel(str(channel_name), category=category_channel)
        else:
            embed = discord.Embed(title="**ERROR** <a:emoji_21:856654949337006111>",
                                  description=f'`{ctx.message.content}` | Name zu lang, maximal 15 Zeichen erlaubt!',
                                  colour=discord.Colour(0xff0000))
            await ctx.channel.send(embed=embed, delete_after=60)

    @commands.command(name="delete-voicechannel")
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def del_voicechannel(self, ctx, channel: discord.VoiceChannel):
        guild = ctx.guild
        category_channel = self.client.get_channel(###################)
        existing_channel = discord.utils.get(guild.channels, name=channel, category=category_channel)
        if not existing_channel:
            print(f'Bot | Delete a channel: {channel}')
            await channel.delete()
        else:
            embed = discord.Embed(title="**ERROR** <a:emoji_21:856654949337006111>",
                                  description=f'`{ctx.message.content}` | {ctx.author} CategoryID not Hexisting here',
                                  colour=discord.Colour(0xff0000))
            await ctx.channel.send(embed=embed, delete_after=60)

    ###################################################################################################################


def setup(client):
    client.add_cog(ModCommands(client))
