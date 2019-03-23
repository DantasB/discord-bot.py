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

from __future__ import division

import random
import time
import discord
import datetime
import aiohttp
import asyncio
import json
import requests
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim

from discord.ext import commands
from forex_python.converter import CurrencyRates
from dhooks import Webhook
from discord.utils import get
from discord.ext.commands import has_permissions, MissingPermissions
from PIL import Image, ImageDraw, ImageFont, ImageOps
from horario import*
from io import BytesIO

dead = [] #dead giphy gifs
alive = [] #alive giphy gifs
hunger_games = ['[nome] encontrou o cara mais bonito do bairro e morreu de tanta beleza.']

with open('limitador.json', 'r') as file:
    try:
        limitador_log = json.load(file)
    except ValueError:
        limitador_log = {}


class Diversão(commands.Cog):
    def __init__(self, client):
        self.client = client

    text_flip = {}
    char_list = "!#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}"
    alt_char_list = "{|}zʎxʍʌnʇsɹbdouɯlʞɾᴉɥƃɟǝpɔqɐ,‾^[\]Z⅄XMΛ∩┴SɹQԀONW˥ʞſIHפℲƎpƆq∀@¿<=>;:68ㄥ9ϛㄣƐᄅƖ0/˙-'+*(),⅋%$#¡"[
                    ::-1]
    for idx, char in enumerate(char_list):
        text_flip[char] = alt_char_list[idx]
        text_flip[alt_char_list[idx]] = char

    @commands.guild_only()
    @commands.command(name='moeda', aliases=['coin', 'ht'])
    async def moeda(self, ctx):
        """Heads and Tails!"""
        guild_id = str(ctx.guild.id)
        user_id = str(ctx.author.id)
        if guild_id in limitador_log:
            if str(ctx.message.channel.id) == limitador_log[guild_id]:

                resultado = random.randint(1, 2)
                if resultado == 1:
                    await ctx.send('😃')
                else:
                    await ctx.send('👑')
            else:
                guild = ctx.guild.get_channel(int(limitador_log[guild_id]))
                await ctx.send(f'Esse não foi o canal definido para usar os comandos. Tente utilizar o canal {guild}')
                return
        else:

            resultado = random.randint(1, 2)
            if resultado == 1:
                await ctx.send('😃')
            else:
                await ctx.send('👑')

    @commands.guild_only()
    @commands.command(name='ppt', aliases=['Rsp', 'jogo'])
    async def ppt(self, ctx, msg: str):
        t = ['pedra', 'papel', 'tesoura']

        channel = ctx.channel
        computer = t[random.randint(0, 2)]
        player = msg.lower()
        guild_id = str(ctx.guild.id)
        user_id = str(ctx.author.id)
        if guild_id in limitador_log:
            if str(ctx.message.channel.id) == limitador_log[guild_id]:

                await ctx.send('``Você escolheu {}{}``'.format(player[:1].upper(), player[1:]))
                await ctx.channel.trigger_typing()
                if player == computer:
                    await ctx.send('``Empatei contigo!``')
                elif player == 'pedra':
                    if computer == 'papel':
                        await ctx.send('``Você perdeu! Papel encobre pedra``')
                    else:
                        await ctx.send('``Você ganhou! Pedra destroi tesoura``')
                elif player == 'papel':
                    if computer == 'tesoura':
                        await ctx.send('``Você perdeu! Tesoura corta papel``')
                    else:
                        await ctx.send('``Você ganhou! Papel encobre pedra``')
                elif player == 'tesoura':
                    if computer == 'pedra':
                        await ctx.send('``Você perdeu! Pedra destroi tesoura!``')
                    else:
                        await ctx.send('``Você ganhou! Tesoura corta papel!``')
                else:
                    await ctx.send('``Escreve direito, por favor!``')
            else:

                guild = ctx.guild.get_channel(int(limitador_log[guild_id]))
                await ctx.send(f'Esse não foi o canal definido para usar os comandos. Tente utilizar o canal {guild}')
                return
        else:

            await ctx.send('``Você escolheu {}{}``'.format(player[:1].upper(), player[1:]))
            await ctx.channel.trigger_typing()
            if player == computer:
                await ctx.send('``Empatei contigo!``')
            elif player == 'pedra':
                if computer == 'papel':
                    await ctx.send('``Você perdeu! Papel encobre pedra``')
                else:
                    await ctx.send('``Você ganhou! Pedra destroi tesoura``')
            elif player == 'papel':
                if computer == 'tesoura':
                    await ctx.send('``Você perdeu! Tesoura corta papel``')
                else:
                    await ctx.send('``Você ganhou! Papel encobre pedra``')
            elif player == 'tesoura':
                if computer == 'pedra':
                    await ctx.send('``Você perdeu! Pedra destroi tesoura!``')
                else:
                    await ctx.send('``Você ganhou! Tesoura corta papel!``')
            else:
                await ctx.send('``Escreve direito, por favor!``')

    @ppt.error
    async def ppt_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'msg':
                embed = discord.Embed(title="Comando $ppt:", colour=discord.Colour(0x370c5e),
                                      description="Inicia um jogo de Pedra, Papel ou tesoura com o bot\n \n**Como usar"
                                                  ": $ppt <Pedra, Papel ou Tesoura>**")

                embed.set_author(name="Betina#9182",
                                 icon_url=betina_icon)
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                           self.client.user.name,
                                                                                           year()))

                embed.add_field(name="📖**Exemplos:**", value="$ppt pedra\n$ppt tesoura", inline=False)
                embed.add_field(name="🔀**Outros Comandos**", value="``$Rsp, $jogo.``", inline=False)

                msg = await ctx.send(embed=embed)
                await msg.add_reaction("❓")

    @commands.guild_only()
    @commands.command(name='rola', aliases=['roll', 'dice'])
    async def rola(self, ctx, a: int):
        """Um Dado de até 20 lados."""

        guild_id = str(ctx.guild.id)
        user_id = str(ctx.author.id)
        if guild_id in limitador_log:
            if str(ctx.message.channel.id) == limitador_log[guild_id]:

                if a > 20:
                    msg = await ctx.send("Nunca vi um dado com mais de ``20`` lados!")
                    await msg.add_reaction("🤔")
                elif a == 3 or a == 7 or a == 11 or a == 13 or a == 5 or a == 1 or a == 17 or a == 19:
                    msg = await ctx.send("Nunca vi um dado com lados ``impares``!")
                    await msg.add_reaction("🤔")
                else:
                    argumento = random.randint(1, int(a))
                    await ctx.send("Você está rolando um ``d{}`` e tirou ``{}``".format(a, argumento))
            else:

                guild = ctx.guild.get_channel(int(limitador_log[guild_id]))
                await ctx.send(f'Esse não foi o canal definido para usar os comandos. Tente utilizar o canal {guild}')
                return
        else:

            if a > 20:
                msg = await ctx.send("Nunca vi um dado com mais de ``20`` lados!")
                await msg.add_reaction("🤔")
            elif a == 3 or a == 7 or a == 11 or a == 13 or a == 5 or a == 1 or a == 17 or a == 19:
                msg = await ctx.send("Nunca vi um dado com lados ``impares``!")
                await msg.add_reaction("🤔")
            else:
                argumento = random.randint(1, int(a))
                await ctx.send("Você está rolando um ``d{}`` e tirou ``{}``".format(a, argumento))

    @rola.error
    async def rola_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'a':
                embed = discord.Embed(title="Comando $rola:", colour=discord.Colour(0x370c5e),
                                      description="Rola um dado de n lados\n \n**Como usar"
                                                  ": $rola <n>**")

                embed.set_author(name="Betina#9182",
                                 icon_url=betina_icon)
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                           self.client.user.name,
                                                                                           year()))
                embed.add_field(name="❗**Atenção:**", value="Escolha um dado que existe!", inline=False)
                embed.add_field(name="📖**Exemplos:**", value="$rola 10\n$rola 4", inline=False)
                embed.add_field(name="🔀**Outros Comandos**", value="``$roll, $dice.``", inline=False)

                msg = await ctx.send(embed=embed)
                await msg.add_reaction("❓")


    @commands.guild_only()
    @commands.command(name='hungergames', aliases=['hg', 'killall'])
    async def HungerGames(self, ctx, number: int):
        guild_id = str(ctx.guild.id)
        user_id = str(ctx.author.id)
        if guild_id in limitador_log:
            if str(ctx.message.channel.id) == limitador_log[guild_id]:

                if ctx.message.author.avatar_url_as(static_format='png')[54:].startswith('a_'):
                    avi = ctx.message.author.avatar_url.rsplit("?", 1)[0]
                else:
                    avi = ctx.message.author.avatar_url_as(static_format='png')

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
                                value=f"```Clique na reação abaixo para participar."
                                f" Quando tivermos {number} participantes começarei o jogo!```")
                message = await ctx.send(embed=embed)
                await message.add_reaction("🏃")

                def check(reaction, number_of_reactions):
                    return reaction.count == number and str(reaction.emoji) == "🏃"

                try:
                    reaction, user = await self.client.wait_for('reaction_add', check=check)

                except:
                    return

                if str(reaction.emoji) == "🏃":
                    i = random.randrange(len(hunger_games))
                    listas = hunger_games[i]

                    iterator = reaction.users()
                    users = await iterator.flatten()
                    for i in users:
                        if i.bot:
                            users.remove(i)

                    while len(users) > 1:
                        loser = random.choice(users)
                        users.remove(loser)
                        msg1 = listas.replace('[nome]', loser.name)
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
                    msg2 = f'``Parabéns, {winner}! Você venceu!``'
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

            if ctx.message.author.avatar_url_as(static_format='png')[54:].startswith('a_'):
                avi = ctx.message.author.avatar_url.rsplit("?", 1)[0]
            else:
                avi = ctx.message.author.avatar_url_as(static_format='png')

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
                            value=f"```Clique na reação abaixo para participar."
                            f" Quando tivermos {number} participantes começarei o jogo!```")
            message = await ctx.send(embed=embed)
            await message.add_reaction("🏃")

            def check(reaction, number_of_reactions):
                return reaction.count == number and str(reaction.emoji) == "🏃"

            try:
                reaction, user = await self.client.wait_for('reaction_add', check=check)

            except:
                return

            if str(reaction.emoji) == "🏃":
                i = random.randrange(len(hunger_games))
                listas = hunger_games[i]

                iterator = reaction.users()
                users = await iterator.flatten()
                for i in users:
                    if i.bot:
                        users.remove(i)

                while len(users) > 1:
                    loser = random.choice(users)
                    users.remove(loser)
                    msg1 = listas.replace('[nome]', loser.name)
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
                msg2 = f'``Parabéns, {winner}! Você venceu!``'
                embed = discord.Embed(title="**Sobreviveu!**", colour=discord.Colour(0x370c5e),
                                      description="{}".format(msg2))
                embed.set_image(url="{}".format(gif2))
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                           self.client.user.name,
                                                                                           year()))
                msg = await ctx.send(embed=embed)

    @HungerGames.error
    async def hunger_games_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'number':
                embed = discord.Embed(title="Comando $hungergames:", colour=discord.Colour(0x370c5e),
                                      description="Rola um dado de n lados\n \n**Como usar"
                                                  ": $hungergames <number>**")

                embed.set_author(name="Betina#9182",
                                 icon_url=betina_icon)
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                           self.client.user.name,
                                                                                           year()))
                embed.add_field(name="📖**Exemplos:**", value="$hungergames 10\n$hungergames 4", inline=False)
                embed.add_field(name="🔀**Outros Comandos**", value="``$hg, $killall.``", inline=False)

                msg = await ctx.send(embed=embed)
                await msg.add_reaction("❓")


    @commands.guild_only()
    @commands.command()
    async def faustao(self, ctx):
        guild_id = str(ctx.guild.id)
        user_id = str(ctx.author.id)
        if guild_id in limitador_log:
            if str(ctx.message.channel.id) == limitador_log[guild_id]:

                with open("faustop.png", "rb") as imageFile:
                    file = bytearray(imageFile.read())
                channel = ctx.channel
                async with aiohttp.ClientSession() as session:
                    webhook = await channel.create_webhook(name='Faustão', avatar=file)

                await webhook.send("Esta Fera Bicho!")
                await ctx.invoke(self.client.get_command('play'), 'https://www.youtube.com/watch?v=bLB6WIwXhTw')
                await webhook.delete()
            else:
                guild = ctx.guild.get_channel(int(limitador_log[guild_id]))
                await ctx.send(f'Esse não foi o canal definido para usar os comandos. Tente utilizar o canal {guild}')
                return

        else:

            with open("faustop.png", "rb") as imageFile:
                file = bytearray(imageFile.read())
            channel = ctx.channel
            async with aiohttp.ClientSession() as session:
                webhook = await channel.create_webhook(name='Faustão', avatar=file)

            await webhook.send("Esta Fera Bicho!")
            await webhook.delete()
        
    @commands.guild_only()
    @commands.command()
    async def taokei(self, ctx):
        guild_id = str(ctx.guild.id)
        user_id = str(ctx.author.id)
        if guild_id in limitador_log:
            if str(ctx.message.channel.id) == limitador_log[guild_id]:

                with open("bolsoboy.png", "rb") as imageFile:
                    file = bytearray(imageFile.read())
                channel = ctx.channel
                async with aiohttp.ClientSession() as session:
                    webhook = await channel.create_webhook(name='Bolsonaro', avatar=file)

                await webhook.send("Taokei?")
                await webhook.delete()
            else:
                guild = ctx.guild.get_channel(int(limitador_log[guild_id]))
                await ctx.send(f'Esse não foi o canal definido para usar os comandos. Tente utilizar o canal {guild}')
                return
        else:

            with open("bolsoboy.png", "rb") as imageFile:
                file = bytearray(imageFile.read())
            channel = ctx.channel
            async with aiohttp.ClientSession() as session:
                webhook = await channel.create_webhook(name='Bolsonaro', avatar=file)

            await webhook.send("Taokei?")
            await webhook.delete()


    @commands.guild_only()
    @commands.command()
    async def miranha(self, ctx):
        guild_id = str(ctx.guild.id)
        user_id = str(ctx.author.id)
        if guild_id in limitador_log:
            if str(ctx.message.channel.id) == limitador_log[guild_id]:

                with open("miranha.png", "rb") as imageFile:
                    file = bytearray(imageFile.read())
                channel = ctx.channel
                async with aiohttp.ClientSession() as session:
                    webhook = await channel.create_webhook(name='Miranha', avatar=file)

                await webhook.send("EU SOU O MIRANHA!")
                await webhook.delete()
            else:
                guild = ctx.guild.get_channel(int(limitador_log[guild_id]))
                await ctx.send(f'Esse não foi o canal definido para usar os comandos. Tente utilizar o canal {guild}')
                return
        else:
            
            with open("miranha.png", "rb") as imageFile:
                file = bytearray(imageFile.read())
            channel = ctx.channel
            async with aiohttp.ClientSession() as session:
                webhook = await channel.create_webhook(name='Miranha', avatar=file)

            await webhook.send("EU SOU O MIRANHA!")
            await webhook.delete()

    @commands.cooldown(2, 10, commands.BucketType.user)
    @commands.guild_only()
    @commands.command()
    async def ata(self, ctx, *, texto='ATA'):
        guild_id = str(ctx.guild.id)
        user_id = str(ctx.author.id)
        if guild_id in limitador_log:
            if str(ctx.message.channel.id) == limitador_log[guild_id]:
                if len(texto) >= 20:
                    return await ctx.send('Tente colocar um texto com menos de 20 letras!')
                if texto == 'ATA' or texto == 'Ata' or texto == 'ata':
                    img = Image.open('monica.png')
                    msg = await ctx.channel.send(f'Sua imagem está carregando {ctx.author.name}! <a:carregando:'
                                       f'509840579316940800>')
                    fonte = ImageFont.truetype('BEBAS.ttf', 60)
                    escrever = ImageDraw.Draw(img)
                    escrever.text(xy=(400, 130), text=f"{texto}", fill=(0, 0, 0), font=fonte)
                    img.save('mnc.png')
                    await msg.delete()
                    await ctx.channel.send(file=discord.File('mnc.png'))
                elif len(texto) <= 15:
                    img = Image.open('monica.png')
                    msg = await ctx.channel.send(f'Sua imagem está carregando {ctx.author.name}! <a:carregando:'
                                       f'509840579316940800>')
                    fonte = ImageFont.truetype('BEBAS.ttf', 30)
                    escrever = ImageDraw.Draw(img)
                    escrever.text(xy=(380, 130), text=f"{texto}", fill=(0, 0, 0), font=fonte)
                    img.save('mnc.png')
                    await msg.delete()
                    await ctx.channel.send(file=discord.File('mnc.png'))
                else:
                    img = Image.open('monica.png')
                    msg = await ctx.channel.send(f'Sua imagem está carregando {ctx.author.name}! <a:carregando:'
                                       f'509840579316940800>')
                    fonte = ImageFont.truetype('BEBAS.ttf', 30)
                    escrever = ImageDraw.Draw(img)
                    escrever.text(xy=(340, 130), text=f"{texto}", fill=(0, 0, 0), font=fonte)
                    img.save('mnc.png')
                    await msg.delete()
                    await ctx.channel.send(file=discord.File('mnc.png'))
            else:
                guild = ctx.guild.get_channel(int(limitador_log[guild_id]))
                await ctx.send(f'Esse não foi o canal definido para usar os comandos. Tente utilizar o canal {guild}')
                return
        else:
            if len(texto) >= 20:
                return await ctx.send('Tente colocar um texto com menos de 20 letras!')
            if texto == 'ATA' or texto == 'Ata' or texto == 'ata':
                img = Image.open('monica.png')
                msg = await ctx.channel.send(f'Sua imagem está carregando {ctx.author.name}! <a:carregando:'
                                       f'509840579316940800>')
                fonte = ImageFont.truetype('BEBAS.ttf', 60)
                escrever = ImageDraw.Draw(img)
                escrever.text(xy=(400, 130), text=f"{texto}", fill=(0, 0, 0), font=fonte)
                img.save('mnc.png')
                await msg.delete()
                await ctx.channel.send(file=discord.File('mnc.png'))
            elif len(texto) <= 15:
                msg = await ctx.channel.send(f'Sua imagem está carregando {ctx.author.name}! <a:carregando:'
                                       f'509840579316940800>')
                img = Image.open('monica.png')
                fonte = ImageFont.truetype('BEBAS.ttf', 30)
                escrever = ImageDraw.Draw(img)
                escrever.text(xy=(380, 130), text=f"{texto}", fill=(0, 0, 0), font=fonte)
                img.save('mnc.png')
                await msg.delete()
                await ctx.channel.send(file=discord.File('mnc.png'))
            else:
                img = Image.open('monica.png')
                msg = await ctx.channel.send(f'Sua imagem está carregando {ctx.author.name}! <a:carregando:'
                                       f'509840579316940800>')
                fonte = ImageFont.truetype('BEBAS.ttf', 30)
                escrever = ImageDraw.Draw(img)
                escrever.text(xy=(340, 130), text=f"{texto}", fill=(0, 0, 0), font=fonte)
                img.save('mnc.png')
                await msg.delete()
                await ctx.channel.send(file=discord.File('mnc.png'))



    @commands.guild_only()
    @commands.command()
    async def tias(self, ctx):
        msg = await ctx.channel.send(f'Sua imagem está carregando {ctx.author.name}! <a:carregando:'
                               f'509840579316940800>')
        await ctx.channel.send(file=discord.File('tias.png'))

    @commands.cooldown(2, 10, commands.BucketType.user)
    @commands.guild_only()
    @commands.command()
    async def bolsonaro(self, ctx, *, texto='Tudo comunista!'):
        guild_id = str(ctx.guild.id)
        user_id = str(ctx.author.id)
        if guild_id in limitador_log:
            if str(ctx.message.channel.id) == limitador_log[guild_id]:
                if len(texto) > 30:
                    return await ctx.send('Tente colocar um texto com menos de 30 letras!')
                if len(texto) <= 25:
                    msg = await ctx.channel.send(f'Sua imagem está carregando {ctx.author.name}! <a:carregando:'
                                       f'509840579316940800>')
                    img = Image.open('bolsonaro.png')
                    fonte = ImageFont.truetype('BEBAS.ttf', 20)
                    escrever = ImageDraw.Draw(img)
                    escrever.text(xy=(170, 80), text=f"{texto}", fill=(0, 0, 0), font=fonte)
                    img.save('blsnr.png')
                    await msg.delete()
                    await ctx.channel.send(file=discord.File('blsnr.png'))
                else:
                    msg = await ctx.channel.send(f'Sua imagem está carregando {ctx.author.name}! <a:carregando:'
                                           f'509840579316940800>')
                    img = Image.open('bolsonaro.png')
                    fonte = ImageFont.truetype('BEBAS.ttf', 20)
                    escrever = ImageDraw.Draw(img)
                    escrever.text(xy=(120, 80), text=f"{texto}", fill=(0, 0, 0), font=fonte)
                    img.save('blsnr.png')
                    await msg.delete()
                    await ctx.channel.send(file=discord.File('blsnr.png'))
            else:
                guild = ctx.guild.get_channel(int(limitador_log[guild_id]))
                await ctx.send(f'Esse não foi o canal definido para usar os comandos. Tente utilizar o canal {guild}')
                return
        else:
            if len(texto) > 30:
                return await ctx.send('Tente colocar um texto com menos de 30 letras!')
            if len(texto) <= 25:
                img = Image.open('bolsonaro.png')
                msg = await ctx.channel.send(f'Sua imagem está carregando {ctx.author.name}! <a:carregando:'
                                       f'509840579316940800>')
                fonte = ImageFont.truetype('BEBAS.ttf', 20)
                escrever = ImageDraw.Draw(img)
                escrever.text(xy=(170, 80), text=f"{texto}", fill=(0, 0, 0), font=fonte)
                img.save('blsnr.png')
                await msg.delete()
                await ctx.channel.send(file=discord.File('blsnr.png'))
            else:
                img = Image.open('bolsonaro.png')
                msg = await ctx.channel.send(f'Sua imagem está carregando {ctx.author.name}! <a:carregando:'
                                       f'509840579316940800>')
                fonte = ImageFont.truetype('BEBAS.ttf', 20)
                escrever = ImageDraw.Draw(img)
                escrever.text(xy=(120, 80), text=f"{texto}", fill=(0, 0, 0), font=fonte)
                img.save('blsnr.png')
                await msg.delete()
                await ctx.channel.send(file=discord.File('blsnr.png'))



    @commands.cooldown(2, 3, commands.BucketType.user)
    @commands.guild_only()
    @commands.command(name='reverse', aliases=['reverte', 'avesso'])
    async def reverse(self, ctx, *, text: str):
        guild_id = str(ctx.guild.id)
        user_id = str(ctx.author.id)
        if guild_id in limitador_log:
            if str(ctx.message.channel.id) == limitador_log[guild_id]:
                t_rev = text[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
                await ctx.send(f"🔁 {t_rev}")
            else:
                guild = ctx.guild.get_channel(int(limitador_log[guild_id]))
                await ctx.send(f'Esse não foi o canal definido para usar os comandos. Tente utilizar o canal {guild}')
                return
        else:
            t_rev = text[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
            await ctx.send(f"🔁 {t_rev}")

    @reverse.error
    async def reverse_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'text':
                embed = discord.Embed(title="Comando $reverse:", colour=discord.Colour(0x370c5e),
                                      description="Reverte uma frase\n \n**Como usar"
                                                  ": $reverse <texto>**")

                embed.set_author(name="Betina#9182",
                                 icon_url=betina_icon)
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                           self.client.user.name,
                                                                                           year()))
                embed.add_field(name="📖**Exemplos:**", value="$reverse 10\n$reverse irreversivel", inline=False)
                embed.add_field(name="🔀**Outros Comandos**", value="``$reverte, $avesso.``", inline=False)

                msg = await ctx.send(embed=embed)
                await msg.add_reaction("❓")


    @commands.cooldown(2, 3, commands.BucketType.user)
    @commands.guild_only()
    @commands.command()
    async def facebook(self, ctx, *, texto='Mark Zuckerberg: um androide!'):
        guild_id = str(ctx.guild.id)
        user_id = str(ctx.author.id)
        if guild_id in limitador_log:
            if str(ctx.message.channel.id) == limitador_log[guild_id]:
                if len(texto) >= 50:
                    return await ctx.send('Tente colocar um texto com menos de 50 letras!')
                else:
                    img = Image.open('face.png')
                    msg = await ctx.channel.send(f'Sua imagem está carregando {ctx.author.name}! <a:carregando:'
                                       f'509840579316940800>')
                    fonte = ImageFont.truetype('Tahoma.ttf', 20)
                    escrever = ImageDraw.Draw(img)
                    escrever.text(xy=(15, 60), text=f"{texto}", fill=(0, 0, 0), font=fonte)
                    img.save('fc.png')
                    await msg.delete()
                    await ctx.channel.send(file=discord.File('fc.png'))
            else:
                guild = ctx.guild.get_channel(int(limitador_log[guild_id]))
                await ctx.send(f'Esse não foi o canal definido para usar os comandos. Tente utilizar o canal {guild}')
                return
        else:
            if len(texto) >= 50:
                return await ctx.send('Tente colocar um texto com menos de 40 letras!')
            else:
                img = Image.open('face.png')
                msg = await ctx.channel.send(f'Sua imagem está carregando {ctx.author.name}! <a:carregando:'
                                       f'509840579316940800>')
                fonte = ImageFont.truetype('Tahoma.ttf', 20)
                escrever = ImageDraw.Draw(img)
                escrever.text(xy=(15, 60), text=f"{texto}", fill=(0, 0, 0), font=fonte)
                img.save('fc.png')
                await msg.delete()
                await ctx.channel.send(file=discord.File('fc.png'))



    @commands.cooldown(2, 3, commands.BucketType.user)
    @commands.guild_only()
    @commands.command()
    async def twitter(self, ctx, *, texto='Eu sou um dos criadores do twitter!'):
        guild_id = str(ctx.guild.id)
        user_id = str(ctx.author.id)
        if guild_id in limitador_log:
            if str(ctx.message.channel.id) == limitador_log[guild_id]:
                if len(texto) > 52:
                    return await ctx.send('Tente colocar um texto com menos de 50 letras!')
                else:
                    img = Image.open('twitter.png')
                    msg = await ctx.channel.send(f'Sua imagem está carregando {ctx.author.name}! <a:carregando:'
                                                 f'509840579316940800>')
                    fonte = ImageFont.truetype('Tahoma.ttf', 20)
                    escrever = ImageDraw.Draw(img)
                    escrever.text(xy=(73, 30), text=f"{texto}", fill=(0, 0, 0), font=fonte)
                    img.save('ttr.png')
                    await msg.delete()
                    await ctx.channel.send(file=discord.File('ttr.png'))
            else:
                guild = ctx.guild.get_channel(int(limitador_log[guild_id]))
                await ctx.send(f'Esse não foi o canal definido para usar os comandos. Tente utilizar o canal {guild}')
                return
        else:
            if len(texto) > 52:
                return await ctx.send('Tente colocar um texto com menos de 50 letras!')
            else:
                img = Image.open('twitter.png')
                msg = await ctx.channel.send(f'Sua imagem está carregando {ctx.author.name}! <a:carregando:'
                                             f'509840579316940800>')
                fonte = ImageFont.truetype('Tahoma.ttf', 20)
                escrever = ImageDraw.Draw(img)
                escrever.text(xy=(73, 30), text=f"{texto}", fill=(0, 0, 0), font=fonte)
                img.save('ttr.png')
                await msg.delete()
                await ctx.channel.send(file=discord.File('ttr.png'))



    @commands.cooldown(2, 3, commands.BucketType.user)
    @commands.guild_only()
    @commands.command()
    async def flip(self, ctx, *, msg='Preciso de um texto para inverter'):
        result = ""
        for char in msg:
            if char in self.text_flip:
                result += self.text_flip[char]
            else:
                result += char
        await ctx.send(content=result[::-1])





def setup(client):
    client.add_cog(Diversão(client))
