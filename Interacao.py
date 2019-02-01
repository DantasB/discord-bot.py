"""
The MIT License (MIT)
Copyright (c) 2015-2019 Rapptz
Copyright (c) 2019 DantasB
Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import random
import time
import discord
import datetime
import aiohttp
import json
import typing

from discord.ext import commands
from forex_python.converter import CurrencyRates
from dhooks import Webhook
from discord.utils import get
from discord.ext.commands import has_permissions, MissingPermissions
from horario import*

# gifs
angry = [] #giphy angry links
cave = [] #giphy cave links
slap = [] #giphy slap links
dance = [] #giphy dance links
hug = [] #giphy hug links
kiss = [] #giphy kiss links
attack = [] #giphy attack links
omg = [] #giphy omg links
rage = [] #giphy rage links
end = [] #giphy end links
dead = [] #giphy dead links
alive = [] #giphy alive links
highfives = [] #giphy highfive links

with open('limitador.json', 'r') as file:
    try:
        limitador_log = json.load(file)
    except ValueError:
        limitador_log = {}

        

class Interação:
    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.command()
    async def treta(self, ctx):
        """Todas as tretas do grupo!"""

    @commands.guild_only()
    @commands.command(name='endeline')
    async def endeline(self, ctx):
        gif = random.choice(end)
        endmessage = '**Sem mais vai e vem!**'
        embed = discord.Embed(title="**FIM DE JOGO!**", colour=discord.Colour(0x370c5e),
                              description="{}".format(endmessage))

        embed.set_image(url="{}".format(gif))
        embed.set_footer(icon_url=betina_icon,
                         text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), self.client.user.name,
                                                                                   year()))
        await ctx.send(embed=embed, delete_after=10)

    @commands.cooldown(2, 10, commands.BucketType.user)
    @commands.guild_only()
    @commands.command(name='emputece', aliases=['angry', 'rage'])
    async def emputece(self, ctx, member: discord.Member, membro=None):
        guild_id = str(ctx.guild.id)
        user_id = str(ctx.author.id)
        if guild_id in limitador_log:
            if str(ctx.message.channel.id) == limitador_log[guild_id]:
                if membro == None:
                    membro = ctx.author
                else:
                    if ctx.author == membro == member:
                        await ctx.invoke(self.client.get_command('endeline'))
                        await msg.delete()

                gif = random.choice(rage)

                emputece2 = '{} **Deixou** {} **PUTO!**'.format(membro.mention, member.mention)
                embed = discord.Embed(title="**EMPUTECEU!**", colour=discord.Colour(0x370c5e),
                                      description="{}".format(emputece2))

                embed.set_image(url="{}".format(gif))
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                           self.client.user.name,
                                                                                           year()))
                msg = await ctx.send(embed=embed)
                await msg.add_reaction('😡')

                def check(reaction, user):
                    return user == member and str(reaction.emoji) == "😡"

                try:
                    reaction, user = await self.client.wait_for('reaction_add', check=check)
                except:
                    return
                else:
                    await msg.delete()
                    await ctx.invoke(self.client.get_command('putin'), ctx.author, member)
            else:
                guild = ctx.guild.get_channel(int(limitador_log[guild_id]))
                await ctx.send(f'Esse não foi o canal definido para usar os comandos. Tente utilizar o canal {guild}')
                return
        else:
            if membro == None:
                membro = ctx.author
            else:
                if ctx.author == membro == member:
                    await ctx.invoke(self.client.get_command('endeline'))
                    await msg.delete()

            gif = random.choice(rage)

            emputece2 = '{} **Deixou** {} **PUTO!**'.format(membro.mention, member.mention)
            embed = discord.Embed(title="**EMPUTECEU!**", colour=discord.Colour(0x370c5e),
                                  description="{}".format(emputece2))

            embed.set_image(url="{}".format(gif))
            embed.set_footer(icon_url=betina_icon,
                             text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), self.client.user.name,
                                                                                       year()))
            msg = await ctx.send(embed=embed)
            await msg.add_reaction('😡')

            def check(reaction, user):
                return user == member and str(reaction.emoji) == "😡"

            try:
                reaction, user = await self.client.wait_for('reaction_add', check=check)
            except:
                return
            else:
                await msg.delete()
                await ctx.invoke(self.client.get_command('putin'), ctx.author, member)

    @emputece.error
    async def emputece_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'member':
                embed = discord.Embed(title="Comando $emputece:", colour=discord.Colour(0x370c5e),
                                      description="Emputece o usuário\n \n**Como usar: $emputece <usuário>**")

                embed.set_author(name="Betina#9182",
                                 icon_url=betina_icon)
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                           self.client.user.name,
                                                                                           year()))

                embed.add_field(name="📖**Exemplos:**", value="$emputece @fulano\n$emputece @sicrano", inline=False)
                embed.add_field(name="🔀**Outros Comandos**", value="``$rage, $angry.``", inline=False)

                msg = await ctx.send(embed=embed)
                await msg.add_reaction("❓")


    @commands.guild_only()
    @commands.command(name='putin')
    async def putin(self, ctx, member: discord.Member, membro=None):
        gif = random.choice(rage)

        emputece1 = '**SAI DA FRENTE QUE AGORA EU TO PUTA CONTIGO!**. \n\nEU VOU MATAR o ' \
                    'usuário {}'.format(ctx.author.mention)
        emputece2 = '{} **Deixou** {} **MAIS PUTO AINDA !**'.format(membro.mention, member.mention)

        embed = discord.Embed(title="**EMPUTECEU MAIS AINDA !**", colour=discord.Colour(0x370c5e),
                                description="{}".format(emputece2))

        embed.set_image(url="{}".format(gif))
        embed.set_footer(icon_url=betina_icon,
                         text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), self.client.user.name,
                                                                                   year()))
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('😡')

        def check(reaction, user):
            return user == member and str(reaction.emoji) == "😡"

        try:
            reaction, user = await self.client.wait_for('reaction_add', check=check)
        except:
            return
        else:
            await msg.delete()
            await ctx.invoke(self.client.get_command('endeline'))

    @commands.cooldown(2, 10, commands.BucketType.user)
    @commands.guild_only()
    @commands.command(name='bate', aliases=['hit', 'punch'])
    async def bate(self, ctx, member: discord.Member, membro=None):
        guild_id = str(ctx.guild.id)
        user_id = str(ctx.author.id)
        if guild_id in limitador_log:
            if str(ctx.message.channel.id) == limitador_log[guild_id]:
                if membro == None:
                    membro = ctx.author
                else:
                    if ctx.author == member == membro:
                        await ctx.invoke(self.client.get_command('endeline'))
                        await msg.delete()

                """<membro>: Tome cuidado com isso."""
                gif = random.choice(slap)

                bate2 = '{} **deu um tapa em** {}'.format(membro.mention, member.mention)
                embed = discord.Embed(title="**Tapão!**", colour=discord.Colour(0x370c5e),
                                      description="{}".format(bate2))

                embed.set_image(url="{}".format(gif))
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                           self.client.user.name,
                                                                                           year()))
                msg = await ctx.send(embed=embed)

                await msg.add_reaction("🔙")

                def check(reaction, user):
                    return user == member and str(reaction.emoji) == "🔙"

                try:
                    reaction, user = await self.client.wait_for('reaction_add', check=check)
                except:
                    return
                else:
                    await msg.delete()
                    await ctx.invoke(self.client.get_command('bate'), ctx.author, member)
            else:
                guild = ctx.guild.get_channel(int(limitador_log[guild_id]))
                await ctx.send(f'Esse não foi o canal definido para usar os comandos. Tente utilizar o canal {guild}')
                return
        else:
            if membro == None:
                membro = ctx.author
            else:
                if ctx.author == member == membro:
                    await ctx.invoke(self.client.get_command('endeline'))
                    await msg.delete()

            """<membro>: Tome cuidado com isso."""
            gif = random.choice(slap)

            bate2 = '{} **deu um tapa em** {}'.format(membro.mention, member.mention)
            embed = discord.Embed(title="**Tapão!**", colour=discord.Colour(0x370c5e), description="{}".format(bate2))

            embed.set_image(url="{}".format(gif))
            embed.set_footer(icon_url=betina_icon,
                             text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), self.client.user.name,
                                                                                       year()))
            msg = await ctx.send(embed=embed)

            await msg.add_reaction("🔙")

            def check(reaction, user):
                return user == member and str(reaction.emoji) == "🔙"

            try:
                reaction, user = await self.client.wait_for('reaction_add', check=check)
            except:
                return
            else:
                await msg.delete()
                await ctx.invoke(self.client.get_command('bate'), ctx.author, member)

    @bate.error
    async def bate_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'member':
                embed = discord.Embed(title="Comando $bate:", colour=discord.Colour(0x370c5e),
                                      description="Bate no usuário\n \n**Como usar: $bate <usuário>**")

                embed.set_author(name="Betina#9182",
                                 icon_url=betina_icon)
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                           self.client.user.name,
                                                                                           year()))

                embed.add_field(name="📖**Exemplos:**", value="$bate @fulano\n$bate @sicrano", inline=False)
                embed.add_field(name="🔀**Outros Comandos**", value="``$hit, $punch.``", inline=False)

                msg = await ctx.send(embed=embed)
                await msg.add_reaction("❓")


    @commands.cooldown(2, 10, commands.BucketType.user)
    @commands.guild_only()
    @commands.command(name='abraça', aliases=['hug', 'abraço'])
    async def abraça(self, ctx, member: discord.Member, membro=None):
        guild_id = str(ctx.guild.id)
        user_id = str(ctx.author.id)
        if guild_id in limitador_log:
            if str(ctx.message.channel.id) == limitador_log[guild_id]:
                if membro == None:
                    membro = ctx.author
                else:
                    if ctx.author == member == membro:
                        await ctx.invoke(self.client.get_command('endeline'))
                        await msg.delete()

                """<membro>: Use isso com amor <3."""
                gif = random.choice(hug)

                abraça2 = '{} **deu um abraço em** {}'.format(membro.mention, member.mention)

                embed = discord.Embed(title="**Abraço!**", colour=discord.Colour(0x370c5e),
                                      description="{}".format(abraça2))

                embed.set_image(url="{}".format(gif))
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                           self.client.user.name,
                                                                                           year()))
                msg = await ctx.send(embed=embed)

                await msg.add_reaction("🔙")

                def check(reaction, user):
                    return user == member and str(reaction.emoji) == "🔙"

                try:
                    reaction, user = await self.client.wait_for('reaction_add', check=check)
                except:
                    return
                else:
                    await msg.delete()
                    await ctx.invoke(self.client.get_command('abraça'), ctx.author, member)
            else:
                guild = ctx.guild.get_channel(int(limitador_log[guild_id]))
                await ctx.send(f'Esse não foi o canal definido para usar os comandos. Tente utilizar o canal {guild}')
                return
        else:
            if membro == None:
                membro = ctx.author
            else:
                if ctx.author == member == membro:
                    await ctx.invoke(self.client.get_command('endeline'))
                    await msg.delete()

            """<membro>: Use isso com amor <3."""
            gif = random.choice(hug)

            abraça2 = '{} **deu um abraço em** {}'.format(membro.mention, member.mention)

            embed = discord.Embed(title="**Abraço!**", colour=discord.Colour(0x370c5e),
                                  description="{}".format(abraça2))

            embed.set_image(url="{}".format(gif))
            embed.set_footer(icon_url=betina_icon,
                             text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), self.client.user.name,
                                                                                       year()))
            msg = await ctx.send(embed=embed)

            await msg.add_reaction("🔙")

            def check(reaction, user):
                return user == member and str(reaction.emoji) == "🔙"

            try:
                reaction, user = await self.client.wait_for('reaction_add', check=check)
            except:
                return
            else:
                await msg.delete()
                await ctx.invoke(self.client.get_command('abraça'), ctx.author, member)

    @abraça.error
    async def abraça_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'member':
                embed = discord.Embed(title="Comando $abraça:", colour=discord.Colour(0x370c5e),
                                      description="Abraça o usuário\n \n**Como usar: $abraça <usuário>**")

                embed.set_author(name="Betina#9182",
                                 icon_url=betina_icon)
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                           self.client.user.name,
                                                                                           year()))

                embed.add_field(name="📖**Exemplos:**", value="$abraça @fulano\n$abraça @sicrano", inline=False)
                embed.add_field(name="🔀**Outros Comandos**", value="``$hug, $abraço.``", inline=False)

                msg = await ctx.send(embed=embed)
                await msg.add_reaction("❓")


    @commands.cooldown(2, 10, commands.BucketType.user)
    @commands.guild_only()
    @commands.command(name='beija', aliases=['kiss', 'beijou'])
    async def beija(self, ctx, member: discord.Member, membro=None):
        guild_id = str(ctx.guild.id)
        user_id = str(ctx.author.id)
        if guild_id in limitador_log:
            if str(ctx.message.channel.id) == limitador_log[guild_id]:
                if membro == None:
                    membro = ctx.author
                else:
                    if ctx.author == member == membro:
                        await ctx.invoke(self.client.get_command('endeline'))
                        await msg.delete()

                """<membro>: Use isso com amor <3."""
                gif1 = random.choice(slap)
                gif2 = random.choice(kiss)
                beija2 = '{} **deu um beijo em** {}'.format(membro.mention, member.mention)

                embed = discord.Embed(title="**Beijo!**", colour=discord.Colour(0x370c5e),
                                      description="{}".format(beija2))

                embed.set_image(url="{}".format(gif2))
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                           self.client.user.name,
                                                                                           year()))
                msg = await ctx.send(embed=embed)

                await msg.add_reaction("🔙")

                def check(reaction, user):
                    return user == member and str(reaction.emoji) == "🔙"

                try:
                    reaction, user = await self.client.wait_for('reaction_add', check=check)
                except:
                    return
                else:
                    await msg.delete()
                    await ctx.invoke(self.client.get_command('beija'), ctx.author, member)
            else:
                guild = ctx.guild.get_channel(int(limitador_log[guild_id]))
                await ctx.send(f'Esse não foi o canal definido para usar os comandos. Tente utilizar o canal {guild}')
                return
        else:
            if membro == None:
                membro = ctx.author
            else:
                if ctx.author == member == membro:
                    await ctx.invoke(self.client.get_command('endeline'))
                    await msg.delete()

            """<membro>: Use isso com amor <3."""
            gif1 = random.choice(slap)
            gif2 = random.choice(kiss)
            beija2 = '{} **deu um beijo em** {}'.format(membro.mention, member.mention)

            embed = discord.Embed(title="**Beijo!**", colour=discord.Colour(0x370c5e), description="{}".format(beija2))

            embed.set_image(url="{}".format(gif2))
            embed.set_footer(icon_url=betina_icon,
                             text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), self.client.user.name,
                                                                                       year()))
            msg = await ctx.send(embed=embed)

            await msg.add_reaction("🔙")

            def check(reaction, user):
                return user == member and str(reaction.emoji) == "🔙"

            try:
                reaction, user = await self.client.wait_for('reaction_add', check=check)
            except:
                return
            else:
                await msg.delete()
                await ctx.invoke(self.client.get_command('beija'), ctx.author, member)

    @beija.error
    async def beija_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'member':
                embed = discord.Embed(title="Comando $beija:", colour=discord.Colour(0x370c5e),
                                      description="Beija o usuário\n \n**Como usar: $beija <usuário>**")

                embed.set_author(name="Betina#9182",
                                 icon_url=betina_icon)
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                           self.client.user.name,
                                                                                           year()))

                embed.add_field(name="📖**Exemplos:**", value="$beija @fulano\n$beija @sicrano", inline=False)
                embed.add_field(name="🔀**Outros Comandos**", value="``$kiss, $beijou.``", inline=False)

                msg = await ctx.send(embed=embed)
                await msg.add_reaction("❓")


    @commands.command()
    async def tnc(self, ctx):
        guild_id = str(ctx.guild.id)
        user_id = str(ctx.author.id)
        if guild_id in limitador_log:
            if str(ctx.message.channel.id) == limitador_log[guild_id]:
                gif1 = random.choice(angry)
                gif2 = random.choice(omg)

                person = random.choice(list(ctx.guild.members))

                tnc1 = '{} mandou {} tomar no cu!'.format(ctx.author.mention, person.mention)

                embed = discord.Embed(title="**Raiva!**", colour=discord.Colour(0x370c5e),
                                      description="{}".format(tnc1))
                embed.set_image(url="{}".format(gif2))
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                           self.client.user.name,
                                                                                           year()))
                msg = await ctx.send(embed=embed)
                await msg.add_reaction('😮')
            else:
                guild = ctx.guild.get_channel(int(limitador_log[guild_id]))
                await ctx.send(f'Esse não foi o canal definido para usar os comandos. Tente utilizar o canal {guild}')
                return
        else:
            gif1 = random.choice(angry)
            gif2 = random.choice(omg)

            person = random.choice(list(ctx.guild.members))

            tnc1 = '{} mandou {} tomar no cu!'.format(ctx.author.mention, person.mention)

            embed = discord.Embed(title="**Raiva!**", colour=discord.Colour(0x370c5e), description="{}".format(tnc1))
            embed.set_image(url="{}".format(gif2))
            embed.set_footer(icon_url=betina_icon,
                             text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), self.client.user.name,
                                                                                       year()))
            msg = await ctx.send(embed=embed)
            await msg.add_reaction('😮')

    @commands.cooldown(2, 10, commands.BucketType.user)
    @commands.guild_only()
    @commands.command(name='voltapracaverna', aliases=['caverna', 'goback'])
    async def voltapracaverna(self, ctx, member: discord.Member, membro=None):
        guild_id = str(ctx.guild.id)
        user_id = str(ctx.author.id)
        if guild_id in limitador_log:
            if str(ctx.message.channel.id) == limitador_log[guild_id]:
                if membro == None:
                    membro = ctx.author
                else:
                    if ctx.author == member == membro:
                        await ctx.invoke(self.client.get_command('endeline'))
                        await msg.delete()

                """<membro>: Use isso com amor <3."""
                gif = random.choice(cave)

                cave2 = '{} **mandou** {} **de volta pra caverna**'.format(membro.mention, member.mention)

                embed = discord.Embed(title="**Volta pra Caverna!**", colour=discord.Colour(0x370c5e),
                                      description="{}".format(cave2))
                embed.set_image(url="{}".format(gif))
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                           self.client.user.name,
                                                                                           year()))
                msg = await ctx.send(embed=embed)

                await msg.add_reaction("🔙")

                def check(reaction, user):
                    return user == member and str(reaction.emoji) == "🔙"

                try:
                    reaction, user = await self.client.wait_for('reaction_add', check=check)
                except:
                    return
                else:
                    await msg.delete()
                    await ctx.invoke(self.client.get_command('voltapracaverna'), ctx.author, member)
            else:
                guild = ctx.guild.get_channel(int(limitador_log[guild_id]))
                await ctx.send(f'Esse não foi o canal definido para usar os comandos. Tente utilizar o canal {guild}')
                return
        else:
            if membro == None:
                membro = ctx.author
            else:
                if ctx.author == member == membro:
                    await ctx.invoke(self.client.get_command('endeline'))
                    await msg.delete()

            """<membro>: Use isso com amor <3."""
            gif = random.choice(cave)

            cave2 = '{} **mandou** {} **de volta pra caverna**'.format(membro.mention, member.mention)

            embed = discord.Embed(title="**Volta pra Caverna!**", colour=discord.Colour(0x370c5e),
                                  description="{}".format(cave2))
            embed.set_image(url="{}".format(gif))
            embed.set_footer(icon_url=betina_icon,
                             text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), self.client.user.name,
                                                                                       year()))
            msg = await ctx.send(embed=embed)

            await msg.add_reaction("🔙")

            def check(reaction, user):
                return user == member and str(reaction.emoji) == "🔙"

            try:
                reaction, user = await self.client.wait_for('reaction_add', check=check)
            except:
                return
            else:
                await msg.delete()
                await ctx.invoke(self.client.get_command('voltapracaverna'), ctx.author, member)

    @voltapracaverna.error
    async def voltapracaverna_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'member':
                embed = discord.Embed(title="Comando $voltapracaverna:", colour=discord.Colour(0x370c5e),
                                      description="Manda o usuário de volta pra caverna\n \n**Como usar: $volta pra caverna"
                                                  " <usuário>**")

                embed.set_author(name="Betina#9182",
                                 icon_url=betina_icon)
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                           self.client.user.name,
                                                                                           year()))

                embed.add_field(name="📖**Exemplos:**", value="$voltapracaverna @fulano\n$voltapracaverna"
                                                              " @sicrano", inline=False)
                embed.add_field(name="🔀**Outros Comandos**", value="``$caverna, $goback.``", inline=False)

                msg = await ctx.send(embed=embed)
                await msg.add_reaction("❓")


    @commands.cooldown(2, 10, commands.BucketType.user)
    @commands.guild_only()
    @commands.command(name='dança', aliases=['dance', 'dançar'])
    async def dança(self, ctx, member: discord.Member, membro=None):
        guild_id = str(ctx.guild.id)
        user_id = str(ctx.author.id)
        if guild_id in limitador_log:
            if str(ctx.message.channel.id) == limitador_log[guild_id]:
                if membro == None:
                    membro = ctx.author
                else:
                    if ctx.author == member == membro:
                        await ctx.invoke(self.client.get_command('endeline'))
                        await msg.delete()

                """<membro>: Use isso com amor <3."""
                gif = random.choice(dance)

                dança2 = '{} **começou a dançar com** {}'.format(membro.mention, member.mention)

                embed = discord.Embed(title="**Dançante!**", colour=discord.Colour(0x370c5e),
                                      description="{}".format(dança2))
                embed.set_image(url="{}".format(gif))
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                           self.client.user.name,
                                                                                           year()))
                msg = await ctx.send(embed=embed)

                await msg.add_reaction("🔙")

                def check(reaction, user):
                    return user == member and str(reaction.emoji) == "🔙"

                try:
                    reaction, user = await self.client.wait_for('reaction_add', check=check)
                except:
                    return
                else:
                    await msg.delete()
                    await ctx.invoke(self.client.get_command('dança'), ctx.author, member)
            else:
                guild = ctx.guild.get_channel(int(limitador_log[guild_id]))
                await ctx.send(f'Esse não foi o canal definido para usar os comandos. Tente utilizar o canal {guild}')
                return
        else:
            if membro == None:
                membro = ctx.author
            else:
                if ctx.author == member == membro:
                    await ctx.invoke(self.client.get_command('endeline'))
                    await msg.delete()

            """<membro>: Use isso com amor <3."""
            gif = random.choice(dance)

            dança2 = '{} **começou a dançar com** {}'.format(membro.mention, member.mention)

            embed = discord.Embed(title="**Dançante!**", colour=discord.Colour(0x370c5e),
                                  description="{}".format(dança2))
            embed.set_image(url="{}".format(gif))
            embed.set_footer(icon_url=betina_icon,
                             text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), self.client.user.name,
                                                                                       year()))
            msg = await ctx.send(embed=embed)

            await msg.add_reaction("🔙")

            def check(reaction, user):
                return user == member and str(reaction.emoji) == "🔙"

            try:
                reaction, user = await self.client.wait_for('reaction_add', check=check)
            except:
                return
            else:
                await msg.delete()
                await ctx.invoke(self.client.get_command('dança'), ctx.author, member)

    @dança.error
    async def dança_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'member':
                embed = discord.Embed(title="Comando $dança:", colour=discord.Colour(0x370c5e),
                                      description="Dança com o usuário\n \n**Como usar: $dança <usuário>**")

                embed.set_author(name="Betina#9182",
                                 icon_url=betina_icon)
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                           self.client.user.name,
                                                                                           year()))

                embed.add_field(name="📖**Exemplos:**", value="$dança @fulano\n$dança @sicrano", inline=False)
                embed.add_field(name="🔀**Outros Comandos**", value="``$dance, $dançar.``", inline=False)

                msg = await ctx.send(embed=embed)
                await msg.add_reaction("❓")


    @commands.cooldown(2, 10, commands.BucketType.user)
    @commands.guild_only()
    @commands.command(name='ataca', aliases=['attack', 'atacar'])
    async def ataca(self, ctx, member: discord.Member, membro=None):
        guild_id = str(ctx.guild.id)
        user_id = str(ctx.author.id)
        if guild_id in limitador_log:
            if str(ctx.message.channel.id) == limitador_log[guild_id]:
                if membro == None:
                    membro = ctx.author
                else:
                    if ctx.author == member == membro:
                        await ctx.invoke(self.client.get_command('endeline'))
                        await msg.delete()
                """<membro>: Cuidado com isso!"""
                gif = random.choice(attack)
                ataca2 = '{} **deu um ataque em** {}'.format(membro.mention, member.mention)

                embed = discord.Embed(title="**Ataque!**", colour=discord.Colour(0x370c5e),
                                      description="{}".format(ataca2))
                embed.set_image(url="{}".format(gif))
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                           self.client.user.name,
                                                                                           year()))
                msg = await ctx.send(embed=embed)

                await msg.add_reaction("🔙")

                def check(reaction, user):
                    return user == member and str(reaction.emoji) == "🔙"

                try:
                    reaction, user = await self.client.wait_for('reaction_add', check=check)
                except:
                    return
                else:
                    await msg.delete()
                    await ctx.invoke(self.client.get_command('ataca'), ctx.author, member)
            else:
                guild = ctx.guild.get_channel(int(limitador_log[guild_id]))
                await ctx.send(f'Esse não foi o canal definido para usar os comandos. Tente utilizar o canal {guild}')
                return
        else:
            if membro == None:
                membro = ctx.author
            else:
                if ctx.author == member == membro:
                    await ctx.invoke(self.client.get_command('endeline'))
                    await msg.delete()
            """<membro>: Cuidado com isso!"""
            gif = random.choice(attack)
            ataca2 = '{} **deu um ataque em** {}'.format(membro.mention, member.mention)

            embed = discord.Embed(title="**Ataque!**", colour=discord.Colour(0x370c5e), description="{}".format(ataca2))
            embed.set_image(url="{}".format(gif))
            embed.set_footer(icon_url=betina_icon,
                             text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), self.client.user.name,
                                                                                       year()))
            msg = await ctx.send(embed=embed)

            await msg.add_reaction("🔙")

            def check(reaction, user):
                return user == member and str(reaction.emoji) == "🔙"

            try:
                reaction, user = await self.client.wait_for('reaction_add', check=check)
            except:
                return
            else:
                await msg.delete()
                await ctx.invoke(self.client.get_command('ataca'), ctx.author, member)

    @ataca.error
    async def ataca_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'member':
                embed = discord.Embed(title="Comando $ataca:", colour=discord.Colour(0x370c5e),
                                      description="ataca o usuário\n \n**Como usar: $ataca <usuário>**")

                embed.set_author(name="Betina#9182",
                                 icon_url=betina_icon)
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                           self.client.user.name,
                                                                                           year()))

                embed.add_field(name="📖**Exemplos:**", value="$ataca @fulano\n$ataca @sicrano", inline=False)
                embed.add_field(name="🔀**Outros Comandos**", value="``$attack, $atacar.``", inline=False)

                msg = await ctx.send(embed=embed)
                await msg.add_reaction("❓")


    @commands.cooldown(2, 10, commands.BucketType.user)
    @commands.guild_only()
    @commands.command(name='ship', aliases=['shipar', 'shipou'])
    async def ship(self, ctx, member: discord.Member, membro: discord.Member = None):
        guild_id = str(ctx.guild.id)
        user_id = str(ctx.author.id)
        if guild_id in limitador_log:
            if str(ctx.message.channel.id) == limitador_log[guild_id]:
                if membro == None:
                    membro = ctx.author
                else:
                    if ctx.author == member == membro:
                        await ctx.invoke(self.client.get_command('endeline'))
                        await msg.delete()
                """<membro>: Cuidado com isso!"""
                gif = random.choice(ship)
                ataca2 = '{} e {} **Formaram um casal!**'.format(membro.mention, member.mention)

                embed = discord.Embed(title="**Shipados!**", colour=discord.Colour(0x370c5e),
                                      description="{}".format(ataca2))
                embed.set_image(url="{}".format(gif))
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                           self.client.user.name,
                                                                                           year()))
                msg = await ctx.send(embed=embed)

                await msg.add_reaction("🔙")

                def check(reaction, user):
                    return user == member and str(reaction.emoji) == "🔙"

                try:
                    reaction, user = await self.client.wait_for('reaction_add', check=check)
                except:
                    return
                else:
                    await msg.delete()
                    await ctx.invoke(self.client.get_command('ship'), ctx.author, member)
            else:
                guild = ctx.guild.get_channel(int(limitador_log[guild_id]))
                await ctx.send(f'Esse não foi o canal definido para usar os comandos. Tente utilizar o canal {guild}')
                return
        else:
            if membro == None:
                membro = ctx.author
            else:
                if ctx.author == member == membro:
                    await ctx.invoke(self.client.get_command('endeline'))
                    await msg.delete()
            """<membro>: Cuidado com isso!"""
            gif = random.choice(ship)
            ataca2 = '{} e {} **Formaram um casal!**'.format(membro.mention, member.mention)

            embed = discord.Embed(title="**Shipados!**", colour=discord.Colour(0x370c5e),
                                  description="{}".format(ataca2))
            embed.set_image(url="{}".format(gif))
            embed.set_footer(icon_url=betina_icon,
                             text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), self.client.user.name,
                                                                                       year()))
            msg = await ctx.send(embed=embed)

            await msg.add_reaction("🔙")

            def check(reaction, user):
                return user == member and str(reaction.emoji) == "🔙"

            try:
                reaction, user = await self.client.wait_for('reaction_add', check=check)
            except:
                return
            else:
                await msg.delete()
                await ctx.invoke(self.client.get_command('ship'), ctx.author, member)

    @ship.error
    async def ship_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'member':
                embed = discord.Embed(title="Comando $ship:", colour=discord.Colour(0x370c5e),
                                      description="Inicia um novo casal!\n \n**Como usar: $ship <usuário1> <usuário2> (opcional)**")

                embed.set_author(name="Betina#9182",
                                 icon_url=betina_icon)
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                           self.client.user.name,
                                                                                           year()))

                embed.add_field(name="📖**Exemplos:**", value="$ship @fulano @sicrano\n$ship @sicrano", inline=False)
                embed.add_field(name="🔀**Outros Comandos**", value="``$shipar, $shipou.``", inline=False)

                msg = await ctx.send(embed=embed)
                await msg.add_reaction("❓")


    @commands.guild_only()
    @commands.command(name='roletarussa', aliases=['roleta', 'rr'])
    async def roletarussa(self, ctx):
        if ctx.message.author.avatar_url_as(static_format='png')[54:].startswith('a_'):
            avi = ctx.message.author.avatar_url.rsplit("?", 1)[0]
        else:
            avi = ctx.message.author.avatar_url_as(static_format='png')
        guild_id = str(ctx.guild.id)
        user_id = str(ctx.author.id)
        if guild_id in limitador_log:
            if str(ctx.message.channel.id) == limitador_log[guild_id]:
                gif1 = random.choice(dead)
                gif2 = random.choice(alive)

                embed = discord.Embed(
                    title=f"*Vamos começar a jogar, {ctx.message.author.name} ? Chame mais pessoas para jogarem conosco!*",
                    colour=discord.Colour(0x370c5e))

                embed.set_author(name=f"{ctx.message.author.name}", icon_url=f"{avi}")
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                           self.client.user.name,
                                                                                           year()))
                embed.add_field(name="**Regras do jogo:**",
                                value="```Clique na arma para participar. Quando tivermos 6 participantes começarei o jogo!```")
                message = await ctx.send(embed=embed)
                await message.add_reaction("🔫")

                def check(reaction, number_of_reactions):
                    return reaction.count == 6 and str(reaction.emoji) == '🔫'

                try:
                    reaction, user = await self.client.wait_for('reaction_add', check=check)

                except:
                    return

                if str(reaction.emoji) == "🔫":

                    iterator = reaction.users()
                    users = await iterator.flatten()
                    while len(users) > 1:
                        loser = random.choice(users)
                        users.remove(loser)
                        msg1 = f'``Que pena, você morreu, {loser}!``'
                        embed = discord.Embed(title="**Morte!**", colour=discord.Colour(0x370c5e),
                                              description="{}".format(msg1))
                        embed.set_image(url="{}".format(gif1))
                        embed.set_footer(icon_url=betina_icon,
                                         text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                                   self.client.user.name,
                                                                                                   year()))
                        msg = await ctx.send(embed=embed)
                        await asyncio.sleep(5)

                    winner = random.choice(users)
                    msg2 = f'``Parabéns, {winner}! Você sobreviveu!``'
                    embed = discord.Embed(title="**Sobreviveu!**", colour=discord.Colour(0x370c5e),
                                          description="{}".format(msg2))
                    embed.set_image(url="{}".format(gif2))
                    embed.set_footer(icon_url=betina_icon,
                                     text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                               self.client.user.name,
                                                                                               year()))
                    msg = await ctx.send(embed=embed)
            else:
                guild = ctx.guild.get_channel(int(limitador_log[guild_id]))
                await ctx.send(f'Esse não foi o canal definido para usar os comandos. Tente utilizar o canal {guild}')
                return
        else:
            gif1 = random.choice(dead)
            gif2 = random.choice(alive)

            embed = discord.Embed(
                title=f"*Vamos começar a jogar, {ctx.message.author.name} ? Chame mais pessoas para jogarem conosco!*",
                colour=discord.Colour(0x370c5e))

            embed.set_author(name=f"{ctx.message.author.name}", icon_url=f"{avi}")
            embed.set_footer(icon_url=betina_icon,
                             text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), self.client.user.name,
                                                                                       year()))
            embed.add_field(name="**Regras do jogo:**",
                            value="```Clique na arma para participar. Quando tivermos 6 participantes começarei o jogo!```")
            message = await ctx.send(embed=embed)
            await message.add_reaction("🔫")

            def check(reaction, number_of_reactions):
                return reaction.count == 6 and str(reaction.emoji) == '🔫'

            try:
                reaction, user = await self.client.wait_for('reaction_add', check=check)

            except:
                return

            if str(reaction.emoji) == "🔫":

                iterator = reaction.users()
                users = await iterator.flatten()
                while len(users) > 1:
                    loser = random.choice(users)
                    users.remove(loser)
                    msg1 = f'``Que pena, você morreu, {loser}!``'
                    embed = discord.Embed(title="**Morte!**", colour=discord.Colour(0x370c5e),
                                          description="{}".format(msg1))
                    embed.set_image(url="{}".format(gif1))
                    embed.set_footer(icon_url=betina_icon,
                                     text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                               self.client.user.name,
                                                                                               year()))
                    msg = await ctx.send(embed=embed)
                    await asyncio.sleep(5)

                winner = random.choice(users)
                msg2 = f'``Parabéns, {winner}! Você sobreviveu!``'
                embed = discord.Embed(title="**Sobreviveu!**", colour=discord.Colour(0x370c5e),
                                      description="{}".format(msg2))
                embed.set_image(url="{}".format(gif2))
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                           self.client.user.name,
                                                                                           year()))
                msg = await ctx.send(embed=embed)

    @commands.cooldown(2, 10, commands.BucketType.user)
    @commands.guild_only()
    @commands.command(name='highfive', aliases=['hf', 'batemao'])
    async def highfive(self, ctx, member: discord.Member, membro: discord.Member = None):
        guild_id = str(ctx.guild.id)
        user_id = str(ctx.author.id)
        if guild_id in limitador_log:
            if str(ctx.message.channel.id) == limitador_log[guild_id]:
                if membro == None:
                    membro = ctx.author
                else:
                    if ctx.author == member == membro:
                        await ctx.invoke(self.client.get_command('endeline'))
                        await msg.delete()
                """<membro>: Cuidado com isso!"""
                gif = random.choice(highfives)
                ataca2 = '{} e {} **Deram um High Five!**'.format(membro.mention, member.mention)

                embed = discord.Embed(title="**Shipados!**", colour=discord.Colour(0x370c5e),
                                      description="{}".format(ataca2))
                embed.set_image(url="{}".format(gif))
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                           self.client.user.name,
                                                                                           year()))
                msg = await ctx.send(embed=embed)

                await msg.add_reaction("🔙")

                def check(reaction, user):
                    return user == member and str(reaction.emoji) == "🔙"

                try:
                    reaction, user = await self.client.wait_for('reaction_add', check=check)
                except:
                    return
                else:
                    await msg.delete()
                    await ctx.invoke(self.client.get_command('highfive'), ctx.author, member)
            else:
                guild = ctx.guild.get_channel(int(limitador_log[guild_id]))
                await ctx.send(f'Esse não foi o canal definido para usar os comandos. Tente utilizar o canal {guild}')
                return
        else:
            if membro == None:
                membro = ctx.author
            else:
                if ctx.author == member == membro:
                    await ctx.invoke(self.client.get_command('endeline'))
                    await msg.delete()
            """<membro>: Cuidado com isso!"""
            gif = random.choice(highfives)
            ataca2 = '{} e {} **Deram um High Five!**'.format(membro.mention, member.mention)

            embed = discord.Embed(title="**Shipados!**", colour=discord.Colour(0x370c5e),
                                  description="{}".format(ataca2))
            embed.set_image(url="{}".format(gif))
            embed.set_footer(icon_url=betina_icon,
                             text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), self.client.user.name,
                                                                                       year()))
            msg = await ctx.send(embed=embed)

            await msg.add_reaction("🔙")

            def check(reaction, user):
                return user == member and str(reaction.emoji) == "🔙"

            try:
                reaction, user = await self.client.wait_for('reaction_add', check=check)
            except:
                return
            else:
                await msg.delete()
                await ctx.invoke(self.client.get_command('highfive'), ctx.author, member)

    @highfive.error
    async def highfive_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'member':
                embed = discord.Embed(title="Comando $highfive:", colour=discord.Colour(0x370c5e),
                                      description="Bate na mão do usuário!\n \n**Como usar: $highfive <usuário1>**")

                embed.set_author(name="Betina#9182",
                                 icon_url=betina_icon)
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                           self.client.user.name,
                                                                                           year()))

                embed.add_field(name="📖**Exemplos:**", value="$highfive @fulano\n$highfive @sicrano", inline=False)
                embed.add_field(name="🔀**Outros Comandos**", value="``$hf, $batemao.``", inline=False)

                msg = await ctx.send(embed=embed)
                await msg.add_reaction("❓")


    @commands.cooldown(2, 10, commands.BucketType.user)
    @commands.guild_only()
    @commands.command(name='mencionar', aliases=['reply', 'quote'])
    async def mention(self, ctx, message: int, *, text: str = ' '):
        guild_id = str(ctx.guild.id)
        user_id = str(ctx.author.id)
        if guild_id in limitador_log:
            if str(ctx.message.channel.id) == limitador_log[guild_id]:
                texto = await ctx.get_message(message)
                embed = discord.Embed(colour=discord.Colour(0x370c5e),
                                      description=f"{texto.content}\nem #{texto.channel}")
                embed.set_author(name=f"{texto.author.name} disse: ", icon_url=texto.author.avatar_url)
                await ctx.send(f'{texto.author.mention} {text}')
                await ctx.send(embed=embed)
            else:
                guild = ctx.guild.get_channel(int(limitador_log[guild_id]))
                await ctx.send(f'Esse não foi o canal definido para usar os comandos. Tente utilizar o canal {guild}')
                return
        else:
            texto = await ctx.get_message(message)
            embed = discord.Embed(colour=discord.Colour(0x370c5e), description=f"{texto.content}\nem #{texto.channel}")
            embed.set_author(name=f"{texto.author.name} disse: ", icon_url=texto.author.avatar_url)
            await ctx.send(f'{texto.author.mention} {text}')
            await ctx.send(embed=embed)

    @mention.error
    async def mention_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):

            if error.param.name == 'message':
                embed = discord.Embed(title="Comando $mencionar:", colour=discord.Colour(0x370c5e),
                                      description="Retorna uma citação do usuário!"
                                                  "\n \n**Como usar: $mencionar <id da mensagem> <texto> (opcional)**")

                embed.set_author(name="Betina#9182",
                                 icon_url=betina_icon)
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                           self.client.user.name,
                                                                                           year()))

                embed.add_field(name="📖**Exemplos:**", value="$mencionar 537452046320664597 filosófico!",
                                inline=False)
                embed.add_field(name="🔀**Outros Comandos**", value="``$reply, $quote.``", inline=False)

                msg = await ctx.send(embed=embed)
                await msg.add_reaction("❓")


    @commands.cooldown(2, 10, commands.BucketType.user)
    @commands.guild_only()
    @commands.command(name='fala', aliases=['speak', 'falar'])
    async def talk(self, ctx, channel: typing.Optional[discord.TextChannel] = None, *, message: str):
        if channel == None:
            guild_id = str(ctx.guild.id)
            user_id = str(ctx.author.id)
            if guild_id in limitador_log:
                if str(ctx.message.channel.id) == limitador_log[guild_id]:
                    await ctx.send(f'{message}')
                else:
                    guild = ctx.guild.get_channel(int(limitador_log[guild_id]))
                    await ctx.send(
                        f'Esse não foi o canal definido para usar os comandos. Tente utilizar o canal {guild}')
                    return
            else:
                await ctx.send(f'{message}')
        else:
            guild_id = str(ctx.guild.id)
            user_id = str(ctx.author.id)
            if guild_id in limitador_log:
                if str(ctx.message.channel.id) == limitador_log[guild_id]:
                    await ctx.send(f'Mensagem enviada para o canal {channel}')
                    await channel.send(f'{message}')
                else:
                    guild = ctx.guild.get_channel(int(limitador_log[guild_id]))
                    await ctx.send(
                        f'Esse não foi o canal definido para usar os comandos. Tente utilizar o canal {guild}')
                    return
            else:
                await ctx.send(f'Mensagem enviada para o canal {channel}')
                await channel.send(f'{message}')

    @talk.error
    async def talk_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):

            if error.param.name == 'message':
                embed = discord.Embed(title="Comando $fala:", colour=discord.Colour(0x370c5e),
                                      description="Faz a betina falar!"
                                                  "\n \n**Como usar: $fala <canal> (opcional) <mensagem>**")

                embed.set_author(name="Betina#9182",
                                 icon_url=betina_icon)
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                           self.client.user.name,
                                                                                           year()))

                embed.add_field(name="📖**Exemplos:**", value="$fala filosófico!",
                                inline=False)
                embed.add_field(name="🔀**Outros Comandos**", value="``$speak, $falar.``", inline=False)

                msg = await ctx.send(embed=embed)
                await msg.add_reaction("❓")



def setup(client):
    client.add_cog(Interação(client))
