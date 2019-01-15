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

from discord.ext import commands
from forex_python.converter import CurrencyRates
from discord.utils import get
from dhooks import Webhook

startup_extensions = ['Music']
prefix = '$'
client = commands.Bot(command_prefix=prefix)
TOKEN = 'Insira seu token aqui!'
GIPHY_TOKEN = 'Insira seu token do Giphy'

client.remove_command('help')
# Musica
players = {}

# devemais e devemenos
devedores = {}
devidos = {}

# tretas
lista = ['[nome] é um bosta! ', '[nome] acha que é gente', '[nome] se acha viado mas na verdade ta certo',
         '[nome] é horrível', '[nome] se acha foda mas perde em qualquer jogo', '[nome] parece que tem 5 anos de idade',
         '[nome] diz que bebe mas é fraco', 'Todo mundo aqui é burro menos eu',
         'Tucker transformou sua filha em um cachorro', '[nome] stalker pra caralho',
         '[nome] não pega ninguem nem na propria casa', 'Eu vou dominar o mundo e to nem aí',
         'Eu sou o grande sabio [nome] e eu vou atirar minha merda em você',
         'Obrigado [nome]! Mas a nossa princesa está em outro castelo!', '[nome] diz que sabe algo mas não sabe nada!',
         '[nome] diz que não tem medo de morrer mas não quer estar lá na hora que isso acontecer!',
         '[nome] se diz bom em cozinhar, mas não sabe cozinhar um ovo!',
         '[nome] é tão azarado que, se quisesse achar uma agulha no palheiro, era só sentar nele',
         '[nome] é tão bonito que quando foi se olhar no espelho ficou apaixonado',
         '[nome] fala tanta merda que quando foi cagar conversou pela bunda!',
         '[nome] aqui nao é a pedovan e não ta dando doce, o que veio fazer aqui ?',
         'Se eu ganhasse um centavo a cada pessoa feia que me aparecesse, só com você, [nome], eu seria bilionaria',
         '[nome] é tão bosta que cheira a merda']

# gifs
angry = [] #links do site giphy
cave = [] #links do site giphy
slap = [] #links do site giphy
dance = [] #links do site giphy
hug = [] #links do site giphy
kiss = [] #links do site giphy
attack = [] #links do site giphy
omg = [] #links do site giphy


@client.event
async def on_ready():
    print('--------------BD--------------')
    print('BOT ONLINE')
    print('Nome do Bot: ' + client.user.name)
    print('ID do Bot: ' + str(client.user.id))
    print('Versao do Discord: ' + discord.__version__)
    print('--------------BD--------------')
    game = discord.Game("$help")
    await client.change_presence(status=discord.Status.idle, activity=game)


@client.event
async def on_guild_join(guild):
        for membro in guild.members:
            if membro.guild_permissions.administrator and membro != client.user:

                embed = discord.Embed(title="Bem vindo ao Suporte da Betina", colour=discord.Colour(0x370c5e),
                                      description="Olá, eu sou a betina: \n esse suporte está aqui para te ajudar e ajudar ao meu criador ```\nSim, eu não vou roubar seus dados...```",
                                      timestamp=datetime.datetime.utcfromtimestamp(1547228918))
                embed.set_image(
                    url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
                embed.set_thumbnail(
                    url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
                embed.set_author(name="Betina")
                embed.set_footer(text="footer text",
                                 icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")

                embed.add_field(name="Precisa de ajuda?🤔", value="para usar meus comandos utilize o $help")
                embed.add_field(name="Teve alguma ideia boa ? 😱: ",
                                value="fale com o meu criador, ele poderá implementar!")
                embed.add_field(name="Teve algum problema com o bot ?🙄",
                                value="não se preocupe, alguns problemas são comuns considerando o fato do bot estar em construção, mas, de qualquer forma,  fale com o meu criador.")
                embed.add_field(name="Criador do bot:", value="DantasB#7096", inline=True)
                embed.add_field(name="Maiores informações:", value="github.com/DantasB", inline=True)

                await membro.send(embed=embed)

        
@client.event
async def on_member_join(member):
    """Envia uma mensagem quando o membro entra no servidor"""
    guild = member.guild.get_channel('id do canal que você quer dar boas vindas')
    fmt = 'Bem vindo ao servidor {1.name}, {0.mention}, aproveita e segue o baile.'
    await guild.send(fmt.format(member, member.guild))
    role = discord.utils.get(member.guild.roles, name='Nome do cargo')
    await member.add_roles(role) #sempre que alguem entrar no servidor receberá esse cargo.


@client.event
async def on_member_remove(member):
    """Envia uma mensagem quando o membro sai do servidor"""
    guild = member.guild.get_channel('id do canal que você quer dar boas vindas')
    fmt = '{0.mention} ficou bolado e saiu do servidor'
    await guild.send(fmt.format(member))


@client.event
async def on_message(message):
    print('Logs:\n', message.author, message.content)
    'if message.author.id != client.user.id:\n        await client.send_message(message.channel, message.content)'
    if message.content.lower().startswith('$treta'):
        i = random.randrange(len(lista))
        listas = lista[i]
        x = random.randrange(len(message.guild.members))
        user = list(message.guild.members)[x]
        fquote = listas.replace('[nome]', user.name)
        await message.channel.send(fquote, tts=True)
    await client.process_commands(message)


@commands.guild_only()
@client.command(name='bate', aliases=['hit', 'punch'])
async def bate(ctx, member: discord.Member):
    """<membro>: Tome cuidado com isso."""
    gif = random.choice(slap)

    bate1 = '**Não acredito que você foi capaz de tentar dar um tapa em alguem como eu !**. \n\n{} deu um ' \
            'soco em {}'.format(client.user.mention, ctx.author.mention)
    bate2 = '{} **deu um soco em** {}'.format(ctx.author.mention, member.mention)

    if member.mention == client.user.mention:
        embed = discord.Embed(title="**Tapão!**", colour=discord.Colour(0x370c5e), description="{}".format(bate1))

        embed.set_image(url="{}".format(gif))
        embed.set_footer(text="Betina Brazilian Bot",
                         icon_url="https://images.discordapp.net/avatars/"
                                  "527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('😭')

    else:
        embed = discord.Embed(title="**Tapão!**", colour=discord.Colour(0x370c5e), description="{}".format(bate2))

        embed.set_image(url="{}".format(gif))
        embed.set_footer(text="Betina Brazilian Bot",
                         icon_url="https://images.discordapp.net/avatars/"
                                  "527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
        msg = await ctx.send(embed=embed)
    await msg.add_reaction('😯')


@bate.error
async def bate_handler(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        if error.param.name == 'member':
            embed = discord.Embed(title="Comando $bate:", colour=discord.Colour(0x370c5e),
                                  description="Bate no usuário\n \n**Como usar: $bate <usuário>**",
                                  timestamp=datetime.datetime.utcfromtimestamp(1547337793))

            embed.set_author(name="Betina#9182",
                             icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")

            embed.add_field(name="📖**Exemplos:**", value="$bate @fulano\n$bate @sicrano", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$hit, $punch.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")


@commands.guild_only()
@client.command(name='abraça', aliases=['hug', 'abraço'])
async def abraça(ctx, member: discord.Member):
    """<membro>: Use isso com amor <3."""
    gif = random.choice(hug)

    abraça1 = '**Fico lisonjeada ao receber um abraço seu, {}**'.format(ctx.author.mention)
    abraça2 = '{} **deu um abraço em** {}'.format(ctx.author.mention, member.mention)

    if member.mention == client.user.mention:
        embed = discord.Embed(title="**Abraço!**", colour=discord.Colour(0x370c5e), description="{}".format(abraça1))

        embed.set_image(url="{}".format(gif))
        embed.set_footer(text="Betina Brazilian Bot",
                         icon_url="https://images.discordapp.net/avatars/"
                                  "527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
        msg = await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="**Abraço!**", colour=discord.Colour(0x370c5e), description="{}".format(abraça2))

        embed.set_image(url="{}".format(gif))
        embed.set_footer(text="Betina Brazilian Bot",
                         icon_url="https://images.discordapp.net/avatars/"
                                  "527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
        msg = await ctx.send(embed=embed)
    await msg.add_reaction('🤗')


@abraça.error
async def abraça_handler(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        if error.param.name == 'member':
            embed = discord.Embed(title="Comando $abraça:", colour=discord.Colour(0x370c5e),
                                  description="Abraça o usuário\n \n**Como usar: $abraça <usuário>**",
                                  timestamp=datetime.datetime.utcfromtimestamp(1547337793))

            embed.set_author(name="Betina#9182",
                             icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")

            embed.add_field(name="📖**Exemplos:**", value="$abraça @fulano\n$abraça @sicrano", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$hug, $abraço.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")


@commands.guild_only()
@client.command(name='beija', aliases=['kiss', 'beijou'])
async def beija(ctx, member: discord.Member):
    """<membro>: Use isso com amor <3."""
    gif1 = random.choice(slap)
    gif2 = random.choice(kiss)

    beija1 = '**Como você pôde fazer isso ? Eu tenho namorado!!!**'.format(ctx.author.mention)
    beija2 = '{} **deu um beijo em** {}'.format(ctx.author.mention, member.mention)

    if member.mention == client.user.mention:
        embed = discord.Embed(title="**Tapão!**", colour=discord.Colour(0x370c5e), description="{}".format(beija1))

        embed.set_image(url="{}".format(gif1))
        embed.set_footer(text="Betina Brazilian Bot",
                         icon_url="https://images.discordapp.net/avatars/"
                                  "527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('😡')
    else:
        embed = discord.Embed(title="**Beijo!**", colour=discord.Colour(0x370c5e), description="{}".format(beija2))

        embed.set_image(url="{}".format(gif2))
        embed.set_footer(text="Betina Brazilian Bot",
                         icon_url="https://images.discordapp.net/avatars/"
                                  "527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('💋')


@beija.error
async def beija_handler(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        if error.param.name == 'member':
            embed = discord.Embed(title="Comando $beija:", colour=discord.Colour(0x370c5e),
                                  description="Beija o usuário\n \n**Como usar: $beija <usuário>**",
                                  timestamp=datetime.datetime.utcfromtimestamp(1547337793))

            embed.set_author(name="Betina#9182",
                             icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")

            embed.add_field(name="📖**Exemplos:**", value="$beija @fulano\n$beija @sicrano", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$kiss, $beijou.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")


@client.command()
async def tnc(ctx):
    gif1 = random.choice(angry)
    gif2 = random.choice(omg)

    tnc1 = '{} mandou {} tomar no cuelinho!'.format(ctx.author.mention, person.mention)
    tnc2 = '**Você é louco em fazer isso comigo ???**'.format(ctx.author.mention)

    person = random.choice(list(ctx.guild.members))
    if person.mention == client.user.mention:
        await ctx.send(tnc1)
        embed = discord.Embed(title="**Raiva!**", colour=discord.Colour(0x370c5e), description="{}".format(tnc2))
        embed.set_image(url="{}".format(gif1))
        embed.set_footer(text="Betina Brazilian Bot",
                         icon_url="https://images.discordapp.net/avatars/"
                                  "527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('😡')
    else:
        embed = discord.Embed(title="**Raiva!**", colour=discord.Colour(0x370c5e), description="{}".format(tnc1))
        embed.set_image(url="{}".format(gif2))
        embed.set_footer(text="Betina Brazilian Bot",
                         icon_url="https://images.discordapp.net/avatars/"
                                  "527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('😮')


@commands.guild_only()
@client.command(name='voltapracaverna', aliases=['caverna', 'goback'])
async def voltapracaverna(ctx, member: discord.Member):
    """<membro>: Use isso com amor <3."""
    gif = random.choice(cave)

    cave1 = '**Como você pode fazer isso,** {} **? Volta pra caverna você!**' \
            '\n\n{} mandou {} de volta pra caverna'.format(ctx.author.mention, member.mention, ctx.author.mention)
    cave2 = '{} **mandou** {} **de volta pra caverna**'.format(ctx.author.mention, member.mention)

    if member.mention == client.user.mention:
        embed = discord.Embed(title="**Volta pra caverna você!**", colour=discord.Colour(0x370c5e),
                              description="{}".format(cave1))
        embed.set_image(url="{}".format(gif))
        embed.set_footer(text="Betina Brazilian Bot",
                         icon_url="https://images.discordapp.net/avatars/"
                                  "527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('😡')
    else:
        embed = discord.Embed(title="**Volta pra Caverna!**", colour=discord.Colour(0x370c5e),
                              description="{}".format(cave2))
        embed.set_image(url="{}".format(gif))
        embed.set_footer(text="Betina Brazilian Bot",
                         icon_url="https://images.discordapp.net/avatars/"
                                  "527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('😮')


@voltapracaverna.error
async def voltapracaverna_handler(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        if error.param.name == 'member':
            embed = discord.Embed(title="Comando $voltapracaverna:", colour=discord.Colour(0x370c5e),
                                  description="Manda o usuário de volta pra caverna\n \n**Como usar: $volta pra caverna"
                                              " <usuário>**",
                                  timestamp=datetime.datetime.utcfromtimestamp(1547337793))

            embed.set_author(name="Betina#9182",
                             icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")

            embed.add_field(name="📖**Exemplos:**", value="$voltapracaverna @fulano\n$voltapracaverna"
                                                          " @sicrano", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$caverna, $goback.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")


@commands.guild_only()
@client.command(name='dança', aliases=['dance', 'dançar'])
async def dança(ctx, member: discord.Member):
    """<membro>: Use isso com amor <3."""
    gif = random.choice(dance)

    dança1 = '**Fico lisonjeada ao receber um pedido de dança seu seu, {}**'.format(ctx.author.mention)
    dança2 = '{} **começou a dançar com** {}'.format(ctx.author.mention, member.mention)

    if member.mention == client.user.mention:
        embed = discord.Embed(title="**Raiva!**", colour=discord.Colour(0x370c5e), description="{}".format(dança1))
        embed.set_image(url="{}".format(gif))
        embed.set_footer(text="Betina Brazilian Bot",
                         icon_url="https://images.discordapp.net/avatars/"
                                  "527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
        msg = await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="**Raiva!**", colour=discord.Colour(0x370c5e), description="{}".format(dança2))
        embed.set_image(url="{}".format(gif))
        embed.set_footer(text="Betina Brazilian Bot",
                         icon_url="https://images.discordapp.net/avatars/"
                                  "527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
        msg = await ctx.send(embed=embed)
    await msg.add_reaction('💃')


@dança.error
async def dança_handler(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        if error.param.name == 'member':
            embed = discord.Embed(title="Comando $dança:", colour=discord.Colour(0x370c5e),
                                  description="Dança com o usuário\n \n**Como usar: $dança <usuário>**",
                                  timestamp=datetime.datetime.utcfromtimestamp(1547337793))

            embed.set_author(name="Betina#9182",
                             icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")

            embed.add_field(name="📖**Exemplos:**", value="$dança @fulano\n$dança @sicrano", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$dance, $dançar.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")


@commands.guild_only()
@client.command(name='ataca', aliases=['attack', 'atacar'])
async def ataca(ctx, member: discord.Member):
    """<membro>: Cuidado com isso!"""
    gif = random.choice(attack)

    ataca1 = '**Como você ousa tentar fazer isso comigo?** ' \
             '\n\n {} deu um ataque em {}'.format(member.mention, ctx.author.mention)
    ataca2 = '{} **deu um ataque em** {}'.format(ctx.author.mention, member.mention)

    if member.mention == client.user.mention:
        embed = discord.Embed(title="**Raiva!**", colour=discord.Colour(0x370c5e), description="{}".format(ataca1))
        embed.set_image(url="{}".format(gif))
        embed.set_footer(text="Betina Brazilian Bot",
                         icon_url="https://images.discordapp.net/avatars/"
                                  "527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('😡')
        await msg.add_reaction('🥊')
    else:
        embed = discord.Embed(title="**Ataque!**", colour=discord.Colour(0x370c5e), description="{}".format(ataca2))
        embed.set_image(url="{}".format(gif))
        embed.set_footer(text="Betina Brazilian Bot",
                         icon_url="https://images.discordapp.net/avatars/"
                                  "527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('😮')
        await msg.add_reaction('🥊')


@ataca.error
async def ataca_handler(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        if error.param.name == 'member':
            embed = discord.Embed(title="Comando $ataca:", colour=discord.Colour(0x370c5e),
                                  description="ataca o usuário\n \n**Como usar: $ataca <usuário>**",
                                  timestamp=datetime.datetime.utcfromtimestamp(1547337793))

            embed.set_author(name="Betina#9182",
                             icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")

            embed.add_field(name="📖**Exemplos:**", value="$ataca @fulano\n$ataca @sicrano", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$attack, $atacar.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")


@commands.guild_only()
@client.command(name='apaga', aliases=['delete', 'clean'])
async def apaga(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)


@apaga.error
async def apaga_handler(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        if error.param.name == 'amount':
            embed = discord.Embed(title="Comando $apaga:", colour=discord.Colour(0x370c5e),
                                  description="Apaga n+1 linhas acima da ultima mensagem\n \n**Como usar: $apaga <linhas>**",
                                  timestamp=datetime.datetime.utcfromtimestamp(1547337793))

            embed.set_author(name="Betina#9182",
                             icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")

            embed.add_field(name="📖**Exemplos:**", value="$apaga 100\n$apaga 10", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$delete, $clean.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")
    
@commands.guild_only()
@client.command(name='ppt', aliases=['Rsp', 'jogo'])
async def ppt(ctx, msg: str):
    t = ['pedra', 'papel', 'tesoura']
    channel = ctx.channel
    computer = t[random.randint(0, 2)]
    player = msg.lower()
    await ctx.send('``Você escolheu {}{}``'.format(player[:1].upper(), player[1:]))
    await channel.trigger_typing()
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
async def ppt_handler(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        if error.param.name == 'msg':
            embed = discord.Embed(title="Comando $ppt:", colour=discord.Colour(0x370c5e),
                                  description="Inicia um jogo de Pedra, Papel ou tesoura com o bot\n \n**Como usar"
                                              ": $ppt <Pedra, Papel ou Tesoura>**",
                                  timestamp=datetime.datetime.utcfromtimestamp(1547337793))

            embed.set_author(name="Betina#9182",
                             icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")

            embed.add_field(name="📖**Exemplos:**", value="$ppt pedra\n$ppt tesoura", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$Rsp, $jogo.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")


@commands.guild_only()
@client.command(name='devemais', aliases=['ntp', 'medeve', 'pay'])
async def devemais(ctx, member: discord.Member, a: float):
    """Adiciona o credito"""
    if member.mention != client.user.mention:
        if (member in devedores) and (ctx.author in devidos):
            devidos[ctx.author] += a
        else:
            devidos[ctx.author] = a
            devedores[member] = devidos
        await ctx.send('**{} deve R$ {} ao {}**'.format(member.mention, devidos[ctx.author], ctx.author.mention))
    else:
        msg = await ctx.send('**Eu sou uma bot e não uma prostituta!! Eu não devo nada a ninguem!**')
        await msg.add_reaction('😡')


@devemais.error
async def devemais_handler(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        if error.param.name == 'member':
            embed = discord.Embed(title="Comando $devemais:", colour=discord.Colour(0x370c5e),
                                  description="Você adiciona uma quantidade ao quanto um usuário te deve\n \n**Como"
                                              " usar: $devemais <usuário> <valor>**",
                                  timestamp=datetime.datetime.utcfromtimestamp(1547337793))

            embed.set_author(name="Betina#9182",
                             icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")

            embed.add_field(name="📖**Exemplos:**", value="$devemais @sicrano 500\n$devemais @fulano 10", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$ntp, $medeve.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")

        elif error.param.name == 'a':
            embed = discord.Embed(title="Comando $devemais:", colour=discord.Colour(0x370c5e),
                                  description="Você adiciona uma quantidade ao quanto um usuário te deve\n \n**Como"
                                              " usar: $devemais <usuário> <valor>**",
                                  timestamp=datetime.datetime.utcfromtimestamp(1547337793))

            embed.set_author(name="Betina#9182",
                             icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")

            embed.add_field(name="📖**Exemplos:**", value="$devemais @sicrano 500\n$devemais @fulano 10", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$ntp, $medeve.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")


@commands.guild_only()
@client.command(name='devemenos', aliases=['dntp', 'naomedeve'])
async def devemenos(ctx, member: discord.Member, a: float):
    """Diminui o credito"""
    if member.mention != client.user.mention:
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
                await ctx.send('**Agora {} deve R$ {} ao {}**'.format(ctx.author.mention, devidos[member], member.mention))
            elif devidos[ctx.author] == 0:
                await ctx.send('**{} não deve nada a {}**'.format(ctx.author.mention, member.mention))
            else:
                await ctx.send('**{} deve R$ {} ao {}**'.format(member.mention, devidos[ctx.author], ctx.author.mention))
        else:
            devedores[ctx.author] = devidos
            devidos[member] = a
            await ctx.send('**{} deve R$ {} ao {}**'.format(ctx.author.mention, devidos[member], member.mention))
    else:
        msg = await ctx.send('**Eu sou uma bot, não uma prostituta!!! Como você pode ficar me devendo algo ???**')
        await msg.add_reaction("🤔")


@devemenos.error
async def devemenos_handler(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        if error.param.name == 'member':
            embed = discord.Embed(title="Comando $devemenos:", colour=discord.Colour(0x370c5e),
                                  description="Você diminui uma quantidade ao quanto um usuário te deve\n \n**Como"
                                              " usar: $devemenos <usuário> <valor>**",
                                  timestamp=datetime.datetime.utcfromtimestamp(1547337793))

            embed.set_author(name="Betina#9182",
                             icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")

            embed.add_field(name="📖**Exemplos:**", value="$devemenos @sicrano 500\n$devemenos @fulano 10",
                            inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$dntp, $naomedeve.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")

        elif error.param.name == 'a':
            embed = discord.Embed(title="Comando $devemenos:", colour=discord.Colour(0x370c5e),
                                  description="Você diminui uma quantidade ao quanto um usuário te deve\n \n**Como"
                                              " usar: $devemenos <usuário> <valor>**",
                                  timestamp=datetime.datetime.utcfromtimestamp(1547337793))

            embed.set_author(name="Betina#9182",
                             icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")

            embed.add_field(name="📖**Exemplos:**", value="$devemenos @sicrano 500\n$devemenos @fulano 10",
                            inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$dntp, $naomedeve.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")


@commands.guild_only()
@client.command(name='deve', aliases=['rsp', 'owe'])
async def deve(ctx, member: discord.Member):
    if member.mention != client.user.mention:
        if not (member in devedores):
            msg = await ctx.send('**{} não deve nada a ninguem!**'.format(member.mention))
            await msg.add_reaction('😯')
        else:
            await ctx.send('**{} deve a tais pessoas: **'.format(member.mention))
            for membros in devedores[member]:
                if membros.id != member.id:
                    await ctx.send('**Deve R$ {} ao {}**'.format(devidos[membros], membros.mention))
    else:
        msg = await ctx.send('**Eu sou uma Bot! Nunca deverei nada a ninguem!**')
        await msg.add_reaction('🤷')


@deve.error
async def deve_handler(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        if error.param.name == 'member':
            embed = discord.Embed(title="Comando $deve:", colour=discord.Colour(0x370c5e),
                                  description="Diz o quanto o usuário deve a cada pessoa do servidor\n \n**Como usar"
                                              ": $deve <usuário>**",
                                  timestamp=datetime.datetime.utcfromtimestamp(1547337793))

            embed.set_author(name="Betina#9182",
                             icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")

            embed.add_field(name="📖**Exemplos:**", value="$deve @sicrano\n$deve @fulano", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$rsp, $owe.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")


@commands.guild_only()
@client.command(name='conversor', aliases=['converter', 'converte'])
async def conversor(ctx, moeda1, moeda2, quantidade=None):
    """Vê o valor da moeda 1 em moeda 2"""
    try:
        channel = ctx.channel
        await channel.trigger_typing()
        c = CurrencyRates()
        msg = c.get_rate(f'''{moeda1.upper()}''', f'''{moeda2.upper()}''')
        if quantidade is None:
            await ctx.send(
                'Esse é o valor da cotacao atual do ``{}`` em ``{}``: **{}**'.format(moeda1.upper(), moeda2.upper(),
                                                                                     msg))
        else:
            msg = msg * quantidade
            await ctx.send(
                'Esse é o valor de {} ``{}`` em ``{}``: **{}**'.format(quantidade, moeda1.upper(), moeda2.upper(), msg))
    except:
        msg = await ctx.send('Tente utilizar o codigo de uma moeda existente. **Por exemplo: $conversor usd brl**')
        await msg.add_reaction('❤')


@conversor.error
async def conversor_handler(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        if error.param.name == 'moeda1':
            embed = discord.Embed(title="Comando $conversor:", colour=discord.Colour(0x370c5e),
                                  description="Você converte a moeda1 em termos de moeda2\n \n**Como"
                                              " usar: $converte <moeda1> <moeda2>**",
                                  timestamp=datetime.datetime.utcfromtimestamp(1547337793))

            embed.set_author(name="Betina#9182",
                             icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")

            embed.add_field(name="📖**Exemplos:**", value="$converte usd brl\n$converte eur pln", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$converter, $converte.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")

        elif error.param.name == 'moeda2':
            embed = discord.Embed(title="Comando $conversor:", colour=discord.Colour(0x370c5e),
                                  description="Você converte a moeda1 em termos de moeda2\n \n**Como"
                                              " usar: $converte <moeda1> <moeda2>**",
                                  timestamp=datetime.datetime.utcfromtimestamp(1547337793))

            embed.set_author(name="Betina#9182",
                             icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")

            embed.add_field(name="📖**Exemplos:**", value="$converte usd brl\n$converte eur pln", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$converter, $converte.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")

@commands.guild_only()
@client.command(name='ppt', aliases=['Rsp', 'jogo'])
async def ppt(ctx, msg: str):
    t = ['pedra', 'papel', 'tesoura']
    channel = ctx.channel
    computer = t[random.randint(0, 2)]
    player = msg.lower()
    await ctx.send('``Você escolheu {}{}``'.format(player[:1].upper(), player[1:]))
    await channel.trigger_typing()
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
async def ppt_handler(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        if error.param.name == 'msg':
            embed = discord.Embed(title="Comando $ppt:", colour=discord.Colour(0x370c5e),
                                  description="Inicia um jogo de Pedra, Papel ou tesoura com o bot\n \n**Como usar"
                                              ": $ppt <Pedra, Papel ou Tesoura>**",
                                  timestamp=datetime.datetime.utcfromtimestamp(1547337793))

            embed.set_author(name="Betina#9182",
                             icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")

            embed.add_field(name="📖**Exemplos:**", value="$ppt pedra\n$ppt tesoura", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$Rsp, $jogo.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")


@commands.guild_only()
@client.command(name='devemais', aliases=['ntp', 'medeve', 'pay'])
async def devemais(ctx, member: discord.Member, a: float):
    """Adiciona o credito"""
    if member.mention != client.user.mention:
        if (member in devedores) and (ctx.author in devidos):
            devidos[ctx.author] += a
        else:
            devidos[ctx.author] = a
            devedores[member] = devidos
        await ctx.send('**{} deve R$ {} ao {}**'.format(member.mention, devidos[ctx.author], ctx.author.mention))
    else:
        msg = await ctx.send('**Eu sou uma bot e não uma prostituta!! Eu não devo nada a ninguem!**')
        await msg.add_reaction('😡')


@devemais.error
async def devemais_handler(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        if error.param.name == 'member':
            embed = discord.Embed(title="Comando $devemais:", colour=discord.Colour(0x370c5e),
                                  description="Você adiciona uma quantidade ao quanto um usuário te deve\n \n**Como"
                                              " usar: $devemais <usuário> <valor>**",
                                  timestamp=datetime.datetime.utcfromtimestamp(1547337793))

            embed.set_author(name="Betina#9182",
                             icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")

            embed.add_field(name="📖**Exemplos:**", value="$devemais @sicrano 500\n$devemais @fulano 10", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$ntp, $medeve.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")

        elif error.param.name == 'a':
            embed = discord.Embed(title="Comando $devemais:", colour=discord.Colour(0x370c5e),
                                  description="Você adiciona uma quantidade ao quanto um usuário te deve\n \n**Como"
                                              " usar: $devemais <usuário> <valor>**",
                                  timestamp=datetime.datetime.utcfromtimestamp(1547337793))

            embed.set_author(name="Betina#9182",
                             icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")

            embed.add_field(name="📖**Exemplos:**", value="$devemais @sicrano 500\n$devemais @fulano 10", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$ntp, $medeve.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")


@commands.guild_only()
@client.command(name='devemenos', aliases=['dntp', 'naomedeve'])
async def devemenos(ctx, member: discord.Member, a: float):
    """Diminui o credito"""
    if member.mention != client.user.mention:
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
                await ctx.send('**Agora {} deve R$ {} ao {}**'.format(ctx.author.mention, devidos[member], member.mention))
            elif devidos[ctx.author] == 0:
                await ctx.send('**{} não deve nada a {}**'.format(ctx.author.mention, member.mention))
            else:
                await ctx.send('**{} deve R$ {} ao {}**'.format(member.mention, devidos[ctx.author], ctx.author.mention))
        else:
            devedores[ctx.author] = devidos
            devidos[member] = a
            await ctx.send('**{} deve R$ {} ao {}**'.format(ctx.author.mention, devidos[member], member.mention))
    else:
        msg = await ctx.send('**Eu sou uma bot, não uma prostituta!!! Como você pode ficar me devendo algo ???**')
        await msg.add_reaction("🤔")


@devemenos.error
async def devemenos_handler(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        if error.param.name == 'member':
            embed = discord.Embed(title="Comando $devemenos:", colour=discord.Colour(0x370c5e),
                                  description="Você diminui uma quantidade ao quanto um usuário te deve\n \n**Como"
                                              " usar: $devemenos <usuário> <valor>**",
                                  timestamp=datetime.datetime.utcfromtimestamp(1547337793))

            embed.set_author(name="Betina#9182",
                             icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")

            embed.add_field(name="📖**Exemplos:**", value="$devemenos @sicrano 500\n$devemenos @fulano 10",
                            inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$dntp, $naomedeve.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")

        elif error.param.name == 'a':
            embed = discord.Embed(title="Comando $devemenos:", colour=discord.Colour(0x370c5e),
                                  description="Você diminui uma quantidade ao quanto um usuário te deve\n \n**Como"
                                              " usar: $devemenos <usuário> <valor>**",
                                  timestamp=datetime.datetime.utcfromtimestamp(1547337793))

            embed.set_author(name="Betina#9182",
                             icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")

            embed.add_field(name="📖**Exemplos:**", value="$devemenos @sicrano 500\n$devemenos @fulano 10",
                            inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$dntp, $naomedeve.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")


@commands.guild_only()
@client.command(name='deve', aliases=['rsp', 'owe'])
async def deve(ctx, member: discord.Member):
    if member.mention != client.user.mention:
        if not (member in devedores):
            msg = await ctx.send('**{} não deve nada a ninguem!**'.format(member.mention))
            await msg.add_reaction('😯')
        else:
            await ctx.send('**{} deve a tais pessoas: **'.format(member.mention))
            for membros in devedores[member]:
                if membros.id != member.id:
                    await ctx.send('**Deve R$ {} ao {}**'.format(devidos[membros], membros.mention))
    else:
        msg = await ctx.send('**Eu sou uma Bot! Nunca deverei nada a ninguem!**')
        await msg.add_reaction('🤷')


@deve.error
async def deve_handler(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        if error.param.name == 'member':
            embed = discord.Embed(title="Comando $deve:", colour=discord.Colour(0x370c5e),
                                  description="Diz o quanto o usuário deve a cada pessoa do servidor\n \n**Como usar"
                                              ": $deve <usuário>**",
                                  timestamp=datetime.datetime.utcfromtimestamp(1547337793))

            embed.set_author(name="Betina#9182",
                             icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")

            embed.add_field(name="📖**Exemplos:**", value="$deve @sicrano\n$deve @fulano", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$rsp, $owe.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")


@commands.guild_only()
@client.command(name='conversor', aliases=['converter', 'converte'])
async def conversor(ctx, moeda1, moeda2, quantidade=None):
    """Vê o valor da moeda 1 em moeda 2"""
    try:
        channel = ctx.channel
        await channel.trigger_typing()
        c = CurrencyRates()
        msg = c.get_rate(f'''{moeda1.upper()}''', f'''{moeda2.upper()}''')
        if quantidade is None:
            await ctx.send(
                'Esse é o valor da cotacao atual do ``{}`` em ``{}``: **{}**'.format(moeda1.upper(), moeda2.upper(),
                                                                                     msg))
        else:
            msg = msg * quantidade
            await ctx.send(
                'Esse é o valor de {} ``{}`` em ``{}``: **{}**'.format(quantidade, moeda1.upper(), moeda2.upper(), msg))
    except:
        msg = await ctx.send('Tente utilizar o codigo de uma moeda existente. **Por exemplo: $conversor usd brl**')
        await msg.add_reaction('❤')


@conversor.error
async def conversor_handler(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        if error.param.name == 'moeda1':
            embed = discord.Embed(title="Comando $conversor:", colour=discord.Colour(0x370c5e),
                                  description="Você converte a moeda1 em termos de moeda2\n \n**Como"
                                              " usar: $converte <moeda1> <moeda2>**",
                                  timestamp=datetime.datetime.utcfromtimestamp(1547337793))

            embed.set_author(name="Betina#9182",
                             icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")

            embed.add_field(name="📖**Exemplos:**", value="$converte usd brl\n$converte eur pln", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$converter, $converte.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")

        elif error.param.name == 'moeda2':
            embed = discord.Embed(title="Comando $conversor:", colour=discord.Colour(0x370c5e),
                                  description="Você converte a moeda1 em termos de moeda2\n \n**Como"
                                              " usar: $converte <moeda1> <moeda2>**",
                                  timestamp=datetime.datetime.utcfromtimestamp(1547337793))

            embed.set_author(name="Betina#9182",
                             icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")

            embed.add_field(name="📖**Exemplos:**", value="$converte usd brl\n$converte eur pln", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$converter, $converte.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")


@commands.guild_only()
@client.command()
async def treta(ctx):
    """Todas as tretas do grupo!"""
    pass


@commands.guild_only()
@client.command()
async def faustao(ctx):
    with open("faustop.png", "rb") as imageFile:
        file = bytearray(imageFile.read())
    channel = ctx.channel
    async with aiohttp.ClientSession() as session:
        webhook = await channel.create_webhook(name='Faustão', avatar=file)

    await webhook.send("Esta Fera Bicho!")


@commands.guild_only()
@client.command()
async def bolsonaro(ctx):
    with open("bolsoboy.png", "rb") as imageFile:
        file = bytearray(imageFile.read())
    channel = ctx.channel
    async with aiohttp.ClientSession() as session:
        webhook = await channel.create_webhook(name='Bolsonaro', avatar=file)

    await webhook.send("Taokei?")


@commands.guild_only()
@client.command(name='rola', aliases=['roll', 'dice'])
async def rola(ctx, a: int):
    """Um Dado de até 20 lados."""
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
async def rola_handler(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        if error.param.name == 'a':
            embed = discord.Embed(title="Comando $rola:", colour=discord.Colour(0x370c5e),
                                  description="Rola um dado de n lados\n \n**Como usar"
                                              ": $rola <n>**",
                                  timestamp=datetime.datetime.utcfromtimestamp(1547337793))

            embed.set_author(name="Betina#9182",
                             icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")

            embed.add_field(name="📖**Exemplos:**", value="$rola 10\n$rola 4", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$roll, $dice.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")


@commands.guild_only()
@client.command()
async def ping(ctx):
    """Retorna o Ping do usuario mais uma piadinha tosca!"""
    channel = ctx.channel
    t1 = time.perf_counter()
    await channel.trigger_typing()
    t2 = time.perf_counter()
    await ctx.send('Pong! Isso me levou {}µs.'.format(round(1000 * (t2 - t1))))


@commands.guild_only()
@client.command(pass_context=True)
async def pong(ctx):
    channel = ctx.channel
    t1 = time.perf_counter()
    await channel.trigger_typing()
    t2 = time.perf_counter()
    await ctx.send('Ping! Uovel em ossI {} sµ.'.format(round(1000 * (t2 - t1))))


@commands.guild_only()
@client.command(name='moeda', aliases=['coin', 'ht'])
async def moeda(ctx):
    """Heads and Tails!"""
    resultado = random.randint(1, 2)
    if resultado == 1:
        await ctx.send('😃')
    else:
        await ctx.send('👑')

@commands.guild_only()
@client.command()
async def help(ctx):
    """Manda mensagem privada pro usuario!"""
    author = ctx.author
    embed = discord.Embed(title="Escolha uma categoria", colour=discord.Colour(0x370c5e),
                          description="```Bem vindo ao"
                                      " meu suporte, escolha abaixo uma das categorias"
                                      " para obter mais informações sobre minhas utilidades ```",
                          timestamp=datetime.datetime.utcfromtimestamp(1547379087))
    embed.set_footer(text="Betina Brazilian Bot",
                     icon_url="https://images.discordapp.net/avatars/"
                              "527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")

    embed.add_field(name="😂 **Diversão**", value="``$moeda, $ppt, $rola ...``", inline=False)
    embed.add_field(name="💰 **Cobrança**", value="``$devemais, $devemenos, $deve...``", inline=False)
    embed.add_field(name="🎵 **Música**", value="``$play, $resume, $stop, $fila...``", inline=False)
    embed.add_field(name="🗣 **Interação**", value="``$bate, $abraça, $treta...``", inline=False)
    embed.add_field(name="👮 **Administração**", value="``$apaga, $ping, $pong...``", inline=False)

    message = await author.send(embed=embed, delete_after=60)

    reaction_list = ["😂", "💰", "🎵", "🗣", "👮"]

    for reaction in reaction_list:
        await message.add_reaction(reaction)

    def check(reaction, user):
        return user == author and str(reaction.emoji) in reaction_list

    try:
        reaction, user = await client.wait_for('reaction_add', check=check)
    except:
        return

    if str(reaction.emoji) == "💰":
        await message.delete()
        embed = discord.Embed(title="Cobrança", colour=discord.Colour(0x370c5e),
                              description="*Bem vindo a categoria Cobrança:\nAqui você encontrará"
                                          " comandos que ajudará você a ter noção de finanças.*",
                              timestamp=datetime.datetime.utcfromtimestamp(1547379087))
        embed.set_thumbnail(
            url="https://images.discordapp.net/avatars/527565353199337474"
                "/40042c09bb354a396928cb91e0288384.png?size=256")
        embed.set_footer(text="Betina Brazilian Bot",
                         icon_url="https://images.discordapp.net/avatars/527565353199337474/"
                                  "40042c09bb354a396928cb91e0288384.png?size=256")
        embed.add_field(name="**$devemais <usuário> <quantidade>**", value="``Você aumentará o quanto um"
                                                                           " usuário te deve!``", inline=False)
        embed.add_field(name="**$devemenos**", value="``Você diminuirá o quanto um usuário te deve!``",
                        inline=False)
        embed.add_field(name="**$deve**", value="``Mostra uma lista de todas as pessoas que um usuário"
                                                " deve!``", inline=False)
        embed.add_field(name="**$conversor <moeda1> <moeda2>"
                             " <quantidade>**", value="``Diz a cotação da moeda 1 em relação a moeda 2,"
                                                      " a quantidade é a quantidade vezes o valor da cotação``",
                        inline=False)
        msg = await author.send(embed=embed, delete_after=40)
        await msg.add_reaction("🔙")

        def check(reaction, user):
            return user == author and str(reaction.emoji) == "🔙"

        try:
            reaction, user = await client.wait_for('reaction_add', check=check)
        except:
            return
        else:
            await msg.delete()
            await ctx.invoke(client.get_command("help"))


    elif str(reaction.emoji) == "😂":
        await message.delete()
        embed = discord.Embed(title="Diversão", colour=discord.Colour(0x370c5e),
                              description="*Bem vindo a categoria diversão:\n"
                                          "Aqui você encontrará comandos que trará alegria a todos no servidor.*",
                              timestamp=datetime.datetime.utcfromtimestamp(1547379087))
        embed.set_thumbnail(
            url="https://images.discordapp.net/avatars/527565353199337474/"
                "40042c09bb354a396928cb91e0288384.png?size=256")
        embed.set_footer(text="Betina Brazilian Bot",
                         icon_url="https://images.discordapp.net/avatars/"
                                  "527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")

        embed.add_field(name="**$moeda**", value="``Jogarei uma moeda. Poderá cair cara ou coroa!``",
                        inline=False)
        embed.add_field(name="**$rola**", value="``Rolarei um dado de até 20 lados!``", inline=False)
        embed.add_field(name="**$ppt <Pedra, Papel ou Tesoura>**", value="``Começarei um jogo de pedra, papel"
                                                                         " ou tesoura contra você!``",
                        inline=False)
        embed.add_field(name="**$bolsonaro**", value="``Taokei ?``",
                        inline=False)
        embed.add_field(name="**$faustao**", value="``Esta Fera, bicho!``",
                        inline=False)

        msg = await author.send(embed=embed, delete_after=40)
        await msg.add_reaction("🔙")

        def check(reaction, user):
            return user == author and str(reaction.emoji) == "🔙"

        try:
            reaction, user = await client.wait_for('reaction_add', check=check)
        except:
            return
        else:
            await msg.delete()
            await ctx.invoke(client.get_command("help"))


    elif str(reaction.emoji) == "🎵":
        await message.delete()
        embed = discord.Embed(title="Música", colour=discord.Colour(0x370c5e),
                              description="*Bem vindo a categoria Música:\nAqui você encontrará"
                                          " comandos que ajudará você a ouvir música enquanto faz suas atividades"
                                          " no discord.*",
                              timestamp=datetime.datetime.utcfromtimestamp(1547379087))
        embed.set_thumbnail(
            url="https://images.discordapp.net/avatars/527565353199337474"
                "/40042c09bb354a396928cb91e0288384.png?size=256")
        embed.set_footer(text="Betina Brazilian Bot",
                         icon_url="https://images.discordapp.net/avatars/527565353199337474/"
                                  "40042c09bb354a396928cb91e0288384.png?size=256")

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
        msg = await author.send(embed=embed, delete_after=40)
        await msg.add_reaction("🔙")

        def check(reaction, user):
            return user == author and str(reaction.emoji) == "🔙"

        try:
            reaction, user = await client.wait_for('reaction_add', check=check)
        except:
            return
        else:
            await msg.delete()
            await ctx.invoke(client.get_command("help"))


    elif str(reaction.emoji) == "🗣":
        await message.delete()
        embed = discord.Embed(title="Interação", colour=discord.Colour(0x370c5e),
                              description="*Bem vindo a categoria Interação:\nAqui você encontrará"
                                          " comandos que ajudará você a interagir com outros membros do seu servidor*",
                              timestamp=datetime.datetime.utcfromtimestamp(1547379087))
        embed.set_thumbnail(
            url="https://images.discordapp.net/avatars/527565353199337474"
                "/40042c09bb354a396928cb91e0288384.png?size=256")
        embed.set_footer(text="Betina Brazilian Bot",
                         icon_url="https://images.discordapp.net/avatars/527565353199337474/"
                                  "40042c09bb354a396928cb91e0288384.png?size=256")

        embed.add_field(name="**$treta **", value="``Diz coisas assustadoras sobre as pessoas do servidor!``",
                        inline=False)
        embed.add_field(name="**$abraça <usuário>**", value="``Abraça o usuário!``",
                        inline=False)
        embed.add_field(name="**$beija <usuário>**", value="``Beija o usuário!``", inline=False)
        embed.add_field(name="**$bate <usuário> **", value="``Bate no usuário!``", inline=False)
        embed.add_field(name="**$dança <usuário> **", value="``Dança com o usuário!``", inline=False)
        embed.add_field(name="**$ataca <usuário> **", value="``Dá um ataque no usuário!``", inline=False)
        embed.add_field(name="**$voltapracaverna <usuário> **", value="``Manda o usuário voltar "
                                                                      "pro seu lugar de origem!``", inline=False)
        embed.add_field(name="**$tnc **", value="``Manda alguem do servidor tomar no você sabe onde!``",
                        inline=False)

        msg = await author.send(embed=embed, delete_after=40)
        await msg.add_reaction("🔙")

        def check(reaction, user):
            return user == author and str(reaction.emoji) == "🔙"

        try:
            reaction, user = await client.wait_for('reaction_add', check=check)
        except:
            return
        else:
            await msg.delete()
            await ctx.invoke(client.get_command("help"))


    elif str(reaction.emoji) == "👮":
        await message.delete()
        embed = discord.Embed(title="Administração", colour=discord.Colour(0x370c5e),
                              description="*Bem vindo a categoria Administração:\nAqui você encontrará"
                                          " comandos que ajudará você a ajudar a controlar seu servidor.*",
                              timestamp=datetime.datetime.utcfromtimestamp(1547379087))
        embed.set_thumbnail(
            url="https://images.discordapp.net/avatars/527565353199337474"
                "/40042c09bb354a396928cb91e0288384.png?size=256")
        embed.set_footer(text="Betina Brazilian Bot",
                         icon_url="https://images.discordapp.net/avatars/527565353199337474/"
                                  "40042c09bb354a396928cb91e0288384.png?size=256")
        embed.add_field(name="**$apaga <quantidade>**", value="``Eu apagarei uma"
                                                              " quantidade de mensagens!``", inline=False)
        embed.add_field(name="**$ping**", value="``Retornarei o ping do usuário``", inline=False)
        embed.add_field(name="**$pong**", value="``oiráusu od gnip o ieranroter``", inline=False)
        embed.add_field(name="**$warn**", value="``Em breve!``", inline=False)
        embed.add_field(name="**$mute**", value="``Em breve!``", inline=False)
        embed.add_field(name="**$ban**", value="``Em breve!``", inline=False)

        msg = await author.send(embed=embed, delete_after=40)
        await msg.add_reaction("🔙")

        def check(reaction, user):
            return user == author and str(reaction.emoji) == "🔙"

        try:
            reaction, user = await client.wait_for('reaction_add', check=check)
        except:
            return
        else:
            await msg.delete()
            await ctx.invoke(client.get_command("help"))


@commands.guild_only()
@client.command()
async def ajuda(ctx):
    await ctx.invoke(client.get_command("help"))
    
    
@commands.guild_only()
@client.command()
async def entra(ctx):
    """O bot entra no chat de voz!"""
    try:
        canal = ctx.author.voice.voice_channel
        await client.join_voice_channel(canal)
    except discord.errors.InvalidArgument:
        msg = await ctx.channel.send('Você precisa estar conectado a um canal de voz!')
        await msg.add_reaction('🤦')


@commands.guild_only()
@client.command()
async def sai(ctx):
    """O bot sai do chat de voz!"""
    try:
        canaldevoz = client.voice_client_in(ctx.guild)
        await canaldevoz.disconnect()
    except AttributeError:
        msg = await ctx.channel.send('O bot nao esta conectado em nenhum canal de voz!')
        await msg.add_reaction('🤦')

        
if __name__ == '__main__':
    for extension in startup_extensions:
        try:
            client.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

client.run(TOKEN)
