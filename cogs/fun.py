import discord
from discord.ext import commands
from bot import bot
import os
import random


class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Fun successfully loaded!')

    @commands.command(
        name='Поцеловать',
        aliases=['поцеловать', 'kiss', 'поц'],
        brief='Поцелуй человека.',
        usage='поцеловать <@user>'
    )
    async def _kiss(self, ctx, member: discord.Member):
        await ctx.channel.purge(limit=1)
        gifs = [
            'https://media1.tenor.com/images/78095c007974aceb72b91aeb7ee54a71/tenor.gif?itemid=5095865',
            'https://media1.tenor.com/images/d0cd64030f383d56e7edc54a484d4b8d/tenor.gif?itemid=17382422',
            'https://media1.tenor.com/images/d307db89f181813e0d05937b5feb4254/tenor.gif?itemid=16371489',
            'https://media1.tenor.com/images/02d9cae34993e48ab5bb27763d5ca2fa/tenor.gif?itemid=4874618',
            'https://media1.tenor.com/images/7de89bb0f49de7bb987f0c3908998cd6/tenor.gif?itemid=19827352',
            'https://media1.tenor.com/images/2f23c53755a5c3494a7f54bbcf04d1cc/tenor.gif?itemid=13970544',
            'https://media1.tenor.com/images/d8ef848243e8b78b24589436b5bd3502/tenor.gif?itemid=11831573',
            'https://media1.tenor.com/images/230e9fd40cd15e3f27fc891bac04248e/tenor.gif?itemid=14751754',
            'https://media1.tenor.com/images/ea9a07318bd8400fbfbd658e9f5ecd5d/tenor.gif?itemid=12612515'
        ]
        random_index = random.randrange(len(gifs))
        await ctx.send(embed=discord.Embed(
            description=f'{ctx.author.mention} поцеловал {member.mention}',
            colour=discord.Colour.random()

        ).set_image(url=gifs[random_index]))

    @commands.command(
        name='Обнять',
        aliases=['обнять', 'hug', 'обн'],
        brief='Обними человека.',
        usage='обнять <@user>'
    )
    async def _hug(self, ctx, member: discord.Member):
        await ctx.channel.purge(limit=1);
        gifs = [
            'https://media1.tenor.com/images/969f0f462e4b7350da543f0231ba94cb/tenor.gif?itemid=14246498',
            'https://media1.tenor.com/images/94989f6312726739893d41231942bb1b/tenor.gif?itemid=14106856',
            'https://media1.tenor.com/images/6db54c4d6dad5f1f2863d878cfb2d8df/tenor.gif?itemid=7324587',
            'https://media1.tenor.com/images/1d94b18b89f600cbb420cce85558b493/tenor.gif?itemid=15942846',
            'https://media1.tenor.com/images/78d3f21a608a4ff0c8a09ec12ffe763d/tenor.gif?itemid=16509980',
            'https://media1.tenor.com/images/daffa3b7992a08767168614178cce7d6/tenor.gif?itemid=15249774',
            'https://media1.tenor.com/images/e9d7da26f8b2adbb8aa99cfd48c58c3e/tenor.gif?itemid=14721541',
            'https://media1.tenor.com/images/8af307989eb713d2f3817f0e2fd1676d/tenor.gif?itemid=15793129',
            'https://media1.tenor.com/images/bb841fad2c0e549c38d8ae15f4ef1209/tenor.gif?itemid=10307432'
        ]
        random_index = random.randrange(len(gifs))
        await ctx.send(embed=discord.Embed(
            description=f'{ctx.author.mention} обнял {member.mention}',
            colour=discord.Colour.random()
        ).set_image(url=gifs[random_index]))

    @commands.command(
        name='Ударить',
        aliases=['ударить', 'slap', 'удр'],
        brief='Ударь человека.',
        usage='ударить <@user>'
    )
    async def _slap(self, ctx, member: discord.Member):
        await ctx.channel.purge(limit=1);
        gifs = [
            'https://media1.tenor.com/images/612e257ab87f30568a9449998d978a22/tenor.gif?itemid=16057834',
            'https://media1.tenor.com/images/9ea4fb41d066737c0e3f2d626c13f230/tenor.gif?itemid=7355956',
            'https://media.tenor.com/images/7706cab57a467d057e1c9ac8ff62aac2/tenor.gif',
            'https://media1.tenor.com/images/528ff731635b64037fab0ba6b76d8830/tenor.gif?itemid=17078255',
            'https://media1.tenor.com/images/74db8b0b64e8d539aebebfbb2094ae84/tenor.gif?itemid=15144612',
            'https://media1.tenor.com/images/a9b8bd2060d76ec286ec8b4c61ec1f5a/tenor.gif?itemid=17784858',
            'https://media1.tenor.com/images/e8f880b13c17d61810ac381b2f6a93c3/tenor.gif?itemid=17897236',
            'https://media1.tenor.com/images/6885c7676d8645bf2891138564159713/tenor.gif?itemid=4436362'
        ]
        random_index = random.randrange(len(gifs))
        await ctx.send(embed=discord.Embed(
            description=f'{ctx.author.mention} ударил {member.mention}.',
            colour=discord.Colour.random()
        ).set_image(url=gifs[random_index]))

    @commands.command(
        name='Погладить',
        aliases=['погладить', 'pat', 'погл'],
        brief='Погладь человека.',
        usage='погладить <@user>'
    )
    async def _rub(self, ctx, member: discord.Member):
        await ctx.channel.purge(limit=1);
        gifs = [
            'https://media.tenor.com/images/1bf28037aa310fadf3711e703a65c3f1/tenor.gif',
            'https://media.tenor.com/images/655784ab933734b2f512d64334c1ad56/tenor.gif',
            'https://media.tenor.com/images/5e6da8ab3cd6be7fde6cd33f3ee2a2a1/tenor.gif',
            'https://media.tenor.com/images/656d4b9402e3bfb4f43bfd8b57ccd5d2/tenor.gif',
            'https://media.tenor.com/images/3704fc0c81005f246f960738586d953e/tenor.gif',
            'https://media.tenor.com/images/aba27a0ad6bdd9312566791060da4fe5/tenor.gif',
            'https://media1.tenor.com/images/f5176d4c5cbb776e85af5dcc5eea59be/tenor.gif?itemid=5081286',
            'https://media1.tenor.com/images/8b5711095b0ba786c43b617bf9c675dd/tenor.gif?itemid=15735895',
            'https://media1.tenor.com/images/0d2fb6ad9a6d71c3a018c0b37ffca50b/tenor.gif?itemid=16121044',
            'https://media1.tenor.com/images/55df4c5fb33f3cd05b2f1ac417e050d9/tenor.gif?itemid=6238142'
        ]
        random_index = random.randrange(len(gifs))
        await ctx.send(embed=discord.Embed(
            description=f'{ctx.author.mention} погладил {member.mention}.',
            colour=discord.Colour.random()
        ).set_image(url=gifs[random_index]))

    @commands.command(
        name='Плакать',
        aliases=['плакать', 'cry', 'плк'],
        brief='Плакать.',
        usage='плакать <@user>'
    )
    async def _cry(self, ctx, member: discord.Member):
        await ctx.channel.purge(limit=1);
        gifs = [
            'https://media1.tenor.com/images/98466bf4ae57b70548f19863ca7ea2b4/tenor.gif?itemid=14682297',
            'https://media1.tenor.com/images/ce52606293142a2bd11cda1d3f0dc12c/tenor.gif?itemid=5184314',
            'https://media1.tenor.com/images/2e4d11202bf35e6d14d5a58a0a322402/tenor.gif?itemid=17484634',
            'https://media1.tenor.com/images/e0fbb27f7f829805155140f94fe86a2e/tenor.gif?itemid=15134708',
            'https://media1.tenor.com/images/2c7885c590eecaafc3fea62b260b63b8/tenor.gif?itemid=19105643',
            'https://media1.tenor.com/images/49e4248f18b359dd46f7b60b01d1a4a0/tenor.gif?itemid=5652241',
            'https://media.tenor.com/images/9db8fbf01901b2a1eb217fb2958d5437/tenor.gif',
            'https://media1.tenor.com/images/de730b51400ed4dfb66d04141ea79a2d/tenor.gif?itemid=7353410'
        ]
        random_index = random.randrange(len(gifs))
        await ctx.send(embed=discord.Embed(
            description=f'{ctx.author.mention} плачет из-за {member.mention}.',
            colour=discord.Colour.random()
        ).set_image(url=gifs[random_index]))

    @commands.command(
        name='Покормить',
        aliases=['покормить', 'feed', 'покр'],
        brief='Покорьми человека.',
        usage='покормить <@user>'
    )
    async def _feed(self, ctx, member: discord.Member):
        await ctx.channel.purge(limit=1);
        gifs = [
            'https://media.tenor.com/images/44bbd1d0f2ee93ba2bbfd28c0fed5614/tenor.gif',
            'https://media.tenor.com/images/3b285be5e3dba04126ab4c921555c41f/tenor.gif',
            'https://media1.tenor.com/images/d08d0825019c321f21293c35df8ed6a9/tenor.gif?itemid=9032297',
            'https://media.tenor.com/images/594f4fa19511d5bf892dd71cf55f5f5b/tenor.gif',
            'https://media.tenor.com/images/b2fbac05d7f8f098e744e414f332044b/tenor.gif',
            'https://media1.tenor.com/images/33cfd292d4ef5e2dc533ff73a102c2e6/tenor.gif?itemid=12165913'
        ]
        random_index = random.randrange(len(gifs))
        await ctx.send(embed=discord.Embed(
            description=f'{ctx.author.mention} покормил {member.mention}',
            colour=discord.Colour.random()
        ).set_image(url=gifs[random_index]))

    @commands.command(
        name='Злиться',
        aliases=['злиться', 'angry', 'злит'],
        brief='Злиться.',
        usage='злиться <@user>'
    )
    async def _angry(self, ctx, member: discord.Member):
        await ctx.channel.purge(limit=1);
        gifs = [
            'https://media1.tenor.com/images/66c32f7c84340c36ab34ea8911e81b2f/tenor.gif?itemid=14108774',
            'https://media1.tenor.com/images/83d3206895a105f1733c7a220cf1fc1f/tenor.gif?itemid=14725928',
            'https://media.tenor.com/images/bb7675affb3cb33240712062b865075e/tenor.gif',
            'https://media1.tenor.com/images/2f198dc24f638fc9f16776c8ebd183fd/tenor.gif?itemid=14682313',
            'https://media.tenor.com/images/bb8da9c2472739fd2ecdfdb30b9ca56c/tenor.gif',
            'https://media.tenor.com/images/e96a7278392de70b8c094ffacaf02247/tenor.gif'
        ]
        random_index = random.randrange(len(gifs))
        await ctx.send(embed=discord.Embed(
            description=f'{ctx.author.mention} злится на {member.mention}.',
            colour=discord.Colour.random()
        ).set_image(url=gifs[random_index]))

    @commands.command(
        name='Грустить',
        aliases=['грустить', 'sad', 'грусть'],
        brief='Грустить.',
        usage='грустить'
    )
    async def _sad(self, ctx):
        await ctx.channel.purge(limit=1);
        gifs = [
            'https://media.tenor.com/images/fe743927dbaf6257ca099a4637488ad3/tenor.gif',
            'https://media1.tenor.com/images/c7e34832328f477aebb88bb8be761754/tenor.gif?itemid=20512321',
            'https://media1.tenor.com/images/2e37a812841715dd21e820ea5f583f0c/tenor.gif?itemid=14754373',
            'https://media1.tenor.com/images/63b45759382601618e270a01f301c6f2/tenor.gif?itemid=17415909',
            'https://media1.tenor.com/images/edd5474d03a0756e45c8c42c2be08043/tenor.gif?itemid=15496297',
            'https://media.tenor.com/images/2b2da5f747ba845a264bb87e10330893/tenor.gif'
        ]
        random_index = random.randrange(len(gifs))
        await ctx.send(embed=discord.Embed(
            description=f'{ctx.author.mention} грустит.',
            colour=discord.Colour.random()
        ).set_image(url=gifs[random_index]))

    @commands.command(
        name='Улыбаться',
        aliases=['улыбаться', 'smile', 'улыбка'],
        brief='Улыбаться.',
        usage='улыбаться'
    )
    async def _smile(self, ctx):
        await ctx.channel.purge(limit=1);
        gifs = [
            'https://media1.tenor.com/images/325b3ba6a2beabe21c79b54c6de4e2c7/tenor.gif?itemid=15060821',
            'https://media1.tenor.com/images/c49dc9422aac61eebbf8ae9d42bb26b7/tenor.gif?itemid=15792815',
            'https://media1.tenor.com/images/6bfcbb252a151933a16fe101c77cc9fa/tenor.gif?itemid=19679235',
            'https://media1.tenor.com/images/82b39c323ca376e9bb5844a54973fc42/tenor.gif?itemid=16596386',
            'https://media1.tenor.com/images/148a2f4fbf904d6008ca9c7d71806859/tenor.gif?itemid=17383218',
            'https://media1.tenor.com/images/d40f71dfc053af4995d48de258931f44/tenor.gif?itemid=7909470'
        ]
        random_index = random.randrange(len(gifs))
        await ctx.send(embed=discord.Embed(
            description=f'{ctx.author.mention} улыбается.',
            colour=discord.Colour.random()
        ).set_image(url=gifs[random_index]))


def setup(bot):
    bot.add_cog(Fun(bot))
