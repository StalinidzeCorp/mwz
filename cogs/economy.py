import asyncio
import random

import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from bot import bot
import datab
import pymongo
import time

tdict = {}
banned_roles = [
    724635293898113044,
    854591574880813087,
    856165995092639764,
    856062383512092682,
    856131072169738292,
    851741566904172564,
    855505956984324166,
    855506090481287178,
    855506122207264788,
    856584604013953034,
    856791847925317633
]


class Economy(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Economy cog successfully loaded!')
        for guild in bot.guilds:
            for member in guild.members:
                post = {
                    '_id': member.id,
                    'name': member.name,
                    'balance': 0,
                    'xp': 0,
                    'lvl': 0,
                    'in_voice_time': 0,
                    'inv_roles': []
                }
                if datab.coll.count_documents({'_id': member.id}) == 0:
                    datab.coll.insert_one(post)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        post = {
            '_id': member.id,
            'name': member.name,
            'balance': 0,
            'xp': 0,
            'lvl': 0,
            'in_voice_time': 0,
            'inv_roles': []
        }
        if datab.coll.count_documents({'_id': member.id}) == 0:
            datab.coll.insert_one(post)

    @commands.command(
        name='Баланс',
        aliases=['баланс', 'бал', 'б', 'balance', 'cash', 'bal', '$'],
        brief='Команда для проверки баланса любого игрока.',
        usage='баланс <@user>'
    )
    async def _member_balance(self, ctx, member: discord.Member = None):
        emoji = datab.colls.find_one({'for': 'валюта'})['name']
        if member is None:
            await ctx.send(embed=discord.Embed(
                description=f'Баланс {ctx.author.mention}: **{datab.coll.find_one({"_id": ctx.author.id})["balance"]}** {emoji}',
                colour=discord.Colour.random()
            ).set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.name))
        else:
            await ctx.send(embed=discord.Embed(
                description=f'Баланс {member.mention}: **{datab.coll.find_one({"_id": member.id})["balance"]}** {emoji}',
                colour=discord.Colour.random()
            ).set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.name))

    @commands.command(
        name='Передать',
        aliases=['передать', 'отдать', 'give', 'пер', 'отд'],
        brief='Команда, которая даст игроку возможность передать деньги другому игроку.',
        usage='передать <@user> <количество>'
    )
    async def _member_give(self, ctx, member: discord.Member, amount: int):
        emoji = datab.colls.find_one({'for': 'валюта'})['name']
        if amount <= 0:
            await ctx.send(embed=discord.Embed(
                description=f'Вы ввели недопустимое значение!',
                colour=discord.Colour.random()
            ).set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.name))
        elif datab.coll.find_one({'_id': ctx.author.id})['balance'] < amount:
            await ctx.send(embed=discord.Embed(
                description=f'У Вас недостаточно на балансе!',
                colour=discord.Colour.random()
            ).set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.name))
        elif ctx.author is member:
            await ctx.send(embed=discord.Embed(
                description=f'Вы не можете передать себе!',
                colour=discord.Colour.random()
            ).set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.name))
        else:
            datab.coll.update_one({'_id': ctx.author.id}, {'$inc': {'balance': -amount}})
            datab.coll.update_one({'_id': member.id}, {'$inc': {'balance': amount}})
            await ctx.send(embed=discord.Embed(
                description=f'Вы передали **{amount}** {emoji} пользователю {member.mention}',
                colour=discord.Colour.random()
            ).set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.name))

    @commands.command(
        name='Бонус',
        aliases=['приз', 'pri', 'bonus', 'bon', 'бонус', 'бон'],
        brief='Команда, которую можно написать один раз в 12 часов. Эта команда даёт игрокам бонус 100 баллов.',
        usage='приз'
    )
    @commands.cooldown(1, 43200, commands.BucketType.user)
    async def _prize_member(self, ctx):
        emoji = datab.colls.find_one({'for': 'валюта'})['name']
        datab.coll.update_one({'_id': ctx.author.id}, {'$inc': {'balance': 100}})
        await ctx.send(embed=discord.Embed(
            description=f'Вы получили **100** {emoji}.',
            colour=discord.Colour.random()
        ).set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.name))

    @commands.command(
        name='Добавить',
        aliases=['добавить', 'доб', 'agive', 'ag'],
        brief='Команда, которая добавит определенному игроку баллы к балансу. Может пользоваться администратор или определенная роль.',
        usage='добавить <@user> <баллы>'
    )
    @has_permissions(manage_roles=True)
    async def _admin_give(self, ctx, member: discord.Member, amount: int):
        emoji = datab.colls.find_one({'for': 'валюта'})['name']
        if amount <= 0:
            await ctx.send(embed=discord.Embed(
                description=f'Вы ввели недопустимое значение!',
                colour=discord.Colour.random()
            ).set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.name))
        else:
            datab.coll.update_one({'_id': member.id}, {'$inc': {'balance': amount}})
            await ctx.send(embed=discord.Embed(
                description=f'Вы добавили **{amount}** {emoji} на баланс {member.mention}',
                colour=discord.Colour.random()
            ).set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.name))

    @commands.command(
        name='Установить-баланс',
        aliases=['установить-баланс', 'уб', 'asetbal', 'asbal'],
        brief='Команда, которая установит игроку валюту на балансе. Может пользоваться администратор или определенная роль.',
        usage='добавить <@user> <баллы>'
    )
    @has_permissions(manage_roles=True)
    async def _admin_set_val(self, ctx, member: discord.Member, amount: int):
        emoji = datab.colls.find_one({'for': 'валюта'})['name']
        if amount <= 0:
            await ctx.send(embed=discord.Embed(
                description=f'Вы ввели недопустимое значение!',
                colour=discord.Colour.random()
            ).set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.name))
        else:
            datab.coll.update_one({'_id': member.id}, {'$set': {'balance': amount}})
            await ctx.send(embed=discord.Embed(
                description=f'Вы установили **{amount}** {emoji} на балансе {member.mention}',
                colour=discord.Colour.random()
            ).set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.name))

    @commands.command(
        name='Забрать',
        aliases=['забрать', 'заб', 'atake', 'at'],
        brief='Команда, которая убирает определенную сумму баллов определенному игроку.',
        usage='забрать <@user> <баллы>'
    )
    @has_permissions(manage_roles=True)
    async def _admin_take(self, ctx, member: discord.Member, amount: int):
        emoji = datab.colls.find_one({'for': 'валюта'})['name']
        if amount <= 0:
            await ctx.send(embed=discord.Embed(
                description=f'Вы ввели недопустимое значение!',
                colour=discord.Colour.random()
            ).set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.name))
        else:
            bl = datab.coll.find_one({'_id': member.id})['balance']
            if amount > int(bl):
                await ctx.send(embed=discord.Embed(
                    description=f'Вы ввели недопустимое значение!',
                    colour=discord.Colour.random()
                ).set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.name))
            else:
                datab.coll.update_one({'_id': member.id}, {'$inc': {'balance': -amount}})
                await ctx.send(embed=discord.Embed(
                    description=f'Вы забрали **{amount}** {emoji} из баланса {member.mention}',
                    colour=discord.Colour.random()
                ).set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.name))

    @commands.command(
        name='Лидеры',
        aliases=['топ', 'лидеры', 'leaders', 'top'],
        brief='Команда, которая показывает игроков топ по деньгам.',
        usage='топ-валюта'
    )
    async def _leaderboard(self, ctx):
        emoji = datab.colls.find_one({'for': 'валюта'})['name']
        embed = discord.Embed(title='ТОП СЕРВЕРА', colour=discord.Colour.random())
        counter = 0
        for row in datab.coll.find().sort("lvl", pymongo.DESCENDING):
            member = ctx.author.guild.get_member(row['_id'])
            counter += 1
            h = row['in_voice_time'] // 3600
            m = (row['in_voice_time'] // 60) % 60
            s = row['in_voice_time'] % 60
            embed.add_field(
                name=f'{counter} | Лвл: ```{row["lvl"]}``` | {emoji}: ```{row["balance"]}``` | 🎤: ```{h}:{m}:{s}```',
                value=f'Игрок: {member.mention}',
                inline=False
            )
            if counter == 10:
                break
        embed.set_thumbnail(url=ctx.author.guild.icon_url)
        embed.set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.name)
        await ctx.send(embed=embed)

    @commands.command(
        name='Рольплюс',
        aliases=['рольплюс', 'рп', 'р+', 'roleplus', 'r+'],
        brief='Команда, для добавления роли в магазин. После этой команды в магазин добавляется роль со своей ценой.',
        usage='рольплюс <@роль> <цена роли>'
    )
    @has_permissions(manage_roles=True)
    async def _add_role(self, ctx, role: discord.Role, cost: int):
        emoji = datab.colls.find_one({'for': 'валюта'})['name']
        rld = datab.collsp.estimated_document_count() + 1
        postsp = {
            'role_id': role.id,
            'role_name': role.name,
            'cost': cost,
            'number': rld
        }
        if cost < 0:
            await ctx.send(embed=discord.Embed(
                description=f'{ctx.author.mention}, Вы ввели недопустимое значение!',
                colour=discord.Colour.random()
            ).set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.name))
        else:
            if datab.collsp.count_documents({'role_id': role.id}) == 0:
                datab.collsp.insert_one(postsp)
                await ctx.send(embed=discord.Embed(
                    description=f'{ctx.author.mention}, **{role.name}** успешно добавлена. Ее стоимость **{cost}** {emoji}',
                    colour=discord.Colour.random()
                ).set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.name))
            else:
                await ctx.send(embed=discord.Embed(
                    description=f'{ctx.author.mention}, данная роль уже продается',
                    colour=discord.Colour.random()
                ).set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.name))

    @commands.command(
        name='Рольминус',
        aliases=['рольминус', 'рм', 'р-', 'roleminus', 'r-'],
        brief='Команда, которая убирает роль из магазина. После этой команды в магазине убирается роль.',
        usage='рольминус <@роль>'
    )
    @has_permissions(manage_roles=True)
    async def _remove_role(self, ctx, role: discord.Role):
        datab.collsp.delete_one({'role_id': role.id})
        await ctx.send(embed=discord.Embed(
            description=f'{ctx.author.mention}, **{role.name}** успешно удалена из магазина.',
            colour=discord.Colour.random()
        ).set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.name))

    @commands.command(
        name='Магазин',
        aliases=['магазин', 'шоп', 'мг', 'shop', 'sp'],
        brief='Команда, которая выведет интерфейс(текст) с ролями сервера, где будет указана сама роль, и её цена.',
        usage='магазин'
    )
    async def _shop(self, ctx):
        emoji = datab.colls.find_one({'for': 'валюта'})['name']
        embed = discord.Embed(title='Магазин', colour=discord.Colour.random())
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.name)
        for row in datab.collsp.find().sort("number", pymongo.ASCENDING):
            embed.add_field(
                name=f'Цена: **{row["cost"]}** {emoji}',
                value=f'**{row["number"]}** | Вы получите: {ctx.guild.get_role(row["role_id"]).mention}',
                inline=False
            )
        await ctx.send(embed=embed)

    @commands.command(
        name='Купить',
        aliases=['купить', 'куп', 'buy'],
        brief='Команда, которая позволяет игроку купить определенную роль в магазине. Если операция покупки прошла успешно, бот должен выдать игроку определенную роль из магазина которую он купил.',
        usage='купить <цифра роли>'
    )
    async def _buy_role(self, ctx, number: int):
        role = ctx.author.guild.get_role(datab.collsp.find_one({'number': number})['role_id'])
        if (role in ctx.author.roles) or (role.id in datab.coll.find_one({'_id': ctx.author.id})['inv_roles']):
            await ctx.send(embed=discord.Embed(
                description=f'{ctx.author.mention}, Вы уже имеете данную роль!',
                colour=discord.Colour.random()
            ).set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.name))
        elif datab.coll.find_one({'_id': ctx.author.id})['balance'] < datab.collsp.find_one({'role_id': role.id})['cost']:
            await ctx.send(embed=discord.Embed(
                description=f'{ctx.author.mention}, эта роль слишком дорогая для вас!',
                colour=discord.Colour.random()
            ).set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.name))
        elif role.id == 856584604013953034:
            cost = datab.collsp.find_one({'role_id': role.id})['cost']
            datab.coll.update_one({'_id': ctx.author.id}, {'$inc': {'balance': -cost}})
            datab.coll.update_one({'_id': ctx.author.id}, {'$push': {'inv_roles': 856584604013953034}})
            await ctx.send(embed=discord.Embed(
                description=f'Вы успешно преобрели роль {role.mention}',
                colour=discord.Colour.random()
            ).set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.name))
        elif role.id == 856791847925317633:
            cost = datab.collsp.find_one({'role_id': role.id})['cost']
            datab.coll.update_one({'_id': ctx.author.id}, {'$inc': {'balance': -cost}})
            datab.coll.update_one({'_id': ctx.author.id}, {'$push': {'inv_roles': 856791847925317633}})
            await ctx.send(embed=discord.Embed(
                description=f'Вы успешно преобрели роль {role.mention}',
                colour=discord.Colour.random()
            ).set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.name))
        else:
            cost = datab.collsp.find_one({'role_id': role.id})['cost']
            datab.coll.update_one({'_id': ctx.author.id}, {'$inc': {'balance': -cost}})
            await ctx.author.add_roles(role)
            await ctx.send(embed=discord.Embed(
                description=f'Вы успешно преобрели роль {role.mention}',
                colour=discord.Colour.random()
            ).set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.name))

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        author = member.id
        if before.channel is None and after.channel is not None:
            t1 = time.time()
            tdict[author] = t1
        elif before.channel is not None and after.channel is None and author in tdict:
            t2 = time.time()
            full_time = t2 - tdict[author]
            datab.coll.update_one({'_id': author}, {'$inc': {'balance': int(round(full_time) // 300)}})
            datab.coll.update_one({'_id': author}, {'$inc': {'in_voice_time': int(round(full_time))}})
            datab.coll.update_one({'_id': author}, {'$inc': {'xp': int(round(full_time) // 300)}})
        if after.channel != None:
            if after.channel.id == 734081948246605906:
                for guild in bot.guilds:
                    maincategory = discord.utils.get(guild.categories, id=734081662861836320)
                    customchannel = await guild.create_voice_channel(name=f'Канал {member.display_name}', category=maincategory)
                    await customchannel.set_permissions(member, connect=True, mute_members=True, move_members=True, manage_channels=True)
                    await member.move_to(customchannel)

                    def check(x, y, z):
                        return len(customchannel.members) == 0

                    await bot.wait_for("voice_state_update", check=check)
                    await customchannel.delete()

    @commands.command(
        name='Cпрятать',
        aliases=['спрятать', 'убрать', 'hide'],
        brief='Команда, которая позволяет игроку спрятать свою роль в инвентарь. Узнать цифру роли можно в магазине',
        usage='спрятать <цифра роли>'
    )
    async def _hide_role(self, ctx, number: int):
        if len(str(number)) < 10:
            role = ctx.author.guild.get_role(datab.collsp.find_one({'number': number})['role_id'])
        else:
            role = ctx.author.guild.get_role(number)
        if role not in ctx.author.roles:
            await ctx.send(embed=discord.Embed(
                description=f'У Вас нет данной роли, или она уже спрятана.',
                colour=discord.Colour.random()
            ).set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.name))
        elif role.id in banned_roles:
            await ctx.send(embed=discord.Embed(
                description=f'Вы пытаетесь спрятать запрещенную роль.',
                colour=discord.Colour.random()
            ).set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.name))
        else:
            datab.coll.update_one({'_id': ctx.author.id}, {'$push': {'inv_roles': role.id}})
            await ctx.author.remove_roles(role)
            await ctx.send(embed=discord.Embed(
                description=f'Вы успешно спрятали роль {role.mention}',
                colour=discord.Colour.random()
            ).set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.name))

    @commands.command(
        name='Достать',
        aliases=['достать', 'взять', 'take'],
        brief='Команда, которая позволяет игроку достать свою роль из инвентаря. Узнать цифру роли можно в магазине',
        usage='достать <цифра роли>'
    )
    async def _take_role(self, ctx, number: int):
        if len(str(number)) < 10:
            role = ctx.author.guild.get_role(datab.collsp.find_one({'number': number})['role_id'])
        else:
            role = ctx.author.guild.get_role(number)
        if role in ctx.author.roles:
            await ctx.send(embed=discord.Embed(
                description=f'У вас уже надета данная роль.',
                colour=discord.Colour.random()
            ).set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.name))
        elif role.id in banned_roles:
            await ctx.send(embed=discord.Embed(
                description=f'Вы пытаетесь достать запрещенную роль.',
                colour=discord.Colour.random()
            ).set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.name))
        elif role.id in datab.coll.find_one({'_id': ctx.author.id})['inv_roles']:
            datab.coll.update_one({'_id': ctx.author.id}, {'$pull': {'inv_roles': role.id}})
            await ctx.author.add_roles(role)
            await ctx.send(embed=discord.Embed(
                description=f'Вы успешно достали роль {role.mention}',
                colour=discord.Colour.random()
            ).set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.name))

    @commands.command(
        name='Инвентарь',
        aliases=['инвентарь', 'инв', 'inv'],
        brief='Команда, которая позволяет игроку посмотреть свои роли в инвентаре.',
        usage='инвентарь'
    )
    async def _user_inventory(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        inventory = datab.coll.find_one({'_id': member.id})['inv_roles']
        embed = discord.Embed(title=f'Инвентарь {member}', colour=discord.Colour.random())
        embed.set_footer(icon_url=ctx.guild.icon_url, text=ctx.guild.name)
        if len(inventory) < 1:
            await ctx.send(embed=discord.Embed(
                title=f'Инвернтарь {member}',
                description=f'У {member.mention} в данный момент нет ролей в инвентаре!'
            ))
        else:
            for roles in inventory:
                role = ctx.guild.get_role(roles)
                embed.add_field(name=f'{datab.collsp.find_one({"role_id": roles})["number"]} | Стоимость: {datab.collsp.find_one({"role_id": roles})["cost"]}', value=f'Название: {role.mention}', inline=False)
            await ctx.send(embed=embed)

    @commands.command(
        name='Забрать-роль',
        aliases=['забрать-роль', 'заб-р', 'atake_r'],
        brief='Команда, которая позволяет админу забрать роль из инвентаря пользователя. Узнать цифру роли можно в магазине',
        usage='забрать-роль <@user> <цифра роли>'
    )
    @has_permissions(administrator=True)
    async def _admin_take_role(self, ctx, member: discord.Member, number: int):
        if len(str(number)) < 10:
            role = ctx.author.guild.get_role(datab.collsp.find_one({'number': number})['role_id'])
        else:
            role = ctx.author.guild.get_role(number)
        if role in member.roles:
            await ctx.send(embed=discord.Embed(
                description=f'Вы пытаетесь забрать надетую роль, данная команда забирает роль из инвенторя.',
                colour=discord.Colour.random()
            ).set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.name))
        elif role.id in datab.coll.find_one({'_id': member.id})['inv_roles']:
            datab.coll.update_one({'_id': member.id}, {'$pull': {'inv_roles': role.id}})
            await ctx.send(embed=discord.Embed(
                description=f'Вы успешно забрали роль {role.mention} из инвенторя {member.mention}.',
                colour=discord.Colour.random()
            ).set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.name))

    @commands.command(
        name='Выдать-роль',
        aliases=['выдать-роль', 'выд-р', 'agive_r'],
        brief='Команда, которая позволяет админу забрать роль из инвентаря пользователя. Узнать цифру роли можно в магазине',
        usage='выдать-роль <@user> <цифра роли>'
    )
    @has_permissions(administrator=True)
    async def _admin_give_role(self, ctx, member: discord.Member, number: int):
        if len(str(number)) < 10:
            role = ctx.author.guild.get_role(datab.collsp.find_one({'number': number})['role_id'])
        else:
            role = ctx.author.guild.get_role(number)

        if role in member.roles:
            await ctx.send(embed=discord.Embed(
                description=f'У пользователя уже есть данная роль.',
                colour=discord.Colour.random()
            ).set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.name))
        elif role.id in datab.coll.find_one({'_id': member.id})['inv_roles']:
            await ctx.send(embed=discord.Embed(
                description=f'У пользователя уже есть данная роль.',
                colour=discord.Colour.random()
            ).set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.name))
        elif role.id in banned_roles:
            await ctx.send(embed=discord.Embed(
                description=f'Вы пытаетесь выдать запрещенную роль.',
                colour=discord.Colour.random()
            ).set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.name))
        else:
            datab.coll.update_one({'_id': member.id}, {'$push': {'inv_roles': role.id}})
            await ctx.send(embed=discord.Embed(
                description=f'Вы успешно выдали роль {role.mention} в инвентарь {member.mention}',
                colour=discord.Colour.random()
            ).set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.name))

    @commands.command(
        name='Продать-роль',
        aliases=['продать-роль', 'прод-р', 'sell_r'],
        brief='Команда, которая позволяет игроку продать роль из инвентаря за полцены. Узнать цифру роли можно в магазине',
        usage='выдать-роль <@user> <цифра роли>'
    )
    async def _user_sell_role(self, ctx, number: int):
        emoji = datab.colls.find_one({'for': 'валюта'})['name']
        if len(str(number)) < 10:
            role = ctx.author.guild.get_role(datab.collsp.find_one({'number': number})['role_id'])
        else:
            role = ctx.author.guild.get_role(number)

        if role in ctx.author.roles:
            await ctx.send(embed=discord.Embed(
                description=f'Роль можно продать только из инвенторя.',
                colour=discord.Colour.random()
            ).set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.name))
        elif role.id in banned_roles:
            await ctx.send(embed=discord.Embed(
                description=f'Вы пытаетесь продать запрещенную роль.',
                colour=discord.Colour.random()
            ).set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.name))
        elif role.id not in datab.coll.find_one({'_id': ctx.author.id})['inv_roles']:
            await ctx.send(embed=discord.Embed(
                description=f'Вы пытаетесь продать роль, которой нет у вас в инвенторе.',
                colour=discord.Colour.random()
            ).set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.name))
        else:
            cost = datab.collsp.find_one({"role_id": role.id})["cost"]
            datab.coll.update_one({'_id': ctx.author.id}, {'$pull': {'inv_roles': role.id}})
            datab.coll.update_one({'_id': ctx.author.id}, {'$inc': {'balance': cost // 2}})
            await ctx.send(embed=discord.Embed(
                description=f'Вы успешно продали роль {role.mention} за **{cost // 2}** {emoji}',
                colour=discord.Colour.random()
            ).set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.name))

    @commands.command(
        name='Розыгрыш',
        aliases=['розыгрыш', 'award', 'роз'],
        brief='Команда которая розыграет денег на баланс.',
        usage='розыгрыш'
    )
    @has_permissions(manage_roles=True)
    async def _award(self, ctx, amount: int, time: str):
        global useri
        useri = []
        emoji = datab.colls.find_one({'for': 'валюта'})['name']
        global money_award
        global times
        money_award = amount
        time_award = ''.join(filter(lambda x: x.isdigit(), time))
        time_zn = ''
        for c in time:
            if c not in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
                time_zn = time_zn + c

        embed = discord.Embed(title='Розыгрыш', colour=discord.Colour.random(), description='Для участия нажмите на реакцию')
        if time_zn == 'сек' or time_zn == 'sec':
            h = int(time_award) // 3600
            m = (int(time_award) // 60) % 60
            s = int(time_award) % 60
            embed.add_field(
                name=f'Розыгрывается {amount} {emoji}',
                value=f'Розыгрыш начал: {ctx.author.mention}',
                inline=False
            )
            embed.add_field(
                name=f'Время действия:',
                value=f'**{h}** ч, **{m}** мин, **{s}** сек.',
                inline=False
            )
            embed.set_footer(icon_url=ctx.guild.icon_url, text='MWZ Розыгрыш')
            mes = await ctx.send(embed=embed)
            await mes.add_reaction('🐥')
            times = int(time_award)
            await asyncio.sleep(times)
            winner = random.choice(useri)
            member = bot.get_user(winner)
            await ctx.send(embed=discord.Embed(
                title='Итоги розыгрыша!',
                description=f'Победителем розыгрыша стал {member.mention}, он получает {money_award} {emoji}',
                colour=discord.Colour.random()
            ).set_footer(icon_url=ctx.guild.icon_url,text='MWZ Розыгрыш'))
            datab.coll.update_one({'_id': winner}, {'$inc': {'balance': money_award}})

        elif time_zn == 'мин' or time_zn == 'min':
            h = int(time_award) // 60
            m = (int(time_award)) % 60
            s = (int(time_award) * 60) % 60
            embed.add_field(
                name=f'Розыгрывается {amount} {emoji}',
                value=f'Розыгрыш начал: {ctx.author.mention}',
                inline=False
            )
            embed.add_field(
                name=f'Время действия:',
                value=f'**{h}** ч, **{m}** мин, **{s}** сек.',
                inline=False
            )
            mes = await ctx.send(embed=embed)
            await mes.add_reaction('🐥')
            times = int(time_award) * 60
            await asyncio.sleep(times)
            winner = random.choice(useri)
            member = bot.get_user(winner)
            await ctx.send(embed=discord.Embed(
                title='Итоги розыгрыша!',
                description=f'Победителем розыгрыша стал {member.mention}, он получает {money_award} {emoji}',
                colour=discord.Colour.random()
            ).set_footer(icon_url=ctx.guild.icon_url,text='MWZ Розыгрыш'))
            datab.coll.update_one({'_id': winner}, {'$inc': {'balance': money_award}})

        elif time_zn == 'ч' or time_zn == 'h':
            h = int(time_award) % 60
            m = (int(time_award) * 60) % 60
            s = (int(time_award) * 3600) % 60
            embed.add_field(
                name=f'Розыгрывается {amount} {emoji}',
                value=f'Розыгрыш начал: {ctx.author.mention}',
                inline=False
            )
            embed.add_field(
                name=f'Время действия:',
                value=f'**{h}** ч, **{m}** мин, **{s}** сек.',
                inline=False
            )
            mes = await ctx.send(embed=embed)
            await mes.add_reaction('🐥')
            times = int(time_award) * 3600
            await asyncio.sleep(times)
            winner = random.choice(useri)
            member = bot.get_user(winner)
            await ctx.send(embed=discord.Embed(
                title='Итоги розыгрыша!',
                description=f'Победителем розыгрыша стал {member.mention}, он получает {money_award} {emoji}',
                colour=discord.Colour.random()
            ).set_footer(icon_url=ctx.guild.icon_url,text='MWZ Розыгрыш'))
            datab.coll.update_one({'_id': winner}, {'$inc': {'balance': money_award}})

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.emoji == '🐥' and not user.bot:
            useri.append(user.id)

    @commands.command(
        name='Активировать',
        aliases=['активировать', 'акт', 'activ'],
        brief='Команда, которая позволяет игроку активировать кастомную роль.',
        usage='активировать <тип(1 - обычная, 2 - показывать отдельно)> <цвет(hex) без #> <название>'
    )
    async def _user_activate_role(self, ctx, value: int, color, *, name: str):
        if value == 1:
            if 856584604013953034 not in datab.coll.find_one({'_id': ctx.author.id})['inv_roles']:
                await ctx.send(embed=discord.Embed(
                    description=f'У Вас нет кастомной роли.',
                    colour=discord.Colour.random()
                ).set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.name))
            else:
                guild = ctx.guild
                role = await guild.create_role(name=f"{name}")
                await role.edit(colour=discord.Colour(int(f"0x{color}", 16)), position=14)
                await ctx.author.add_roles(role)
                await ctx.send(embed=discord.Embed(
                    description=f'Вы успешно создали роль {role.mention}.',
                    colour=discord.Colour.random()
                ).set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.name))
                datab.coll.update_one({'_id': ctx.author.id}, {'$pull': {'inv_roles': 856584604013953034}})
        elif value == 2:
            if 856791847925317633 not in datab.coll.find_one({'_id': ctx.author.id})['inv_roles']:
                await ctx.send(embed=discord.Embed(
                    description=f'У Вас нет кастомной роли.',
                    colour=discord.Colour.random()
                ).set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.name))
            else:
                guild = ctx.guild
                role = await guild.create_role(name=f"{name}")
                await role.edit(colour=discord.Colour(int(f"0x{color}", 16)), position=22, hoist=True)
                await ctx.author.add_roles(role)
                await ctx.send(embed=discord.Embed(
                    description=f'Вы успешно создали роль {role.mention}.',
                    colour=discord.Colour.random()
                ).set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.name))
                datab.coll.update_one({'_id': ctx.author.id}, {'$pull': {'inv_roles': 856791847925317633}})
        else:
            await ctx.send(embed=discord.Embed(
                description=f'Вы ввели неправильный тип кастомной роли.',
                colour=discord.Colour.random()
            ).set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.name))


def setup(bot):
    bot.add_cog(Economy(bot))

