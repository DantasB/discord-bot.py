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
import re
import json
import requests
import secrets
import pycep_correios


from discord.ext import commands
from forex_python.converter import CurrencyRates
from dhooks import Webhook
from discord.utils import get
from discord.ext.commands import has_permissions, MissingPermissions
from googletrans import Translator
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO


def open_image(path):
    newImage = Image.open(path)
    return newImage


# Save Image
def save_image(image, path):
    image.save(path, 'png')


# Create a new image with the given size
def create_image(i, j):
    image = Image.new("RGB", (i, j), "white")
    return image


# Get the pixel from the given image
def get_pixel(image, i, j):
    # Inside image bounds?
    width, height = image.size
    if i > width or j > height:
        return None

    # Get Pixel
    pixel = image.getpixel((i, j))
    return pixel


def get_saturation(value, quadrant):
    if value > 223:
        return 255
    elif value > 159:
        if quadrant != 1:
            return 255

        return 0
    elif value > 95:
        if quadrant == 0 or quadrant == 3:
            return 255

        return 0
    elif value > 32:
        if quadrant == 1:
            return 255

        return 0
    else:
        return 0
    
  
# devemais e devemenos
devedores = {}
devidos = {}

betina_icon = ""

with open('limitador.json', 'r') as file:
    try:
        limitador_log = json.load(file)
    except ValueError:
        limitador_log = {}


class Utilidades:
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
                await ctx.send(
                    '**{} deve R$ {} ao {}**'.format(member.mention, devidos[ctx.author], ctx.author.mention))
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

    @commands.guild_only()
    @commands.command()
    async def clima(self, ctx, *, buscar=None):
        guild_id = str(ctx.guild.id)
        user_id = str(ctx.author.id)
        if guild_id in limitador_log:
            if str(ctx.message.channel.id) == limitador_log[guild_id]:
                if buscar is None:
                    await ctx.send(f"Olá {ctx.author.mention}, você precisa digitar uma cidade ou país.")
                    return

                busca = str(buscar).replace(" ", "%20")
                r = requests.get(f'http://api.apixu.com/v1/current.json?key=6a0d3673a1ec4ceb8f5152802182112&q={busca}')
                if r.status_code == 200:
                    js = r.json()

                embed = discord.Embed(title="Clima do dia:", color=0x370c5e)
                embed.add_field(name="Nome", value=str(js['location']['name']), inline=False)
                embed.add_field(name="Região", value=str(js['location']['region']), inline=True)
                embed.add_field(name="País", value=str(js['location']['country']), inline=True)
                local = str(js['location']['lat']) + "/" + str(js['location']['lon'])
                embed.add_field(name="Lat & Lon", value=str(local), inline=True)
                temp = str(js['current']['temp_c']) + "/" + str(js['current']['temp_f'])
                embed.add_field(name="c° & f°", value=str(temp), inline=True)
                url = "https:" + str(js['current']['condition']["icon"])
                embed.set_thumbnail(url=url)
                embed.set_footer(text="Climatempo 2019")
                await ctx.send(embed=embed)
            else:
                guild = ctx.guild.get_channel(int(limitador_log[guild_id]))
                await ctx.send(f'Esse não foi o canal definido para usar os comandos. Tente utilizar o canal {guild}')
                return
        else:
            if buscar is None:
                await ctx.send(f"Olá {ctx.author.mention}, você precisa digitar uma cidade ou país.")
                return

            busca = str(buscar).replace(" ", "%20")
            r = requests.get(f'http://api.apixu.com/v1/current.json?key=6a0d3673a1ec4ceb8f5152802182112&q={busca}')
            if r.status_code == 200:
                js = r.json()

            embed = discord.Embed(title="Clima do dia:", color=0x370c5e)
            embed.add_field(name="Nome", value=str(js['location']['name']), inline=False)
            embed.add_field(name="Região", value=str(js['location']['region']), inline=True)
            embed.add_field(name="País", value=str(js['location']['country']), inline=True)
            local = str(js['location']['lat']) + "/" + str(js['location']['lon'])
            embed.add_field(name="Lat & Lon", value=str(local), inline=True)
            temp = str(js['current']['temp_c']) + "/" + str(js['current']['temp_f'])
            embed.add_field(name="c° & f°", value=str(temp), inline=True)
            url = "https:" + str(js['current']['condition']["icon"])
            embed.set_thumbnail(url=url)
            embed.set_footer(text="Climatempo 2019")
            await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command()
    async def picture(self, ctx, *, user: discord.Member = None):
        guild_id = str(ctx.guild.id)
        user_id = str(ctx.author.id)
        if guild_id in limitador_log:
            if str(ctx.message.channel.id) == limitador_log[guild_id]:
                if user is None:
                    usuario = ctx.author.avatar_url_as(size=256)
                    texto = f"Olá {ctx.author.name}, está é sua imagem de perfil."
                else:
                    usuario = user.avatar_url_as(size=256)
                    texto = f"Olá {ctx.author.name}, está é a imagem do usuário {user.name}"

                embed = discord.Embed(title=texto, color=0x370c5e)
                embed.set_image(url=usuario)
                embed.set_footer(text=self.client.user.name + " Brazilian Bot.")

                await ctx.send(embed=embed)
            else:
                guild = ctx.guild.get_channel(int(limitador_log[guild_id]))
                await ctx.send(f'Esse não foi o canal definido para usar os comandos. Tente utilizar o canal {guild}')
                return
        else:
            if user is None:
                usuario = ctx.author.avatar_url_as(size=256)
                texto = f"Olá {ctx.author.name}, está é sua imagem de perfil."
            else:
                usuario = user.avatar_url_as(size=256)
                texto = f"Olá {ctx.author.name}, está é a imagem do usuário {user.name}"

            embed = discord.Embed(title=texto, color=0x370c5e)
            embed.set_image(url=usuario)
            embed.set_footer(text=self.client.user.name + " Brazilian Bot.", icon_url=betina_icon)

            await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command()
    async def gerasenha(self, ctx, nbytes: int = 18):
        guild_id = str(ctx.guild.id)
        user_id = str(ctx.author.id)
        if guild_id in limitador_log:
            if str(ctx.message.channel.id) == limitador_log[guild_id]:
                if nbytes not in range(3, 1401):
                    return await ctx.send("Só aceito números entre 3 e 1400!")
                if hasattr(ctx, 'guild') and ctx.guild is not None:
                    await ctx.send(
                        f"Estou enviando uma mensagem direta para você contendo a sua senha, **{ctx.author.name}**")

                await ctx.author.send(f"🎁 **Aqui está sua senha:**\n{secrets.token_urlsafe(nbytes)}")
            else:
                guild = ctx.guild.get_channel(int(limitador_log[guild_id]))
                await ctx.send(f'Esse não foi o canal definido para usar os comandos. Tente utilizar o canal {guild}')
                return
        else:
            if nbytes not in range(3, 1401):
                return await ctx.send("Só aceito números entre 3 e 1400!")
            if hasattr(ctx, 'guild') and ctx.guild is not None:
                await ctx.send(
                    f"Estou enviando uma mensagem direta para você contendo a sua senha, **{ctx.author.name}**")

            await ctx.author.send(f"🎁 **Aqui está sua senha:**\n{secrets.token_urlsafe(nbytes)}")

    @commands.guild_only()
    @commands.command(name='geraconvite', aliases=['invitegenerator', 'gerador'])
    @has_permissions(manage_channels=True)
    async def invite(self, ctx):
        if ctx.message.author.avatar_url_as(static_format='png')[54:].startswith('a_'):
            avi = ctx.message.author.avatar_url.rsplit("?", 1)[0]
        else:
            avi = ctx.message.author.avatar_url_as(static_format='png')

        channel = ctx.channel
        invitelinknew = await ctx.channel.create_invite(unique=True, reason='Automatizar a função do usuário!')
        embedMsg = discord.Embed(color=0x370c5e)
        embedMsg.add_field(name="Convite criado:", value=invitelinknew)
        embedMsg.set_author(name=f"{ctx.message.author.name}", icon_url=f"{avi}")
        embedMsg.set_footer(text="Convite do servidor", icon_url=ctx.message.guild.icon_url)
        await ctx.send(embed=embedMsg)

    @invite.error
    async def invite_handler(self, ctx, error):
        if isinstance(error, MissingPermissions):
            embed = discord.Embed(
                title="Comando $geraconvite: Gera um convite para o seu servidor"
                      "\n \n**Como usar: $geraconvite**", colour=discord.Colour(0x370c5e))

            embed.set_author(name="Betina#9182",
                             icon_url=betina_icon)
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url=betina_icon)
            embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                            "ter a permissão de* ``"
                                                            "Gerenciar canais`` *para utilizar este comando!*",
                            inline=False)
            embed.add_field(name="📖**Exemplos:**", value="$gerador"
                                                          "\n$invitegenerator"
                                                          "", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$gerador, $invitegenerator.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")

    @commands.guild_only()
    @commands.command(name='tradutor', aliases=['translate', 'traduz'])
    async def traduz(self, ctx, *, arg):
        if ctx.message.author.avatar_url_as(static_format='png')[54:].startswith('a_'):
            avi = ctx.message.author.avatar_url.rsplit("?", 1)[0]
        else:
            avi = ctx.message.author.avatar_url_as(static_format='png')

        guild_id = str(ctx.guild.id)
        user_id = str(ctx.author.id)
        translator = Translator()
        if guild_id in limitador_log:
            if str(ctx.message.channel.id) == limitador_log[guild_id]:
                embedMsg = discord.Embed(color=0x370c5e)
                mensagem = translator.translate(f'{arg}', dest='pt')
                embedMsg.add_field(name="➡ Mensagem enviada:", value=arg, inline=False)
                embedMsg.add_field(name="🔙 Mensagem traduzida:", value=mensagem.text, inline=False)
                embedMsg.set_author(name=f"{ctx.message.author.name}", icon_url=f"{avi}")
                embedMsg.set_footer(text="Google Translate 2019")
                await ctx.send(embed=embedMsg)
            else:
                guild = ctx.guild.get_channel(int(limitador_log[guild_id]))
                await ctx.send(f'Esse não foi o canal definido para usar os comandos. Tente utilizar o canal {guild}')
                return
        else:
            embedMsg = discord.Embed(color=0x370c5e)
            mensagem = translator.translate(f'{arg}', dest='pt')
            embedMsg.add_field(name="➡ Mensagem enviada:", value=arg, inline=False)
            embedMsg.add_field(name="🔙 Mensagem traduzida:", value=mensagem.text, inline=False)
            embedMsg.set_author(name=f"{ctx.message.author.name}", icon_url=f"{avi}")
            embedMsg.set_footer(text="Google Translate 2019")
            await ctx.send(embed=embedMsg)

    @traduz.error
    async def traduz_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'arg':
                embed = discord.Embed(title="Comando $traduz:", colour=discord.Colour(0x370c5e),
                                      description="Traduz uma frase\n \n**Como"
                                                  " usar: $traduz <texto>**")

                embed.set_author(name="Betina#9182",
                                 icon_url=betina_icon)
                embed.set_footer(text="Betina Brazilian Bot",
                                 icon_url=betina_icon)

                embed.add_field(name="📖**Exemplos:**", value="$traduz como se dize esto\n$traduz knowledge",
                                inline=False)
                embed.add_field(name="🔀**Outros Comandos**", value="``$translate, $traduzir.``", inline=False)

                msg = await ctx.send(embed=embed)
                await msg.add_reaction("❓")

    @commands.guild_only()
    @commands.command(name='buscacep')
    async def cep(self, ctx, buscar):
        guild_id = str(ctx.guild.id)
        user_id = str(ctx.author.id)
        if guild_id in limitador_log:
            if str(ctx.message.channel.id) == limitador_log[guild_id]:
                if buscar is None:
                    await ctx.send(f"Olá {ctx.author.mention}, digite um cep.")
                    return
                try:
                    endereco = pycep_correios.consultar_cep(f'{buscar}')
                    embed = discord.Embed(title=f"Cep procurado {buscar}:", color=0x370c5e)
                    embed.add_field(name="Bairro", value=endereco['bairro'])
                    embed.add_field(name="Cep", value=endereco['cep'], inline=True)
                    embed.add_field(name="Cidade", value=endereco['cidade'], inline=True)
                    embed.add_field(name="Uf", value=endereco['uf'], inline=True)
                    embed.add_field(name="Rua", value=endereco['end'], inline=True)
                    embed.add_field(name="Bairro", value=endereco['bairro'], inline=True)
                    embed.set_thumbnail(url='https://warehouse-camo.cmh1.psfhosted.org/84cd'
                                            '73e1f12421aca2cc6ae603ecdb96d312f663/68747470733a2f'
                                            '2f7261772e67697468756275736572636f6e74656e742e636f6d2'
                                            'f6d7374757474676172742f70796365702d636f727265696f732f6465'
                                            '76656c6f702f646f63732f5f7374617469632f6c6f676f2e6a7067')
                    embed.set_footer(text="Correios 2019")
                    await ctx.send(embed=embed)
                except ExcecaoPyCEPCorreios as exc:
                    embed = discord.Embed(title="Comando $buscacep:", colour=discord.Colour(0x370c5e),
                                          description="Busca um cep\n \n**Como"
                                                      " usar: $busca <cep>**")

                    embed.set_author(name="Betina#9182",
                                     icon_url=betina_icon)
                    embed.set_footer(text="Betina Brazilian Bot",
                                     icon_url=betina_icon)
                    embed.add_field(name="❗**Atenção:**", value="Utilize um cep existente!", inline=False)
                    msg = await ctx.send(embed=embed)
                    await msg.add_reaction("❓")
                    return
            else:
                guild = ctx.guild.get_channel(int(limitador_log[guild_id]))
                await ctx.send(f'Esse não foi o canal definido para usar os comandos. Tente utilizar o canal {guild}')
                return
        else:
            if buscar is None:
                await ctx.send(f"Olá {ctx.author.mention}, digite um cep.")
                return
            try:
                endereco = pycep_correios.consultar_cep(f'{buscar}')
                embed = discord.Embed(title=f"Cep procurado {buscar}:", color=0x370c5e)
                embed.add_field(name="Bairro", value=endereco['bairro'])
                embed.add_field(name="Cep", value=endereco['cep'], inline=True)
                embed.add_field(name="Cidade", value=endereco['cidade'], inline=True)
                embed.add_field(name="Uf", value=endereco['uf'], inline=True)
                embed.add_field(name="Rua", value=endereco['end'], inline=True)
                embed.add_field(name="Bairro", value=endereco['bairro'], inline=True)
                embed.set_thumbnail(url='https://warehouse-camo.cmh1.psfhosted.org/84cd'
                                        '73e1f12421aca2cc6ae603ecdb96d312f663/68747470733a2f'
                                        '2f7261772e67697468756275736572636f6e74656e742e636f6d2'
                                        'f6d7374757474676172742f70796365702d636f727265696f732f6465'
                                        '76656c6f702f646f63732f5f7374617469632f6c6f676f2e6a7067')
                embed.set_footer(text="Correios 2019")
                await ctx.send(embed=embed)
            except ExcecaoPyCEPCorreios as exc:
                embed = discord.Embed(title="Comando $buscacep:", colour=discord.Colour(0x370c5e),
                                      description="Busca um cep\n \n**Como"
                                                  " usar: $busca <cep>**")

                embed.set_author(name="Betina#9182",
                                 icon_url=betina_icon)
                embed.set_footer(text="Betina Brazilian Bot",
                                 icon_url=betina_icon)
                embed.add_field(name="❗**Atenção:**", value="Utilize um cep existente!", inline=False)
                msg = await ctx.send(embed=embed)
                await msg.add_reaction("❓")
                return

    @commands.guild_only()
    @commands.command(name='cor', aliases=['randomcolour', 'geracor'])
    async def cor(self, ctx):
        guild_id = str(ctx.guild.id)
        user_id = str(ctx.author.id)
        if guild_id in limitador_log:
            if str(ctx.message.channel.id) == limitador_log[guild_id]:
                color = "%06x" % random.randint(0, 0xFFFFFF)
                if re.search(r'^(?:[0-9a-fA-F]{3}){1,2}$', color):
                    color = discord.Color(int(color, 16))
                else:
                    await ctx.send('cor não encontrada')

                if ctx.message.author.avatar_url_as(static_format='png')[54:].startswith('a_'):
                    avi = ctx.message.author.avatar_url.rsplit("?", 1)[0]
                else:
                    avi = ctx.message.author.avatar_url_as(static_format='png')
                embed = discord.Embed(title=f"<:gay:539489743067545622> Cor gerada: {color}",
                                      colour=color)
                embed.set_footer(text="Betina Brazilian Bot", icon_url=betina_icon)
                await ctx.send(embed=embed)
            else:
                guild = ctx.guild.get_channel(int(limitador_log[guild_id]))
                await ctx.send(f'Esse não foi o canal definido para usar os comandos. Tente utilizar o canal {guild}')
                return
        else:
            color = "%06x" % random.randint(0, 0xFFFFFF)
            if re.search(r'^(?:[0-9a-fA-F]{3}){1,2}$', color):
                color = discord.Color(int(color, 16))
            else:
                await ctx.send('cor não encontrada')

            if ctx.message.author.avatar_url_as(static_format='png')[54:].startswith('a_'):
                avi = ctx.message.author.avatar_url.rsplit("?", 1)[0]
            else:
                avi = ctx.message.author.avatar_url_as(static_format='png')
            embed = discord.Embed(title=f"<:gay:539489743067545622> Cor gerada: {color}",
                                  colour=color)
            embed.set_footer(text="Betina Brazilian Bot", icon_url=betina_icon)
            await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command(name='pb', aliases=['bw'])
    async def preto_e_branco(self, ctx, user: discord.Member = None):
        guild_id = str(ctx.guild.id)
        user_id = str(ctx.author.id)
        if guild_id in limitador_log:
            if str(ctx.message.channel.id) == limitador_log[guild_id]:
                try:
                    if user is None:
                        imagem = ctx.author.avatar_url_as(size=256)
                        response = requests.get(imagem)
                        image = Image.open(BytesIO(response.content))
                        texto = f"Olá {ctx.author.name}, está é sua imagem de perfil em preto e branco."
                        width, height = image.size

                        new = create_image(width, height)
                        pixels = new.load()

                        for i in range(width):
                            for j in range(height):
                                pixel = get_pixel(image, i, j)

                                red = pixel[0]
                                green = pixel[1]
                                blue = pixel[2]

                                gray = (red * 0.299) + (green * 0.587) + (blue * 0.114)

                                pixels[i, j] = (int(gray), int(gray), int(gray))
                    else:
                        imagem = user.avatar_url_as(size=256)
                        response = requests.get(imagem)
                        image = Image.open(BytesIO(response.content))
                        texto = f"Olá {ctx.author.name}, está é a imagem do usuário {user.name} em preto e branco."
                        width, height = image.size

                        new = create_image(width, height)
                        pixels = new.load()

                        for i in range(width):
                            for j in range(height):
                                pixel = get_pixel(image, i, j)

                                red = pixel[0]
                                green = pixel[1]
                                blue = pixel[2]

                                gray = (red * 0.299) + (green * 0.587) + (blue * 0.114)

                                pixels[i, j] = (int(gray), int(gray), int(gray))
                    new.save('usuariopb.png')
                    await ctx.channel.send(file=discord.File('usuariopb.png'))
                except:
                    return await ctx.send('A imagem enviada é muito grande. Eu não pude converter')
            else:
                guild = ctx.guild.get_channel(int(limitador_log[guild_id]))
                await ctx.send(f'Esse não foi o canal definido para usar os comandos. Tente utilizar o canal {guild}')
                return
        else:
            try:
                if user is None:
                    imagem = ctx.author.avatar_url_as(size=256)
                    response = requests.get(imagem)
                    image = Image.open(BytesIO(response.content))
                    texto = f"Olá {ctx.author.name}, está é sua imagem de perfil em preto e branco."
                    width, height = image.size

                    new = create_image(width, height)
                    pixels = new.load()

                    for i in range(width):
                        for j in range(height):
                            pixel = get_pixel(image, i, j)

                            red = pixel[0]
                            green = pixel[1]
                            blue = pixel[2]

                            gray = (red * 0.299) + (green * 0.587) + (blue * 0.114)

                            pixels[i, j] = (int(gray), int(gray), int(gray))
                else:
                    imagem = user.avatar_url_as(size=256)
                    response = requests.get(imagem)
                    image = Image.open(BytesIO(response.content))
                    texto = f"Olá {ctx.author.name}, está é a imagem do usuário {user.name} em preto e branco."
                    width, height = image.size

                    new = create_image(width, height)
                    pixels = new.load()

                    for i in range(width):
                        for j in range(height):
                            pixel = get_pixel(image, i, j)

                            red = pixel[0]
                            green = pixel[1]
                            blue = pixel[2]

                            gray = (red * 0.299) + (green * 0.587) + (blue * 0.114)

                            pixels[i, j] = (int(gray), int(gray), int(gray))
                new.save('usuariopb.png')
                await ctx.channel.send(file=discord.File('usuariopb.png'))
            except:
                return await ctx.send('A imagem enviada é muito grande. Eu não pude converter')

    @commands.guild_only()
    @commands.command(name='primario', aliases=['primary'])
    async def primario(self, ctx, user: discord.Member = None):
        guild_id = str(ctx.guild.id)
        user_id = str(ctx.author.id)
        if guild_id in limitador_log:
            if str(ctx.message.channel.id) == limitador_log[guild_id]:
                try:
                    if user is None:
                        imagem = ctx.author.avatar_url_as(size=256)
                        response = requests.get(imagem)
                        image = Image.open(BytesIO(response.content))
                        texto = f"Olá {ctx.author.name}, está é sua imagem de perfil em preto e branco."
                        width, height = image.size

                        new = create_image(width, height)
                        pixels = new.load()

                        for i in range(width):
                            for j in range(height):
                                # Get Pixel
                                pixel = get_pixel(image, i, j)

                                red = pixel[0]
                                green = pixel[1]
                                blue = pixel[2]

                                if red > 127:
                                    red = 255
                                else:
                                    red = 0
                                if green > 127:
                                    green = 255
                                else:
                                    green = 0
                                if blue > 127:
                                    blue = 255
                                else:
                                    blue = 0

                                pixels[i, j] = (int(red), int(green), int(blue))
                    else:
                        imagem = user.avatar_url_as(size=256)
                        response = requests.get(imagem)
                        image = Image.open(BytesIO(response.content))
                        texto = f"Olá {ctx.author.name}, está é a imagem do usuário {user.name} em preto e branco."
                        width, height = image.size

                        new = create_image(width, height)
                        pixels = new.load()

                        for i in range(width):
                            for j in range(height):
                                # Get Pixel
                                pixel = get_pixel(image, i, j)

                                red = pixel[0]
                                green = pixel[1]
                                blue = pixel[2]

                                if red > 127:
                                    red = 255
                                else:
                                    red = 0
                                if green > 127:
                                    green = 255
                                else:
                                    green = 0
                                if blue > 127:
                                    blue = 255
                                else:
                                    blue = 0

                                pixels[i, j] = (int(red), int(green), int(blue))
                    new.save('usuarioprimario.png')
                    await ctx.channel.send(file=discord.File('usuarioprimario.png'))
                except:
                    return await ctx.send('A imagem enviada é muito grande. Eu não pude converter')
            else:
                guild = ctx.guild.get_channel(int(limitador_log[guild_id]))
                await ctx.send(f'Esse não foi o canal definido para usar os comandos. Tente utilizar o canal {guild}')
                return
        else:
            try:
                if user is None:
                    imagem = ctx.author.avatar_url_as(size=256)
                    response = requests.get(imagem)
                    image = Image.open(BytesIO(response.content))
                    texto = f"Olá {ctx.author.name}, está é sua imagem de perfil em preto e branco."
                    width, height = image.size

                    new = create_image(width, height)
                    pixels = new.load()

                    for i in range(width):
                        for j in range(height):
                            # Get Pixel
                            pixel = get_pixel(image, i, j)

                            red = pixel[0]
                            green = pixel[1]
                            blue = pixel[2]

                            if red > 127:
                                red = 255
                            else:
                                red = 0
                            if green > 127:
                                green = 255
                            else:
                                green = 0
                            if blue > 127:
                                blue = 255
                            else:
                                blue = 0

                            pixels[i, j] = (int(red), int(green), int(blue))
                else:
                    imagem = user.avatar_url_as(size=256)
                    response = requests.get(imagem)
                    image = Image.open(BytesIO(response.content))
                    texto = f"Olá {ctx.author.name}, está é a imagem do usuário {user.name} em preto e branco."
                    width, height = image.size

                    new = create_image(width, height)
                    pixels = new.load()

                    for i in range(width):
                        for j in range(height):
                            # Get Pixel
                            pixel = get_pixel(image, i, j)

                            red = pixel[0]
                            green = pixel[1]
                            blue = pixel[2]

                            if red > 127:
                                red = 255
                            else:
                                red = 0
                            if green > 127:
                                green = 255
                            else:
                                green = 0
                            if blue > 127:
                                blue = 255
                            else:
                                blue = 0

                            pixels[i, j] = (int(red), int(green), int(blue))
                new.save('usuarioprimario.png')
                await ctx.channel.send(file=discord.File('usuarioprimario.png'))
            except:
                return await ctx.send('A imagem enviada é muito grande. Eu não pude converter')

    @commands.guild_only()
    @commands.command(name='pontilhado', aliases=['dither'])
    async def pontilhado(self, ctx, user: discord.Member = None):
        guild_id = str(ctx.guild.id)
        user_id = str(ctx.author.id)
        if guild_id in limitador_log:
            if str(ctx.message.channel.id) == limitador_log[guild_id]:
                try:
                    if user is None:
                        imagem = ctx.author.avatar_url_as(size=256)
                        response = requests.get(imagem)
                        image = Image.open(BytesIO(response.content))
                        texto = f"Olá {ctx.author.name}, está é sua imagem de perfil em preto e branco."
                        width, height = image.size

                        new = create_image(width, height)
                        pixels = new.load()

                        for i in range(0, width, 2):
                            for j in range(0, height, 2):
                                # Get Pixels
                                p1 = get_pixel(image, i, j)
                                p2 = get_pixel(image, i, j + 1)
                                p3 = get_pixel(image, i + 1, j)
                                p4 = get_pixel(image, i + 1, j + 1)

                                # Color Saturation by RGB channel
                                red = (p1[0] + p2[0] + p3[0] + p4[0]) / 4
                                green = (p1[1] + p2[1] + p3[1] + p4[1]) / 4
                                blue = (p1[2] + p2[2] + p3[2] + p4[2]) / 4

                                # Results by channel
                                r = [0, 0, 0, 0]
                                g = [0, 0, 0, 0]
                                b = [0, 0, 0, 0]

                                # Get Quadrant Color
                                for x in range(0, 4):
                                    r[x] = get_saturation(red, x)
                                    g[x] = get_saturation(green, x)
                                    b[x] = get_saturation(blue, x)

                                # Set Dithered Colors
                                pixels[i, j] = (r[0], g[0], b[0])
                                pixels[i, j + 1] = (r[1], g[1], b[1])
                                pixels[i + 1, j] = (r[2], g[2], b[2])
                                pixels[i + 1, j + 1] = (r[3], g[3], b[3])
                    else:
                        imagem = user.avatar_url_as(size=256)
                        response = requests.get(imagem)
                        image = Image.open(BytesIO(response.content))
                        texto = f"Olá {ctx.author.name}, está é a imagem do usuário {user.name} em preto e branco."
                        width, height = image.size

                        new = create_image(width, height)
                        pixels = new.load()

                        for i in range(0, width, 2):
                            for j in range(0, height, 2):
                                # Get Pixels
                                p1 = get_pixel(image, i, j)
                                p2 = get_pixel(image, i, j + 1)
                                p3 = get_pixel(image, i + 1, j)
                                p4 = get_pixel(image, i + 1, j + 1)

                                # Color Saturation by RGB channel
                                red = (p1[0] + p2[0] + p3[0] + p4[0]) / 4
                                green = (p1[1] + p2[1] + p3[1] + p4[1]) / 4
                                blue = (p1[2] + p2[2] + p3[2] + p4[2]) / 4

                                # Results by channel
                                r = [0, 0, 0, 0]
                                g = [0, 0, 0, 0]
                                b = [0, 0, 0, 0]

                                # Get Quadrant Color
                                for x in range(0, 4):
                                    r[x] = get_saturation(red, x)
                                    g[x] = get_saturation(green, x)
                                    b[x] = get_saturation(blue, x)

                                # Set Dithered Colors
                                pixels[i, j] = (r[0], g[0], b[0])
                                pixels[i, j + 1] = (r[1], g[1], b[1])
                                pixels[i + 1, j] = (r[2], g[2], b[2])
                                pixels[i + 1, j + 1] = (r[3], g[3], b[3])
                    new.save('usuariopontilhado.png')
                    await ctx.channel.send(file=discord.File('usuariopontilhado.png'))
                except:
                    return await ctx.send('A imagem enviada é muito grande. Eu não pude converter')
            else:
                guild = ctx.guild.get_channel(int(limitador_log[guild_id]))
                await ctx.send(f'Esse não foi o canal definido para usar os comandos. Tente utilizar o canal {guild}')
                return
        else:
            try:
                if user is None:
                    imagem = ctx.author.avatar_url_as(size=256)
                    response = requests.get(imagem)
                    image = Image.open(BytesIO(response.content))
                    texto = f"Olá {ctx.author.name}, está é sua imagem de perfil em preto e branco."
                    width, height = image.size

                    new = create_image(width, height)
                    pixels = new.load()

                    for i in range(0, width, 2):
                        for j in range(0, height, 2):
                            # Get Pixels
                            p1 = get_pixel(image, i, j)
                            p2 = get_pixel(image, i, j + 1)
                            p3 = get_pixel(image, i + 1, j)
                            p4 = get_pixel(image, i + 1, j + 1)

                            # Color Saturation by RGB channel
                            red = (p1[0] + p2[0] + p3[0] + p4[0]) / 4
                            green = (p1[1] + p2[1] + p3[1] + p4[1]) / 4
                            blue = (p1[2] + p2[2] + p3[2] + p4[2]) / 4

                            # Results by channel
                            r = [0, 0, 0, 0]
                            g = [0, 0, 0, 0]
                            b = [0, 0, 0, 0]

                            # Get Quadrant Color
                            for x in range(0, 4):
                                r[x] = get_saturation(red, x)
                                g[x] = get_saturation(green, x)
                                b[x] = get_saturation(blue, x)

                            # Set Dithered Colors
                            pixels[i, j] = (r[0], g[0], b[0])
                            pixels[i, j + 1] = (r[1], g[1], b[1])
                            pixels[i + 1, j] = (r[2], g[2], b[2])
                            pixels[i + 1, j + 1] = (r[3], g[3], b[3])
                else:
                    imagem = user.avatar_url_as(size=256)
                    response = requests.get(imagem)
                    image = Image.open(BytesIO(response.content))
                    texto = f"Olá {ctx.author.name}, está é a imagem do usuário {user.name} em preto e branco."
                    width, height = image.size

                    new = create_image(width, height)
                    pixels = new.load()

                    for i in range(0, width, 2):
                        for j in range(0, height, 2):
                            # Get Pixels
                            p1 = get_pixel(image, i, j)
                            p2 = get_pixel(image, i, j + 1)
                            p3 = get_pixel(image, i + 1, j)
                            p4 = get_pixel(image, i + 1, j + 1)

                            # Color Saturation by RGB channel
                            red = (p1[0] + p2[0] + p3[0] + p4[0]) / 4
                            green = (p1[1] + p2[1] + p3[1] + p4[1]) / 4
                            blue = (p1[2] + p2[2] + p3[2] + p4[2]) / 4

                            # Results by channel
                            r = [0, 0, 0, 0]
                            g = [0, 0, 0, 0]
                            b = [0, 0, 0, 0]

                            # Get Quadrant Color
                            for x in range(0, 4):
                                r[x] = get_saturation(red, x)
                                g[x] = get_saturation(green, x)
                                b[x] = get_saturation(blue, x)

                            # Set Dithered Colors
                            pixels[i, j] = (r[0], g[0], b[0])
                            pixels[i, j + 1] = (r[1], g[1], b[1])
                            pixels[i + 1, j] = (r[2], g[2], b[2])
                            pixels[i + 1, j + 1] = (r[3], g[3], b[3])
                new.save('usuariopontilhado.png')
                await ctx.channel.send(file=discord.File('usuariopontilhado.png'))
            except:
                return await ctx.send('A imagem enviada é muito grande. Eu não pude converter')


def setup(client):
    client.add_cog(Utilidades(client))
