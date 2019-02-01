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
import psutil
import logging
import asyncio
import requests
import time

from discord.ext import commands
from forex_python.converter import CurrencyRates
from dhooks import Webhook
from discord.utils import get
from discord.ext.commands import has_permissions, MissingPermissions
from horario import *
from PIL import Image, ImageDraw, ImageFont, ImageOps
from io import BytesIO


with open('prefixes.json', 'r') as file:
    try:
        bot_prefix = json.load(file)
    except ValueError:
        bot_prefix = {}

        
async def get_pre(client, message):
    guild_id = str(message.guild.id)
    if guild_id in bot_prefix:
        return bot_prefix[guild_id]
    return '$'

startup_extensions = ['Music', 'Diversao', 'Interacao', 'Utilidades', 'Error', 'Administracao']
prefix = get_pre
client = commands.Bot(command_prefix=prefix)
TOKEN = 'Seu discord bot token'
client.remove_command('help')

logging.basicConfig(level=logging.WARNING)


with open('users.json', 'r') as file:
    try:
        level_system = json.load(file)
    except ValueError:
        level_system = {}


def lvl_up(author_id, guild_id):
    xp_atual = level_system[guild_id][author_id]['experiencia']
    level_atual = level_system[guild_id][author_id]['level']

    if xp_atual >= round((5 * (level_atual ** 3))):
        level_system[guild_id][author_id]['level'] += 1
        return True
    else:
        return False


c = 0

# Musica
players = {}

# tretas
lista = ['[nome] saiu de casa novo']#Deve ser escrito como: '[nome] fez algo'

# afk
with open('afks.json', 'r') as file:
    try:
        afklist = json.load(file)
    except ValueError:
        afklist = {}

with open('reactions.json', 'r') as file:
    try:
        reactions_list = json.load(file)
    except ValueError:
        reactions_list = {}

with open('join.json', 'r') as file:
    try:
        join_list = json.load(file)
    except ValueError:
        join_list = {}

with open('leave.json', 'r') as file:
    try:
        leave_list = json.load(file)
    except ValueError:
        leave_list = {}

with open('reactionslogsin.json', 'r') as file:
    try:
        reactions_logs_in = json.load(file)
    except ValueError:
        reactions_logs_in = {}
        
with open('reactionslogsout.json', 'r') as file:
    try:
        reactions_logs_out = json.load(file)
    except ValueError:
        reactions_logs_out = {}
        
with open('initialsrole.json', 'r') as file:
    try:
        initial_role = json.load(file)
    except ValueError:
        initial_role = {}

with open('digitlogs.json', 'r') as file:
    try:
        digit_log = json.load(file)
    except ValueError:
        digit_log = {}
        
with open('limitador.json', 'r') as file:
    try:
        limitador_log = json.load(file)
    except ValueError:
        limitador_log = {}
        
with open('levelon.json', 'r') as file:
    try:
        level_on = json.load(file)
    except ValueError:
        level_on = {}
        
@client.event
async def on_ready():
    print('--------------BD--------------')
    print('BOT ONLINE')
    print('Nome do Bot: ' + client.user.name)
    print('ID do Bot: ' + str(client.user.id))
    print('Versao do Discord: ' + discord.__version__)
    print('--------------BD--------------')
    game = discord.Game(f"$ajuda | atualmente em {str(len(client.guilds))} serve"
                        f"rs com {str(len(set(client.users)))} usuários!")
    await client.change_presence(status=discord.Status.online, activity=game)


@client.event
async def on_member_update(before, after):
    if str(before.guild.id) in digit_log:
        if before.avatar_url_as(static_format='png')[54:].startswith('a_'):
            avi = before.avatar_url.rsplit("?", 1)[0]
        else:
            avi = before.avatar_url_as(static_format='png')
        if before.nick == after.nick:
            return
        guild = after.guild.get_channel(int(digit_log[str(before.guild.id)]))
        embed = discord.Embed(title="Apelido alterado:", colour=discord.Colour(0x370c5e))
        embed.set_thumbnail(url=avi)
        embed.add_field(name='Usuário:', value=str(before) + ' (' + str(before.name) + ')',
                        inline=False)
        if before.nick == None:
            nick1 = 'Nenhum'
        else:
            nick1 = str(before.nick)
        if after.nick == None:
            nick = 'Nenhum'
        else:
            nick = str(after.nick)
        embed.add_field(name='Apelido Anterior:', value=f'{nick1}', inline=False)
        embed.add_field(name='Apelido Posterior:', value=f'{nick}', inline=False)
        embed.add_field(name='Horário:', value=str(before.created_at.strftime("%H:%M:%S - %d/%m/%y")), inline=False)
        embed.set_footer(icon_url=betina_icon,
                         text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name, year()))
        await guild.send(embed=embed)


@client.event
async def on_message_edit(before, after):
    if before.guild is None:
        try:
            if str(after.guild.id) in digit_log:
                if after.author.avatar_url_as(static_format='png')[54:].startswith('a_'):
                    avi = after.author.avatar_url.rsplit("?", 1)[0]
                else:
                    avi = after.author.avatar_url_as(static_format='png')
                if after.content == after.content:
                    return
                guild = after.author.guild.get_channel(int(digit_log[str(after.guild.id)]))
                embed = discord.Embed(title="Mensagem alterada:", colour=discord.Colour(0x370c5e))
                embed.set_thumbnail(url=avi)
                embed.add_field(name='Usuário:', value=str(after.author) + ' (' + str(after.author.name) + ')',
                                inline=False)
                embed.add_field(name='Mensagem Anterior:', value=str(before.content), inline=False)
                embed.add_field(name='Mensagem Posterior:', value=str(after.content), inline=False)
                embed.add_field(name='Canal', value='#' + str(after.channel), inline=True)
                embed.add_field(name='Horário:', value=str(before.created_at.strftime("%H:%M:%S - %d/%m/%y")), inline=False)
                embed.set_footer(text="Betina Brazilian Bot", icon_url=betina_icon)
                await guild.send(embed=embed)
        except:
            return
    elif after.guild is None:
        try:
            if str(before.guild.id) in digit_log:
                if before.author.avatar_url_as(static_format='png')[54:].startswith('a_'):
                    avi = before.author.avatar_url.rsplit("?", 1)[0]
                else:
                    avi = before.author.avatar_url_as(static_format='png')
                if before.content == after.content:
                    return
                guild = before.author.guild.get_channel(int(digit_log[str(before.guild.id)]))
                embed = discord.Embed(title="Mensagem alterada:", colour=discord.Colour(0x370c5e))
                embed.set_thumbnail(url=avi)
                embed.add_field(name='Usuário:', value=str(before.author) + ' (' + str(before.author.name) + ')',
                                inline=False)
                embed.add_field(name='Mensagem Anterior:', value=str(before.content), inline=False)
                embed.add_field(name='Mensagem Posterior:', value=str(after.content), inline=False)
                embed.add_field(name='Canal', value='#' + str(before.channel), inline=True)
                embed.add_field(name='Horário:', value=str(before.created_at.strftime("%H:%M:%S - %d/%m/%y")), inline=False)
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name,
                                                                                           year()))
                await guild.send(embed=embed)
        except:
            return
    else:
        try:
            if str(after.guild.id) in digit_log and after.guild != None:
                if after.author.avatar_url_as(static_format='png')[54:].startswith('a_'):
                    avi = after.author.avatar_url.rsplit("?", 1)[0]
                else:
                    avi = after.author.avatar_url_as(static_format='png')
                if before.content == after.content:
                    return
                guild = after.author.guild.get_channel(int(digit_log[str(after.guild.id)]))
                embed = discord.Embed(title="Mensagem alterada:", colour=discord.Colour(0x370c5e))
                embed.set_thumbnail(url=avi)
                embed.add_field(name='Usuário:', value=str(after.author) + ' (' + str(before.author.name) + ')',
                                inline=False)
                embed.add_field(name='Mensagem Anterior:', value=str(before.content), inline=False)
                embed.add_field(name='Mensagem Posterior:', value=str(after.content), inline=False)
                embed.add_field(name='Canal', value='#' + str(after.channel), inline=True)
                embed.add_field(name='Horário:', value=str(after.created_at.strftime("%H:%M:%S - %d/%m/%y")), inline=False)
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name,
                                                                                           year()))
                await guild.send(embed=embed)
            else:
                if str(before.guild.id) in digit_log and before.guild != None:
                    if before.author.avatar_url_as(static_format='png')[54:].startswith('a_'):
                        avi = before.author.avatar_url.rsplit("?", 1)[0]
                    else:
                        avi = before.author.avatar_url_as(static_format='png')
                    if before.content == after.content:
                        return
                    guild = before.author.guild.get_channel(int(digit_log[str(before.guild.id)]))
                    embed = discord.Embed(title="Mensagem alterada:", colour=discord.Colour(0x370c5e))
                    embed.set_thumbnail(url=avi)
                    embed.add_field(name='Usuário:', value=str(before.author) + ' (' + str(before.author.name) + ')',
                                    inline=False)
                    embed.add_field(name='Mensagem Anterior:', value=str(before.content), inline=False)
                    embed.add_field(name='Mensagem Posterior:', value=str(after.content), inline=False)
                    embed.add_field(name='Canal', value='#' + str(before.channel), inline=True)
                    embed.add_field(name='Horário:', value=str(before.created_at.strftime("%H:%M:%S - %d/%m/%y")),
                                    inline=False)
                    embed.set_footer(icon_url=betina_icon,
                                     text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name,
                                                                                               year()))
                    await guild.send(embed=embed)
        except:
            return


@client.event
async def on_guild_channel_create(channel):
    guild_do_canal = channel.guild
    async for channels in guild_do_canal.audit_logs(action=discord.AuditLogAction.channel_create):
        usuario = guild_do_canal.get_member(channels.user.id)
        if str(guild_do_canal.id) in digit_log:
            guild = channel.guild.get_channel(int(digit_log[str(guild_do_canal.id)]))
            embed = discord.Embed(title="Canal criado:", colour=discord.Colour(0x370c5e))
            embed.set_thumbnail(url=usuario.avatar_url)
            embed.add_field(name='Usuário:', value=str(channels.user.name)
                                                   + ' (' +
                                                   str(channels.user.name) + '#' + str(channels.user.discriminator) + ')',
                            inline=False)
            embed.add_field(name='Canal', value='#' + str(channel.name), inline=True)
            embed.add_field(name='Horário:', value=str(channel.created_at.strftime("%H:%M:%S - %d/%m/%y")), inline=False)
            embed.set_footer(icon_url=betina_icon,
                             text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name, year()))
            await guild.send(embed=embed)
            break
        else:
            return


@client.event
async def on_guild_channel_delete(channel):
    guild_do_canal = channel.guild
    async for channels in guild_do_canal.audit_logs(action=discord.AuditLogAction.channel_delete):
        usuario = guild_do_canal.get_member(channels.user.id)
        if str(guild_do_canal.id) in digit_log:
            guild = channel.guild.get_channel(int(digit_log[str(guild_do_canal.id)]))
            embed = discord.Embed(title="Canal deletado:", colour=discord.Colour(0x370c5e))
            embed.set_thumbnail(url=usuario.avatar_url)
            embed.add_field(name='Usuário:', value=str(channels.user.name)
                                                   + ' (' +
                                                   str(channels.user.name) + '#' + str(channels.user.discriminator) + ')',
                            inline=False)
            embed.add_field(name='Canal', value='#' + str(channel.name), inline=True)
            embed.add_field(name='Horário:', value=str(channel.created_at.strftime("%H:%M:%S - %d/%m/%y")), inline=False)
            embed.set_footer(icon_url=betina_icon,
                             text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name, year()))
            await guild.send(embed=embed)
            break
        else:
            return


@client.event
async def on_guild_update(before, after):
    if str(before.id) in digit_log:
        async for channels in before.audit_logs(action=discord.AuditLogAction.guild_update):
            print(f'{channels}')
            if before.name == after.name:
                return
            guild = after.get_channel(int(digit_log[str(before.id)]))
            embed = discord.Embed(title="Nome do servidor alterado:", colour=discord.Colour(0x370c5e))
            embed.set_thumbnail(url=before.icon_url)
            embed.add_field(name='Usuário:', value=str(channels.user.name) +
                                                   ' (' + '#' + str(channels.user.name) + ')',
                            inline=False)
            if before.name == None:
                nick1 = 'Nenhum'
            else:
                nick1 = str(before.name)
            if after.name == None:
                nick = 'Nenhum'
            else:
                nick = str(after.name)
            embed.add_field(name='Nome Anterior:', value=f'{nick1}', inline=False)
            embed.add_field(name='Nome Posterior:', value=f'{nick}', inline=False)
            embed.add_field(name='Horário:', value=str(before.created_at.strftime("%H:%M:%S - %d/%m/%y")), inline=False)
            embed.set_footer(icon_url=betina_icon,
                             text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name, year()))
            await guild.send(embed=embed)
            break


@client.event
async def on_message_delete(message):
    if str(message.guild.id) in digit_log:
        if message.author.avatar_url_as(static_format='png')[54:].startswith('a_'):
            avi = message.author.avatar_url.rsplit("?", 1)[0]
        else:
            avi = message.author.avatar_url_as(static_format='png')
        if message.author.bot:
            return
        guild = message.author.guild.get_channel(int(digit_log[str(message.guild.id)]))
        embed = discord.Embed(title="Mensagem apagada:", colour=discord.Colour(0x370c5e))
        embed.set_thumbnail(url=avi)
        embed.add_field(name='Usuário:', value=str(message.author) + ' (' + str(message.author.name) + ')',
                        inline=False)
        embed.add_field(name='Horário:', value=str(message.created_at.strftime("%H:%M:%S - %d/%m/%y")), inline=True)
        embed.add_field(name='Mensagem:', value=str(message.content), inline=False)
        embed.add_field(name='Canal', value='#' + str(message.channel), inline=True)
        embed.set_footer(icon_url=betina_icon,
                         text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name, year()))
        await guild.send(embed=embed)


@client.event
async def on_member_join(member):
    if str(member.guild.id) not in join_list:
        return
    canal = member.guild.get_channel(int(join_list[str(member.guild.id)][0]))
    fmt = '{0.mention} ' + join_list[str(member.guild.id)][1]
    embed = discord.Embed(colour=discord.Colour(0x370c5e), description=f"{fmt}".format(member))
    embed.set_thumbnail(url=member.guild.icon_url)
    embed.set_footer(icon_url=betina_icon,
                     text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name,
                                                                               year()))
    await canal.send(embed=embed)
    await canal.send(f'Agora temos exatamente: {len(member.guild.members)} membros no servidor!')
    if str(member.guild.id) not in initial_role:
        return
    role = discord.utils.get(member.guild.roles, name=initial_role[str(member.guild.id)])
    await member.add_roles(role)


@client.event
async def on_member_remove(member):
    if str(member.guild.id) in leave_list:
        guild = member.guild.get_channel(int(leave_list[str(member.guild.id)][0]))
        fmt = f'{member.name} ' + leave_list[str(member.guild.id)][1]
        embed = discord.Embed(colour=discord.Colour(0x370c5e), description=f"{fmt}".format(member))
        embed.set_thumbnail(url=member.guild.icon_url)
        embed.set_footer(icon_url=betina_icon,
                         text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name,
                                                                                   year()))
        await guild.send(embed=embed)
        await guild.send(f'Agora temos exatamente: {len(member.guild.members)} membros no servidor!')
    else:
        return


@client.event
async def on_guild_join(guild):
    for membro in guild.members:
        if membro.guild_permissions.administrator and membro != client.user:
            embed = discord.Embed(title="Bem vindo ao meu Suporte", colour=discord.Colour(0x370c5e),
                                  description="Olá, eu sou a Betina: \n esse suporte está aqui para te ajudar e "
                                              "ajudar ao meu criador ```\nSim, eu sou um bot e não vou roubar seus "
                                              "dados...```")
            embed.set_image(
                url=betina_icon)
            embed.set_thumbnail(
                url=betina_icon)
            embed.set_author(name="Betina")
            embed.set_footer(icon_url=betina_icon,
                             text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name,
                                                                                       year()))

            embed.add_field(name="Precisa de ajuda?🤔", value="para usar meus comandos utilize o $help")
            embed.add_field(name="Teve alguma ideia boa ? 😱: ",
                            value="fale com o meu criador, ele poderá implementar!")
            embed.add_field(name="Teve algum problema com o bot ?🙄",
                            value="não se preocupe, alguns problemas são comuns"
                                  " considerando o fato do bot estar em construção,"
                                  " mas, de qualquer forma,  fale com o meu criador.")
            embed.add_field(name="Criador do bot:", value="DantasB#7096", inline=True)
            embed.add_field(name="Maiores informações:", value="github.com/DantasB", inline=True)
            try:
                await membro.send(embed=embed)
            except:
                return


@client.event
async def on_message(message):
    print('Logs:\n', message.author, message.content)
    if message.author == client.user:
        return
    if message.author.bot:
        return
    guild_id = str(message.guild.id)
    if guild_id in level_on:
        author_id = str(message.author.id)
        if not guild_id in level_system:
            level_system[guild_id] = {}
        if not author_id in level_system[guild_id]:
            level_system[guild_id][author_id] = {}
            level_system[guild_id][author_id]['level'] = 1
            level_system[guild_id][author_id]['experiencia'] = 1

        level_system[guild_id][author_id]['experiencia'] += 2

        if lvl_up(author_id, guild_id):
            embed = discord.Embed(title="LEVEL UP!", colour=discord.Colour(0x68c46b),
                                  description=f"Parabéns, {message.author.mention}, você agora está no {level_system[guild_id][author_id]['level']}")
            embed.set_image(url="http://piedmontmediation.com/var/m_8/8c/8c0/39741/745358-level-up.png")
            embed.set_footer(icon_url=betina_icon,
                             text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name,
                                                                                       year()))
            channel = message.guild.get_channel(int(level_on[guild_id]))
            await channel.send(embed=embed)

    if message.content.startswith('<@527565353199337474>'):
        if not message.guild:
            return
        guild_id = str(message.guild.id)
        author_id = str(message.author.id)
        if guild_id in limitador_log:
            if str(message.channel.id) == limitador_log[guild_id]:
                embed = discord.Embed(colour=discord.Colour(0x370c5e), description="**Digite: `$help"
                                                                                   " ou $ajuda` para ver"
                                                                                   " meus comandos**")
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name,
                                                                                           year()))
                await message.channel.send(embed=embed)
            else:
                return
        else:
            embed = discord.Embed(colour=discord.Colour(0x370c5e),
                                  description="**Digite: `$help ou $ajuda` para ver meus comandos**")
            embed.set_footer(icon_url=betina_icon,
                             text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name,
                                                                                       year()))
            await message.channel.send(embed=embed)

    if message.content.lower().startswith('$treta'):
        if not message.guild:
            return
        guild_id = str(message.guild.id)
        author_id = str(message.author.id)
        if guild_id in limitador_log:
            if str(message.channel.id) == limitador_log[guild_id]:
                i = random.randrange(len(lista))
                listas = lista[i]
                x = random.randrange(len(message.guild.members))
                user = list(message.guild.members)[x]
                fquote = listas.replace('[nome]', user.name)
                await message.channel.send(fquote)
            else:
                return
        else:
            i = random.randrange(len(lista))
            listas = lista[i]
            x = random.randrange(len(message.guild.members))
            user = list(message.guild.members)[x]
            fquote = listas.replace('[nome]', user.name)
            await message.channel.send(fquote)

    try:
        if not message.guild:
            return
        if message.content.lower().startswith('betina'):
            if message.content[7] == 'q' \
                    and message.content[8] == 'u' \
                    and message.content[9] == 'e' \
                    and message.content[10] == 'm' \
                    and message.content[12] == 'é' \
                    and message.content[14] == 's' \
                    and message.content[15] == 'e' \
                    and message.content[16] == 'u':

                guild_id = str(message.guild.id)
                author_id = str(message.author.id)
                if guild_id in limitador_log:
                    if str(message.channel.id) == limitador_log[guild_id]:
                        resposta = 'Bruno Dantas'
                        await message.channel.send(resposta)
                        return
                    else:
                        return
                else:
                    resposta = 'Bruno Dantas'
                    await message.channel.send(resposta)
                    return
            elif message.content[-1] == '?':
                guild_id = str(message.guild.id)
                author_id = str(message.author.id)
                if guild_id in limitador_log:
                    if str(message.channel.id) == limitador_log[guild_id]:
                        resposta = random.choice(['Não respondo a isso', 'Sim',
                                                  'As vezes', 'Não', 'Claro', 'NUNCA!',
                                                  'Um dia talvez', 'A resposta está dentro de você'
                                                     , 'Mais ou menos', 'Uma Bosta', 'Podia ser pior', 'Não sei',
                                                  'Não tenho certeza', 'Sua mãe deve saber',
                                                  'Pergunta pra sua webnamorada',
                                                  'Eu não tenho cara de Yoda pra achar algo',
                                                  'Se eu fosse você desistiria de perguntar isso', 'Talvez'])
                        await message.channel.send(resposta)
                        return
                    else:
                        return
                else:
                    resposta = random.choice(['Não respondo a isso', 'Sim',
                                              'As vezes', 'Não', 'Claro', 'NUNCA!',
                                              'Um dia talvez', 'A resposta está dentro de você'
                                                 , 'Mais ou menos', 'Uma Bosta', 'Podia ser pior', 'Não sei',
                                              'Não tenho certeza', 'Sua mãe deve saber',
                                              'Pergunta pra sua webnamorada', 'Eu não tenho cara de Yoda',
                                              'Se eu fosse você desistiria de perguntar isso', 'Talvez'])
                    await message.channel.send(resposta)
                    return
    except:
        pass
    if len(message.mentions) > 0:

        if not message.guild:
            return
        guild_id = str(message.guild.id)
        author_id = str(message.author.id)
        afk_users = []

        if guild_id in afklist:
            if author_id in afklist[guild_id]:
                del afklist[guild_id][author_id]
                embed = discord.Embed(colour=discord.Colour(0x370c5e),
                                      description=f" Bem vindo de volta {message.author.name}")
                await message.channel.send(embed=embed, delete_after=10)
            else:
                mentions = message.mentions
                for member in mentions:
                    if guild_id in afklist:
                        if str(member.id) in afklist[guild_id]:
                            embed = discord.Embed(colour=discord.Colour(0x370c5e),
                                                  description=f"{member.name} está"
                                                  f" **AFK**: *{afklist[str(guild_id)][str(member.id)]}*")
                            await message.channel.send(embed=embed, delete_after=10)

    else:
        if not message.guild:
            return
        guild_id = str(message.guild.id)
        author_id = str(message.author.id)
        afk_users = []
        if guild_id in afklist:
            if author_id in afklist[guild_id]:
                del afklist[guild_id][author_id]
                embed = discord.Embed(colour=discord.Colour(0x370c5e),
                                      description=f" Bem vindo de volta {message.author.name}")
                await message.channel.send(embed=embed, delete_after=10)
    with open('afks.json', 'w') as file:
        json.dump(afklist, file)

    with open('users.json', 'w') as file:
        json.dump(level_system, file, indent=4)
    global c
    c += 1
    if c == 200:
        try:
            x = random.choice(message.guild.emojis)
            await message.add_reaction(x)
            c = 0
        except:
            c = 0

    await client.process_commands(message)


@client.event
async def on_raw_reaction_add(payload):
    if not payload.guild_id:
        return
    if str(payload.message_id) not in reactions_list:
        return

    guild = client.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)

    if client.user.id == member.id:
        return

    if str(payload.emoji) == reactions_list[str(payload.message_id)][1]:
        role = discord.utils.get(guild.roles, name=reactions_list[str(payload.message_id)][0])

    else:
        return
    try:
        await member.add_roles(role)
    except:
        return
    if str(payload.guild_id) not in reactions_logs_in:
        return
    servidor = member.guild.get_channel(int(reactions_logs_in[str(payload.guild_id)][0]))
    fmt = '{0.mention} ' + str(reactions_logs_in[str(payload.guild_id)][1])
    await servidor.send(fmt.format(member))


@client.event
async def on_raw_reaction_remove(payload):
    if not payload.guild_id:
        return
    if str(payload.message_id) not in reactions_list:
        return
    guild = client.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    if client.user.id == member.id:
        return
    if str(payload.emoji) == reactions_list[str(payload.message_id)][1]:
        role = discord.utils.get(guild.roles, name=reactions_list[str(payload.message_id)][0])
    else:
        return
    try:
        await member.remove_roles(role)
    except:
        return
    if str(payload.guild_id) not in reactions_logs_out:
        return
    servidor = member.guild.get_channel(int(reactions_logs_out[str(payload.guild_id)][0]))
    fmt = '{0.mention} ' + str(reactions_logs_out[str(payload.guild_id)][1])
    await servidor.send(fmt.format(member))


@commands.guild_only()
@client.command()
async def help(ctx):
    """Manda mensagem privada pro usuario!"""
    author = ctx.author
    embed = discord.Embed(title="Escolha uma categoria", colour=discord.Colour(0x370c5e),
                          description="```Bem vindo ao"
                                      " meu suporte, escolha abaixo uma das categorias"
                                      " para obter mais informações sobre minhas utilidades ```")
    embed.set_footer(icon_url=betina_icon,
                     text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name, year()))

    embed.add_field(name="😂 **Diversão**", value="``$moeda, $ppt, $rola ...``", inline=False)
    embed.add_field(name="🛠 **Utilidades**", value="``$devemais, $devemenos, $deve...``", inline=False)
    embed.add_field(name="🎵 **Música**", value="``$play, $resume, $stop, $fila...``", inline=False)
    embed.add_field(name="🗣 **Interação**", value="``$bate, $abraça, $treta...``", inline=False)
    embed.add_field(name="👮 **Administração**", value="``$apaga, $ping, $pong...``", inline=False)
    embed.add_field(name="⚙ **Configuração**", value="``$joinlogs, $leavelogs, $autorole...``", inline=False)
    embed.add_field(name="🤑 **Doação**", value="``donateinfo``", inline=False)
    try:
        message = await author.send(embed=embed)
    except:
        return await ctx.send('Você está com sua DM bloqueada. Por favor desbloqueie!')

    reaction_list = ["😂", "🛠", "🎵", "🗣", "👮", "⚙", "🤑"]

    for reaction in reaction_list:
        await message.add_reaction(reaction)

    def check(reaction, user):
        return user == author and str(reaction.emoji) in reaction_list

    try:
        while True:
            reaction, user = await client.wait_for('reaction_add', check=check)
            if str(reaction.emoji) == "🛠":
                embed = discord.Embed(title="Utilidades", colour=discord.Colour(0x370c5e),
                                      description="*Bem vindo a categoria Utilidades:\nAqui você encontrará"
                                                  " comandos que ajudará você a ter noção"
                                                  " de finanças, tempo e outras coisas.*")
                embed.set_thumbnail(
                    url=betina_icon)
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name,
                                                                                           year()))
                embed.add_field(name="**$devemais <usuário> <quantidade>**", value="``Você aumentará o quanto um"
                                                                                   " usuário te deve!``", inline=False)
                embed.add_field(name="**$devemenos <usuário> <quantidade>**", value="``Você "
                                                                                    "diminuirá o quanto um usuário te deve!``",
                                inline=False)
                embed.add_field(name="**$deve <usuário>**",
                                value="``Mostrarei uma lista de todas as pessoas que um usuário"
                                      " deve!``", inline=False)
                embed.add_field(name="**$conversor <moeda1> <moeda2>"
                                     "**", value="``Direi a cotação da moeda 1 em relação a moeda 2``",
                                inline=False)
                embed.add_field(name="**$clima <local>"
                                     "**", value="``Direi o clima do local.``",
                                inline=False)
                embed.add_field(name="**$wordcloud <texto>"
                                     "**", value="``Gerarei um wordcloud com as palavras do texto.``",
                                inline=False)
                embed.add_field(name="**$picture <usuário> (opcional)"
                                     "**", value="``Darei a foto do usuário em questão.``",
                                inline=False)
                embed.add_field(name="**$pb <usuário> (opcional)"
                                     "**", value="``Darei a foto do usuário marcado em preto e branco.``",
                                inline=False)
                embed.add_field(name="**$pontilhado <usuário> (opcional)"
                                     "**", value="``Darei a foto do usuário marcado na forma pontilhada.``",
                                inline=False)
                embed.add_field(name="**$primario <usuário> (opcional)"
                                     "**", value="``Darei a foto do usuário marcado nas cores primárias.``",
                                inline=False)
                embed.add_field(name="**$gerasenha <número> (opcional)"
                                     "**", value="``Gerarei uma senha aleatória com o tamanho do número.``",
                                inline=False)
                embed.add_field(name="**$geraconvite **", value="``Gerarei um convite para o seu servidor!``",
                                inline=False)
                embed.add_field(name="**$buscacep <cep> **", value="``Darei as informações sobre o cep requisitado!``",
                                inline=False)
                embed.add_field(name="**$geracor **", value="``Gera uma cor aleatória para o discord!``",
                                inline=False)
                embed.add_field(name="**$anuncio <link> (opcional) <canal> (opcional) <texto>"
                                     "**", value="``Gera um anúncio com o texto e"
                                                 " o link em questão (pode ser imagem)``",
                                inline=False)
                msg = await message.edit(embed=embed)

            elif str(reaction.emoji) == "😂":
                embed = discord.Embed(title="Diversão", colour=discord.Colour(0x370c5e),
                                      description="*Bem vindo a categoria diversão:\n"
                                                  "Aqui você encontrará comandos que trará alegria a todos no servidor.*")
                embed.set_thumbnail(
                    url=betina_icon)
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name,
                                                                                           year()))

                embed.add_field(name="**$moeda**", value="``Jogarei uma moeda. Poderá cair cara ou coroa!``",
                                inline=False)
                embed.add_field(name="**$rola <número>**", value="``Rolarei um dado de até 20 lados!``", inline=False)
                embed.add_field(name="**$ppt <Pedra, Papel ou Tesoura>**", value="``Começarei um jogo de pedra, papel"
                                                                                 " ou tesoura contra você!``",
                                inline=False)
                embed.add_field(name="**$bolsonaro** <texto> (opcional)", value="``O Bolsonaro aparece!``",
                                inline=False)
                embed.add_field(name="**$taokei**", value="``O Bolsonaro aparece!``",
                                inline=False)
                embed.add_field(name="**$faustao**", value="``O Faustão aparece!``", inline=False)
                embed.add_field(name="**$miranha**", value="``O Miranha aparece!``", inline=False)
                embed.add_field(name="**$ata <texto> (opcional)**", value="``Ata!``", inline=False)
                embed.add_field(name="**$facebook <texto> (opcional)**", value="``Cria um post "
                                                                               "do facebook com o "
                                                                               "seu texto!``", inline=False)
                embed.add_field(name="**$twitter <texto> (opcional)**", value="``Cria um post "
                                                                               "do twitter com o "
                                                                               "seu texto!``", inline=False)
                embed.add_field(name="**$hungergames <número>**", value="``Iniciarei um jogo de Hunger Games!``",
                                inline=False)
                embed.add_field(name="**$reverse <texto>**", value="``Reverte o texto!``",
                                inline=False)
                embed.add_field(name="**$flip <texto>**", value="``Deixa o texto de cabeça para baixo!``",
                                inline=False)
                msg = await message.edit(embed=embed)

            elif str(reaction.emoji) == "🎵":
                embed = discord.Embed(title="Música", colour=discord.Colour(0x370c5e),
                                      description="*Bem vindo a categoria Música:\nAqui você encontrará"
                                                  " comandos que ajudará você a ouvir música enquanto faz suas atividades"
                                                  " no discord.*")
                embed.set_thumbnail(
                    url=betina_icon)
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name,
                                                                                           year()))

                embed.add_field(name="**$play <música>**",
                                value="``Busco pela música ou toco a música de link específico!``",
                                inline=False)
                embed.add_field(name="**$pause**", value="``Pauso a música que está tocando atualmente!``",
                                inline=False)
                embed.add_field(name="**$stop**", value="``Paro de tocar a música e saio do canal de voz!``",
                                inline=False)
                embed.add_field(name="**$skip **", value="``Pularei a música que está tocando atualmente!``",
                                inline=False)
                embed.add_field(name="**$volume <quantidade>**",
                                value="``Mudarei o volume que está tocando a música!``",
                                inline=False)
                embed.add_field(name="**$fila **", value="``Mostrarei todas as músicas que estão na fila!``",
                                inline=False)
                embed.add_field(name="**$tocando**", value="``Direi a música que está tocando a música atualmente``",
                                inline=False)
                embed.add_field(name="**$sai**", value="``Sairei do canal de voz!``", inline=False)
                msg = await message.edit(embed=embed)

            elif str(reaction.emoji) == "🗣":
                embed = discord.Embed(title="Interação", colour=discord.Colour(0x370c5e),
                                      description="*Bem vindo a categoria Interação:\nAqui você encontrará"
                                                  " comandos que ajudará você a interagir com outros membros do seu servidor*")
                embed.set_thumbnail(
                    url=betina_icon)
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name,
                                                                                           year()))

                embed.add_field(name="**$treta **", value="``Direi coisas assustadoras sobre as pessoas do servidor!``",
                                inline=False)
                embed.add_field(name="**$fala <#canal> (opcional) <mensagem> **",
                                value="``Olha, eu sei falar sua mensagem!``",
                                inline=False)
                embed.add_field(name="**$abraça <usuário>**", value="``Abraça o usuário!``",
                                inline=False)
                embed.add_field(name="**$beija <usuário>**", value="``Beija o usuário!``", inline=False)
                embed.add_field(name="**$bate <usuário> **", value="``Bate no usuário!``", inline=False)
                embed.add_field(name="**$dança <usuário> **", value="``Dança com o usuário!``", inline=False)
                embed.add_field(name="**$ataca <usuário> **", value="``Dá um ataque no usuário!``", inline=False)
                embed.add_field(name="**$emputece <usuário> **", value="``Deixa o usuário puto!``", inline=False)
                embed.add_field(name="**$voltapracaverna <usuário> **", value="``Manda o usuário voltar "
                                                                              "pro seu lugar de origem!``",
                                inline=False)
                embed.add_field(name="**$ship <usuário1> <usuário2> (opcional)**", value="``Forma um novo casal!``",
                                inline=False)
                embed.add_field(name="**$tnc **", value="``Manda alguem do servidor tomar no você sabe onde!``",
                                inline=False)
                embed.add_field(name="**$highfive <usuário>**", value="``Bate na mão do usuário!``",
                                inline=False)
                embed.add_field(name="**$roletarussa**", value="``Brincarei de roleta russa com você "
                                                               "e mais 4 pessoas!``", inline=False)
                embed.add_field(name="**$mencionar <Id da mensagem> <texto> (opcional)**",
                                value="``Transformarei a frase"
                                      " do usuário em uma citação"
                                      "!``", inline=False)
                embed.add_field(name="**$level <user>**", value="``Direi o level daquele usuário``", inline=False)

                msg = await message.edit(embed=embed)

            elif str(reaction.emoji) == "👮":
                embed = discord.Embed(title="Administração", colour=discord.Colour(0x370c5e),
                                      description="*Bem vindo a categoria Administração:\nAqui você encontrará"
                                                  " comandos que ajudará você a controlar seu servidor.\n"
                                                  "OBS: Você precisará de algumas permissões para utilizar esses comandos!*")
                embed.set_thumbnail(
                    url=betina_icon)
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name,
                                                                                           year()))
                embed.add_field(name="**$apaga <quantidade>**", value="``Eu apagarei uma"
                                                                      " quantidade de mensagens!``", inline=False)
                embed.add_field(name="**$ping**", value="``Retornarei o ping do usuário``", inline=False)
                embed.add_field(name="**$pong**", value="``oiráusu od gnip o ieranroter``", inline=False)
                embed.add_field(name="**$userinfo <usuário>**", value="``Retornarei informações sobre o usuário!``",
                                inline=False)
                embed.add_field(name="**$serverinfo**", value="``Retornarei informações sobre o servidor!``",
                                inline=False)
                embed.add_field(name="**$afk <motivo> (opcional)**", value="``Definirei o usuário como afk!``",
                                inline=False)
                embed.add_field(name="**$warn <usuário> <motivo> (opcional)**", value="``Darei um Warn no usuário!``",
                                inline=False)
                embed.add_field(name="**$mute <usuário>**", value="``Deixarei o usuário no estado de mute!``",
                                inline=False)
                embed.add_field(name="**$unmute <usuário>**", value="``Tirarei o usuário do estado de mute!``",
                                inline=False)
                embed.add_field(name="**$ban <motivo> (opcional)**", value="``Banirei o usuário do servidor!``",
                                inline=False)
                embed.add_field(name="**$clearlastwarn <usuário>**", value="``Tirarei o ultimo warn do usuário!``",
                                inline=False)
                embed.add_field(name="**$kick <usuário> <motivo> (opcional)**", value="``Tirarei o ultimo warn do usuário!``",
                                inline=False)

                msg = await message.edit(embed=embed)

            elif str(reaction.emoji) == "⚙":
                embed = discord.Embed(title="Configuração", colour=discord.Colour(0x370c5e),
                                      description="*Bem vindo a categoria Configuração:\nAqui você encontrará"
                                                  " comandos que ajudará você a configurar algumas de minhas funções.\n"
                                                  "OBS: Você precisa da permissão de administrador!*")
                embed.set_thumbnail(
                    url=betina_icon)
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name,
                                                                                           year()))
                embed.add_field(name="**$config**", value="``Mostra todas as configurações do bot!``", inline=False)
                embed.add_field(name="**$betinainfo**", value="``Mostra todas as informações do bot!``", inline=False)
                embed.add_field(name="**$joinlogs <#canal> <mensagem>**",
                                value="``Definirei um canal para enviar uma mensagem"
                                      " toda vez que um usuário"
                                      " entrar no servidor``", inline=False)
                embed.add_field(name="**$leavelogs <#canal> <mensagem> **",
                                value="``Definirei um canal para enviar uma mensagem"
                                      " toda vez que um usuário"
                                      " sair do servidor``", inline=False)
                embed.add_field(name="**$reactionlogsin <#canal> <mensagem> (opcional)**", value="``Definirei um"
                                                                                                 " canal para enviar"
                                                                                                 " uma mensagem"
                                                                                                 " toda vez que um usuário"
                                                                                                 " reagir no sistema de auto"
                                                                                                 "role``", inline=False)
                embed.add_field(name="**$reactionlogsout <#canal> <mensagem> (opcional)**",
                                value="``Definirei um canal para"
                                      " enviar uma mensagem"
                                      " toda vez que um usuário"
                                      " deixar de reagir no sistema de"
                                      " autorole``", inline=False)
                embed.add_field(name="**$autorole <@Cargo> <Reação> <Mensagem> (opcional)**",
                                value="``Criarei uma mensagem que"
                                      " ao reagir com a Reação"
                                      " definida adiciona o Cargo"
                                      " definido!``", inline=False)
                embed.add_field(name="**$addtreta <treta>**", value="``Adicionarei uma treta a listra de tretas!``",
                                inline=False)
                embed.add_field(name="**$sugestão <mensagem>**", value="``Adicionarei uma sugestão que você "
                                                                       "requisitar``", inline=False)
                embed.add_field(name="**$cargoinicial <@cargo>**", value="``Adicionarei um cargo inicial a todos"
                                                                         " aqueles que entrarem no servidor!``",
                                inline=False)
                embed.add_field(name="**$prefixo <caracter>**", value="``Definirei um novo prefixo ao bot!``",
                                inline=False)
                embed.add_field(name="**$digitlogs <#Canal>**", value="``Definirei um canal para receber os logs de "
                                                                      "todos os comandos da administração"
                                                                      " utilizados!``", inline=False)
                embed.add_field(name="**$invites <usuário>**", value="``Direi todos os invites criados por"
                                                                     " um usuário!``", inline=False)
                embed.add_field(name="**$botchannel <#Canal>**", value="``Define um canal para poder"
                                                                       " utilizar os meus comandos``", inline=False)
                embed.add_field(name="**$tirabotchannel **", value="``Tira o canal definido para"
                                                                   " poder utilizar os comandos.``", inline=False)
                embed.add_field(name="**$levelson <#Canal>**", value="``Ativa o s"
                                                                     "istema de level nesse servidor``", inline=False)
                msg = await message.edit(embed=embed)

            elif str(reaction.emoji) == "🤑":
                embed = discord.Embed(title="Doação", colour=discord.Colour(0x370c5e),
                                      description="*Bem vindo a categoria Doação:\nAqui você encontrará"
                                                  " comandos que poderão ser importantes"
                                                  " caso você queira ajudar este bot a crescer!*")
                embed.set_thumbnail(
                    url=betina_icon)
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name,
                                                                                           year()))
                embed.add_field(name="**donateinfo**", value="``Informações de contas para"
                                                             " recebimento de doações!``", inline=False)
                msg = await message.edit(embed=embed)
    except:
        return


@commands.cooldown(2, 10, commands.BucketType.user)
@commands.guild_only()
@client.command(name='afk', aliases=['away', 'ausente'])
async def afk(ctx, *, arg: str = None):
    if arg == None:
        reason = 'Sem motivos específicados!'
    else:
        reason = arg
    guild_id = str(ctx.guild.id)
    user_id = str(ctx.author.id)
    if guild_id in limitador_log:
        if str(ctx.message.channel.id) == limitador_log[guild_id]:

            if guild_id in afklist:
                afklist[guild_id][user_id] = reason
                embed = discord.Embed(colour=discord.Colour(0x370c5e),
                                      description=f"{ctx.author.mention} Está como afk agora! | {reason}")
                await ctx.send(embed=embed)
            else:
                afklist[guild_id] = {}
                afklist[guild_id][user_id] = reason
                embed = discord.Embed(colour=discord.Colour(0x370c5e),
                                      description=f"{ctx.author.mention} Está como afk agora! | {reason}")
                await ctx.send(embed=embed)
        else:
            guild = ctx.guild.get_channel(int(limitador_log[guild_id]))
            await ctx.send(f'Esse não foi o canal definido para usar os comandos. Tente utilizar o canal {guild}')
            return
    else:

        if guild_id in afklist:
            afklist[guild_id][user_id] = reason
            embed = discord.Embed(colour=discord.Colour(0x370c5e),
                                  description=f"{ctx.author.mention} Está como afk agora! | {reason}")
            await ctx.send(embed=embed)
        else:
            afklist[guild_id] = {}
            afklist[guild_id][user_id] = reason
            embed = discord.Embed(colour=discord.Colour(0x370c5e),
                                  description=f"{ctx.author.mention} Está como afk agora! | {reason}")
            await ctx.send(embed=embed)

    with open("afks.json", "w") as file:
        json.dump(afklist, file)




@commands.cooldown(2, 10, commands.BucketType.guild)
@commands.guild_only()
@client.command(pass_context=True, name='addtreta', aliases=['maistreta', 'adiciona'])
@has_permissions(administrator=True)
async def addtreta(ctx, *, arg: str):
    lista.append(arg)

    embed = discord.Embed(title="Treta adicionada: ", colour=discord.Colour(0x370c5e), description=f"{arg}")
    embed.set_footer(icon_url=betina_icon,
                     text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name, year()))
    msg = await ctx.send(embed=embed, delete_after=10)


@addtreta.error
async def addtreta_handler(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(title="Comando $addtreta:", colour=discord.Colour(0x370c5e),
                              description="Adiciona uma treta a lista de tretas"
                                          "\n \n**Como usar: $addtreta <treta> Obs: dentro da treta em vez "
                                          "do nome do usuário, deve-se colocar [nome]!**")

        embed.set_author(name="Betina#9182",
                         icon_url=betina_icon)
        embed.set_footer(icon_url=betina_icon,
                         text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name, year()))
        embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                        "ter a permissão de* ``"
                                                        "Administrador`` *para utilizar este comando!*",
                        inline=False)
        embed.add_field(name="📖**Exemplos:**", value="$addtreta [nome] é vacilão\n$addtreta [nome] só faz besteira"
                                                      "", inline=False)
        embed.add_field(name="🔀**Outros Comandos**", value="``$maistreta, $adiciona.``", inline=False)

        msg = await ctx.send(embed=embed)
        await msg.add_reaction("❓")

    elif isinstance(error, commands.MissingRequiredArgument):
        if error.param.name == 'arg':
            embed = discord.Embed(title="Comando $addtreta:", colour=discord.Colour(0x370c5e),
                                  description="Adiciona uma treta a lista de tretas"
                                              "\n \n**Como usar: $addtreta <treta> Obs: dentro da treta em vez "
                                              "do nome do usuário, deve-se colocar [nome]!**")

            embed.set_author(name="Betina#9182",
                             icon_url=betina_icon)
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url=betina_icon)
            embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                            "ter a permissão de* ``"
                                                            "Administrador`` *para utilizar este comando!*",
                            inline=False)
            embed.add_field(name="📖**Exemplos:**", value="$addtreta [nome] é vacilão\n$addtreta [nome] só faz besteira"
                                                          "", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$maistreta, $adiciona.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")




@commands.cooldown(2, 10, commands.BucketType.guild)
@commands.guild_only()
@client.command(name='cargo', aliases=['cargoauto', 'autorole'])
@has_permissions(administrator=True)
async def cargo(ctx, cargo: discord.Role, reaction: str, *, arg: str = 'Clique na reação abaixo para selecionar:'):
    embed = discord.Embed(title="Cargo " + str(cargo), colour=discord.Colour(0x370c5e), description=f"{arg}")
    embed.set_footer(icon_url=betina_icon,
                     text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name, year()))
    msg = await ctx.send(embed=embed)
    await msg.add_reaction(reaction)
    reactions_list[str(msg.id)] = (str(cargo), reaction)

    with open('reactions.json', 'w') as file:
        json.dump(reactions_list, file)


@cargo.error
async def cargo_handler(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(title="Comando $cargo:", colour=discord.Colour(0x370c5e),
                              description="Adiciona uma mensagem que ao ser reagida, adiciona um cargo a pessoa"
                                          "\n \n**Como usar: $cargo <@Cargo> <Reação> <Mensagem> (opcional)**")

        embed.set_author(name="Betina#9182",
                         icon_url=betina_icon)
        embed.set_footer(icon_url=betina_icon,
                         text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name, year()))
        embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                        "ter a permissão de* ``"
                                                        "Administrador`` *para utilizar este comando!*",
                        inline=False)
        embed.add_field(name="📖**Exemplos:**", value="$cargo @Gamer ❓ Clique para ganhar o cargo Gamer"
                                                      "\n$cargo @iniciado ✅ "
                                                      "", inline=False)
        embed.add_field(name="🔀**Outros Comandos**", value="``$cargoauto, $autorole.``", inline=False)

        msg = await ctx.send(embed=embed)
        await msg.add_reaction("❓")

    elif isinstance(error, commands.MissingRequiredArgument):

        if error.param.name == 'reaction':
            embed = discord.Embed(title="Comando $cargo:", colour=discord.Colour(0x370c5e),
                                  description="Adiciona uma mensagem que ao ser reagida, adiciona um cargo a pessoa"
                                              "\n \n**Como usar: $cargo <@Cargo> <Reação> <Mensagem> (opcional)**")

            embed.set_author(name="Betina#9182",
                             icon_url=betina_icon)
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url=betina_icon)
            embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                            "ter a permissão de* ``"
                                                            "Administrador`` *para utilizar este comando!*",
                            inline=False)
            embed.add_field(name="📖**Exemplos:**", value="$cargo @Gamer ❓ Clique para ganhar o cargo Gamer"
                                                          "\n$cargo @iniciado ✅ Clique para entrar no servidor"
                                                          "", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$cargoauto, $autorole.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")


        elif error.param.name == 'cargo':
            embed = discord.Embed(title="Comando $cargo:", colour=discord.Colour(0x370c5e),
                                  description="Adiciona uma mensagem que ao ser reagida, adiciona um cargo a pessoa"
                                              "\n \n**Como usar: $cargo <@Cargo> <Reação> <Mensagem> (opcional)**")

            embed.set_author(name="Betina#9182",
                             icon_url=betina_icon)
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url=betina_icon)
            embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                            "ter a permissão de* ``"
                                                            "Administrador`` *para utilizar este comando!*",
                            inline=False)
            embed.add_field(name="📖**Exemplos:**", value="$cargo @Gamer ❓ Clique para ganhar o cargo Gamer"
                                                          "\n$cargo @iniciado ✅ Clique para entrar no servidor"
                                                          "", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$cargoauto, $autorole.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")


@commands.cooldown(2, 10, commands.BucketType.guild)
@commands.guild_only()
@client.command(name='joinlogs', aliases=['defjoinlogs', 'djlogs'])
@has_permissions(administrator=True)
async def join_logs(ctx, channel: discord.TextChannel, *, arg: str):
    guild_id = str(ctx.guild.id)
    channel_id = str(channel.id)

    embed = discord.Embed(title="Canal de logs de entrada definido: " + str(channel), colour=discord.Colour(0x370c5e),
                          description=f"{arg}")
    embed.set_footer(icon_url=betina_icon,
                     text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name, year()))
    await ctx.send(embed=embed, delete_after=10)
    join_list[guild_id] = (channel_id, arg)
    with open('join.json', 'w') as file:
        json.dump(join_list, file)


@join_logs.error
async def joinlogs_handler(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(
            title="Comando $joinlogs:define um canal que irá receber as mensagens quando alguem entrar"
                  " no servidor"
                  "\n \n**Como usar: $joinlogs <#Canal> <Mensagem>**", colour=discord.Colour(0x370c5e))

        embed.set_author(name="Betina#9182",
                         icon_url=betina_icon)
        embed.set_footer(icon_url=betina_icon,
                         text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name, year()))
        embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                        "ter a permissão de* ``"
                                                        "Administrador`` *para utilizar este comando!*",
                        inline=False)
        embed.add_field(name="📖**Exemplos:**", value="$joinlogs #jogadores Bem vindo ao servidor, usuário"
                                                      "\n$joinlogs #iniciado Bem vindo a nossa casa"
                                                      "", inline=False)
        embed.add_field(name="🔀**Outros Comandos**", value="``$defjoinlogs, $djlogs.``", inline=False)

        msg = await ctx.send(embed=embed)
        await msg.add_reaction("❓")

    elif isinstance(error, commands.MissingRequiredArgument):
        if error.param.name == 'arg':
            embed = discord.Embed(
                title="Comando $joinlogs:define um canal que irá receber as mensagens quando alguem entrar"
                      " no servidor"
                      "\n \n**Como usar: $joinlogs <#Canal> <Mensagem>**", colour=discord.Colour(0x370c5e))

            embed.set_author(name="Betina#9182",
                             icon_url=betina_icon)
            embed.set_footer(icon_url=betina_icon,
                             text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name,
                                                                                       year()))
            embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                            "ter a permissão de* ``"
                                                            "Administrador`` *para utilizar este comando!*",
                            inline=False)
            embed.add_field(name="📖**Exemplos:**", value="$joinlogs #jogadores Bem vindo ao servidor, usuário"
                                                          "\n$joinlogs #iniciado Bem vindo a nossa casa"
                                                          "", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$defjoinlogs, $djlogs.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")

        if error.param.name == 'channel':
            embed = discord.Embed(
                title="Comando $joinlogs:define um canal que irá receber as mensagens quando alguem entrar"
                      " no servidor"
                      "\n \n**Como usar: $joinlogs <#Canal> <Mensagem>**", colour=discord.Colour(0x370c5e))

            embed.set_author(name="Betina#9182",
                             icon_url=betina_icon)
            embed.set_footer(icon_url=betina_icon,
                             text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name,
                                                                                       year()))
            embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                            "ter a permissão de* ``"
                                                            "Administrador`` *para utilizar este comando!*",
                            inline=False)
            embed.add_field(name="📖**Exemplos:**", value="$joinlogs #jogadores Bem vindo ao servidor, usuário"
                                                          "\n$joinlogs #iniciado Bem vindo a nossa casa"
                                                          "", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$defjoinlogs, $djlogs.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")


@commands.cooldown(2, 10, commands.BucketType.guild)
@commands.guild_only()
@client.command(name='leavelogs', aliases=['defleavelogs', 'dllogs'])
@has_permissions(administrator=True)
async def leave_logs(ctx, channel: discord.TextChannel, *, arg: str):
    guild_id = str(ctx.guild.id)
    channel_id = str(channel.id)

    embed = discord.Embed(title="Canal de logs de saída definido: " + str(channel), colour=discord.Colour(0x370c5e),
                          description=f"{arg}")
    embed.set_footer(icon_url=betina_icon,
                     text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name, year()))
    await ctx.send(embed=embed, delete_after=10)
    leave_list[guild_id] = (channel_id, arg)
    with open('leave.json', 'w') as file:
        json.dump(leave_list, file)


@leave_logs.error
async def leave_handler(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(title="Comando $leavelogs:define um canal que irá receber as mensagens quando alguem sair"
                                    " do servidor"
                                    "\n \n**Como usar: $leavelogs <#Canal> <Mensagem>**",
                              colour=discord.Colour(0x370c5e))

        embed.set_author(name="Betina#9182",
                         icon_url=betina_icon)
        embed.set_footer(icon_url=betina_icon,
                         text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name, year()))
        embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                        "ter a permissão de* ``"
                                                        "Administrador`` *para utilizar este comando!*",
                        inline=False)
        embed.add_field(name="📖**Exemplos:**", value="$leavelogs #jogadores Adeus!"
                                                      "\n$leavelogs #iniciado Tchau, vacilão"
                                                      "", inline=False)
        embed.add_field(name="🔀**Outros Comandos**", value="``$defleavelogs, $dllogs.``", inline=False)

        msg = await ctx.send(embed=embed)
        await msg.add_reaction("❓")

    elif isinstance(error, commands.MissingRequiredArgument):
        if error.param.name == 'arg':
            embed = discord.Embed(
                title="Comando $leavelogs:define um canal que irá receber as mensagens quando alguem sair"
                      " do servidor"
                      "\n \n**Como usar: $leavelogs <#Canal> <Mensagem>**", colour=discord.Colour(0x370c5e))

            embed.set_author(name="Betina#9182",
                             icon_url=betina_icon)
            embed.set_footer(icon_url=betina_icon,
                             text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name,
                                                                                       year()))
            embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                            "ter a permissão de* ``"
                                                            "Administrador`` *para utilizar este comando!*",
                            inline=False)
            embed.add_field(name="📖**Exemplos:**", value="$leavelogs #jogadores Adeus!"
                                                          "\n$leavelogs #iniciado Tchau, vacilão"
                                                          "", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$defleavelogs, $dllogs.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")

        if error.param.name == 'channel':
            embed = discord.Embed(
                title="Comando $leavelogs:define um canal que irá receber as mensagens quando alguem sair"
                      " do servidor"
                      "\n \n**Como usar: $leavelogs <#Canal> <Mensagem>**", colour=discord.Colour(0x370c5e))

            embed.set_author(name="Betina#9182",
                             icon_url=betina_icon)
            embed.set_footer(icon_url=betina_icon,
                             text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name,
                                                                                       year()))
            embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                            "ter a permissão de* ``"
                                                            "Administrador`` *para utilizar este comando!*",
                            inline=False)
            embed.add_field(name="📖**Exemplos:**", value="$leavelogs #jogadores Adeus!"
                                                          "\n$leavelogs #iniciado Tchau, vacilão"
                                                          "", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$defleavelogs, $dllogs.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")



@commands.cooldown(2, 10, commands.BucketType.guild)
@commands.guild_only()
@client.command(name='reactionlogsin', aliases=['defreactionlogsin', 'drlogsin'])
@has_permissions(administrator=True)
async def reaction_logsin(ctx, channel: discord.TextChannel, *, arg: str = 'Acabou de ganhar o cargo de: '):
    guild_id = str(ctx.guild.id)
    channel_id = str(channel.id)

    embed = discord.Embed(title="Canal de logs do sistema de reação automático"
                                " definido: " + str(channel), colour=discord.Colour(0x370c5e))
    embed.set_footer(icon_url=betina_icon,
                     text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name, year()))
    await ctx.send(embed=embed, delete_after=10)
    reactions_logs_in[guild_id] = (channel_id, arg)

    with open('reactionslogsin.json', 'w') as file:
        json.dump(reactions_logs_in, file)


@reaction_logsin.error
async def reaction_logsin_handler(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(
            title="Comando $reactionlogsin: define um canal que irá receber as mensagens quando alguem reagir"
                  " no sistema de autorole"
                  "\n \n**Como usar: $reactionlogs <#Canal> <Mensagem> (opcional)**", colour=discord.Colour(0x370c5e))

        embed.set_author(name="Betina#9182",
                         icon_url=betina_icon)
        embed.set_footer(icon_url=betina_icon,
                         text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name, year()))
        embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                        "ter a permissão de* ``"
                                                        "Administrador`` *para utilizar este comando!*",
                        inline=False)
        embed.add_field(name="📖**Exemplos:**", value="$reactionlogsin #jogadores Pegou o melhor cargo de todos"
                                                      "\n$reactionlogsin #iniciado Entrou no novo mundo"
                                                      "", inline=False)
        embed.add_field(name="🔀**Outros Comandos**", value="``$defreactionlogsin, $drlogsin.``", inline=False)

        msg = await ctx.send(embed=embed)
        await msg.add_reaction("❓")

    elif isinstance(error, commands.MissingRequiredArgument):
        if error.param.name == 'channel':
            embed = discord.Embed(
                title="Comando $reactionlogsin: define um canal que irá receber as mensagens quando alguem reagir"
                      " no sistema de autorole"
                      "\n \n**Como usar: $reactionlogs <#Canal> <Mensagem> (opcional)**",
                colour=discord.Colour(0x370c5e))

            embed.set_author(name="Betina#9182",
                             icon_url=betina_icon)
            embed.set_footer(icon_url=betina_icon,
                             text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name,
                                                                                       year()))
            embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                            "ter a permissão de* ``"
                                                            "Administrador`` *para utilizar este comando!*",
                            inline=False)
            embed.add_field(name="📖**Exemplos:**", value="$reactionlogsin #jogadores Pegou o melhor cargo de todos"
                                                          "\n$reactionlogsin #iniciado Entrou no novo mundo"
                                                          "", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$defreactionlogsin, $drlogsin.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")




@commands.cooldown(2, 10, commands.BucketType.guild)
@commands.guild_only()
@client.command(name='reactionlogsout', aliases=['defreactionlogsout', 'drlogsout'])
@has_permissions(administrator=True)
async def reaction_logsout(ctx, channel: discord.TextChannel, *, arg: str = 'Acabou de perder o cargo de: '):
    guild_id = str(ctx.guild.id)
    channel_id = str(channel.id)
    embed = discord.Embed(title="Canal de logs do sistema de reação automático"
                                " definido: " + str(channel), colour=discord.Colour(0x370c5e))
    embed.set_footer(icon_url=betina_icon,
                     text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name, year()))
    await ctx.send(embed=embed, delete_after=10)
    reactions_logs_out[guild_id] = (channel_id, arg)

    with open('reactionslogsout.json', 'w') as file:
        json.dump(reactions_logs_out, file)


@reaction_logsout.error
async def reaction_logsout_handler(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(
            title="Comando $reactionlogsout: define um canal que irá receber as mensagens quando alguem reagir"
                  " no sistema de autorole"
                  "\n \n**Como usar: $reactionlogsout <#Canal> <Mensagem> (opcional)**",
            colour=discord.Colour(0x370c5e))

        embed.set_author(name="Betina#9182",
                         icon_url=betina_icon)
        embed.set_footer(icon_url=betina_icon,
                         text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name, year()))
        embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                        "ter a permissão de* ``"
                                                        "Administrador`` *para utilizar este comando!*",
                        inline=False)
        embed.add_field(name="📖**Exemplos:**", value="$reactionlogsout #jogadores Perdeu o melhor cargo de todos"
                                                      "\n$reactionlogsin #iniciado Saiu do novo mundo"
                                                      "", inline=False)
        embed.add_field(name="🔀**Outros Comandos**", value="``$defreactionlogsout, $drlogsout.``", inline=False)

        msg = await ctx.send(embed=embed)
        await msg.add_reaction("❓")

    elif isinstance(error, commands.MissingRequiredArgument):
        if error.param.name == 'channel':
            embed = discord.Embed(
                title="Comando $reactionlogsout: define um canal que irá receber as mensagens quando alguem reagir"
                      " no sistema de autorole"
                      "\n \n**Como usar: $reactionlogsout <#Canal> <Mensagem> (opcional)**",
                colour=discord.Colour(0x370c5e))

            embed.set_author(name="Betina#9182",
                             icon_url=betina_icon)
            embed.set_footer(icon_url=betina_icon,
                             text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name,
                                                                                       year()))
            embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                            "ter a permissão de* ``"
                                                            "Administrador`` *para utilizar este comando!*",
                            inline=False)
            embed.add_field(name="📖**Exemplos:**", value="$reactionlogsout #jogadores Perdeu o melhor cargo de todos"
                                                          "\n$reactionlogsin #iniciado Saiu do novo mundo"
                                                          "", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$defreactionlogsout, $drlogsout.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")




@commands.cooldown(2, 10, commands.BucketType.guild)
@commands.guild_only()
@client.command(name='cargoinicial', aliases=['defci', 'dci'])
@has_permissions(administrator=True)
async def cargo_inicial(ctx, role: discord.Role):
    guild_id = str(ctx.guild.id)

    embed = discord.Embed(title="Cargo inicial definido: " + str(role), colour=discord.Colour(0x370c5e))
    embed.set_footer(icon_url=betina_icon,
                     text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name, year()))
    await ctx.send(embed=embed, delete_after=10)
    initial_role[guild_id] = str(role)

    with open('initialsrole.json', 'w') as file:
        json.dump(initial_role, file)


@cargo_inicial.error
async def cargo_inicial_handler(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(
            title="Comando $cargoinicial: define um cargo inicial para dar a um membro "
                  " sempre que entrar no servidor!"
                  "\n \n**Como usar: $cargoinicial <@cargo>**", colour=discord.Colour(0x370c5e))

        embed.set_author(name="Betina#9182",
                         icon_url=betina_icon)
        embed.set_footer(icon_url=betina_icon,
                         text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name, year()))
        embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                        "ter a permissão de* ``"
                                                        "Administrador`` *para utilizar este comando!*",
                        inline=False)
        embed.add_field(name="📖**Exemplos:**", value="$cargoinicial @jogadores"
                                                      "\n$cargoinicial @iniciado"
                                                      "", inline=False)
        embed.add_field(name="🔀**Outros Comandos**", value="``$defci, $dci.``", inline=False)

        msg = await ctx.send(embed=embed)
        await msg.add_reaction("❓")

    elif isinstance(error, commands.MissingRequiredArgument):
        if error.param.name == 'role':
            embed = discord.Embed(
                title="Comando $cargoinicial: define um cargo inicial para dar a um membro "
                      " sempre que entrar no servidor!"
                      "\n \n**Como usar: $cargoinicial <@cargo>**", colour=discord.Colour(0x370c5e))

            embed.set_author(name="Betina#9182",
                             icon_url=betina_icon)
            embed.set_footer(icon_url=betina_icon,
                             text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name,
                                                                                       year()))
            embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                            "ter a permissão de* ``"
                                                            "Administrador`` *para utilizar este comando!*",
                            inline=False)
            embed.add_field(name="📖**Exemplos:**", value="$cargoinicial @jogadores"
                                                          "\n$cargoinicial @iniciado"
                                                          "", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$defci, $dci.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")



@commands.cooldown(2, 10, commands.BucketType.guild)
@commands.guild_only()
@client.command(name='prefixo', aliases=['newprefix', 'novoprefixo'])
@has_permissions(administrator=True)
async def novo_prefixo(ctx, prefix: str):
    guild_id = str(ctx.guild.id)
    embed = discord.Embed(title="Novo prefixo definido: " + prefix, colour=discord.Colour(0x370c5e))
    embed.set_footer(icon_url=betina_icon,
                     text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name, year()))
    await ctx.send(embed=embed, delete_after=10)
    bot_prefix[guild_id] = prefix

    with open('prefixes.json', 'w') as file:
        json.dump(bot_prefix, file)

    return prefix


@novo_prefixo.error
async def novo_prefixo_handler(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(
            title="Comando $prefixo: define um novo prefixo para o bot!"
                  "\n \n**Como usar: $prefixo <caracter>**")

        embed.set_author(name="Betina#9182",
                         icon_url=betina_icon)
        embed.set_footer(icon_url=betina_icon,
                         text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name, year()))
        embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                        "ter a permissão de* ``"
                                                        "Administrador`` *para utilizar este comando!*",
                        inline=False)
        embed.add_field(name="📖**Exemplos:**", value="$prefixo @"
                                                      "\n$prefixo >"
                                                      "", inline=False)
        embed.add_field(name="🔀**Outros Comandos**", value="``$newprefix, $np.``", inline=False)

        msg = await ctx.send(embed=embed)
        await msg.add_reaction("❓")

    elif isinstance(error, commands.MissingRequiredArgument):
        if error.param.name == 'prefix':
            embed = discord.Embed(
                title="Comando $prefixo: define um novo prefixo para o bot!"
                      "\n \n**Como usar: $prefixo <caracter>**", colour=discord.Colour(0x370c5e))

            embed.set_author(name="Betina#9182",
                             icon_url=betina_icon)
            embed.set_footer(icon_url=betina_icon,
                             text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name,
                                                                                       year()))
            embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                            "ter a permissão de* ``"
                                                            "Administrador`` *para utilizar este comando!*",
                            inline=False)
            embed.add_field(name="📖**Exemplos:**", value="$prefixo @"
                                                          "\n$prefixo >"
                                                          "", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$newprefix, $np.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")




@commands.cooldown(2, 10, commands.BucketType.guild)
@commands.guild_only()
@client.command(name='config', aliases=['configuration', 'definições'])
@has_permissions(administrator=True)
async def configuration(ctx):
    if ctx.message.author.avatar_url_as(static_format='png')[54:].startswith('a_'):
        avi = ctx.message.author.avatar_url.rsplit("?", 1)[0]
    else:
        avi = ctx.message.author.avatar_url_as(static_format='png')
    guild_id = str(ctx.guild.id)
    if guild_id not in reactions_list:
        status = 'Inativo'
    else:
        status = 'Ativo'

    if guild_id not in reactions_logs_in:
        status1 = 'Não tem canal definido!'
    else:
        guild = ctx.guild.get_channel(int(reactions_logs_in[guild_id][0]))
        status1 = guild

    if guild_id not in reactions_logs_out:
        status2 = 'Não tem canal definido!'
    else:
        guild = ctx.guild.get_channel(int(reactions_logs_out[guild_id][0]))
        status2 = guild

    if guild_id not in initial_role:
        status3 = 'Não tem cargo definido!'
    else:
        status3 = initial_role[guild_id]

    if guild_id not in leave_list:
        status4 = 'Não tem canal definido!'
    else:
        guild = ctx.guild.get_channel(int(leave_list[guild_id][0]))
        status4 = guild

    if guild_id not in join_list:
        status5 = 'Não tem canal definido!'
    else:
        guild = ctx.guild.get_channel(int(join_list[guild_id][0]))
        status5 = guild

    if guild_id not in bot_prefix:
        status6 = '$'
    else:
        status6 = bot_prefix[guild_id]

    if guild_id not in digit_log:
        status7 = 'Não tem canal definido!'
    else:
        guild = ctx.guild.get_channel(int(digit_log[guild_id]))
        status7 = guild

    if guild_id not in limitador_log:
        status8 = 'Desligado!'
    else:
        status8 = 'Ligado!'
    if guild_id not in levels_on:
        status9 = 'Desligado!'
    else:
        status9 = 'Ligado!'

    embed = discord.Embed(title="⚙ Configurações do servidor:", colour=discord.Colour(0x370c5e),
                          description="Abaixo estarão listadas todas as configurações do bot!\n\n")
    embed.set_thumbnail(url=ctx.message.guild.icon_url)
    embed.set_author(name=ctx.message.author.name, icon_url=avi)
    embed.set_footer(icon_url=betina_icon,
                     text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name, year()))
    embed.add_field(name="💬**Prefixo do bot neste servidor**", value=f"O prefixo atual do bot é: " + f'{status6}',
                    inline=False)
    embed.add_field(name="🚪**Join Logs neste servidor:**",
                    value=f"O nome do Canal definido para Join Logs é: " + f'{status5}')
    embed.add_field(name="🚪**Leave Logs neste servidor:**",
                    value=f"O nome do Canal definido para Leave Logs é: " + f'{status4}', inline=False)
    embed.add_field(name="🔗**Auto Role neste servidor:**", value=f'O status do auto role é ' + f'{status}',
                    inline=False)
    embed.add_field(name="🚪**Reaction Logs In neste servidor:**",
                    value=f"O nome do Canal definido para Reaction Logs In é: " + f'{status1}')
    embed.add_field(name="🚪**Reaction Logs Out neste servidor:**",
                    value=f"O nome do Canal definido para Reaction Logs Out é: " + f'{status2}', inline=False)
    embed.add_field(name="🎌 **Cargo Inicial neste servidor:**",
                    value=f"O cargo definido neste servidor é: " + f'{status3}')
    embed.add_field(name="🚪 **Digit Logs neste servidor:**",
                    value=f"O nome do Canal definido para Digit Logs é: " + f'{status7}', inline=False)
    embed.add_field(name="💬 **Bot Channel neste servidor:**",
                    value=f"O Status do bot channel é: " + f'{status8}')
    embed.add_field(name="⭐ **Sistema de xp:**",
                    value=f"O Status do sistema de xp é: " + f'{status9}')
    await ctx.send(embed=embed)


@configuration.error
async def configuration_handler(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(
            title="Comando $config: Diz a configuração do bot nesses servidor!"
                  "\n \n**Como usar: $config**", colour=discord.Colour(0x370c5e))

        embed.set_author(name="Betina#9182",
                         icon_url=betina_icon)
        embed.set_footer(icon_url=betina_icon,
                         text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name, year()))
        embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                        "ter a permissão de* ``"
                                                        "Administrador`` *para utilizar este comando!*",
                        inline=False)
        embed.add_field(name="📖**Exemplos:**", value="$config", inline=False)
        embed.add_field(name="🔀**Outros Comandos**", value="``$configuration, $definições.``", inline=False)

        msg = await ctx.send(embed=embed)
        await msg.add_reaction("❓")



@commands.cooldown(2, 10, commands.BucketType.guild)
@commands.guild_only()
@client.command(name='digitlogs', aliases=['defdigitlogs', 'ddlogs'])
@has_permissions(administrator=True)
async def digilog(ctx, channel: discord.TextChannel):
    guild_id = str(ctx.guild.id)
    channel_id = str(channel.id)
    embed = discord.Embed(title="Canal de logs do sistema"
                                " definido: " + str(channel), colour=discord.Colour(0x370c5e))
    embed.set_footer(icon_url=betina_icon,
                     text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name, year()))
    await ctx.send(embed=embed, delete_after=10)
    digit_log[guild_id] = channel_id

    with open('digitlogs.json', 'w') as file:
        json.dump(digit_log, file)


@digilog.error
async def digilog_handler(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(
            title="Comando $digitlogs: define um canal que irá receber as mensagens dizendo todos"
                  " os comandos de administracao usado"
                  "\n \n**Como usar: $digitlogs <#Canal>**", colour=discord.Colour(0x370c5e))

        embed.set_author(name="Betina#9182",
                         icon_url=betina_icon)
        embed.set_footer(icon_url=betina_icon,
                         text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name, year()))
        embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                        "ter a permissão de* ``"
                                                        "Administrador`` *para utilizar este comando!*",
                        inline=False)
        embed.add_field(name="📖**Exemplos:**", value="$digitlogs #jogadores"
                                                      "\n$digitlogs #iniciado"
                                                      "", inline=False)
        embed.add_field(name="🔀**Outros Comandos**", value="``$defdigitlogs, $ddlogs.``", inline=False)

        msg = await ctx.send(embed=embed)
        await msg.add_reaction("❓")

    elif isinstance(error, commands.MissingRequiredArgument):
        if error.param.name == 'channel':
            embed = discord.Embed(
                title="Comando $digitlogs: define um canal que irá receber as mensagens dizendo todos"
                      " os comandos de administracao usado"
                      "\n \n**Como usar: $digitlogs <#Canal>**", colour=discord.Colour(0x370c5e))

            embed.set_author(name="Betina#9182",
                             icon_url=betina_icon)
            embed.set_footer(icon_url=betina_icon,
                             text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name,
                                                                                       year()))
            embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                            "ter a permissão de* ``"
                                                            "Administrador`` *para utilizar este comando!*",
                            inline=False)
            embed.add_field(name="📖**Exemplos:**", value="$digitlogs #jogadores"
                                                          "\n$digitlogs #iniciado"
                                                          "", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$defdigitlogs, $ddlogs.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")




@commands.cooldown(2, 10, commands.BucketType.guild)
@commands.guild_only()
@client.command(name='invites', aliases=['userinv', 'uinv'])
@has_permissions(administrator=True)
async def invites(ctx, user: discord.Member = None):
    total_uses = 0
    embed = discord.Embed(title='🎟 __Convites criados pelo {}__'.format(user.name), colour=discord.Colour(0x370c5e))
    invites = await ctx.message.guild.invites()
    for invite in invites:
        if invite.inviter == user:
            total_uses += invite.uses
            embed.add_field(name='🎟 Convite', value=invite.id)
            embed.add_field(name='📋 Usos', value=invite.uses)
            embed.add_field(name='💬 Canal', value=invite.channel)
            embed.set_footer(icon_url=betina_icon,
                             text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name,
                                                                                       year()))
    embed.add_field(name='🖊__Usos Totais__', value=total_uses)
    await ctx.send(embed=embed)


@invites.error
async def invites_handler(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(
            title="Comando $invites: diz todos os invites criados por um usuário e suas informações."
                  "\n \n**Como usar: $invites <usuário>**", colour=discord.Colour(0x370c5e))

        embed.set_author(name="Betina#9182",
                         icon_url=betina_icon)
        embed.set_footer(icon_url=betina_icon,
                         text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name, year()))
        embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                        "ter a permissão de* ``"
                                                        "Administrador`` *para utilizar este comando!*",
                        inline=False)
        embed.add_field(name="📖**Exemplos:**", value="$invites @fulano"
                                                      "\n$invites @sicrano"
                                                      "", inline=False)
        embed.add_field(name="🔀**Outros Comandos**", value="``$userinv, $uinv.``", inline=False)

        msg = await ctx.send(embed=embed)
        await msg.add_reaction("❓")

    elif isinstance(error, commands.MissingRequiredArgument):
        if error.param.name == 'user':
            embed = discord.Embed(
                title="Comando $invites: diz todos os invites criados por um usuário e suas informações."
                      "\n \n**Como usar: $invites <usuário>**", colour=discord.Colour(0x370c5e))

            embed.set_author(name="Betina#9182",
                             icon_url=betina_icon)
            embed.set_footer(icon_url=betina_icon,
                             text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name,
                                                                                       year()))
            embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                            "ter a permissão de* ``"
                                                            "Administrador`` *para utilizar este comando!*",
                            inline=False)
            embed.add_field(name="📖**Exemplos:**", value="$invites @fulano"
                                                          "\n$invites @sicrano"
                                                          "", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$userinv, $uinv.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")



@commands.cooldown(2, 10, commands.BucketType.guild)
@commands.guild_only()
@client.command(name='botchannel', aliases=['canaldobot', 'cdb'])
@has_permissions(administrator=True)
async def limite(ctx, channel: discord.TextChannel):
    guild_id = str(ctx.guild.id)
    channel_id = str(channel.id)
    embed = discord.Embed(title="Canal de funcionamento do bot"
                                " definido: " + str(channel),
                          colour=discord.Colour(0x370c5e), description='*Os únicos comandos'
                                                                       ' limitados são: afk, userinfo, '
                                                                       'todas as funções da parte de Diversão,'
                                                                       ' Interação e Cobrança*.')
    embed.set_footer(icon_url=betina_icon,
                     text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name, year()))
    await ctx.send(embed=embed, delete_after=30)
    limitador_log[guild_id] = channel_id

    with open('limitador.json', 'w') as file:
        json.dump(limitador_log, file)


@limite.error
async def limite_handler(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(
            title="Comando $botchannel: define um canal que será o único local que pode usar o comando da Betina"
                  "\n \n**Como usar: $canald"
                  "obot <#Canal>**", colour=discord.Colour(0x370c5e), description='*Os únicos comandos'
                                                                                  ' limitados são: afk, userinfo, '
                                                                                  'todas as funções da parte de Diversão,'
                                                                                  ' Interação e Cobrança*.')

        embed.set_author(name="Betina#9182",
                         icon_url=betina_icon)
        embed.set_footer(icon_url=betina_icon,
                         text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name, year()))
        embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                        "ter a permissão de* ``"
                                                        "Administrador`` *para utilizar este comando!*",
                        inline=False)
        embed.add_field(name="📖**Exemplos:**", value="$canaldobot #jogadores"
                                                      "\n$botchannel #iniciado"
                                                      "", inline=False)
        embed.add_field(name="🔀**Outros Comandos**", value="``$canaldobot, $cdb.``", inline=False)

        msg = await ctx.send(embed=embed)
        await msg.add_reaction("❓")

    elif isinstance(error, commands.MissingRequiredArgument):
        if error.param.name == 'channel':
            embed = discord.Embed(
                title="Comando $botchannel: define um canal que será o único local que pode usar o comando da Betina"
                      "\n \n**Como usar: $canaldobot"
                      " <#Canal>**", colour=discord.Colour(0x370c5e), description='*Os únicos comandos'
                                                                                  ' limitados são: afk, userinfo, '
                                                                                  'todas as funções da parte de Diversão,'
                                                                                  ' Interação e Cobrança*.')

            embed.set_author(name="Betina#9182",
                             icon_url=betina_icon)
            embed.set_footer(icon_url=betina_icon,
                             text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name,
                                                                                       year()))
            embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                            "ter a permissão de* ``"
                                                            "Administrador`` *para utilizar este comando!*",
                            inline=False)
            embed.add_field(name="📖**Exemplos:**", value="$canaldobot #jogadores"
                                                          "\n$botchannel #iniciado"
                                                          "", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$canaldobot, $cdb.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")




@commands.cooldown(2, 10, commands.BucketType.guild)
@commands.guild_only()
@client.command(name='tirabotchannel', aliases=['tiracanaldobot', 'tiracdb'])
@has_permissions(administrator=True)
async def tiralimite(ctx):
    guild_id = str(ctx.guild.id)

    if guild_id in limitador_log:
        embed = discord.Embed(title="Canal de funcionamento do bot"
                                    " foi retirado.",
                              colour=discord.Colour(0x370c5e),
                              description='*Os comandos agora não estão mais limitados!*.')
        embed.set_footer(icon_url=betina_icon,
                         text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name, year()))
        await ctx.send(embed=embed, delete_after=30)
        del limitador_log[guild_id]
    else:
        await ctx.send('Você não tem nenhum canal definido para usar os meus comandos, como posso tirar ele ?')

    with open('limitador.json', 'w') as file:
        json.dump(limitador_log, file)


@tiralimite.error
async def tira_limite_handler(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(
            title="Comando $tirabotchannel: retira o canal definido pelo comando botchannel"
                  "\n \n**Como usar: $canaldobot <#Canal>**", colour=discord.Colour(0x370c5e)
            , description='*Os comandos não serão mais limitados a um canal único*.')

        embed.set_author(name="Betina#9182",
                         icon_url=betina_icon)
        embed.set_footer(icon_url=betina_icon,
                         text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name, year()))
        embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                        "ter a permissão de* ``"
                                                        "Administrador`` *para utilizar este comando!*",
                        inline=False)
        embed.add_field(name="📖**Exemplos:**", value="$tiracanaldobot"
                                                      "\n$tirabotchannel"
                                                      "", inline=False)
        embed.add_field(name="🔀**Outros Comandos**", value="``$tiracanaldobot, $tiracdb.``", inline=False)

        msg = await ctx.send(embed=embed)
        await msg.add_reaction("❓")



@commands.cooldown(2, 10, commands.BucketType.guild)
@commands.guild_only()
@client.command(name='betinainfo')
async def betinainfo(ctx):
    guild_id = str(ctx.guild.id)
    user_id = str(ctx.author.id)
    if guild_id in limitador_log:
        if str(ctx.message.channel.id) == limitador_log[guild_id]:
            t1 = time.perf_counter()
            async with ctx.message.channel.typing():
                t2 = time.perf_counter()
                embed = discord.Embed(colour=discord.Colour(0x370c5e), description='**<a:carregando:'
                                                                                   '509840579316940800> Inf'
                                                                                   'ormações da Betina:**')
                criador = '\n 🤴 BDantas#7096'
                nome = 'Betina'
                id = str(client.user.id)
                tag = str(client.user)
                ping = '{}ms'.format(round((t2 - t1) * 1000))
                users = str(len(set(client.users)))
                servers = str(len(client.guilds))
                canais = str(len(set(client.get_all_channels())))
                fundado = '02/01/2019'
                avatar = f"[Icone]({betina_icon})"
                program = "Python 3.6.6"
                hospedagem = 'Raspberry Pi'
                uptime = "{} horas {} minutos ".format(0, 0)
                temp =[x.name for x in ctx.bot.commands]
                commandos2 = str(len(temp))
                cpu = "{} % ".format(str(psutil.cpu_percent(interval=1)))
                invite = '[[Me adicione]](https://discordapp.com/oauth2/authorize?&client_id=527' \
                         '565353199337474&scope=bot&permissions=8)'
                suporte = '[[Peça ajuda]](https://discord.gg/eZrzDfs)'
                aa = "\n<:bot:510893" \
                     "968414867468> **Nom" \
                     "e:** " + nome + "\n💻 **I" \
                                      "D:** " + id + "\n📛 **T" \
                                                     "ag:** " + tag + "\n⭐ **" \
                                                                      "Fundado em:**" \
                                                                      " " + fundado + "\n<a:pin" \
                                                                                      "g:51206" \
                                                                                      "5320320761867>**Ping:** " + ping
                bb = "\n🌐 **Servidores:** " + servers + "\n<a:happy:51551" \
                                                         "8973618683910> **Usuár" \
                                                         "ios:** " + users + "\n📇 **Canais:** " + canais
                cc = "\n<a:faps:515518909521330176> **Totais:** " + commandos2
                ee = "\n<:python:" \
                     "507486258184978443>" \
                     " **Programaçã" \
                     "o:** " + program + "\n<a:cursor" \
                                         ":507925560333434890> **H" \
                                         "ospedagem:** " + hospedagem + "\n🕒 **Tem" \
                                                                        "po Online:" \
                                                                        "** " + uptime + "\n💽 **Cpu Usado:** " + cpu
                gg = "\n🖼️ **Avatar:** " + avatar + "\n✉ **Invite:** " + invite + "\n**<:Di" \
                                                                                   "scordDev:507925" \
                                                                                   "579245551616> S" \
                                                                                   "uporte:** " + suporte
                ff = criador
                embed.add_field(name="`📑 | Informações:`", value=aa, inline=False)
                embed.set_thumbnail(url=f"{betina_icon}")
                embed.add_field(name="`🗣 | Desenvolvedor:`", value=ff)
                embed.add_field(name="`🌐 | Conexões:`", value=bb, inline=False)
                embed.add_field(name="`⚙ | Configurações:`", value=ee, inline=False)
                embed.add_field(name="`🗃️ | Links:`", value=gg)
                embed.add_field(name="`📋 | Comandos:`", value=cc, inline=False)
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name,
                                                                                           year()))
            await ctx.send(embed=embed)
        else:
            guild = ctx.guild.get_channel(int(limitador_log[guild_id]))
            await ctx.send(f'Esse não foi o canal definido para usar os comandos. Tente utilizar o canal {guild}')
            return
    else:
        t1 = time.perf_counter()
        async with ctx.message.channel.typing():
            t2 = time.perf_counter()
            embed = discord.Embed(colour=discord.Colour(0x370c5e), description='**<a:carregando:'
                                                                               '509840579316940800> Inf'
                                                                               'ormações da Betina:**')
            criador = '\n 🤴 BDantas#7096'
            nome = 'Betina'
            id = str(client.user.id)
            tag = str(client.user)
            ping = '{}ms'.format(round((t2 - t1) * 1000))
            users = str(len(set(client.users)))
            servers = str(len(client.guilds))
            canais = str(len(set(client.get_all_channels())))
            fundado = '02/01/2019'
            avatar = f"[Icone]({betina_icon})"
            program = "Python 3.6.6"
            hospedagem = 'Raspberry Pi'
            uptime = "{} horas {} minutos ".format(0, 0)
            temp = [x.name for x in ctx.bot.commands] 
            commandos2 = str(len(temp))
            cpu = "{} % ".format(str(psutil.cpu_percent(interval=1)))
            invite = '[[Me adicione]](https://discordapp.com/oauth2/authorize?&client_id=527' \
                     '565353199337474&scope=bot&permissions=8)'
            suporte = '[[Peça ajuda]](https://discord.gg/eZrzDfs)'
            aa = "\n<:bot:510893" \
                 "968414867468> **Nom" \
                 "e:** " + nome + "\n💻 **I" \
                                  "D:** " + id + "\n📛 **T" \
                                                 "ag:** " + tag + "\n⭐ **" \
                                                                  "Fundado em:**" \
                                                                  " " + fundado + "\n<a:pin" \
                                                                                  "g:51206" \
                                                                                  "5320320761867>**Ping:** " + ping
            bb = "\n🌐 **Servidores:** " + servers + "\n<a:happy:51551" \
                                                     "8973618683910> **Usuár" \
                                                     "ios:** " + users + "\n📇 **Canais:** " + canais
            cc = "\n<a:faps:515518909521330176> **Totais:** " + commandos2
            ee = "\n<:python:" \
                 "507486258184978443>" \
                 " **Programaçã" \
                 "o:** " + program + "\n<a:cursor:507925560333434890>" \
                                     " **Hospedagem:** " + hospedagem + "\n🕒 **Tempo Online:** " + uptime + "\n💽 **C" \
                                                                                                             "pu Usado:** " + cpu
            gg = "\n🖼️ **Avatar:** " + avatar + "\n✉ **Invite:** " + invite + "\n**<:Di" \
                                                                               "scordDev:507925" \
                                                                               "579245551616> Suporte:** " + suporte
            ff = criador
            embed.add_field(name="`📑 | Informações:`", value=aa, inline=False)
            embed.set_thumbnail(url=f"{betina_icon}")
            embed.add_field(name="`🗣 | Desenvolvedor:`", value=ff)
            embed.add_field(name="`🌐 | Conexões:`", value=bb, inline=False)
            embed.add_field(name="`⚙ | Configurações:`", value=ee, inline=False)
            embed.add_field(name="`🗃️ | Links:`", value=gg)
            embed.add_field(name="`📋 | Comandos:`", value=cc, inline=False)
            embed.set_footer(icon_url=betina_icon,
                             text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name,
                                                                                       year()))
        await ctx.send(embed=embed)


@commands.cooldown(2, 10, commands.BucketType.guild)
@commands.guild_only()
@client.command(name='levelson')
@has_permissions(administrator=True)
async def levelson(ctx, channel: discord.TextChannel):
    guild_id = str(ctx.guild.id)
    channel_id = str(channel.id)
    embed = discord.Embed(title="Canal de funcionamento do sistema de level"
                                " definido: " + str(channel),
                          colour=discord.Colour(0x370c5e))
    embed.set_footer(icon_url=betina_icon,
                     text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name, year()))
    await ctx.send(embed=embed, delete_after=30)
    level_on[guild_id] = channel_id

    with open('levelon.json', 'w') as file:
        json.dump(level_on, file)


@levelson.error
async def levelson_handler(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        if error.param.name == 'channel':
            embed = discord.Embed(
                title="Comando $levelson: ativa o sistema de level da betina"
                      " e receberá todas as mensagens de level up em um canal definido!"
                      "\n \n**Como usar: $levelson <#canal>**", colour=discord.Colour(0x370c5e))

            embed.set_author(name="Betina#9182",
                             icon_url=betina_icon)
            embed.set_footer(icon_url=betina_icon,
                             text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name,
                                                                                       year()))
            embed.add_field(name="📖**Exemplos:**", value="$levelson #logs"
                                                          "\n$levelson #canal"
                                                          "", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")


    elif isinstance(error, MissingPermissions):
        embed = discord.Embed(
            title="Comando $levelson: ativa o sistema de level da betina"
                  " e receberá todas as mensagens de level up em um canal definido!"
                  "\n \n**Como usar: $levelson <#canal>**", colour=discord.Colour(0x370c5e))

        embed.set_author(name="Betina#9182",
                         icon_url=betina_icon)
        embed.set_footer(icon_url=betina_icon,
                         text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name,
                                                                                   year()))
        embed.add_field(name="📖**Exemplos:**", value="$levelson #logs"
                                                      "\n$levelson #canal"
                                                      "", inline=False)

        msg = await ctx.send(embed=embed)
        await msg.add_reaction("❓")


@commands.cooldown(2, 10, commands.BucketType.guild)
@commands.guild_only()
@client.command(name='level', aliases=['nivel', 'lvl'])
async def level(ctx, user: discord.Member = None):
    if user is None:
        user = ctx.author

    guild_id = str(ctx.message.guild.id)
    author_id = str(ctx.message.author.id)

    if guild_id not in level_on:
        embed = discord.Embed(title="Esse servidor não tem sistema de level definido!",
                              colour=discord.Colour(0x370c5e))
        embed.set_footer(icon_url=betina_icon,
                         text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name, year()))
        return await ctx.send(embed=embed)
    url = requests.get(user.avatar_url)
    msg = await ctx.channel.send(f'Sua imagem está carregando {ctx.author.name}! <a:carregando:'
                                 f'509840579316940800>')
    level = level_system[guild_id][author_id]['level']
    xp_atual = level_system[guild_id][author_id]['experiencia']
    xp_max = round((5 * (level ** 3)))
    avatar = Image.open(BytesIO(url.content))
    avatar = avatar.resize((150, 150))
    bigsize = (avatar.size[0] * 3, avatar.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(avatar.size, Image.ANTIALIAS)
    avatar.putalpha(mask)
    output = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)
    output.save('avatar.png')
    variavel = round((xp_atual/xp_max)*100)
    if variavel == 0:
        fundo = Image.open('level0.png')
    elif variavel <= 5 and variavel != 0:
        fundo = Image.open('level5.png')
    elif 10 >= variavel > 5:
        fundo = Image.open('level10.png')
    elif 30 >= variavel > 10:
        fundo = Image.open('level30.png')
    elif 40 >= variavel > 30:
        fundo = Image.open('level40.png')
    elif 60 >= variavel > 40:
        fundo = Image.open('level60.png')
    elif 75 >= variavel > 60:
        fundo = Image.open('level75.png')
    else:
        fundo = Image.open('level.png')
    fonte = ImageFont.truetype('Square.ttf', size=30)
    escrever = ImageDraw.Draw(fundo)
    if xp_atual >= 1000 and xp_max >= 1000:
        escrever.text(xy=(710, 190), text=f'{xp_atual/1000}k - {xp_max/1000}k xp', fill=(255, 255, 255), font=fonte)
    elif xp_atual >= 1000 > xp_max:
        escrever.text(xy=(710, 190), text=f'{xp_atual/1000}k - {xp_max} xp', fill=(255, 255, 255), font=fonte)
    elif xp_atual < 1000 <= xp_max:
        escrever.text(xy=(710, 190), text=f'{xp_atual} - {xp_max/1000}k xp', fill=(255, 255, 255), font=fonte)
    else:
        escrever.text(xy=(710, 190), text=f'{xp_atual} - {xp_max} xp', fill=(255, 255, 255), font=fonte)
    escrever.text(xy=(265, 140), text=f'{user}', fill=(255, 255, 255), font=fonte)
    escrever.text(xy=(65, 50), text=f'Level {level}', fill=(255, 255, 255), font=fonte)
    fundo.paste(avatar, (40, 90), avatar)
    fundo.save('infolevel.png')
    await msg.delete()
    await ctx.channel.send(file=discord.File('infolevel.png'))


@level.error
async def level_handler(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        if error.param.name == 'user':
            embed = discord.Embed(
                title="Comando $level: diz o level do usuário."
                      "\n \n**Como usar: $level <usuário> (opcional)**", colour=discord.Colour(0x370c5e))

            embed.set_author(name="Betina#9182",
                             icon_url=betina_icon)
            embed.set_footer(icon_url=betina_icon,
                             text="Usado às {} Horário de Brasília | © {} {} .".format(hora(), client.user.name,
                                                                                       year()))
            embed.add_field(name="📖**Exemplos:**", value="$level @fulano"
                                                          "\n$level @sicrano"
                                                          "", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$nivel, $lvl.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")


if __name__ == '__main__':
    for extension in startup_extensions:
        try:
            client.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Falha ao carregar a extensão {}\n{}'.format(extension, exc))


client.run(TOKEN)
