import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from bot import bot
import datab
import requests
from PIL import Image, ImageFont, ImageDraw
import io
import pymongo
import random
import typing


class Lvl(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self._cd = commands.CooldownMapping.from_cooldown(1, 60, commands.BucketType.member)

    def get_ratelimit(self, message: discord.Message) -> typing.Optional[int]:
        bucket = self._cd.get_bucket(message)
        return bucket.update_rate_limit()

    @commands.Cog.listener()
    async def on_ready(self):
        print('Lvl cog successfully loaded!')

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            ratelimit = self.get_ratelimit(message)
            if ratelimit is None:
                author_id = message.author.id
                user_id = {"_id": author_id}
                exp = datab.coll.find(user_id)
                for xp in exp:
                    cur_xp = xp["xp"]
                    new_xp = cur_xp + random.randint(1, 15)

                datab.coll.update_one({"_id": author_id}, {"$set": {"xp": new_xp}}, upsert=True)

                lvl = datab.coll.find(user_id)
                for levl in lvl:
                    lvl_start = levl["lvl"]
                    new_level = lvl_start + 1

                if cur_xp >= ((5 * (lvl_start ** 2)) + (50 * lvl_start)) + 95:
                    datab.coll.update_one({"_id": author_id}, {"$set": {"lvl": new_level}}, upsert=True)
                    datab.coll.update_one({"_id": author_id}, {"$set": {"xp": 0}}, upsert=True)
                    await message.channel.send(embed=discord.Embed(
                        description=f'{message.author.mention} повысил свой лвл: **{new_level}**',
                        colour=discord.Colour.random()
                    ))
            else:
                pass
        else:
            return

    @commands.command(
        name='Личная-карточка',
        aliases=['лк', 'личная-карточка'],
        brief='Команда которая показывает вашу личную карточку.',
        usage='лк'
    )
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def _lvl_card(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        img = Image.open('cogs/img/card2.png')
        url_ava = str(member.avatar_url)[:-10]
        response = requests.get(url_ava, stream=True)
        response = Image.open(io.BytesIO(response.content))
        response = response.convert('RGBA')
        response = response.resize((100, 100), Image.ANTIALIAS)
        img.paste(response, (15, 50, 115, 150))

        date_format = "%d.%m.%Y"
        lvl = datab.coll.find_one({'_id': member.id})['lvl']
        money = datab.coll.find_one({'_id': member.id})['balance']
        counter = 0
        for row in datab.coll.find().sort("balance", pymongo.DESCENDING):
            user = ctx.author.guild.get_member(row['_id'])
            counter += 1
            if user.id == member.id:
                break
        counter1 = 0
        for row in datab.coll.find().sort("lvl", pymongo.DESCENDING):
            user = ctx.author.guild.get_member(row['_id'])
            counter1 += 1
            if user.id == member.id:
                break
        in_voice_sec = datab.coll.find_one({'_id': member.id})['in_voice_time']
        h = round(in_voice_sec) // 3600
        m = (round(in_voice_sec) // 60) % 60
        s = round(in_voice_sec) % 60

        role_m = discord.utils.find(lambda r: r.id == 855505956984324166, ctx.author.guild.roles)
        if role_m in member.roles:
            img_ma = Image.open('cogs/img/male.png')
            response = img_ma.convert('RGBA')
            response = response.resize((25, 25), Image.ANTIALIAS)
            img.paste(response, (367, 166, 392, 191))
        role_g = discord.utils.find(lambda r: r.id == 855506090481287178, ctx.author.guild.roles)
        if role_g in member.roles:
            img_fe = Image.open('cogs/img/female.png')
            response = img_fe.convert('RGBA')
            response = response.resize((25, 25), Image.ANTIALIAS)
            img.paste(response, (367, 166, 392, 191))
        role_t = discord.utils.find(lambda r: r.id == 855506122207264788, ctx.author.guild.roles)
        if role_t in member.roles:
            img_tr = Image.open('cogs/img/trans.png')
            response = img_tr.convert('RGBA')
            response = response.resize((25, 25), Image.ANTIALIAS)
            img.paste(response, (367, 166, 392, 191))
        if role_t not in member.roles and role_m not in member.roles and role_g not in member.roles:
            img_st = Image.open('cogs/img/com.jpg')
            response = img_st.convert('RGBA')
            response = response.resize((25, 25), Image.ANTIALIAS)
            img.paste(response, (367, 166, 392, 191))

        idraw = ImageDraw.Draw(img)
        name = member.name
        tag = member.discriminator
        title = ImageFont.truetype('cogs/fonts/Rubik-Medium.ttf', size=24)
        mwz = ImageFont.truetype('cogs/fonts/Rubik-Medium.ttf', size=16)
        headline = ImageFont.truetype('cogs/fonts/Symbola.ttf', size=20, encoding='utf-8')
        gender_t = ImageFont.truetype('cogs/fonts/Symbola.ttf', size=30, encoding='utf-8')
        undertext = ImageFont.truetype('cogs/fonts/Rubik-Medium.ttf', size=16)
        idtext = ImageFont.truetype('cogs/fonts/Rubik-Medium.ttf', size=12)

        idraw.text((17, 7), f'Удостоверение личности MWZ', font=title)
        idraw.text((135, 45), f'{name}#{tag}', font=headline)
        idraw.text((135, 64), f'ID: {member.id}', font=idtext)
        idraw.text((135, 85), f'Лвл: {lvl}', font=mwz)
        idraw.text((280, 85), f'Топ: #{counter1}', font=mwz)
        idraw.text((280, 107), f'Топ: #{counter}', font=mwz)
        idraw.text((135, 107), f'Баланс: {money}', font=mwz)
        idraw.text((16, 155), f'Вошёл на сервер: {member.joined_at.strftime(date_format)}', font=undertext)
        idraw.text((16, 176), f'Создал аккаунт: {member.created_at.strftime(date_format)}', font=undertext)
        idraw.text((135, 130), f'Время в войсе: {h}:{m}:{s}', font=undertext)

        img.save('user_card.png')
        await ctx.send(file=discord.File(fp='user_card.png'))

    @commands.command(
        name='Лвл',
        aliases=['лвл', 'lvl'],
        brief='Команда, которая показывает ваш уровень.',
        usage='лвл'
    )
    async def _lvl(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        lvl = datab.coll.find_one({'_id': member.id})['lvl']
        embed = discord.Embed(
            description=f'Уровень: **{lvl}**',
            colour=discord.Colour.random()
        )
        embed.set_footer(icon_url=member.avatar_url, text=member.name)
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
        await ctx.send(embed=embed)

    @commands.command(
        name='Опыт',
        aliases=['опыт', 'xp', 'хп'],
        brief='Команда, которая показывает ваш текущий опыт.',
        usage='опыт'
    )
    async def _xp(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        lvl_start = datab.coll.find_one({'_id': member.id})['lvl']
        xp = datab.coll.find_one({'_id': member.id})['xp']
        embed = discord.Embed(
            # description=f'Опыт: **{xp}** / **{((5 * (lvl_start ** 2)) + (50 * lvl_start)) + 100}**',
            colour=discord.Colour.random()
        )
        embed.set_footer(icon_url=member.avatar_url, text=member.name)
        embed.add_field(name='Опыт:', value=f'{xp} **/** {((5 * (lvl_start ** 2)) + (50 * lvl_start)) + 100}')
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
        await ctx.send(embed=embed)

    @commands.command(
        name='Дать-лвл',
        aliases=['дать-лвл', 'дл'],
        brief='Команда, которая выдает лвл пользователю',
        usage='дать-лвл'
    )
    @has_permissions(manage_roles=True)
    async def _give_rank(self, ctx, member: discord.Member, amount: int):
        if amount <= 0:
            await ctx.send(embed=discord.Embed(
                description=f'{ctx.author.mention}, Вы ввели недопустимое значение!',
                colour=discord.Colour.random()
            ))
        else:
            datab.coll.update_one({'_id': member.id}, {'$inc': {'lvl': amount}})
            await ctx.send(embed=discord.Embed(
                description=f'Вы добавили **{amount}** лвл {member.mention}',
                colour=discord.Colour.random()
            ).set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.name))

    @commands.command(
        name='Дать-опыт',
        aliases=['дать-опыт', 'до'],
        brief='Команда, которая выдает опыт пользователю',
        usage='дать-опыт <@user> <количество>'
    )
    @has_permissions(manage_roles=True)
    async def _give_xp(self, ctx, member: discord.Member, amount: int):
        if amount <= 0:
            await ctx.send(embed=discord.Embed(
                description=f'{ctx.author.mention}, Вы ввели недопустимое значение!',
                colour=discord.Colour.random()
            ).set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.name))
        else:
            datab.coll.update_one({'_id': member.id}, {'$inc': {'xp': amount}})
            await ctx.send(embed=discord.Embed(
                description=f'Вы добавили **{amount}** xp {member.mention}',
                colour=discord.Colour.random()
            ).set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.name))

    @commands.command(
        name='Установить-лвл',
        aliases=['установить-лвл', 'ул'],
        brief='Команда, которая устанавливает лвл пользователю',
        usage='установить-лвл <@user> <количество>'
    )
    @has_permissions(manage_roles=True)
    async def _set_rank(self, ctx, member: discord.Member, amount: int):
        if amount <= 0:
            await ctx.send(embed=discord.Embed(
                description=f'{ctx.author.mention}, Вы ввели недопустимое значение!',
                colour=discord.Colour.random()
            ).set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.name))
        else:
            datab.coll.update_one({'_id': member.id}, {'$set': {'lvl': amount}})
            await ctx.send(embed=discord.Embed(
                description=f'Вы установили **{amount}** лвл {member.mention}',
                colour=discord.Colour.random()
            ).set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.name))


def setup(bot):
    bot.add_cog(Lvl(bot))
