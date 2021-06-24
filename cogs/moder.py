import discord
from discord.ext import commands
from bot import bot
from discord.ext.commands import has_permissions
import asyncio


class Moder(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Moder cog successfully loaded!')

    @commands.command(
        name='Верификация',
        aliases=['вер', 'верификация'],
        brief='Создает сообщения с реакциями для верификации.',
        usage='верификация'
    )
    @has_permissions(manage_roles=True)
    async def _verify_mes(self, ctx, message):
        send = await ctx.send(embed=discord.Embed(
            title='Верификация',
            description=f'{message}',
            colour=discord.Colour.random()
        ))
        await send.add_reaction('♂')
        await send.add_reaction('♀')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel = bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        guild = bot.get_guild(payload.guild_id)
        reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)

        # only work if it is the client
        if payload.member.id == bot.user.id:
            return

        if reaction.emoji == '♂':
            role = discord.utils.get(guild.roles, name='♂')
            await payload.member.add_roles(role)
            await reaction.remove(payload.member)
        elif reaction.emoji == '♀':
            role = discord.utils.get(guild.roles, name='♀')
            await payload.member.add_roles(role)
            await reaction.remove(payload.member)

    @commands.command(
        name='Мут',
        aliases=['мут', 'mute'],
        brief='Мутит человека.',
        usage='мут <@user> <тип> <время> <причина>'
    )
    @has_permissions(manage_roles=True)
    async def _mute(self, ctx, member: discord.Member, tip: int = None, time: str = None, *, reason: str = None):
        await ctx.channel.purge(limit=1)
        global times
        if tip is None:
            tip = 3
        if reason is None:
            reason = 'Без причины'
        if time is None:
            time = 0
        time_award = ''.join(filter(lambda x: x.isdigit(), time))
        time_zn = ''
        for c in time:
            if c not in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
                time_zn = time_zn + c

        if time_zn == 'сек' or time_zn == 'sec':
            h = int(time_award) // 3600
            m = (int(time_award) // 60) % 60
            s = int(time_award) % 60
            times = int(time_award)
        elif time_zn == 'мин' or time_zn == 'min':
            h = int(time_award) // 60
            m = (int(time_award)) % 60
            s = (int(time_award) * 60) % 60
            times = int(time_award) * 60
        elif time_zn == 'ч' or time_zn == 'h':
            h = int(time_award) % 60
            m = (int(time_award) * 60) % 60
            s = (int(time_award) * 3600) % 60
            times = int(time_award) * 3600

        muterole_chat = discord.utils.get(ctx.guild.roles, name='chat muted')
        muterole_voice = discord.utils.get(ctx.guild.roles, name='voice muted')
        embed = discord.Embed(title='МУТ', colour=discord.Colour.random())
        embed.add_field(name='Нарушитель:', value=f'{member.mention}', inline=False)
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name='Выдал:', value=f'{ctx.author.mention}', inline=False)
        embed.add_field(name='Причина:', value=f'{reason}', inline=False)
        if tip == 1:
            embed.add_field(name='Тип:', value=f'чат', inline=False)
        elif tip == 2:
            embed.add_field(name='Тип:', value=f'голос', inline=False)
        else:
            embed.add_field(name='Тип:', value=f'фулл', inline=False)
        if time == 0:
            embed.add_field(name='Время до снятия:', value=f'Бессрочно', inline=False)
        else:
            embed.add_field(name='Время до снятия:', value=f'**{h}** ч, **{m}** мин, **{s}** сек.', inline=False)
        await ctx.send(embed=embed)
        if time == 0:
            if tip == 1:
                await member.add_roles(muterole_chat)
            if tip == 2:
                await member.add_roles(muterole_voice)
            else:
                await member.add_roles(muterole_chat)
                await member.add_roles(muterole_voice)
        else:
            if tip == 1:
                await member.add_roles(muterole_chat)
                await asyncio.sleep(times)
                await member.remove_roles(muterole_chat)

            if tip == 2:
                await member.add_roles(muterole_voice)
                await asyncio.sleep(times)
                await member.remove_roles(muterole_voice)

            else:
                await member.add_roles(muterole_chat)
                await member.add_roles(muterole_voice)
                await asyncio.sleep(times)
                await member.remove_roles(muterole_chat)
                await member.remove_roles(muterole_voice)

    @commands.command(
        name='Бан',
        aliases=['бан', 'ban'],
        brief='Банит человека.',
        usage='мут <@user> <время> <причина>'
    )
    @has_permissions(manage_roles=True)
    async def _ban(self, ctx, member: discord.Member, time: str = None, *, reason: str = None):
        await ctx.channel.purge(limit=1)
        global times
        if reason is None:
            reason = 'Без причины'
        if time is None:
            time = 0
        time_award = ''.join(filter(lambda x: x.isdigit(), time))
        time_zn = ''
        for c in time:
            if c not in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
                time_zn = time_zn + c

        if time_zn == 'сек' or time_zn == 'sec':
            h = int(time_award) // 3600
            m = (int(time_award) // 60) % 60
            s = int(time_award) % 60
            times = int(time_award)
        elif time_zn == 'мин' or time_zn == 'min':
            h = int(time_award) // 60
            m = (int(time_award)) % 60
            s = (int(time_award) * 60) % 60
            times = int(time_award) * 60
        elif time_zn == 'ч' or time_zn == 'h':
            h = int(time_award) % 60
            m = (int(time_award) * 60) % 60
            s = (int(time_award) * 3600) % 60
            times = int(time_award) * 3600

        muterole_chat = discord.utils.get(ctx.guild.roles, name='banned')
        ver = discord.utils.get(ctx.guild.roles, name='verifyed')
        embed = discord.Embed(title='БАН', colour=discord.Colour.random())
        embed.add_field(name='Нарушитель:', value=f'{member.mention}', inline=False)
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name='Выдал:', value=f'{ctx.author.mention}', inline=False)
        embed.add_field(name='Причина:', value=f'{reason}', inline=False)
        if time == 0:
            embed.add_field(name='Время до снятия:', value=f'Бессрочно', inline=False)
        else:
            embed.add_field(name='Время до снятия:', value=f'**{h}** ч, **{m}** мин, **{s}** сек.', inline=False)
        await ctx.send(embed=embed)
        if time == 0:
            await member.add_roles(muterole_chat)
            await member.remove_roles(ver)
            user = await bot.fetch_user(user_id=member.id)
            embed = discord.Embed(title='БАН', colour=discord.Colour.random())
            embed.add_field(name='Нарушитель:', value=f'{member.mention}', inline=False)
            embed.set_thumbnail(url=member.avatar_url)
            embed.add_field(name='Выдал:', value=f'{ctx.author.mention}', inline=False)
            embed.add_field(name='Причина:', value=f'{reason}', inline=False)
            await user.send(embed=embed)
        else:
            await member.add_roles(muterole_chat)
            await member.remove_roles(ver)
            user = await bot.fetch_user(user_id=member.id)
            embed = discord.Embed(title='БАН', colour=discord.Colour.random())
            embed.add_field(name='Нарушитель:', value=f'{member.mention}', inline=False)
            embed.set_thumbnail(url=member.avatar_url)
            embed.add_field(name='Выдал:', value=f'{ctx.author.mention}', inline=False)
            embed.add_field(name='Причина:', value=f'{reason}', inline=False)
            await user.send(embed=embed)
            await asyncio.sleep(times)
            await member.remove_roles(muterole_chat)
            await member.add_roles(ver)
            embed = discord.Embed(title='РАЗБАН', colour=discord.Colour.random())
            embed.add_field(name='Нарушитель:', value=f'{member.mention}', inline=False)
            embed.set_thumbnail(url=member.avatar_url)
            embed.add_field(name='Снял:', value=f'Вышло время', inline=False)
            await user.send(embed=embed)

    @commands.command(
        name='Размут',
        aliases=['размут', 'unmute'],
        brief='Размутит человека.',
        usage='размут <@user>'
    )
    @has_permissions(manage_roles=True)
    async def _unmute(self, ctx, member: discord.Member):
        await ctx.channel.purge(limit=1);
        muterole_c = discord.utils.get(ctx.guild.roles, name='chat muted')
        muterole_v = discord.utils.get(ctx.guild.roles, name='voice muted')
        embed = discord.Embed(title='РАЗМУТ', colour=discord.Colour.random())
        embed.add_field(name='Нарушитель:', value=f'{member.mention}', inline=False)
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name='Снял:', value=f'{ctx.author.mention}', inline=False)
        await ctx.send(embed=embed)
        await member.remove_roles(muterole_c)
        await member.remove_roles(muterole_v)

    @commands.command(
        name='Разбан',
        aliases=['разбан', 'unban'],
        brief='Разбанит человека.',
        usage='разбан <@user>'
    )
    @has_permissions(manage_roles=True)
    async def _unban(self, ctx, member: discord.Member):
        await ctx.channel.purge(limit=1);
        muterole_c = discord.utils.get(ctx.guild.roles, name='banned')
        ver = discord.utils.get(ctx.guild.roles, name='verifyed')
        user = await bot.fetch_user(user_id=member.id)
        embed = discord.Embed(title='РАЗБАН', colour=discord.Colour.random())
        embed.add_field(name='Нарушитель:', value=f'{member.mention}', inline=False)
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name='Снял:', value=f'{ctx.author.mention}', inline=False)
        await ctx.send(embed=embed)
        await member.remove_roles(muterole_c)
        await member.add_roles(ver)
        await user.send('Вы были разбанены на сервере MWZ!')

    @commands.command(
        name='Очистить',
        aliases=['очистить', 'clear'],
        brief='Очистить чат.',
        usage='очистить <количство>'
    )
    @has_permissions(manage_roles=True)
    async def _clear(self, ctx, amount: int = 100):
        await ctx.channel.purge(limit=amount+1)
        await ctx.send(embed=discord.Embed(
            title='Очистка чата',
            description=f'Очищено **{amount}** сообщений!',
            colour=discord.Colour.random()
        ))
        await asyncio.sleep(5)
        await ctx.channel.purge(limit=1)


def setup(bot):
    bot.add_cog(Moder(bot))
