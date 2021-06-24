import os
import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions, CommandNotFound, has_permissions
import datab

bot = commands.Bot(
    command_prefix='.',
    intents=discord.Intents.all()
)
bot.remove_command('help')


@bot.event
async def on_command_error(ctx, error):
    print(error)

    if isinstance(error, commands.UserInputError):
        embed = discord.Embed(
            title='Вы неправильно использовали команду.',
            description=f'{ctx.command.brief}',
            colour=discord.Colour.random()
        )
        embed.add_field(name='Правильное использование команды:', value=f'`{ctx.prefix}{ctx.command.usage}`')
        embed.set_footer(icon_url=ctx.author.avatar_url, text=ctx.author.name)
        await ctx.send(embed=embed)

    if isinstance(error, commands.CommandOnCooldown):
        hours = round(error.cooldown.per) // 3600
        minutes = (round(error.cooldown.per) // 60) % 60
        sec = round(error.cooldown.per) % 60
        h = round(error.retry_after) // 3600
        m = (round(error.retry_after) // 60) % 60
        s = round(error.retry_after) % 60
        await ctx.send(embed=discord.Embed(
            description=f"Попробуйте через **{h}** ч, **{m}** мин, **{s}** сек.",
            colour=discord.Colour.random()
        ))
        # `{ctx.prefix}{ctx.command.name}` можно использовать только **{error.cooldown.rate}** раз в **{int(hours)}** ч, **{int(minutes)}** мин, **{int(sec)}** сек.

    if isinstance(error, MissingPermissions):
        await ctx.send(embed=discord.Embed(
            description='У вас нет доступа к данной команде!',
            colour=discord.Colour.random()
        ))

    if isinstance(error, CommandNotFound):
        await ctx.send(embed=discord.Embed(
            description=f'Данной команды не существует. Узнать команды можно прописав ``{ctx.prefix}help``',
            colour=discord.Colour.random()
        ))


@bot.command(
    name='Символ',
    aliases=['символ', 'сим'],
    brief='Команда которая устанавливает символ валюты сервера.',
    usage='символ <эмоджи> <для чего>'
)
@has_permissions(manage_roles=True)
async def _set_emoji(ctx, message: str, dla: str):
    if dla != 'валюта':
        await ctx.send(embed=discord.Embed(
            description='Вы указали неверное назначение!',
            colour=discord.Colour.random()
        ))
    datab.colls.update_one({'for': dla}, {'$set': {'name': message}})
    await ctx.send(embed=discord.Embed(
        title='Успешно!',
        description=f'Вы указали новую {dla}: {message}',
        colour=discord.Colour.random()
    ))


@bot.command(aliases=['ld'])
async def load(ctx, extension):
    if ctx.author.id == 284171332516839426:
        bot.load_extension(f'cogs.{extension}')
        await ctx.send('Cog is loaded!')
    else:
        await ctx.send("You don't have permission!")


@bot.command(aliases=['uld'])
async def unload(ctx, extension):
    if ctx.author.id == 284171332516839426:
        bot.unload_extension(f'cogs.{extension}')
        await ctx.send('Cog is unloaded!')
    else:
        await ctx.send("You don't have permission!")


@bot.command(aliases=['rld'])
async def reload(ctx, extension):
    if ctx.author.id == 284171332516839426:
        bot.unload_extension(f'cogs.{extension}')
        bot.load_extension(f'cogs.{extension}')
        await ctx.send('Cog is reloaded!')
    else:
        await ctx.send("You don't have permission!")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


token = os.environ.get('BOT_TOKEN')
bot.run(token)
