import discord
from discord.ext import commands
from bot import bot
import random
import datab


class Kamnojbum(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('KamNojBum successfully loaded!')

    @commands.command(
        name='Камень-ножницы-бумага',
        aliases=['камень-ножницы-бумага', 'кнб'],
        brief='Начнет игру: "Крестики нолики"',
        usage='кнб'
    )
    async def _knm_start(self, ctx, amount: int):
        if datab.coll.find_one({'_id': ctx.author.id})['balance'] >= amount:
            knm = await ctx.send(embed=discord.Embed(
                title='Камень-ножницы-бумага',
                description='Выберите: 👊 | ✌ | ✋',
                colour=discord.Colour.random()
            ))
            await knm.add_reaction('👊')
            await knm.add_reaction('✌')
            await knm.add_reaction('✋')
            global money
            money = amount
        else:
            await ctx.send(embed=discord.Embed(
                description=f'У вас недостаточно денег!',
                colour=discord.Colour.random()
            ))

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel = bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        guild = bot.get_guild(payload.guild_id)
        reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)

        emoji = datab.colls.find_one({'for': 'валюта'})['name']

        if payload.member.id == bot.user.id:
            return

        if reaction.emoji == '👊':
            znak = 1
            comp = random.randint(1, 3)
            if comp == znak:
                await channel.send(embed=discord.Embed(
                    title='Ничья',
                    description=f'Вы показали 👊, бот показал 👊.\nВы ничего не потеряли!',
                    colour=discord.Colour.random()
                ))
            elif comp == 2:
                await channel.send(embed=discord.Embed(
                    title='Победа',
                    description=f'Вы показали 👊, бот показал ✌.\nВы выиграли **{money*2}** {emoji}',
                    colour=discord.Colour.random()
                ))
                datab.coll.update_one({'_id': payload.member.id}, {'$inc': {'balance': +money * 2}})
            elif comp == 3:
                await channel.send(embed=discord.Embed(
                    title='Поражение',
                    description=f'Вы показали 👊, бот показал ✋.\nВы проиграли **{money}** {emoji}',
                    colour=discord.Colour.random()
                ))
                datab.coll.update_one({'_id': payload.member.id}, {'$inc': {'balance': -money}})
        if reaction.emoji == '✌':
            znak = 2
            comp = random.randint(1, 3)
            if comp == znak:
                await channel.send(embed=discord.Embed(
                    title='Ничья',
                    description=f'Вы показали ✌, бот показал ✌.\nВы ничего не потеряли!',
                    colour=discord.Colour.random()
                ))
            elif comp == 3:
                await channel.send(embed=discord.Embed(
                    title='Победа',
                    description=f'Вы показали ✌, бот показал **бумага**.\nВы выиграли **{money * 2}** {emoji}',
                    colour=discord.Colour.random()
                ))
                datab.coll.update_one({'_id': payload.member.id}, {'$inc': {'balance': +money * 2}})
            elif comp == 1:
                await channel.send(embed=discord.Embed(
                    title='Поражение',
                    description=f'Вы показали ✌, бот показал 👊.\nВы проиграли **{money}** {emoji}',
                    colour=discord.Colour.random()
                ))
                datab.coll.update_one({'_id': payload.member.id}, {'$inc': {'balance': -money}})
        if reaction.emoji == '✋':
            znak = 3
            comp = random.randint(1, 3)
            if comp == znak:
                await channel.send(embed=discord.Embed(
                    title='Ничья',
                    description=f'Вы показали ✋, бот показал ✋.\nВы ничего не потеряли!',
                    colour=discord.Colour.random()
                ))
            elif comp == 2:
                await channel.send(embed=discord.Embed(
                    title='Победа',
                    description=f'Вы показали ✋, бот показал 👊.\nВы выиграли **{money * 2}** {emoji}',
                    colour=discord.Colour.random()
                ))
                datab.coll.update_one({'_id': payload.member.id}, {'$inc': {'balance': +money * 2}})
            elif comp == 1:
                await channel.send(embed=discord.Embed(
                    title='Поражение',
                    description=f'Вы показали ✋, бот показал ✌.\nВы проиграли **{money}** {emoji}',
                    colour=discord.Colour.random()
                ))
                datab.coll.update_one({'_id': payload.member.id}, {'$inc': {'balance': -money}})


def setup(bot):
    bot.add_cog(Kamnojbum(bot))
