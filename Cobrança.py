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

from discord.ext import commands
from forex_python.converter import CurrencyRates
from dhooks import Webhook
from discord.utils import get
from discord.ext.commands import has_permissions, MissingPermissions


# devemais e devemenos
devedores = {}
devidos = {}

betina_icon = ''

with open('limitador.json', 'r') as file:
    try:
        limitador_log = json.load(file)
    except ValueError:
        limitador_log = {}


class Cobrança:
    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.command(name='conversor', aliases=['converter', 'converte'])
    async def conversor(self, ctx, moeda1, moeda2, quantidade=None):
        """Vê o valor da moeda 1 em moeda 2"""
        guild_id = str(ctx.guild.id)
        if guild_id in limitador_log:
            if str(ctx.message.channel.id) == limitador_log[guild_id]:
                try:
                    channel = ctx.channel
                    await channel.trigger_typing()
                    c = CurrencyRates()
                    msg = c.get_rate(f'''{moeda1.upper()}''', f'''{moeda2.upper()}''')
                    if quantidade is None:
                        await ctx.send(
                            'Esse é o valor da cotacao atual do ``{}`` em ``{}``: **{}**'.format(moeda1.upper(),
                                                                                                 moeda2.upper(),
                                                                                                 msg))
                    else:
                        msg = msg * quantidade
                        await ctx.send(
                            'Esse é o valor de {} ``{}`` em ``{}``: **{}**'.format(quantidade, moeda1.upper(),
                                                                                   moeda2.upper(),
                                                                                   msg))
                except:
                    msg = await ctx.send(
                        'Tente utilizar o codigo de uma moeda existente. **Por exemplo: $conversor usd brl**')
                    await msg.add_reaction('❤')
            else:
                guild = ctx.guild.get_channel(int(limitador_log[guild_id]))
                await ctx.send(f'Esse não foi o canal definido para usar os comandos. Tente utilizar o canal {guild}')
                return
        else:
            try:
                channel = ctx.channel
                await channel.trigger_typing()
                c = CurrencyRates()
                msg = c.get_rate(f'''{moeda1.upper()}''', f'''{moeda2.upper()}''')
                if quantidade is None:
                    await ctx.send(
                        'Esse é o valor da cotacao atual do ``{}`` em ``{}``: **{}**'.format(moeda1.upper(),
                                                                                             moeda2.upper(),
                                                                                             msg))
                else:
                    msg = msg * quantidade
                    await ctx.send(
                        'Esse é o valor de {} ``{}`` em ``{}``: **{}**'.format(quantidade, moeda1.upper(),
                                                                               moeda2.upper(),
                                                                               msg))
            except:
                msg = await ctx.send(
                    'Tente utilizar o codigo de uma moeda existente. **Por exemplo: $conversor usd brl**')
                await msg.add_reaction('❤')

    @conversor.error
    async def conversor_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'moeda1':
                embed = discord.Embed(title="Comando $conversor:", colour=discord.Colour(0x370c5e),
                                      description="Você converte a moeda1 em termos de moeda2\n \n**Como"
                                                  " usar: $converte <moeda1> <moeda2>**")

                embed.set_author(name="Betina#9182",
                                 icon_url=betina_icon)
                embed.set_footer(text="Betina Brazilian Bot",
                                 icon_url=betina_icon)

                embed.add_field(name="📖**Exemplos:**", value="$converte usd brl\n$converte eur pln", inline=False)
                embed.add_field(name="🔀**Outros Comandos**", value="``$converter, $converte.``", inline=False)

                msg = await ctx.send(embed=embed)
                await msg.add_reaction("❓")

            elif error.param.name == 'moeda2':
                embed = discord.Embed(title="Comando $conversor:", colour=discord.Colour(0x370c5e),
                                      description="Você converte a moeda1 em termos de moeda2\n \n**Como"
                                                  " usar: $converte <moeda1> <moeda2>**")

                embed.set_author(name="Betina#9182",
                                 icon_url=betina_icon)
                embed.set_footer(text="Betina Brazilian Bot",
                                 icon_url=betina_icon)

                embed.add_field(name="📖**Exemplos:**", value="$converte usd brl\n$converte eur pln", inline=False)
                embed.add_field(name="🔀**Outros Comandos**", value="``$converter, $converte.``", inline=False)

                msg = await ctx.send(embed=embed)
                await msg.add_reaction("❓")


    @commands.guild_only()
    @commands.command(name='deve', aliases=['rsp', 'owe'])
    async def deve(self, ctx, member: discord.Member):
        guild_id = str(ctx.guild.id)
        if guild_id in limitador_log:
            if str(ctx.message.channel.id) == limitador_log[guild_id]:
                if not (member in devedores):
                    msg = await ctx.send('**{} não deve nada a ninguem!**'.format(member.mention))
                    await msg.add_reaction('😯')
                else:
                    await ctx.send('**{} deve a tais pessoas: **'.format(member.mention))
                    for membros in devedores[member]:
                        if membros.id != member.id:
                            await ctx.send('**Deve R$ {} ao {}**'.format(devidos[membros], membros.mention))

            else:
                guild = ctx.guild.get_channel(int(limitador_log[guild_id]))
                await ctx.send(f'Esse não foi o canal definido para usar os comandos. Tente utilizar o canal {guild}')
                return
        else:
            if not (member in devedores):
                msg = await ctx.send('**{} não deve nada a ninguem!**'.format(member.mention))
                await msg.add_reaction('😯')
            else:
                await ctx.send('**{} deve a tais pessoas: **'.format(member.mention))
                for membros in devedores[member]:
                    if membros.id != member.id:
                        await ctx.send('**Deve R$ {} ao {}**'.format(devidos[membros], membros.mention))

    @deve.error
    async def deve_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'member':
                embed = discord.Embed(title="Comando $deve:", colour=discord.Colour(0x370c5e),
                                      description="Diz o quanto o usuário deve a cada pessoa do servidor\n \n**Como usar"
                                                  ": $deve <usuário>**")

                embed.set_author(name="Betina#9182",
                                 icon_url=betina_icon)
                embed.set_footer(text="Betina Brazilian Bot",
                                 icon_url=betina_icon)

                embed.add_field(name="📖**Exemplos:**", value="$deve @sicrano\n$deve @fulano", inline=False)
                embed.add_field(name="🔀**Outros Comandos**", value="``$rsp, $owe.``", inline=False)

                msg = await ctx.send(embed=embed)
                await msg.add_reaction("❓")

    @commands.guild_only()
    @commands.command(name='devemenos', aliases=['dntp', 'naomedeve'])
    async def devemenos(self, ctx, member: discord.Member, a: float):
        """Diminui o credito"""
        guild_id = str(ctx.guild.id)
        if guild_id in limitador_log:
            if str(ctx.message.channel.id) == limitador_log[guild_id]:
                if (member in devedores) and (ctx.author in devidos):
                    devidos[ctx.author] -= a
                    if devidos[ctx.author] < 0:
                        if (ctx.author in devedores) and (member in devidos):
                            devidos[member] += (- devidos[ctx.author])
                            devidos[ctx.author] = 0
                        else:
                            devidos[member] = (- devidos[ctx.author])
                            devidos[ctx.author] = 0
                            devedores[ctx.author] = devidos
                        await ctx.send(
                            '**Agora {} deve R$ {} ao {}**'.format(ctx.author.mention, devidos[member], member.mention))
                    elif devidos[ctx.author] == 0:
                        await ctx.send('**{} não deve nada a {}**'.format(ctx.author.mention, member.mention))
                    else:
                        await ctx.send(
                            '**{} deve R$ {} ao {}**'.format(member.mention, devidos[ctx.author], ctx.author.mention))
                else:
                    devedores[ctx.author] = devidos
                    devidos[member] = a
                    await ctx.send(
                        '**{} deve R$ {} ao {}**'.format(ctx.author.mention, devidos[member], member.mention))
            else:
                guild = ctx.guild.get_channel(int(limitador_log[guild_id]))
                await ctx.send(f'Esse não foi o canal definido para usar os comandos. Tente utilizar o canal {guild}')
                return
        else:
            if (member in devedores) and (ctx.author in devidos):
                devidos[ctx.author] -= a
                if devidos[ctx.author] < 0:
                    if (ctx.author in devedores) and (member in devidos):
                        devidos[member] += (- devidos[ctx.author])
                        devidos[ctx.author] = 0
                    else:
                        devidos[member] = (- devidos[ctx.author])
                        devidos[ctx.author] = 0
                        devedores[ctx.author] = devidos
                    await ctx.send(
                        '**Agora {} deve R$ {} ao {}**'.format(ctx.author.mention, devidos[member], member.mention))
                elif devidos[ctx.author] == 0:
                    await ctx.send('**{} não deve nada a {}**'.format(ctx.author.mention, member.mention))
                else:
                    await ctx.send(
                        '**{} deve R$ {} ao {}**'.format(member.mention, devidos[ctx.author], ctx.author.mention))
            else:
                devedores[ctx.author] = devidos
                devidos[member] = a
                await ctx.send('**{} deve R$ {} ao {}**'.format(ctx.author.mention, devidos[member], member.mention))

    @devemenos.error
    async def devemenos_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'member':
                embed = discord.Embed(title="Comando $devemenos:", colour=discord.Colour(0x370c5e),
                                      description="Você diminui uma quantidade ao quanto um usuário te deve\n \n**Como"
                                                  " usar: $devemenos <usuário> <valor>**")

                embed.set_author(name="Betina#9182",
                                 icon_url=betina_icon)
                embed.set_footer(text="Betina Brazilian Bot",
                                 icon_url=betina_icon)

                embed.add_field(name="📖**Exemplos:**", value="$devemenos @sicrano 500\n$devemenos @fulano 10",
                                inline=False)
                embed.add_field(name="🔀**Outros Comandos**", value="``$dntp, $naomedeve.``", inline=False)

                msg = await ctx.send(embed=embed)
                await msg.add_reaction("❓")

            elif error.param.name == 'a':
                embed = discord.Embed(title="Comando $devemenos:", colour=discord.Colour(0x370c5e),
                                      description="Você diminui uma quantidade ao quanto um usuário te deve\n \n**Como"
                                                  " usar: $devemenos <usuário> <valor>**")

                embed.set_author(name="Betina#9182",
                                 icon_url=betina_icon)
                embed.set_footer(text="Betina Brazilian Bot",
                                 icon_url=betina_icon)

                embed.add_field(name="📖**Exemplos:**", value="$devemenos @sicrano 500\n$devemenos @fulano 10",
                                inline=False)
                embed.add_field(name="🔀**Outros Comandos**", value="``$dntp, $naomedeve.``", inline=False)

                msg = await ctx.send(embed=embed)
                await msg.add_reaction("❓")

    @commands.guild_only()
    @commands.command(name='devemais', aliases=['ntp', 'medeve', 'pay'])
    async def devemais(self, ctx, member: discord.Member, a: float):
        """Adiciona o credito"""
        guild_id = str(ctx.guild.id)
        if guild_id in limitador_log:
            if str(ctx.message.channel.id) == limitador_log[guild_id]:
                if (member in devedores) and (ctx.author in devidos):
                    devidos[ctx.author] += a
                else:
                    devidos[ctx.author] = a
                    devedores[member] = devidos
                await ctx.send('**{} deve R$ {} ao {}**'.format(member.mention, devidos[ctx.author], ctx.author.mention))
            else:
                guild = ctx.guild.get_channel(int(limitador_log[guild_id]))
                await ctx.send(f'Esse não foi o canal definido para usar os comandos. Tente utilizar o canal {guild}')
                return
        else:
            if (member in devedores) and (ctx.author in devidos):
                devidos[ctx.author] += a
            else:
                devidos[ctx.author] = a
                devedores[member] = devidos
            await ctx.send('**{} deve R$ {} ao {}**'.format(member.mention, devidos[ctx.author], ctx.author.mention))

    @devemais.error
    async def devemais_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'member':
                embed = discord.Embed(title="Comando $devemais:", colour=discord.Colour(0x370c5e),
                                      description="Você adiciona uma quantidade ao quanto um usuário te deve\n \n**Como"
                                                  " usar: $devemais <usuário> <valor>**")

                embed.set_author(name="Betina#9182",
                                 icon_url=betina_icon)
                embed.set_footer(text="Betina Brazilian Bot",
                                 icon_url=betina_icon)

                embed.add_field(name="📖**Exemplos:**", value="$devemais @sicrano 500\n$devemais @fulano 10",
                                inline=False)
                embed.add_field(name="🔀**Outros Comandos**", value="``$ntp, $medeve.``", inline=False)

                msg = await ctx.send(embed=embed)
                await msg.add_reaction("❓")

            elif error.param.name == 'a':
                embed = discord.Embed(title="Comando $devemais:", colour=discord.Colour(0x370c5e),
                                      description="Você adiciona uma quantidade ao quanto um usuário te deve\n \n**Como"
                                                  " usar: $devemais <usuário> <valor>**")

                embed.set_author(name="Betina#9182",
                                 icon_url=betina_icon)
                embed.set_footer(text="Betina Brazilian Bot",
                                 icon_url=betina_icon)

                embed.add_field(name="📖**Exemplos:**", value="$devemais @sicrano 500\n$devemais @fulano 10",
                                inline=False)
                embed.add_field(name="🔀**Outros Comandos**", value="``$ntp, $medeve.``", inline=False)

                msg = await ctx.send(embed=embed)
                await msg.add_reaction("❓")


def setup(client):
    client.add_cog(Cobrança(client))
