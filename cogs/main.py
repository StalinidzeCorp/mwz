import discord
from discord.ext import commands
from bot import bot
import datab


class Main(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot and main cog successfully loaded!')
        song_name = f'{bot.command_prefix}help'
        activity_type = discord.ActivityType.watching
        await bot.change_presence(activity=discord.Activity(type=activity_type, name=song_name))

    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        embed = discord.Embed(
            title='Помощь по командам',
            description=f'```Чтобы узнать как использовать команду, пропишите {ctx.prefix}команда```',
            colour=discord.Colour.random()
        )
        embed.add_field(name='Магазин', value=f'```магазин\nкупить\nспрятать\nдостать\nпродатьроль\nинвентарь```')
        embed.add_field(name='Личный счет', value=f'```баланс\nбонус\nлидеры\nпередать```')
        embed.add_field(name='Лвл', value=f'```лк\nопыт\nлвл```')
        embed.add_field(name='Модерация', value=f'```верификация\nустановитьбаланс\nдобавить\nзабрать\nустановитьлвл\nдатьлвл\nдатьопыт\nрольплюс\nрольминус\nсимвол\nмут\nразмут\nзабратьроль\nвыдатьроль\nрозыгрыш\nбан```')
        embed.add_field(name='Игры', value=f'```крестикинолики\nкаменьножницыбумага```')
        embed.add_field(name='Эмоции | Действия', value=f'```поцеловать\nпогладить\nшлепнуть\nгрустить\nзлиться\nулыбаться\nпокормить\nплакать\nобнять```')
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
        embed.set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.name)

        await ctx.send(embed=embed)

    @help.command()
    async def магазин(self, ctx):
        embed = discord.Embed(
            title='Магазин',
            description='Команда, которая выведет интерфейс(текст) с ролями сервера, где указана сама роль и её цена.',
            colour=discord.Colour.random()
        )
        embed.add_field(name='Как использовать:', value=f'{ctx.prefix}магазин')
        await ctx.send(embed=embed)

    @help.command()
    async def купить(self, ctx):
        embed = discord.Embed(
            title='Купить',
            description='Команда, которая позволяет игроку купить определенную роль из магазина. Если операция покупки прошла успешно, бот должен выдать игроку роль, которую он купил.',
            colour=discord.Colour.random()
        )
        embed.add_field(name='Как использовать:', value=f'{ctx.prefix}купить <номер роли>')
        await ctx.send(embed=embed)

    @help.command()
    async def рольплюс(self, ctx):
        embed = discord.Embed(
            title='Рольплюс',
            description='Команда для добавления роли в магазин. После этой команды в магазин добавляется роль со своей ценой.',
            colour=discord.Colour.random()
        )
        embed.add_field(name='Как использовать:', value=f'{ctx.prefix}рольплюс <@роль> <цена роли>')
        await ctx.send(embed=embed)

    @help.command()
    async def рольминус(self, ctx):
        embed = discord.Embed(
            title='Рольминус',
            description='Команда, которая убирает роль из магазина. После этой команды в магазине убирается роль.',
            colour=discord.Colour.random()
        )
        embed.add_field(name='Как использовать:', value=f'{ctx.prefix}рольминус <@роль>')
        await ctx.send(embed=embed)

    @help.command()
    async def символ(self, ctx):
        embed = discord.Embed(
            title='Символ',
            description='Команда, которая устанавливает символ валюты сервера.',
            colour=discord.Colour.random()
        )
        embed.add_field(name='Как использовать:', value=f'{ctx.prefix}символ <эмодзи>')
        await ctx.send(embed=embed)

    @help.command()
    async def баланс(self, ctx):
        embed = discord.Embed(
            title='Баланс',
            description='Команда для проверки баланса любого игрока.',
            colour=discord.Colour.random()
        )
        embed.add_field(name='Как использовать:', value=f'{ctx.prefix}баланс\nбаланс <@user>')
        await ctx.send(embed=embed)

    @help.command()
    async def бонус(self, ctx):
        embed = discord.Embed(
            title='Бонус',
            description='Команда, которую вы можете написать один раз в 12 часов. Эта команда даёт игрокам бонус в 100 конфет.',
            colour=discord.Colour.random()
        )
        embed.add_field(name='Как использовать:', value=f'{ctx.prefix}бонус')
        await ctx.send(embed=embed)

    @help.command()
    async def добавить(self, ctx):
        embed = discord.Embed(
            title='Добавить',
            description='Команда, которая даёт игроку возможность передать деньги другому.',
            colour=discord.Colour.random()
        )
        embed.add_field(name='Как использовать:', value=f'{ctx.prefix}добавить <@user> <количество>')
        await ctx.send(embed=embed)

    @help.command()
    async def забрать(self, ctx):
        embed = discord.Embed(
            title='Забрать',
            description='Команда, которая убирает определенную сумму баллов определенному игроку.',
            colour=discord.Colour.random()
        )
        embed.add_field(name='Как использовать:', value=f'{ctx.prefix}забрать <@user> <количество>')
        await ctx.send(embed=embed)

    @help.command()
    async def лидеры(self, ctx):
        embed = discord.Embed(
            title='Лидеры',
            description='Команда, которая показывает игроков топ по деньгам.',
            colour=discord.Colour.random()
        )
        embed.add_field(name='Как использовать:', value=f'{ctx.prefix}лидеры')
        await ctx.send(embed=embed)

    @help.command()
    async def передать(self, ctx):
        embed = discord.Embed(
            title='Передать',
            description='Команда, которая даст игроку возможность передать деньги другому игроку.',
            colour=discord.Colour.random()
        )
        embed.add_field(name='Как использовать:', value=f'{ctx.prefix}передать <@user> <количество>')
        await ctx.send(embed=embed)

    @help.command()
    async def лк(self, ctx):
        embed = discord.Embed(
            title='Личная карточка',
            description='Команда, которая показывает вашу личную карточку.',
            colour=discord.Colour.random()
        )
        embed.add_field(name='Как использовать:', value=f'{ctx.prefix}лк')
        await ctx.send(embed=embed)

    @help.command()
    async def лвл(self, ctx):
        embed = discord.Embed(
            title='Лвл',
            description='Команда, которая показывает ваш уровень.',
            colour=discord.Colour.random()
        )
        embed.add_field(name='Как использовать:', value=f'{ctx.prefix}лвл')
        await ctx.send(embed=embed)

    @help.command()
    async def установитьбаланс(self, ctx):
        embed = discord.Embed(
            title='Установить-баланс',
            description='Команда, которая установит игроку валюту на балансе.',
            colour=discord.Colour.random()
        )
        embed.add_field(name='Как использовать:', value=f'{ctx.prefix}установить-баланс <@user> <количество>')
        await ctx.send(embed=embed)

    @help.command()
    async def установитьлвл(self, ctx):
        embed = discord.Embed(
            title='Установить-лвл',
            description='Команда, которая устанавливает лвл пользователю',
            colour=discord.Colour.random()
        )
        embed.add_field(name='Как использовать:', value=f'{ctx.prefix}установить-лвл <@user> <количество>')
        await ctx.send(embed=embed)

    @help.command()
    async def датьлвл(self, ctx):
        embed = discord.Embed(
            title='Дать-лвл',
            description='Команда, которая выдает лвл пользователю',
            colour=discord.Colour.random()
        )
        embed.add_field(name='Как использовать:', value=f'{ctx.prefix}дать-лвл <@user> <количество>')
        await ctx.send(embed=embed)

    @help.command()
    async def датьопыт(self, ctx):
        embed = discord.Embed(
            title='Дать-опыт',
            description='Команда, которая выдает опыт пользователю',
            colour=discord.Colour.random()
        )
        embed.add_field(name='Как использовать:', value=f'{ctx.prefix}дать-опыт <@user> <количество>')
        await ctx.send(embed=embed)

    @help.command()
    async def верификация(self, ctx):
        embed = discord.Embed(
            title='Верификация',
            description='Создает сообщения с реакциями для верификации.',
            colour=discord.Colour.random()
        )
        embed.add_field(name='Как использовать:', value=f'{ctx.prefix}верификация <текст>')
        await ctx.send(embed=embed)

    @help.command()
    async def крестикинолики(self, ctx):
        embed = discord.Embed(
            title='Крестики-нолики',
            description='Начнет игру: "Крестики нолики"',
            colour=discord.Colour.random()
        )
        embed.add_field(name='Как использовать:', value=f'{ctx.prefix}крестики-нолики <@игрок> <ставка>\n{ctx.prefix}кн <@игрок> <ставка>')
        await ctx.send(embed=embed)

    @help.command()
    async def каменьножницыбумага(self, ctx):
        embed = discord.Embed(
            title='Камень-ножницы-бумага',
            description='Начнет игру: "Камень-ножницы-бумага"',
            colour=discord.Colour.random()
        )
        embed.add_field(name='Как использовать:',
                        value=f'{ctx.prefix}камень-ножницы-бумага <ставка>\n{ctx.prefix}кнб <ставка>')
        await ctx.send(embed=embed)

    @commands.command(
        name='Стримеры',
        aliases=['стримеры', 'streamers'],
        brief='Команда, которая позволяет игроку посмотреть список стримеров.',
        usage='стримеры'
    )
    async def _streamers_mwz(self, ctx):
        embed = discord.Embed(title=f'Стримеры MWZ', colour=discord.Colour.random())
        embed.set_thumbnail(url='https://pubgmania.ru/wp-content/uploads/2017/09/twitch1600-768x768.png')
        streamers = datab.collst.find()
        for streamer in streamers:
            embed.add_field(name=f'{streamer["twitch_link"]}', value=f'Ник: **{streamer["twitch_name"]}** | Дискорд: <@{streamer["_id"]}>', inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Main(bot))


