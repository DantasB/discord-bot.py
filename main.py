""" If you have any trouble with the bot and want some help, fell free to send me a message on discord: DantasB#7096.
    Some commands that i used in this bot were inspired in another discord bots functions."""

import random
import time
import discord
from discord.ext import commands
from forex_python.converter import CurrencyRates


startup_extensions = ['Music']
prefix = '$'
client = commands.Bot(command_prefix=prefix)
TOKEN = 'Insira seu token aqui!'

client.remove_command('help')

players = {}
devedores = {}
devidos = {}
lista = ['[nome] insira frases com [nome] ou não']


@client.event
async def on_ready():
    print('--------------BD--------------')
    print('BOT ONLINE')
    print('Nome do Bot: ' + client.user.name)
    print('ID do Bot: ' + str(client.user.id))
    print('Versao do Discord: ' + discord.__version__)
    print('--------------BD--------------')
    game = discord.Game("com a API")
    await client.change_presence(status=discord.Status.idle, activity=game)


@client.event
async def on_member_join(member):
    """Envia uma mensagem quando o membro entra no servidor"""
    guild = member.guild.get_channel('id do canal que você quer dar boas vindas')
    fmt = 'Bem vindo ao servidor {1.name}, {0.mention}, aproveita e segue o baile.'
    await guild.send(fmt.format(member, member.guild))


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


@client.command()
async def bate(ctx, member: discord.Member):
    """<membro>: Tome cuidado com isso."""
    msg = await ctx.send('{} bate em {}'.format(ctx.author.mention, member.mention))
    await msg.add_reaction('😯')


@client.command()
async def abraça(ctx, member: discord.Member):
    """<membro>: Use isso com amor <3."""
    msg = await ctx.send('{} abraça {}'.format(ctx.author.mention, member.mention))
    await msg.add_reaction('🤗')


@client.command()
async def apaga(ctx, amount: int):
    """Apaga uma quantidade amount de mensagens no servidor"""
    await ctx.channel.purge(limit=amount)


@client.command()
async def ppt(ctx, msg: str):
    """Pedra, papel e tesoura"""
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


@client.command()
async def devemais(ctx, member: discord.Member, a: float):
    """Adiciona o credito"""
    if (member in devedores) and (ctx.author in devidos):
        devidos[ctx.author] += a
    else:
        devidos[ctx.author] = a
        devedores[member] = devidos
    await ctx.send('{} deve R$ {} ao {}'.format(member.mention, devidos[ctx.author], ctx.author.mention))


@client.command()
async def devemenos(ctx, member: discord.Member, a: float):
    """Diminui o credito"""
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
            await ctx.send('Agora {} deve R$ {} ao {}'.format(ctx.author.mention, devidos[member], member.mention))
        elif devidos[ctx.author] == 0:
            await ctx.send('{} não deve nada a {}'.format(ctx.author.mention, member.mention))
        else:
            await ctx.send('{} deve R$ {} ao {}'.format(member.mention, devidos[ctx.author], ctx.author.mention))
    else:
        devedores[ctx.author] = devidos
        devidos[member] = a
        await ctx.send('{} deve R$ {} ao {}'.format(ctx.author.mention, devidos[member], member.mention))


@client.command()
async def deve(ctx, member: discord.Member):
    """Diz o quanto uma pessoa deve as outras"""
    if not (member in devedores):
        msg = await ctx.send('{} não deve nada a ninguem!'.format(member.mention))
        await msg.add_reaction('😯')
    else:
        await ctx.send('{} deve a tais pessoas: '.format(member.mention))
        for membros in devedores[member]:
            if membros.id != member.id:
                await ctx.send('R$ {} ao {}'.format(devidos[membros], membros.mention))


@client.command()
async def conversor(ctx, moeda1, moeda2, quantidade=None):
    """Vê o valor da moeda 1 em moeda 2"""
    try:
        channel = ctx.channel
        await channel.trigger_typing()
        c = CurrencyRates()
        msg = c.get_rate(f'''{moeda1.upper()}''', f'''{moeda2.upper()}''')
        if quantidade is None:
            await ctx.send('Esse é o valor da cotacao atual do ``{}`` em ``{}``: **{}**'.format(moeda1.upper(), moeda2.upper(), msg))
        else:
            msg = msg * quantidade
            await ctx.send('Esse é o valor de {} ``{}`` em ``{}``: **{}**'.format(quantidade, moeda1.upper(), moeda2.upper(), msg))
    except:
        msg = await ctx.send('Tente utilizar o codigo de uma moeda existente. **Por exemplo: $conversor usd brl**')
        await msg.add_reaction('❤')



@client.command()
async def treta(ctx):
    """Todas as tretas do grupo!"""
    pass


@client.command(pass_context=True)
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


@client.command()
async def ping(ctx):
    """Retorna o Ping do usuario mais uma piadinha tosca!"""
    channel = ctx.channel
    t1 = time.perf_counter()
    await channel.trigger_typing()
    t2 = time.perf_counter()
    await ctx.send('Pong! Isso me levou {}µs.'.format(round(1000 * (t2 - t1))))


@client.command(pass_context=True)
async def pong(ctx):
    """O inverso de Ping!"""
    channel = ctx.channel
    t1 = time.perf_counter()
    await channel.trigger_typing()
    t2 = time.perf_counter()
    await ctx.send('Ping! Uovel em ossI {} sµ.'.format(round(1000 * (t2-t1))))



@client.command()
async def moeda(ctx):
    """Heads and Tails!"""
    resultado = random.randint(1, 2)
    if resultado == 1:
        await ctx.send('😃')
    else:
        await ctx.send('👑')


@client.command()
async def help(ctx):
    """Manda mensagem privada pro usuario!"""
    author = ctx.author
    embed = discord.Embed(colour=discord.Colour.orange())
    embed.set_author(name='Ajuda eles aí, Betina:')
    embed.add_field(name='$ping', value='Retorna Pong!', inline=False)
    embed.add_field(name='$pong', value='???', inline=False)
    embed.add_field(name='$treta', value='Algo tenso acontece', inline=False)
    embed.add_field(name='$abraça @usuario', value='Abraca o usuario', inline=False)
    embed.add_field(name='$bate @usuario', value='bate no usuario', inline=False)
    embed.add_field(name='$conversor moeda1 moeda2', value='Dá a cotacao da moeda1 em relacao a moeda2', inline=False)
    embed.add_field(name='$devemais @usuario quantidade', value='O usuario te deve + quantidade', inline=False)
    embed.add_field(name='$devemenos @usuario quantidade', value='O usuario te deve - quantidade', inline=False)
    embed.add_field(name='$deve @usuario', value='Retorna uma lista de pessoas a quem usuario deve', inline=False)
    embed.add_field(name='$rola n', value='Retona um valor aleatorio de um dado de n lados', inline=False)
    embed.add_field(name='$apaga ***', value='Apaga *** linhas acima da sua mensagem, incluindo ela', inline=False)
    embed.add_field(name='$moeda', value='Retorna Cara ou Coroa', inline=False)
    embed.add_field(name='$play música', value='Procura a música no youtube e da play.', inline=False)
    embed.add_field(name='$skip', value='Pula a música que está tocando', inline=False)
    embed.add_field(name='$pause', value='Pausa a música que está tocando', inline=False)
    embed.add_field(name='$stop', value='Para de tocar a música que esta tocando', inline=False)
    embed.add_field(name='$volume **', value='Altera o volume da música para **%', inline=False)
    embed.add_field(name='$fila', value='Diz a fila das músicas que estão tocando', inline=False)
    embed.add_field(name='$tocando', value='Diz qual música esta tocando', inline=False)
    embed.add_field(name='$resume', value='Retorna a tocar a música pausada', inline=False)

    await author.send(embed=embed)


@client.command()
async def entra(ctx):
    """O bot entra no chat de voz!"""
    try:
        canal = ctx.author.voice.voice_channel
        await client.join_voice_channel(canal)
    except discord.errors.InvalidArgument:
        msg = await ctx.channel.send('Você precisa estar conectado a um canal de voz!')
        await msg.add_reaction('🤦')


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
