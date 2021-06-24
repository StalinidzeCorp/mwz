import discord
from discord.ext import commands
from bot import bot
import random


class Duel(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Duel successfully loaded!')

    @commands.command(
        name='Дуэль',
        aliases=['дуэль', 'ду'],
        brief='Начнет игру: "Дуэль"',
        usage='дуэль <@игрок> <ставка>'
    )
    async def _duel(self, ctx, member: discord.Member, amount: int):
        player1 = ctx.author
        player2 = member
        rand = random.randint(1, 2)
        global money
        money = amount
        if rand == 1:
            player_r = player1
        else:
            player_r = player2
        send = await ctx.send(embed=discord.Embed(
            title='Дуэль',
            description=f'Первым стреляет {player_r}',
            colour=discord.Colour.random()
        ))
        await send.add_reaction('🔫')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel = bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        guild = bot.get_guild(payload.guild_id)
        reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)

        if payload.member.id == bot.user.id:
            return

        shoot1 = 0
        shoot2 = 0

        rand = random.randint(1, 2)
        if rand == 1:
            if reaction.emoji == '🔫':
                await channel.send(embed=discord.Embed(
                    title='Попадание',
                    description=f'{payload.member.mention} попал по противнику!',
                    colour=discord.Colour.random()
                ))
                shoot1 += 1
        else:
            if reaction.emoji == '🔫':
                await channel.send(embed=discord.Embed(
                    title='Ничья',
                    description=f'{payload.member.mention} **не** попал по противнику!',
                    colour=discord.Colour.random()
                ))


def setup(bot):
    bot.add_cog(Duel(bot))

