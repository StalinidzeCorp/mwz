import os
import sys
import random
import asyncio
import discord
from discord.ext.commands import has_permissions
from discord.ext import commands
from bot import bot
import json

'''
Перед использованием создайте файл по пути files/servers.json с контентном '{}' (без апострофов)
Создайте категорию и установите её id с помощью команды tickets_category_set
Далее, настройте эту категорию, чтобы никто, кроме админов/проверяющих не имел доступ к этой категории, все нужные права для участников настроит бот
Поменяйте id админов в листе admin_ids или же сделайте проверку с определённой ролью
Поменяйте при необходимости значение логической переменной CAN_READ_IF_CLOSE
'''

CAN_READ_IF_CLOSE = True
admin_ids = ['284171332516839426']
right_channel = 856146608060366849
moder_channel = 856152928318390282
ident = []


def generate(length):
    letters = 'qwertyuiopasdfghjklzxcvbnm1234567890'
    name = ''.join(random.choice(letters) for i in range(length))
    return name


async def create_text_channel(category, channel_name):
    channel = await category.create_text_channel(channel_name)
    return channel


async def create_voice_channel(category, channel_name):
    channel = await category.create_voice_channel(channel_name)
    return channel


async def delete_channel(guild, channel_id):
    channel = guild.get_channel(channel_id)
    await channel.delete()


def is_ticket_message(ctx):
    with open('files/servers.json', 'r') as f:
        table = json.load(f)

    channel_name = (ctx.message.channel.name)[-7:]
    guild_id = str(ctx.message.guild.id)

    if (guild_id in table):
        if ('tickets' in table[guild_id]):
            if (channel_name in table[guild_id]['tickets']):
                return True

    return False


def is_ticket_server(server):
    with open('files/servers.json', 'r') as f:
        table = json.load(f)

    if not server.channel:
        return False

    channel_name = (server.channel.name)[-7:]
    guild_id = str(server.channel.guild.id)

    if (guild_id in table):
        if ('tickets' in table[guild_id]):
            if (channel_name in table[guild_id]['tickets']):
                return True

    return False


class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Tickets successfully loaded!')

    @commands.command(aliases=['tickets_category_set', 'tcs'])
    @has_permissions(administrator=True)
    async def __tickets_category_set(self, ctx, id: int):

        category = bot.get_channel(id)
        print(category)
        if not category:
            return False

        with open('files/servers.json', 'r') as f:
            table = json.load(f)

        guild_id = str(ctx.message.guild.id)

        if not guild_id in table:
            table[guild_id] = {}

        table[guild_id]['tickets_category'] = id

        with open('files/servers.json', 'w') as f:
            json.dump(table, f)

        await ctx.message.delete()

    @commands.command(aliases=['ticket'])
    async def __ticket(self, ctx, *users: discord.User):

        with open('files/servers.json', 'r') as f:
            table = json.load(f)

        ticket_id = generate(7)
        channel_name = ticket_id
        guild_id = str(ctx.message.guild.id)

        # Если в нашем файле нет ключа нашего сервера - записываем
        if not guild_id in table:
            table[guild_id] = {}
            table[guild_id]['tickets'] = {}

            with open('files/servers.json', 'w') as f:
                json.dump(table, f)

            return False

        # Есть ли запись категории с тикетами
        if not 'tickets_category' in table[guild_id]:
            print('Tickets category ID is invalid, update it (!tickets_category_set)')
            return False

        category_id = table[guild_id]['tickets_category']
        category = bot.get_channel(category_id)

        # Существует ли категория с таким id
        if not category:
            print('Tickets category ID is invalid, update it (!tickets_category_set)')
            return False

        if not 'tickets' in table[guild_id]:
            table[guild_id]['tickets'] = {}

        # Если id тикета совпал с существующим
        while ticket_id in table[guild_id]['tickets']:
            ticket_id = generate(7)
            channel_name = ticket_id

        # Создаём текстовый канал нашего тикета
        channel = await create_text_channel(category, channel_name)

        if not channel:
            print('Cant create a text-channel' + channel_name)
            return False

        users_list = []

        for user in users:
            if user.id != ctx.message.author.id:
                users_list.append(user.id)

        # Создаём новую запись о тикете в файле
        table[guild_id]['tickets'][ticket_id] = {}
        table[guild_id]['tickets'][ticket_id]['channel'] = channel.id
        table[guild_id]['tickets'][ticket_id]['author'] = ctx.message.author.id
        table[guild_id]['tickets'][ticket_id]['users'] = users_list
        table[guild_id]['tickets'][ticket_id]['closed'] = False

        with open('files/servers.json', 'w') as f:
            json.dump(table, f)

        # Создаём оверрайт-права
        overwrite = discord.PermissionOverwrite()
        overwrite.send_messages = True
        overwrite.read_messages = True
        overwrite.read_message_history = True
        overwrite.attach_files = True
        overwrite.view_channel = True

        # Задаём права автору сообщения и тегаем
        await channel.set_permissions(ctx.message.author, overwrite=overwrite)
        await channel.send(f'<@{ctx.message.author.id}>')

        await asyncio.sleep(1)

        # Задаём права доп. участникам тикета и тегаем
        for user in users:
            await channel.set_permissions(user, overwrite=overwrite)
            await channel.send(f'<@{user.id}>')
            await asyncio.sleep(1)

        # Саздём emb
        emb = discord.Embed(title=f'Тикет #{ticket_id}', description='', colour=discord.Color.red())

        emb.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

        emb.add_field(name='Команды', value=f'`{ctx.prefix}voice <@moderator>`', inline=False)
        emb.add_field(name='Модер-команды', value=f'`{ctx.prefix}close` `{ctx.prefix}open`', inline=False)
        emb.add_field(name='Админ-команды', value=f'`{ctx.prefix}delete`', inline=False)

        emb.set_thumbnail(url="https://icons.iconarchive.com/icons/sonya/swarm/128/Ticket-icon.png")

        await channel.send(embed=emb)

        await ctx.send(f':tickets: Тикет {ticket_id} создан! (<#{channel.id}>)')

        # Отправляем тикет в модер чат
        date_format = "%d.%m.%Y"
        role_moder = 856165995092639764
        role_admin = 724635293898113044
        mod_chat = bot.get_channel(moder_channel)
        emed = discord.Embed(title='Новый тикет!',
                             description=f'Создан новый тикет.\nЧтобы его принять, напишите {ctx.prefix}accept <TICKET_ID>', colour=discord.Colour.random())
        emed.add_field(name='Канал:', value=f'<#{channel.id}>', inline=False)
        emed.add_field(name='Ник:', value=ctx.author.name, inline=False)
        emed.add_field(name='Дата:', value=ctx.message.created_at.strftime(date_format), inline=False)
        emed.add_field(name='TICKET_ID:', value=ticket_id, inline=False)
        await mod_chat.send(f'<@&{role_moder}><@&{role_admin}>')
        await mod_chat.send(embed=emed)

    @commands.command(aliases=['voice'])
    async def __voice(self, ctx, member: discord.Member):
        if not is_ticket_message(ctx):
            return False

        with open('files/servers.json', 'r') as f:
            table = json.load(f)

        channel = await create_voice_channel(ctx.message.channel.category, ctx.message.channel.name)
        ticket_id = (ctx.message.channel.name)[-7:]
        guild_id = str(ctx.message.guild.id)

        # Создаём оверрайт-права
        overwrite = discord.PermissionOverwrite()
        overwrite.connect = True
        overwrite.speak = True
        overwrite.stream = True
        overwrite.view_channel = True

        author = ctx.message.guild.get_member(table[guild_id]['tickets'][ticket_id]['author'])

        # Выдаём войс-права для автора
        await channel.set_permissions(author, overwrite=overwrite)
        await channel.set_permissions(member, overwrite=overwrite)

        # Выдаём войс-права сторонним пользователям
        for user_id in table[guild_id]['tickets'][ticket_id]['users']:
            user = ctx.message.guild.get_member(user_id)
            if (not user):
                continue

            await channel.set_permissions(user, overwrite=overwrite)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if (is_ticket_server(before)):
            if len(before.channel.members) == 0:
                await delete_channel(before.channel.guild, before.channel.id)

    @commands.command(aliases=['close'])
    @has_permissions(manage_roles=True)
    async def __close(self, ctx):
        if not is_ticket_message(ctx):
            return False

        with open('files/servers.json', 'r') as f:
            table = json.load(f)

        ticket_id = (ctx.message.channel.name)[-7:]
        guild_id = str(ctx.message.guild.id)
        channel_id = table[guild_id]['tickets'][ticket_id]['channel']
        channel = ctx.message.channel.guild.get_channel(channel_id)

        table[guild_id]['tickets'][ticket_id]['closed'] = True

        with open('files/servers.json', 'w') as f:
            json.dump(table, f)

        # Создаём оверрайт-права
        overwrite = discord.PermissionOverwrite()
        overwrite.send_messages = False
        overwrite.read_messages = CAN_READ_IF_CLOSE
        overwrite.read_message_history = CAN_READ_IF_CLOSE
        overwrite.attach_files = False
        overwrite.view_channel = False

        author = ctx.message.guild.get_member(table[guild_id]['tickets'][ticket_id]['author'])

        # Удаляем права с создателя
        await channel.set_permissions(author, overwrite=overwrite)

        await asyncio.sleep(1)

        # Удаляем права с юзеров
        for user_id in table[guild_id]['tickets'][ticket_id]['users']:
            user = ctx.message.guild.get_member(user_id)
            if (not user):
                continue

            await channel.set_permissions(user, overwrite=overwrite)
        await ctx.send(embed=discord.Embed(
            title='Тикет закрыт!',
            description=f'Данный тикет закрыл: {ctx.author.mention}. Данный тикет еще может быть открыт модератором или другим администратором.',
            colour=discord.Colour.random()

        ))

    @commands.command(aliases=['open'])
    @has_permissions(manage_roles=True)
    async def __open(self, ctx):
        if not is_ticket_message(ctx):
            return False

        with open('files/servers.json', 'r') as f:
            table = json.load(f)

        ticket_id = (ctx.message.channel.name)[-7:]
        guild_id = str(ctx.message.guild.id)
        channel_id = table[guild_id]['tickets'][ticket_id]['channel']
        channel = ctx.message.channel.guild.get_channel(channel_id)

        table[guild_id]['tickets'][ticket_id]['closed'] = False

        with open('files/servers.json', 'w') as f:
            json.dump(table, f)

        # Создаём оверрайт-права
        overwrite = discord.PermissionOverwrite()
        overwrite.send_messages = True
        overwrite.read_messages = True
        overwrite.read_message_history = True
        overwrite.attach_files = True
        overwrite.view_channel = True

        author = ctx.message.guild.get_member(table[guild_id]['tickets'][ticket_id]['author'])

        # Удаляем права с создателя
        await channel.set_permissions(author, overwrite=overwrite)

        await asyncio.sleep(1)

        # Удаляем права с юзеров
        for user_id in table[guild_id]['tickets'][ticket_id]['users']:
            user = ctx.message.guild.get_member(user_id)
            if (not user):
                continue

            await channel.set_permissions(user, overwrite=overwrite)
        await ctx.send(f'{author.mention}')
        await ctx.send(embed=discord.Embed(
            title='Тикет открыт!',
            description=f'{author.mention}, Ваш тикет снова открыт! Данный тикет открыл: {ctx.author.mention}.',
            colour=discord.Colour.random()
        ))

    @commands.command(aliases=['delete'])
    @commands.has_permissions(administrator=True)
    async def __delete(self, ctx):
        if not is_ticket_message(ctx):
            return False

        with open('files/servers.json', 'r') as f:
            table = json.load(f)

        ticket_id = (ctx.message.channel.name)[-7:]
        guild_id = str(ctx.message.guild.id)
        channel_id = table[guild_id]['tickets'][ticket_id]['channel']
        channel = ctx.message.channel.guild.get_channel(channel_id)

        # delete text channel & ticket
        await channel.delete()
        del table[guild_id]['tickets'][ticket_id]

        # delete voice_channel probably
        channel = discord.utils.get(ctx.message.guild.channels, name=ctx.message.channel.name)
        if (channel is not None):
            await channel.delete()

    @commands.command(aliases=['accept', 'принять'])
    @commands.has_permissions(manage_roles=True)
    async def _accept_ticket(self, ctx, iden: str):
        with open('files/servers.json', 'r') as f:
            table = json.load(f)

        guild_id = str(ctx.message.guild.id)
        channel_id = table[guild_id]['tickets'][iden]['channel']
        channel = ctx.message.channel.guild.get_channel(channel_id)
        overwrite = discord.PermissionOverwrite()
        overwrite.send_messages = True
        overwrite.read_messages = True
        overwrite.read_message_history = True
        overwrite.attach_files = True
        overwrite.view_channel = True
        overwrite.connect = True
        overwrite.speak = True
        overwrite.stream = True
        await channel.set_permissions(ctx.author, overwrite=overwrite)
        await ctx.channel.purge(limit=3)
        await ctx.send(embed=discord.Embed(
            title='Тикет принят!',
            description=f'{ctx.author.mention} принял тикет.',
            colour=discord.Colour.random()
        ))


def setup(bot):
    bot.add_cog(Tickets(bot))
