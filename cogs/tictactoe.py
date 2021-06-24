import asyncio
import discord
from discord.ext import commands
from bot import bot
import random
import datab

player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True


class Tictactoe(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('TicTacToe successfully loaded!')

    @commands.command(
        name='Крестики-нолики',
        aliases=['кн', 'крестики-нолики'],
        brief='Начнет игру: "Крестики нолики"',
        usage='крестики-нолики <@игрок> <ставка>'
    )
    async def tictactoe(self, ctx, p2: discord.Member, amount: int, p1: discord.Member = None):
        global count
        global player1
        global player2
        global turn
        global gameOver
        global money
        money = amount
        if p1 is None:
            p1 = ctx.author
        emoji = datab.colls.find_one({'for': 'валюта'})['name']

        def check(message):
            return (message.author == p2 and (message.content == '+' or message.content == '-')) or (message.author == p1 and (message.content == '+' or message.content == '-'))

        if datab.coll.find_one({'_id': p1.id})['balance'] >= amount and datab.coll.find_one({'_id': p2.id})['balance'] >= amount:
            await ctx.send(f'{p2.mention}, с вами хочет сыграть в крестики нолики {ctx.author.mention}, банк: **{amount*2}** {emoji}, напишите в чат "+" или "-".')
            react = await bot.wait_for('message', check=check)
            if react.content == '+':
                tic_name = ctx.author.name + "'s party"
                channel_name = tic_name
                guild = ctx.guild
                category = bot.get_channel(724546327903731723)
                channel = await guild.create_text_channel(channel_name, category=category)
                overwrite = discord.PermissionOverwrite()
                overwrite.send_messages = True
                overwrite.read_messages = True
                overwrite.read_message_history = True
                overwrite.view_channel = True

                # Задаём права автору сообщения и тегаем
                await channel.set_permissions(p1, overwrite=overwrite)
                await channel.set_permissions(p2, overwrite=overwrite)
                await channel.send(f'<@{p1.id}><@{p2.id}>\nВаш канал для игры крестики нолики создан!')
                if gameOver:
                    global board
                    board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                             ":white_large_square:", ":white_large_square:", ":white_large_square:",
                             ":white_large_square:", ":white_large_square:", ":white_large_square:"]
                    turn = ""
                    gameOver = False
                    count = 0

                    player1 = p1
                    player2 = p2

                    # print the board
                    line = ""
                    for x in range(len(board)):
                        if x == 2 or x == 5 or x == 8:
                            line += " " + board[x]
                            await channel.send(line)
                            line = ""
                        else:
                            line += " " + board[x]

                    # determine who goes first
                    num = random.randint(1, 2)
                    if num == 1:
                        turn = player1
                        embed = discord.Embed(
                            title='Игра началась!',
                            description=f"Это ход <@{player1.id}>\nЧтобы сходить, нужно прописать {ctx.prefix}пост <цифра>",
                            colour=discord.Colour.random()
                        )
                        await channel.send(embed=embed)
                    elif num == 2:
                        turn = player2
                        embed = discord.Embed(
                            title='Игра началась!',
                            description=f"Это ход <@{player2.id}>\nЧтобы сходить, нужно прописать {ctx.prefix}пост <цифра>",
                            colour=discord.Colour.random()
                        )
                        await channel.send(embed=embed)
                else:
                    await ctx.send("Игра уже началась!")
            elif react.content == '-' and ctx.author == p1:
                await ctx.send(f'{p1.mention} отменил игру!')
            else:
                await ctx.send(f'{ctx.author.mention}, {p2.mention} отказался от игры!')
        else:
            await ctx.send("У Вас или у Вашего опонента нехватает денег на балансе!")

    @commands.command(
        name='Поставить',
        aliases=['пост', 'поставить'],
        brief='Ставит ваш символ, в игре крестики нолики',
        usage='поставить <@место>'
    )
    async def place(self, ctx, pos: int):
        global turn
        global player1
        global player2
        global board
        global count
        global gameOver
        emoji = datab.colls.find_one({'for': 'валюта'})['name']
        # channel = ctx.channel

        if not gameOver:
            mark = ""
            if turn == ctx.author:
                if turn == player1:
                    mark = ":regional_indicator_x:"
                elif turn == player2:
                    mark = ":o2:"
                if 0 < pos < 10 and board[pos - 1] == ":white_large_square:":
                    board[pos - 1] = mark
                    count += 1

                    # print the board
                    line = ""
                    for x in range(len(board)):
                        if x == 2 or x == 5 or x == 8:
                            line += " " + board[x]
                            await ctx.send(line)
                            line = ""
                        else:
                            line += " " + board[x]

                    checkWinner(winningConditions, mark)
                    if gameOver:
                        if mark == ':regional_indicator_x:':
                            embed = discord.Embed(
                                title=f'Победа {player1}',
                                description=f'Он(а) получает {money * 2} {emoji}\nДанный канал удалится через 15 секунд!',
                                colour=discord.Colour.random()
                            )
                            await ctx.send(embed=embed)
                            datab.coll.update_one({'_id': player1.id}, {'$inc': {'balance': +money*2}})
                            datab.coll.update_one({'_id': player2.id}, {'$inc': {'balance': -money*2}})
                            await asyncio.sleep(15)
                            await ctx.channel.delete()
                        else:
                            embed = discord.Embed(
                                title=f'Победа {player2}',
                                description=f'Он(а) получает {money*2} {emoji}\nДанный канал удалится через 15 секунд!',
                                colour=discord.Colour.random()
                            )
                            await ctx.send(embed=embed)
                            datab.coll.update_one({'_id': player2.id}, {'$inc': {'balance': +money*2}})
                            datab.coll.update_one({'_id': player1.id}, {'$inc': {'balance': -money*2}})
                            await asyncio.sleep(15)
                            await ctx.channel.delete()

                    elif count >= 9:
                        gameOver = True
                        embed = discord.Embed(
                            title='Это ничья!',
                            description='Данный канал удалится через 15 секунд!',
                            colour=discord.Colour.random()
                        )
                        await ctx.send(embed=embed)
                        await asyncio.sleep(15)
                        await ctx.channel.delete()

                    # switch turns
                    if turn == player1:
                        turn = player2
                    elif turn == player2:
                        turn = player1
                else:
                    await ctx.send("Укажите число от 1 до 9")
            else:
                await ctx.send("Сейчас ход вашего соперника")
        else:
            await ctx.send("Пожалуйста начните новую игру!")


def setup(bot):
    bot.add_cog(Tictactoe(bot))
