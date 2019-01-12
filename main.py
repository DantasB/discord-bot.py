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


@client.command(name='bate', aliases=['hit', 'punch', 'kick'])
async def bate(ctx, member: discord.Member):
    """<membro>: Tome cuidado com isso."""
    msg = await ctx.send('{} bate em {}'.format(ctx.author.mention, member.mention))
    await msg.add_reaction('😯')


@bate.error
async def bate_handler(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        if error.param.name == 'member':
            await ctx.send("``Você precisa me dizer qual membro você quer bater. Ex:``** $bate @fulaninho**")    
    
    
@client.command(name='abraça', aliases=['hug', 'abraço'])
async def abraça(ctx, member: discord.Member):
    """<membro>: Use isso com amor <3."""
    msg = await ctx.send('{} abraça {}'.format(ctx.author.mention, member.mention))
    await msg.add_reaction('🤗')


 @abraça.error
async def abraça_handler(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        if error.param.name == 'member':
            await ctx.send("``Você precisa me dizer qual membro você quer abraçar. Ex:``** $abraça @fulaninho**")   
 

@client.command(name='apaga', aliases=['delete', 'clean', 'clear', 'c'])
async def apaga(ctx, amount: int):
    """Apaga uma quantidade amount de mensagens no servidor"""
    await ctx.channel.purge(limit=amount)


@apaga.error
async def apaga_handler(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        if error.param.name == 'amount':
            await ctx.send("``Você precisa me dizer a quantidade de mensagens que quer apagar. Ex:``** $apaga quantidade**")    
    
    
@client.command(name='ppt', aliases=['Rsp'])
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


@ppt.error
async def ppt_handler(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        if error.param.name == 'msg':
            await ctx.send("``Você precisa me dizer se quer pedra, papel ou tesoura. Ex:``** $ppt pedra**")        
        
        
@client.command(name='devemais', aliases=['ntp', 'medeve', 'pay'])
async def devemais(ctx, member: discord.Member, a: float):
    """Adiciona o credito"""
    if (member in devedores) and (ctx.author in devidos):
        devidos[ctx.author] += a
    else:
        devidos[ctx.author] = a
        devedores[member] = devidos
    await ctx.send('{} deve R$ {} ao {}'.format(member.mention, devidos[ctx.author], ctx.author.mention))

    
@devemais.error
async def devemais_handler(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        if error.param.name == 'member':
            await ctx.send("``Você precisa me dizer quem deve você. Ex:``** $devemais @fulano 10**")
        elif error.param.name == 'a':
            await ctx.send("``Você precisa me dizer a quantidade que a pessoa te deve. Ex:``** $devemais @fulano 10**")
    
    
@client.command(name='devemenos', aliases=['dntp', 'naomedeve', 'npay'])
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


@devemenos.error
async def devemenos_handler(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        if error.param.name == 'member':
            await ctx.send("``Você precisa me dizer quem pagou você. Ex:``** $devemenos @fulano 10**")
        elif error.param.name == 'a':
            await ctx.send("``Você precisa me dizer a quantidade que a pessoa te pagou. Ex:``** $devemenos @fulano 10**")
        
             
@client.command(name='deve', aliases=['rsp', 'owe'])
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


@deve.error
async def deve_handler(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        if error.param.name == 'member':
            await ctx.send("``Você precisa me dizer qual a pessoa. Ex:``** $deve @fulano**")                
                
                
@client.command(name='conversor', aliases=['converter', 'converte'])
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


@conversor.error
async def conversor_handler(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        if error.param.name == 'moeda1':
            await ctx.send("``Você precisa me dizer qual o código da moeda que você quer converter. Ex:`` **$conversor usd brl**")
        elif error.param.name =='moeda2':
            await ctx.send(
                "``Você precisa me dizer qual o código da moeda no qual você quer saber o valor. Ex:`` **$conversor usd brl**")

        
@client.command()
async def treta(ctx):
    """Todas as tretas do grupo!"""
    pass


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
            await ctx.send("``Você precisa me dizer qual o número de lados do dado. Ex:`` **$rola 10**")        
        
        
@client.command(pass_context=True)
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


@client.command(name='moeda', aliases=['coin', 'ht'])
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
