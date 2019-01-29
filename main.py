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

from discord.ext import commands
from forex_python.converter import CurrencyRates
from dhooks import Webhook
from discord.utils import get
from discord.ext.commands import has_permissions, MissingPermissions


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
        
        
@client.event
async def on_ready():
    print('--------------BD--------------')
    print('BOT ONLINE')
    print('Nome do Bot: ' + client.user.name)
    print('ID do Bot: ' + str(client.user.id))
    print('Versao do Discord: ' + discord.__version__)
    print('--------------BD--------------')
    game = discord.Game("$ajuda")
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
        embed.set_footer(text="Betina Brazilian Bot", icon_url=betina_icon)
        await guild.send(embed=embed)


@client.event
async def on_message_edit(before, after):
    if before is None:
        if after.guild.id in digit_log:
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
    elif after is None:
        if before.guild.id in digit_log:
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
            embed.add_field(name='Canal', value='#' + str(after.channel), inline=True)
            embed.add_field(name='Horário:', value=str(before.created_at.strftime("%H:%M:%S - %d/%m/%y")), inline=False)
            embed.set_footer(text="Betina Brazilian Bot", icon_url=betina_icon)
            await guild.send(embed=embed)
    else:
        if after.guild.id in digit_log:
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
            embed.add_field(name='Canal', value='#' + str(after.channel), inline=True)
            embed.add_field(name='Horário:', value=str(before.created_at.strftime("%H:%M:%S - %d/%m/%y")), inline=False)
            embed.set_footer(text="Betina Brazilian Bot", icon_url=betina_icon)
            await guild.send(embed=embed)


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
        embed.add_field(name='Usuário:', value=str(message.author) + ' (' + str(message.author.name) + ')', inline=False)
        embed.add_field(name='Horário:', value=str(message.created_at.strftime("%H:%M:%S - %d/%m/%y")), inline=True)
        embed.add_field(name='Mensagem:', value=str(message.content), inline=False)
        embed.add_field(name='Canal', value='#' + str(message.channel), inline=True)
        embed.set_footer(text="Betina Brazilian Bot", icon_url=betina_icon)
        await guild.send(embed=embed)


@client.event
async def on_member_join(member):
    if str(member.guild.id) not in join_list:
        return
    canal = member.guild.get_channel(int(join_list[str(member.guild.id)][0]))
    fmt = '{0.name} ' + join_list[str(member.guild.id)][1]
    await canal.send(fmt.format(member))
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
        await guild.send(fmt)
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
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url=betina_icon)

            embed.add_field(name="Precisa de ajuda?🤔", value="para usar meus comandos utilize o $help")
            embed.add_field(name="Teve alguma ideia boa ? 😱: ",
                            value="fale com o meu criador, ele poderá implementar!")
            embed.add_field(name="Teve algum problema com o bot ?🙄",
                            value="não se preocupe, alguns problemas são comuns"
                                  " considerando o fato do bot estar em construção,"
                                  " mas, de qualquer forma,  fale com o meu criador.")
            embed.add_field(name="Criador do bot:", value="DantasB#7096", inline=True)
            embed.add_field(name="Maiores informações:", value="github.com/DantasB", inline=True)

            await membro.send(embed=embed)


@client.event
async def on_message(message):
    print('Logs:\n', message.author, message.content)
    if message.content.startswith('<@527565353199337474>'):
        if not message.guild:
            return
        guild_id = str(message.guild.id)
        author_id = str(message.author.id)
        if guild_id in limitador_log:
            if str(message.channel.id) == limitador_log[guild_id]:
                embed = discord.Embed(colour=discord.Colour(0x370c5e), description="**Digite: `$help ou $ajuda` para ver meus comandos**")
                embed.set_footer(text="Betina Brazilian Bot")
                await message.channel.send(embed=embed)
            else:
                return
        else:
            embed = discord.Embed(colour=discord.Colour(0x370c5e),
                                  description="**Digite: `$help ou $ajuda` para ver meus comandos**")
            embed.set_footer(text="Betina Brazilian Bot")
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
        if message.content[-1] == '?' and message.content[-2] == '?':
            guild_id = str(message.guild.id)
            author_id = str(message.author.id)
            if guild_id in limitador_log:
                if str(message.channel.id) == limitador_log[guild_id]:
                    resposta = random.choice(['Não respondo a isso', 'Sim',
                                                  'As vezes', 'Não', 'Claro', 'NUNCA!',
                                                  'Um dia talvez', 'A resposta está dentro de você'
                                                     , 'Mais ou menos', 'Uma Bosta', 'Podia ser pior', 'Não sei',
                                              'Não tenho certeza', 'Sua mãe deve saber',
                                              'Pergunta pra sua webnamorada', 'Eu não tenho cara de Yoda',
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
    await member.add_roles(role)
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
    await member.remove_roles(role)
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
    embed.set_footer(text="Betina Brazilian Bot",
                     icon_url=betina_icon)

    embed.add_field(name="😂 **Diversão (11)**", value="``$moeda, $ppt, $rola ...``", inline=False)
    embed.add_field(name="🛠 **Utilidades (13)**", value="``$devemais, $devemenos, $deve...``", inline=False)
    embed.add_field(name="🎵 **Música (8)**", value="``$play, $resume, $stop, $fila...``", inline=False)
    embed.add_field(name="🗣 **Interação (14)**", value="``$bate, $abraça, $treta...``", inline=False)
    embed.add_field(name="👮 **Administração (11)**", value="``$apaga, $ping, $pong...``", inline=False)
    embed.add_field(name="⚙ **Configuração (15)**", value="``$joinlogs, $leavelogs, $autorole...``", inline=False)
    message = await author.send(embed=embed)

    reaction_list = ["😂", "🛠", "🎵", "🗣", "👮", "⚙"]

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
                embed.set_footer(text="Betina Brazilian Bot",
                                 icon_url=betina_icon)
                embed.add_field(name="**$devemais <usuário> <quantidade>**", value="``Você aumentará o quanto um"
                                                                                   " usuário te deve!``", inline=False)
                embed.add_field(name="**$devemenos <usuário> <quantidade>**", value="``Você "
                                                                                    "diminuirá o quanto um usuário te deve!``",
                                inline=False)
                embed.add_field(name="**$deve <usuário>**", value="``Mostrarei uma lista de todas as pessoas que um usuário"
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
                embed.add_field(name="**$geraconvite **", value="``Gerarei um convite para o seu servidor!``", inline=False)
                embed.add_field(name="**$buscacep <cep> **", value="``Darei as informações sobre o cep requisitado!``",
                                inline=False)
                embed.add_field(name="**$geracor **", value="``Gera uma cor aleatória para o discord!``",
                                inline=False)
                msg = await message.edit(embed=embed)

            elif str(reaction.emoji) == "😂":
                embed = discord.Embed(title="Diversão", colour=discord.Colour(0x370c5e),
                                      description="*Bem vindo a categoria diversão:\n"
                                                  "Aqui você encontrará comandos que trará alegria a todos no servidor.*")
                embed.set_thumbnail(
                    url=betina_icon)
                embed.set_footer(text="Betina Brazilian Bot",
                                 icon_url=betina_icon)

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
                embed.add_field(name="**$hungergames <número>**", value="``Iniciarei um jogo de Hunger Games!``",
                                inline=False)
                embed.add_field(name="**$reverse <texto>**", value="``Reverte o texto!``",
                                inline=False)
                msg = await message.edit(embed=embed)

            elif str(reaction.emoji) == "🎵":
                embed = discord.Embed(title="Música", colour=discord.Colour(0x370c5e),
                                      description="*Bem vindo a categoria Música:\nAqui você encontrará"
                                                  " comandos que ajudará você a ouvir música enquanto faz suas atividades"
                                                  " no discord.*")
                embed.set_thumbnail(
                    url=betina_icon)
                embed.set_footer(text="Betina Brazilian Bot",
                                 icon_url=betina_icon)

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
                embed.set_footer(text="Betina Brazilian Bot",
                                 icon_url=betina_icon)

                embed.add_field(name="**$treta **", value="``Direi coisas assustadoras sobre as pessoas do servidor!``",
                                inline=False)
                embed.add_field(name="**$fala <#canal> (opcional) <mensagem> **", value="``Olha, eu sei falar sua mensagem!``",
                                inline=False)
                embed.add_field(name="**$abraça <usuário>**", value="``Abraça o usuário!``",
                                inline=False)
                embed.add_field(name="**$beija <usuário>**", value="``Beija o usuário!``", inline=False)
                embed.add_field(name="**$bate <usuário> **", value="``Bate no usuário!``", inline=False)
                embed.add_field(name="**$dança <usuário> **", value="``Dança com o usuário!``", inline=False)
                embed.add_field(name="**$ataca <usuário> **", value="``Dá um ataque no usuário!``", inline=False)
                embed.add_field(name="**$emputece <usuário> **", value="``Deixa o usuário puto!``", inline=False)
                embed.add_field(name="**$voltapracaverna <usuário> **", value="``Manda o usuário voltar "
                                                                              "pro seu lugar de origem!``", inline=False)
                embed.add_field(name="**$ship <usuário1> <usuário2> (opcional)**", value="``Forma um novo casal!``", inline=False)
                embed.add_field(name="**$tnc **", value="``Manda alguem do servidor tomar no você sabe onde!``",
                                inline=False)
                embed.add_field(name="**$highfive <usuário>**", value="``Bate na mão do usuário!``",
                                inline=False)
                embed.add_field(name="**$roletarussa**", value="``Brincarei de roleta russa com você "
                                                               "e mais 4 pessoas!``", inline=False)
                embed.add_field(name="**$mencionar <Id da mensagem> <texto> (opcional)**", value="``Transformarei a frase"
                                                                                      " do usuário em uma citação"
                                                                                      "!``", inline=False)


                msg = await message.edit(embed=embed)

            elif str(reaction.emoji) == "👮":
                embed = discord.Embed(title="Administração", colour=discord.Colour(0x370c5e),
                                      description="*Bem vindo a categoria Administração:\nAqui você encontrará"
                                                  " comandos que ajudará você a controlar seu servidor.\n"
                                                  "OBS: Você precisará de algumas permissões para utilizar esses comandos!*")
                embed.set_thumbnail(
                    url=betina_icon)
                embed.set_footer(text="Betina Brazilian Bot",
                                 icon_url=betina_icon)
                embed.add_field(name="**$apaga <quantidade>**", value="``Eu apagarei uma"
                                                                      " quantidade de mensagens!``", inline=False)
                embed.add_field(name="**$ping**", value="``Retornarei o ping do usuário``", inline=False)
                embed.add_field(name="**$pong**", value="``oiráusu od gnip o ieranroter``", inline=False)
                embed.add_field(name="**$userinfo <usuário>**", value="``Retornarei informações sobre o usuário!``", inline=False)
                embed.add_field(name="**$serverinfo**", value="``Retornarei informações sobre o servidor!``", inline=False)
                embed.add_field(name="**$afk <motivo> (opcional)**", value="``Definirei o usuário como afk!``", inline=False)
                embed.add_field(name="**$warn <usuário> <motivo> (opcional)**", value="``Darei um Warn no usuário!``", inline=False)
                embed.add_field(name="**$mute <usuário>**", value="``Deixarei o usuário no estado de mute!``", inline=False)
                embed.add_field(name="**$unmute <usuário>**", value="``Tirarei o usuário do estado de mute!``", inline=False)
                embed.add_field(name="**$ban <motivo> (opcional)**", value="``Banirei o usuário do servidor!``", inline=False)
                embed.add_field(name="**$clearlastwarn <usuário>**", value="``Tirarei o ultimo warn do usuário!``", inline=False)

                msg = await message.edit(embed=embed)

            elif str(reaction.emoji) == "⚙":
                embed = discord.Embed(title="Configuração", colour=discord.Colour(0x370c5e),
                                      description="*Bem vindo a categoria Configuração:\nAqui você encontrará"
                                                  " comandos que ajudará você a configurar algumas de minhas funções.\n"
                                                  "OBS: Você precisa da permissão de administrador!*")
                embed.set_thumbnail(
                    url=betina_icon)
                embed.set_footer(text="Betina Brazilian Bot",
                                 icon_url=betina_icon)
                embed.add_field(name="**$config**", value="``Mostra todas as configurações do bot!``", inline=False)
                embed.add_field(name="**$betinainfo**", value="``Mostra todas as informações do bot!``", inline=False)
                embed.add_field(name="**$joinlogs <#canal> <mensagem>**", value="``Definirei um canal para enviar uma mensagem"
                                                                                " toda vez que um usuário"
                                                                                " entrar no servidor``", inline=False)
                embed.add_field(name="**$leavelogs <#canal> <mensagem> **", value="``Definirei um canal para enviar uma mensagem"
                                                                                " toda vez que um usuário"
                                                                                " sair do servidor``", inline=False)
                embed.add_field(name="**$reactionlogsin <#canal> <mensagem> (opcional)**", value="``Definirei um"
                                                                                                 " canal para enviar"
                                                                                                 " uma mensagem"
                                                                                " toda vez que um usuário"
                                                                                " reagir no sistema de auto"
                                                                                                 "role``", inline=False)
                embed.add_field(name="**$reactionlogsout <#canal> <mensagem> (opcional)**", value="``Definirei um canal para"
                                                                                                  " enviar uma mensagem"
                                                                           " toda vez que um usuário"
                                                                           " deixar de reagir no sistema de"
                                                                                                  " autorole``", inline=False)
                embed.add_field(name="**$autorole <@Cargo> <Reação> <Mensagem> (opcional)**", value="``Criarei uma mensagem que"
                                                                                         " ao reagir com a Reação"
                                                                                     " definida adiciona o Cargo"
                                                                                     " definido!``", inline=False)
                embed.add_field(name="**$addtreta <treta>**", value="``Adicionarei uma treta a listra de tretas!``", inline=False)
                embed.add_field(name="**$sugestão <mensagem>**", value="``Adicionarei uma sugestão que você "
                                                                       "requisitar``", inline=False)
                embed.add_field(name="**$cargoinicial <@cargo>**", value="``Adicionarei um cargo inicial a todos"
                                                                         " aqueles que entrarem no servidor!``", inline=False)
                embed.add_field(name="**$prefixo <caracter>**", value="``Definirei um novo prefixo ao bot!``", inline=False)
                embed.add_field(name="**$digitlogs <#Canal>**", value="``Definirei um canal para receber os logs de "
                                                                      "todos os comandos da administração"
                                                                      " utilizados!``", inline=False)
                embed.add_field(name="**$invites <usuário>**", value="``Direi todos os invites criados por"
                                                                     " um usuário!``", inline=False)
                embed.add_field(name="**$botchannel <#Canal>**", value="``Define um canal para poder"
                                                                       " utilizar os meus comandos``", inline=False)
                embed.add_field(name="**$tirabotchannel **", value="``Tira o canal definido para"
                                                                   " poder utilizar os comandos.``", inline=False)
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


@afk.error
async def afk_error(ctx, error):
    if isinstance(error, discord.ext.commands.CommandOnCooldown):
        min, sec = divmod(error.retry_after, 60)
        h, min = divmod(min, 60)
        if min == 0.0 and h == 0:
            await ctx.send('**Espere `{0}` segundos . Para usar o comando afk novamente.**'.format(round(sec)))
        else:
            await ctx.send('**Espere `{0}` horas `{1}` '
                           'minutos  e `{2}` segundos. Para'
                           ' usar o comando afk novamente.**'.format(round(h), round(min), round(sec)))


@commands.cooldown(2, 10, commands.BucketType.guild)
@commands.guild_only()
@client.command(pass_context=True, name='addtreta', aliases=['maistreta', 'adiciona'])
@has_permissions(administrator=True)
async def addtreta(ctx, *, arg: str):
    lista.append(arg)

    embed = discord.Embed(title="Treta adicionada: ", colour=discord.Colour(0x370c5e), description=f"{arg}")
    embed.set_footer(text="Betina Brazilian Bot", icon_url=betina_icon)
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

    elif isinstance(error, discord.ext.commands.CommandOnCooldown):
        min, sec = divmod(error.retry_after, 60)
        h, min = divmod(min, 60)
        if min == 0.0 and h == 0:
            await ctx.send('**Espere `{0}` segundos . Para usar o comando addtreta novamente.**'.format(round(sec)))
        else:
            await ctx.send('**Espere `{0}` horas `{1}` '
                           'minutos  e `{2}` segundos. Para'
                           ' usar o comando addtreta novamente.**'.format(round(h), round(min), round(sec)))


@commands.cooldown(2, 10, commands.BucketType.guild)
@commands.guild_only()
@client.command(name='cargo', aliases=['cargoauto', 'autorole'])
@has_permissions(administrator=True)
async def cargo(ctx, cargo: discord.Role, reaction: str, *, arg: str = 'Clique na reação abaixo para selecionar:'):

    embed = discord.Embed(title="Cargo " + str(cargo), colour=discord.Colour(0x370c5e), description=f"{arg}")
    embed.set_footer(text="Betina Brazilian Bot", icon_url=betina_icon)
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
        embed.set_footer(text="Betina Brazilian Bot",
                             icon_url=betina_icon)
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

    elif isinstance(error, discord.ext.commands.CommandOnCooldown):
        min, sec = divmod(error.retry_after, 60)
        h, min = divmod(min, 60)
        if min == 0.0 and h == 0:
            await ctx.send('**Espere `{0}` segundos . Para usar o comando autorole novamente.**'.format(round(sec)))
        else:
            await ctx.send('**Espere `{0}` horas `{1}` '
                           'minutos  e `{2}` segundos. Para'
                           ' usar o comando autorole novamente.**'.format(round(h), round(min), round(sec)))


@commands.cooldown(2, 10, commands.BucketType.guild)
@commands.guild_only()
@client.command(name='joinlogs', aliases=['defjoinlogs', 'djlogs'])
@has_permissions(administrator=True)
async def join_logs(ctx, channel: discord.TextChannel , *, arg: str):
    guild_id = str(ctx.guild.id)
    channel_id = str(channel.id)

    embed = discord.Embed(title="Canal de logs de entrada definido: " + str(channel), colour=discord.Colour(0x370c5e),
                          description=f"{arg}")
    embed.set_footer(text="Betina Brazilian Bot", icon_url=betina_icon)
    await ctx.send(embed=embed, delete_after=10)
    join_list[guild_id] = (channel_id, arg)
    with open('join.json', 'w') as file:
        json.dump(join_list, file)


@join_logs.error
async def joinlogs_handler(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(title="Comando $joinlogs:define um canal que irá receber as mensagens quando alguem entrar"
                                    " no servidor"
                                              "\n \n**Como usar: $joinlogs <#Canal> <Mensagem>**", colour=discord.Colour(0x370c5e))

        embed.set_author(name="Betina#9182",
                             icon_url=betina_icon)
        embed.set_footer(text="Betina Brazilian Bot",
                             icon_url=betina_icon)
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
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url=betina_icon)
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
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url=betina_icon)
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

    elif isinstance(error, discord.ext.commands.CommandOnCooldown):
        min, sec = divmod(error.retry_after, 60)
        h, min = divmod(min, 60)
        if min == 0.0 and h == 0:
            await ctx.send('**Espere `{0}` segundos . Para usar o comando joinlogs novamente.**'.format(round(sec)))
        else:
            await ctx.send('**Espere `{0}` horas `{1}` '
                           'minutos  e `{2}` segundos. Para'
                           ' usar o comando joinlogs novamente.**'.format(round(h), round(min), round(sec)))


@commands.cooldown(2, 10, commands.BucketType.guild)
@commands.guild_only()
@client.command(name='leavelogs', aliases=['defleavelogs', 'dllogs'])
@has_permissions(administrator=True)
async def leave_logs(ctx, channel: discord.TextChannel, *, arg: str):
    guild_id = str(ctx.guild.id)
    channel_id = str(channel.id)

    embed = discord.Embed(title="Canal de logs de saída definido: " + str(channel), colour=discord.Colour(0x370c5e),
                          description=f"{arg}")
    embed.set_footer(text="Betina Brazilian Bot", icon_url=betina_icon)
    await ctx.send(embed=embed, delete_after=10)
    leave_list[guild_id] = (channel_id, arg)
    with open('leave.json', 'w') as file:
        json.dump(leave_list, file)


@leave_logs.error
async def leave_handler(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(title="Comando $leavelogs:define um canal que irá receber as mensagens quando alguem sair"
                                    " do servidor"
                                              "\n \n**Como usar: $leavelogs <#Canal> <Mensagem>**", colour=discord.Colour(0x370c5e))

        embed.set_author(name="Betina#9182",
                             icon_url=betina_icon)
        embed.set_footer(text="Betina Brazilian Bot",
                             icon_url=betina_icon)
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
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url=betina_icon)
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
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url=betina_icon)
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

    elif isinstance(error, discord.ext.commands.CommandOnCooldown):
        min, sec = divmod(error.retry_after, 60)
        h, min = divmod(min, 60)
        if min == 0.0 and h == 0:
            await ctx.send('**Espere `{0}` segundos . Para usar o comando leavelogs novamente.**'.format(round(sec)))
        else:
            await ctx.send('**Espere `{0}` horas `{1}` '
                           'minutos  e `{2}` segundos. Para'
                           ' usar o comando leavelogs novamente.**'.format(round(h), round(min), round(sec)))


@commands.cooldown(2, 10, commands.BucketType.guild)
@commands.guild_only()
@client.command(name='reactionlogsin', aliases=['defreactionlogsin', 'drlogsin'])
@has_permissions(administrator=True)
async def reaction_logsin(ctx, channel: discord.TextChannel, *, arg: str = 'Acabou de ganhar o cargo de: '):
    guild_id = str(ctx.guild.id)
    channel_id = str(channel.id)

    embed = discord.Embed(title="Canal de logs do sistema de reação automático"
                                " definido: " + str(channel), colour=discord.Colour(0x370c5e))
    embed.set_footer(text="Betina Brazilian Bot", icon_url=betina_icon)
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
        embed.set_footer(text="Betina Brazilian Bot",
                         icon_url=betina_icon)
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
                      "\n \n**Como usar: $reactionlogs <#Canal> <Mensagem> (opcional)**", colour=discord.Colour(0x370c5e))

            embed.set_author(name="Betina#9182",
                             icon_url=betina_icon)
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url=betina_icon)
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

    elif isinstance(error, discord.ext.commands.CommandOnCooldown):
        min, sec = divmod(error.retry_after, 60)
        h, min = divmod(min, 60)
        if min == 0.0 and h == 0:
            await ctx.send('**Espere `{0}` segundos . Para usar o comando reactionlogsin '
                           'novamente.**'.format(round(sec)))
        else:
            await ctx.send('**Espere `{0}` horas `{1}` '
                           'minutos  e `{2}` segundos. Para'
                           ' usar o comando reactionlogsin novamente.**'.format(round(h), round(min), round(sec)))


@commands.cooldown(2, 10, commands.BucketType.guild)
@commands.guild_only()
@client.command(name='reactionlogsout', aliases=['defreactionlogsout', 'drlogsout'])
@has_permissions(administrator=True)
async def reaction_logsout(ctx, channel: discord.TextChannel, *, arg: str = 'Acabou de perder o cargo de: '):

    guild_id = str(ctx.guild.id)
    channel_id = str(channel.id)
    embed = discord.Embed(title="Canal de logs do sistema de reação automático"
                                " definido: " + str(channel), colour=discord.Colour(0x370c5e))
    embed.set_footer(text="Betina Brazilian Bot", icon_url=betina_icon)
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
                  "\n \n**Como usar: $reactionlogsout <#Canal> <Mensagem> (opcional)**", colour=discord.Colour(0x370c5e))

        embed.set_author(name="Betina#9182",
                         icon_url=betina_icon)
        embed.set_footer(text="Betina Brazilian Bot",
                         icon_url=betina_icon)
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
                      "\n \n**Como usar: $reactionlogsout <#Canal> <Mensagem> (opcional)**", colour=discord.Colour(0x370c5e))

            embed.set_author(name="Betina#9182",
                             icon_url=betina_icon)
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url=betina_icon)
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

    elif isinstance(error, discord.ext.commands.CommandOnCooldown):
        min, sec = divmod(error.retry_after, 60)
        h, min = divmod(min, 60)
        if min == 0.0 and h == 0:
            await ctx.send('**Espere `{0}` segundos . Para usar o comando reactionlogsout '
                           'novamente.**'.format(round(sec)))
        else:
            await ctx.send('**Espere `{0}` horas `{1}` '
                           'minutos  e `{2}` segundos. Para'
                           ' usar o comando reactionlogsout novamente.**'.format(round(h), round(min), round(sec)))


@commands.cooldown(2, 10, commands.BucketType.guild)
@commands.guild_only()
@client.command(name='cargoinicial', aliases=['defci', 'dci'])
@has_permissions(administrator=True)
async def cargo_inicial(ctx, role: discord.Role):
    guild_id = str(ctx.guild.id)

    embed = discord.Embed(title="Cargo inicial definido: " + str(role), colour=discord.Colour(0x370c5e))
    embed.set_footer(text="Betina Brazilian Bot", icon_url=betina_icon)
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
        embed.set_footer(text="Betina Brazilian Bot",
                         icon_url=betina_icon)
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
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url=betina_icon)
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

    elif isinstance(error, discord.ext.commands.CommandOnCooldown):
        min, sec = divmod(error.retry_after, 60)
        h, min = divmod(min, 60)
        if min == 0.0 and h == 0:
            await ctx.send('**Espere `{0}` segundos . Para usar o comando cargoinicial '
                           'novamente.**'.format(round(sec)))
        else:
            await ctx.send('**Espere `{0}` horas `{1}` '
                           'minutos  e `{2}` segundos. Para'
                           ' usar o comando cargoinicial novamente.**'.format(round(h), round(min), round(sec)))


@commands.cooldown(2, 10, commands.BucketType.guild)
@commands.guild_only()
@client.command(name='prefixo', aliases=['newprefix', 'novoprefixo'])
@has_permissions(administrator=True)
async def novo_prefixo(ctx, prefix: str):

    guild_id = str(ctx.guild.id)
    embed = discord.Embed(title="Novo prefixo definido: " + prefix, colour=discord.Colour(0x370c5e))
    embed.set_footer(text="Betina Brazilian Bot", icon_url=betina_icon)
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
        embed.set_footer(text="Betina Brazilian Bot",
                         icon_url=betina_icon)
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
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url=betina_icon)
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

    elif isinstance(error, discord.ext.commands.CommandOnCooldown):
        min, sec = divmod(error.retry_after, 60)
        h, min = divmod(min, 60)
        if min == 0.0 and h == 0:
            await ctx.send('**Espere `{0}` segundos . Para usar o comando newprefix '
                           'novamente.**'.format(round(sec)))
        else:
            await ctx.send('**Espere `{0}` horas `{1}` '
                           'minutos  e `{2}` segundos. Para'
                           ' usar o comando newprefix novamente.**'.format(round(h), round(min), round(sec)))


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

    embed = discord.Embed(title="⚙ Configurações do servidor:", colour=discord.Colour(0x370c5e),
                          description="Abaixo estarão listadas todas as configurações do bot!\n\n")
    embed.set_thumbnail(url=ctx.message.guild.icon_url)
    embed.set_author(name=ctx.message.author.name, icon_url=avi)
    embed.set_footer(text="Betina Brazilian Bot", icon_url=betina_icon)
    embed.add_field(name="💬**Prefixo do bot neste servidor**", value=f"O prefixo atual do bot é: " + f'{status6}', inline=False)
    embed.add_field(name="🚪**Join Logs neste servidor:**", value=f"O nome do Canal definido para Join Logs é: " + f'{status5}')
    embed.add_field(name="🚪**Leave Logs neste servidor:**", value=f"O nome do Canal definido para Leave Logs é: " + f'{status4}', inline=False)
    embed.add_field(name="🔗**Auto Role neste servidor:**", value=f'O status do auto role é ' + f'{status}', inline=False)
    embed.add_field(name="🚪**Reaction Logs In neste servidor:**", value=f"O nome do Canal definido para Reaction Logs In é: " + f'{status1}')
    embed.add_field(name="🚪**Reaction Logs Out neste servidor:**", value=f"O nome do Canal definido para Reaction Logs Out é: " + f'{status2}', inline=False)
    embed.add_field(name="🎌 **Cargo Inicial neste servidor:**", value=f"O cargo definido neste servidor é: " + f'{status3}')
    embed.add_field(name="🚪 **Digit Logs neste servidor::**", value=f"O nome do Canal definido para Digit Logs é: " + f'{status7}', inline=False)
    embed.add_field(name="💬 **Bot Channel neste servidor::**",
                    value=f"O Status do bot channel é: " + f'{status8}')
    await ctx.send(embed=embed)


@configuration.error
async def configuration_handler(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(
            title="Comando $config: Diz a configuração do bot nesses servidor!"
                  "\n \n**Como usar: $config**", colour=discord.Colour(0x370c5e))

        embed.set_author(name="Betina#9182",
                         icon_url=betina_icon)
        embed.set_footer(text="Betina Brazilian Bot",
                         icon_url=betina_icon)
        embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                        "ter a permissão de* ``"
                                                        "Administrador`` *para utilizar este comando!*",
                        inline=False)
        embed.add_field(name="📖**Exemplos:**", value="$config", inline=False)
        embed.add_field(name="🔀**Outros Comandos**", value="``$configuration, $definições.``", inline=False)

        msg = await ctx.send(embed=embed)
        await msg.add_reaction("❓")

    elif isinstance(error, discord.ext.commands.CommandOnCooldown):
        min, sec = divmod(error.retry_after, 60)
        h, min = divmod(min, 60)
        if min == 0.0 and h == 0:
            await ctx.send('**Espere `{0}` segundos . Para usar o comando config '
                           'novamente.**'.format(round(sec)))
        else:
            await ctx.send('**Espere `{0}` horas `{1}` '
                           'minutos  e `{2}` segundos. Para'
                           ' usar o comando config novamente.**'.format(round(h), round(min), round(sec)))


@commands.cooldown(2, 10, commands.BucketType.guild)
@commands.guild_only()
@client.command(name='digitlogs', aliases=['defdigitlogs', 'ddlogs'])
@has_permissions(administrator=True)
async def digilog(ctx, channel: discord.TextChannel):

    guild_id = str(ctx.guild.id)
    channel_id = str(channel.id)
    embed = discord.Embed(title="Canal de logs do sistema"
                                " definido: " + str(channel), colour=discord.Colour(0x370c5e))
    embed.set_footer(text="Betina Brazilian Bot", icon_url=betina_icon)
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
        embed.set_footer(text="Betina Brazilian Bot",
                         icon_url=betina_icon)
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
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url=betina_icon)
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

    elif isinstance(error, discord.ext.commands.CommandOnCooldown):
        min, sec = divmod(error.retry_after, 60)
        h, min = divmod(min, 60)
        if min == 0.0 and h == 0:
            await ctx.send('**Espere `{0}` segundos . Para usar o comando digitlogs '
                           'novamente.**'.format(round(sec)))
        else:
            await ctx.send('**Espere `{0}` horas `{1}` '
                           'minutos  e `{2}` segundos. Para'
                           ' usar o comando digitlogs novamente.**'.format(round(h), round(min), round(sec)))


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
            embed.set_footer(text=f'Requisitado por: {ctx.message.author.display_name}',
                                 icon_url=f'{ctx.message.author.avatar_url}')
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
        embed.set_footer(text="Betina Brazilian Bot",
                         icon_url=betina_icon)
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
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url=betina_icon)
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

    elif isinstance(error, discord.ext.commands.CommandOnCooldown):
        min, sec = divmod(error.retry_after, 60)
        h, min = divmod(min, 60)
        if min == 0.0 and h == 0:
            await ctx.send('**Espere `{0}` segundos . Para usar o comando invites '
                           'novamente.**'.format(round(sec)))
        else:
            await ctx.send('**Espere `{0}` horas `{1}` '
                           'minutos  e `{2}` segundos. Para'
                           ' usar o comando invites novamente.**'.format(round(h), round(min), round(sec)))


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
    embed.set_footer(text="Betina Brazilian Bot", icon_url=betina_icon)
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
        embed.set_footer(text="Betina Brazilian Bot",
                         icon_url=betina_icon)
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
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url=betina_icon)
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

    elif isinstance(error, discord.ext.commands.CommandOnCooldown):
        min, sec = divmod(error.retry_after, 60)
        h, min = divmod(min, 60)
        if min == 0.0 and h == 0:
            await ctx.send('**Espere `{0}` segundos . Para usar o comando botchannel '
                           'novamente.**'.format(round(sec)))
        else:
            await ctx.send('**Espere `{0}` horas `{1}` '
                           'minutos  e `{2}` segundos. Para'
                           ' usar o comando botchannel novamente.**'.format(round(h), round(min), round(sec)))


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
        embed.set_footer(text="Betina Brazilian Bot", icon_url=betina_icon)
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
        embed.set_footer(text="Betina Brazilian Bot",
                         icon_url=betina_icon)
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

    elif isinstance(error, discord.ext.commands.CommandOnCooldown):
        min, sec = divmod(error.retry_after, 60)
        h, min = divmod(min, 60)
        if min == 0.0 and h == 0:
            await ctx.send('**Espere `{0}` segundos . Para usar o comando tirabotchannel '
                           'novamente.**'.format(round(sec)))
        else:
            await ctx.send('**Espere `{0}` horas `{1}` '
                           'minutos  e `{2}` segundos. Para'
                           ' usar o comando tirabotchannel novamente.**'.format(round(h), round(min), round(sec)))


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
                commandos2 = '71'
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
                embed.set_footer(text="Betina Brazilian Bot")
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
            commandos2 = '71'
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
            embed.set_footer(text="Betina Brazilian Bot")
        await ctx.send(embed=embed)


@betinainfo.error
async def betina_info_error(ctx, error):
    if isinstance(error, discord.ext.commands.CommandOnCooldown):
        min, sec = divmod(error.retry_after, 60)
        h, min = divmod(min, 60)
        if min == 0.0 and h == 0:
            await ctx.send('**Espere `{0}` segundos . Para usar o comando betinainfo novamente.**'.format(round(sec)))
        else:
            await ctx.send('**Espere `{0}` horas `{1}` '
                           'minutos  e `{2}` segundos. Para'
                           ' usar o comando betinainfo novamente.**'.format(round(h), round(min), round(sec)))


if __name__ == '__main__':
    for extension in startup_extensions:
        try:
            client.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Falha ao carregar a extensão {}\n{}'.format(extension, exc))

client.run(TOKEN)
