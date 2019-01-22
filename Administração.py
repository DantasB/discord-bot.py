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

banhammer = [] #banhammer giphy gifs
omg = [] #omg giphy gifs

betina_icon = " " #bot icon

with open('reports.json', encoding='utf-8') as f:
    try:
        report = json.load(f)
    except ValueError:
        report = {}
        report['users'] = []


with open('mutados.json', 'r') as file:
    try:
        cargos_dos_mutados = json.load(file)
    except ValueError:
        cargos_dos_mutados = {}


class Administração:
    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.command()
    async def ping(self, ctx):
        """Retorna o Ping do usuario mais uma piadinha tosca!"""
        channel = ctx.channel
        t1 = time.perf_counter()
        await channel.trigger_typing()
        t2 = time.perf_counter()
        await ctx.send('Pong! Isso me levou {}µs.'.format(round(1000 * (t2 - t1))))

    @commands.guild_only()
    @commands.command(pass_context=True)
    async def pong(self, ctx):
        channel = ctx.channel
        t1 = time.perf_counter()
        await channel.trigger_typing()
        t2 = time.perf_counter()
        await ctx.send('Ping! Uovel em ossI {} sµ.'.format(round(1000 * (t2 - t1))))

    @commands.guild_only()
    @commands.command(name='apaga', aliases=['delete', 'clean'])
    @has_permissions(manage_messages=True, read_message_history=True)
    async def apaga(self, ctx, amount: int):
        if ctx.message.author.avatar_url_as(static_format='png')[54:].startswith('a_'):
            avi = ctx.message.author.avatar_url.rsplit("?", 1)[0]
        else:
            avi = ctx.message.author.avatar_url_as(static_format='png')

        await ctx.channel.purge(limit=amount + 1)
        embed = discord.Embed(title=f"*{amount} mensagens foram apagadas, {ctx.message.author}*",
                              colour=discord.Colour(0x370c5e))

        embed.set_author(name=f"{ctx.message.author}", icon_url=f"{avi}")
        embed.set_footer(text="Betina Brazilian Bot", icon_url=betina_icon)

        await ctx.send(embed=embed, delete_after=10)

    @apaga.error
    async def apaga_handler(self, ctx, error):
        if isinstance(error, MissingPermissions):
            embed = discord.Embed(title="Comando $apaga:", colour=discord.Colour(0x370c5e),
                                  description="Apaga n+1 linhas acima da ultima mensagem\n \n**Como usar: $apaga <linhas>**")

            embed.set_author(name="Betina#9182",
                             icon_url=betina_icon)
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url=betina_icon)
            embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                            "ter a permissão de* ``"
                                                            "Gerenciar Mensagens, Ler o histórico de "
                                                            "mensagens`` *para utilizar este comando!*", inline=False)
            embed.add_field(name="📖**Exemplos:**", value="$apaga 100\n$apaga 10", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$delete, $clean.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")


        elif isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'amount':
                embed = discord.Embed(title="Comando $apaga:", colour=discord.Colour(0x370c5e),
                                      description="Apaga n+1 linhas acima da ultima mensagem\n \n**Como usar: $apaga <linhas>**")

                embed.set_author(name="Betina#9182",
                                 icon_url=betina_icon)
                embed.set_footer(text="Betina Brazilian Bot",
                                 icon_url=betina_icon)
                embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                                "ter a permissão de* ``"
                                                                "Gerenciar Mensagens, Ler o histórico de "
                                                                "mensagens`` *para utilizar este comando!*",
                                inline=False)
                embed.add_field(name="📖**Exemplos:**", value="$apaga 100\n$apaga 10", inline=False)
                embed.add_field(name="🔀**Outros Comandos**", value="``$delete, $clean.``", inline=False)

                msg = await ctx.send(embed=embed)
                await msg.add_reaction("❓")

    @commands.guild_only()
    @commands.command(name='ban', aliases=['banir', 'bane'])
    @has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, arg=None):
        if member.top_role >= member.guild.me.top_role:
            embed = discord.Embed(title="Comando $ban:", colour=discord.Colour(0x370c5e),
                                  description="Bane o usuário do servidor por um motivo"
                                              "\n \n**Como usar: $bane <usuário> <motivo> (opcional)**")

            embed.set_author(name="Betina#9182",
                             icon_url=betina_icon)
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url=betina_icon)
            embed.add_field(name="👮**Permissões:**", value="*Você e o bot precisam "
                                                            "ter a permissão de* ``"
                                                            "Banir membros e estar no topo dos cargos`` *para utilizar este comando!*",
                            inline=False)
            embed.add_field(name="📖**Exemplos:**", value="$ban @fulano\n$ban @fulano xingou o moderador",
                            inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$bane, $banir.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")
            return
        else:
            if arg == None:
                reason = 'Sem motivos específicados!'
            else:
                reason = arg

            gif1 = random.choice(banhammer)
            gif2 = random.choice(omg)
            msg1 = '**Você estava tentando se banir ?**'
            msg2 = '{} foi banido do servidor {} pelo seguinte motivo: {}'.format(member, ctx.guild.name, reason)
            msg3 = 'Você foi banido do servidor {} pelo seguinte motivo: {}'.format(ctx.guild.name, reason)
            if member == ctx.message.author:

                embed = discord.Embed(title="**Pensativa...**", colour=discord.Colour(0x370c5e),
                                      description="{}".format(msg1))
                embed.set_image(url="{}".format(gif2))
                embed.set_footer(text="Betina Brazilian Bot",
                                 icon_url=betina_icon)
                await ctx.channel.send(embed=embed)
                return
            else:
                embed = discord.Embed(title="**BAN!**", colour=discord.Colour(0x370c5e), description="{}".format(msg2))
                embed.set_image(url="{}".format(gif1))
                embed.set_footer(text="Betina Brazilian Bot",
                                 icon_url=betina_icon)
                mbd = discord.Embed(title="**BAN!**", colour=discord.Colour(0x370c5e), description="{}".format(msg3))
                mbd.set_image(url="{}".format(gif1))
                mbd.set_footer(text="Betina Brazilian Bot",
                               icon_url=betina_icon)

                if not member.bot:
                    await member.send(embed=mbd)
                    await ctx.channel.send(embed=embed)
                    await ctx.guild.ban(member)
                else:
                    await ctx.channel.send(embed=embed)
                    await ctx.guild.ban(member)

    @ban.error
    async def ban_handler(self, ctx, error):
        if isinstance(error, MissingPermissions):
            embed = discord.Embed(title="Comando $ban:", colour=discord.Colour(0x370c5e),
                                  description="Bane o usuário do servidor por um motivo"
                                              "\n \n**Como usar: $bane <usuário> <motivo> (opcional)**")

            embed.set_author(name="Betina#9182",
                             icon_url=betina_icon)
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url=betina_icon)
            embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos"
                                                            "ter a permissão de* ``"
                                                            "Banir membros e estar no topo dos cargos`` *para utilizar este comando!*",
                            inline=False)
            embed.add_field(name="📖**Exemplos:**", value="$ban @fulano gado demais\n$ban @fulano xingou "
                                                          "o moderador", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$bane, $banir.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")


        elif isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'member':
                embed = discord.Embed(title="Comando $ban:", colour=discord.Colour(0x370c5e),
                                      description="Bane o usuário do servidor por um motivo"
                                                  "\n \n**Como usar: $bane <usuário> <motivo> (opcional)**")

                embed.set_author(name="Betina#9182",
                                 icon_url=betina_icon)
                embed.set_footer(text="Betina Brazilian Bot",
                                 icon_url=betina_icon)
                embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                                "ter a permissão de* ``"
                                                                "Banir membros e estar no topo dos cargos`` *para utilizar este comando!*",
                                inline=False)
                embed.add_field(name="📖**Exemplos:**", value="$ban @fulano\n$ban @fulano xingou o moderador",
                                inline=False)
                embed.add_field(name="🔀**Outros Comandos**", value="``$bane, $banir.``", inline=False)

                msg = await ctx.send(embed=embed)
                await msg.add_reaction("❓")

        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(title="Comando $ban:", colour=discord.Colour(0x370c5e),
                                  description="Bane o usuário do servidor por um motivo"
                                              "\n \n**Como usar: $bane <usuário> <motivo> (opcional)**")

            embed.set_author(name="Betina#9182",
                             icon_url=betina_icon)
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url=betina_icon)
            embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                            "ter a permissão de* ``"
                                                            "Banir membros e estar no topo dos cargos`` *para utilizar este comando!*",
                            inline=False)
            embed.add_field(name="📖**Exemplos:**", value="$ban @fulano\n$ban @fulano xingou o moderador",
                            inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$bane, $banir.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")


    @commands.guild_only()
    @commands.command()
    async def ajuda(self, ctx):
        await ctx.invoke(self.client.get_command("help"))

    @commands.guild_only()
    @commands.command(name='membro', aliases=['userinfo', 'ui'])
    @has_permissions(manage_roles=True)
    async def membro(self, ctx, member: discord.Member):
        if ctx.message.author.avatar_url_as(static_format='png')[54:].startswith('a_'):
            avi1 = ctx.message.author.avatar_url.rsplit("?", 1)[0]
        else:
            avi1 = ctx.message.author.avatar_url_as(static_format='png')
        roles = ', '.join([x.name for x in member.roles if x.name != "@everyone"])
        if member.avatar_url_as(static_format='png')[54:].startswith('a_'):
            avi = member.avatar_url.rsplit("?", 1)[0]
        else:
            avi = member.avatar_url_as(static_format='png')
        embed = discord.Embed(title='📟 Informações do Usuário {}'.format(member.name), color=member.color)
        embed.set_footer(text="{}".format(ctx.message.author),
                         icon_url=avi1)
        if member.nick == None:
            embed.add_field(name='📛 Apelido:', value='Não tem nenhum nick!', inline=True)
        else:
            embed.add_field(name='📛 Apelido:', value='{}'.format(member.nick), inline=True)
        embed.add_field(name='💻 Id:', value='{}'.format(member.id), inline=True)
        embed.add_field(name='📆 Conta criada em', value=member.created_at.__format__('%d de %b de %Y às %H:%M:%S'))
        embed.add_field(name='⭐ Entrou no servidor em:',
                        value='{}'.format(member.joined_at.__format__('%d de %b de %Y às %H:%M:%S')), inline=True)
        embed.add_field(name='📃 Status:', value='{}'.format(member.status), inline=True)
        embed.add_field(name='🎌 Cargos:', value='{}'.format(roles), inline=True)
        embed.set_thumbnail(url=avi)
        if member.id == ctx.message.guild.owner.id:
            if str(member.status) == 'online':
                embed.set_author(name='👑 ✅ {}'.format(member))
            elif str(member.status) == 'dnd':
                embed.set_author(name='👑 🔴 {}'.format(member))
            elif str(member.status) == 'idle':
                embed.set_author(name='👑 🐤 {}'.format(member))
            elif str(member.status) == 'offline':
                embed.set_author(name='👑 ⚪ {}'.format(member))
        else:
            if str(member.status) == 'online':
                embed.set_author(name='✅ {}'.format(member))
            elif str(member.status) == 'dnd':
                embed.set_author(name='🔴 {}'.format(member))
            elif str(member.status) == 'idle':
                embed.set_author(name='🐤 {}'.format(member))
            elif str(member.status) == 'offline':
                embed.set_author(name='⚪ {}'.format(member))
        await ctx.send(embed=embed)

    @membro.error
    async def membro_handler(self, ctx, error):
        if isinstance(error, MissingPermissions):
            embed = discord.Embed(title="Comando $membro:", colour=discord.Colour(0x370c5e),
                                  description="Diz as informações sobre o usuário"
                                              "\n \n**Como usar: $membro <usuário>**")

            embed.set_author(name="Betina#9182",
                             icon_url=betina_icon)
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url=betina_icon)
            embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                            "ter a permissão de* ``"
                                                            "Gerenciar Cargos`` *para utilizar este comando!*",
                            inline=False)
            embed.add_field(name="📖**Exemplos:**", value="$membro @fulano\n$membro @sicrano",
                            inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$userinfo, $ui.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")


        elif isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'member':
                embed = discord.Embed(title="Comando $membro:", colour=discord.Colour(0x370c5e),
                                      description="Diz as informações sobre o usuário"
                                                  "\n \n**Como usar: $membro <usuário>**")

                embed.set_author(name="Betina#9182",
                                 icon_url=betina_icon)
                embed.set_footer(text="Betina Brazilian Bot",
                                 icon_url=betina_icon)
                embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                                "ter a permissão de* ``"
                                                                "Gerenciar Cargos`` *para utilizar este comando!*",
                                inline=False)
                embed.add_field(name="📖**Exemplos:**", value="$membro @fulano\n$membro @sicrano",
                                inline=False)
                embed.add_field(name="🔀**Outros Comandos**", value="``$memberinfo, $ui.``", inline=False)

                msg = await ctx.send(embed=embed)
                await msg.add_reaction("❓")

    @commands.guild_only()
    @commands.command(pass_context=True, name='servidor', aliases=['serverinfo', 'si'])
    @has_permissions(administrator=True)
    async def servidor(self, ctx):
        if ctx.message.author.avatar_url_as(static_format='png')[54:].startswith('a_'):
            avi = ctx.message.author.avatar_url.rsplit("?", 1)[0]
        else:
            avi = ctx.message.author.avatar_url_as(static_format='png')
        embed = discord.Embed(name='Informações do {}'.format(ctx.message.guild.name),
                              description='Aqui está tudo o que pude encontrar sobre esse servidor!', color=0x370c5e)
        embed.set_footer(text="{}".format(ctx.message.author),
                         icon_url=avi)
        embed.set_author(name='📟 Informações do servidor {}:'.format(ctx.message.guild.name))
        embed.add_field(name='📛 Nome do Servidor:', value=ctx.message.guild.name, inline=True)
        embed.add_field(name='👑 Dono do Servidor:', value=ctx.message.guild.owner, inline=True)
        embed.add_field(name='🗺️ Região do Servidor:', value=ctx.message.guild.region, inline=True)
        embed.add_field(name='💻 Id do Servidor:', value=ctx.message.guild.id)
        embed.add_field(name='💬 Número de Canais:', value=len(ctx.message.guild.channels), inline=True)
        embed.add_field(name='👥 Número de Membros:', value=len(ctx.message.guild.members), inline=True)
        embed.add_field(name='📆 Criado em:',
                        value=ctx.message.guild.created_at.strftime("%d de %b de %Y"), inline=True)
        embed.add_field(name='🎌 Número de Cargos:', value=len(ctx.message.guild.roles), inline=True)
        embed.add_field(name='🎌 Nome dos Cargos:',
                        value=', '.join([role.name for role in ctx.message.guild.roles if role.name != '@everyone']),
                        inline=False)
        embed.set_thumbnail(url=ctx.message.guild.icon_url)
        await ctx.send(embed=embed)

    @servidor.error
    async def servidor_handler(self, ctx, error):
        if isinstance(error, MissingPermissions):
            embed = discord.Embed(title="Comando $servidor:", colour=discord.Colour(0x370c5e),
                                  description="Diz as informações sobre o servidor"
                                              "\n \n**Como usar: $servidor**")

            embed.set_author(name="Betina#9182",
                             icon_url=betina_icon)
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url=betina_icon)
            embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                            "ter a permissão de* ``"
                                                            "Administrador`` *para utilizar este comando!*",
                            inline=False)
            embed.add_field(name="📖**Exemplos:**", value="$servidor", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$serverinfo, $si.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")


    @commands.guild_only()
    @commands.command(pass_context=True, name='warn', aliases=['aviso', 'wrn'])
    @has_permissions(kick_members=True)
    async def warn(self, ctx, user: discord.User, *, arg: str = None):
        if arg == None:
            reason = 'Sem motivos específicados'
        else:
            reason = arg

        for current_user in report['users']:
            if current_user['name'] == user.name:
                current_user['reasons'].append(reason)
                if ctx.message.author.avatar_url_as(static_format='png')[54:].startswith('a_'):
                    avi = ctx.message.author.avatar_url.rsplit("?", 1)[0]
                else:
                    avi = ctx.message.author.avatar_url_as(static_format='png')

                embed = discord.Embed(title=f"*O {user.name} foi warnado pelo {ctx.message.author}*",
                                      colour=discord.Colour(0x370c5e), description=f"Pelo seguinte motivo: {reason}")

                embed.set_author(name=f"{ctx.message.author}", icon_url=f"{avi}")
                embed.set_footer(text="Betina Brazilian Bot", icon_url=betina_icon)

                await ctx.send(embed=embed, delete_after=10)
                break
        else:
            report['users'].append({
                'name': user.name,
                'reasons': [reason, ]
            })
            if ctx.message.author.avatar_url_as(static_format='png')[54:].startswith('a_'):
                avi = ctx.message.author.avatar_url.rsplit("?", 1)[0]
            else:
                avi = ctx.message.author.avatar_url_as(static_format='png')

            embed = discord.Embed(title=f"*O {user.name} foi warnado pelo {ctx.message.author}*",
                                  colour=discord.Colour(0x370c5e), description=f"Pelo seguinte motivo: {reason}")

            embed.set_author(name=f"{ctx.message.author}", icon_url=f"{avi}")
            embed.set_footer(text="Betina Brazilian Bot", icon_url=betina_icon)

            await ctx.send(embed=embed, delete_after=10)
        with open('reports.json', 'w+') as f:
            json.dump(report, f)


    @warn.error
    async def warn_handler(self, ctx, error):
        if isinstance(error, MissingPermissions):
            embed = discord.Embed(title="Comando $warn:", colour=discord.Colour(0x370c5e),
                                  description="Dá um warn no usuário"
                                              "\n \n**Como usar: $warn <usuário> <motivo> (opcional)**")

            embed.set_author(name="Betina#9182",
                             icon_url=betina_icon)
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url=betina_icon)
            embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                            "ter a permissão de* ``"
                                                            "Expulsar membros`` *para utilizar este comando!*",
                            inline=False)
            embed.add_field(name="📖**Exemplos:**", value="$warn @fulano xingou o moderador", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$aviso, $wrn.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")

        elif isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'user':
                embed = discord.Embed(title="Comando $warn:", colour=discord.Colour(0x370c5e),
                                      description="Dá um warn no usuário"
                                                  "\n \n**Como usar: $warn <usuário> <motivo> (opcional)**")

                embed.set_author(name="Betina#9182",
                                 icon_url=betina_icon)
                embed.set_footer(text="Betina Brazilian Bot",
                                 icon_url=betina_icon)
                embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                                "ter a permissão de* ``"
                                                                "Expulsar membros`` *para utilizar este comando!*",
                                inline=False)
                embed.add_field(name="📖**Exemplos:**", value="$warn @fulano xingou o moderador", inline=False)
                embed.add_field(name="🔀**Outros Comandos**", value="``$aviso, $wrn.``", inline=False)

                msg = await ctx.send(embed=embed)
                await msg.add_reaction("❓")


    @commands.guild_only()
    @commands.command(pass_context=True, name='warnings', aliases=['avisos', 'wrns'])
    @has_permissions(kick_members=True)
    async def warnings(self, ctx, user: discord.User):
        if user == None:
            embed = discord.Embed(title="Comando $warnings:", colour=discord.Colour(0x370c5e),
                                  description="Diz quantos warnings um usuário recebeu"
                                              "\n \n**Como usar: $warnings <usuário>**")

            embed.set_author(name="Betina#9182",
                             icon_url=betina_icon)
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url=betina_icon)
            embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                            "ter a permissão de* ``"
                                                            "Expulsar membros`` *para utilizar este comando!*",
                            inline=False)
            embed.add_field(name="📖**Exemplos:**", value="$warnings @fulano\n$warnings @sicrano", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$avisos, $wrns.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")
            return
        else:
            for current_user in report['users']:
                if user.name == current_user['name']:
                    if len(current_user['reasons']) == 1:
                        await ctx.send(f"{user.name} foi warnado {len(current_user['reasons'])} vez : {' ,'.join(current_user['reasons'])}")
                        break
                    else:
                        await ctx.send(f"{user.name} foi warnado {len(current_user['reasons'])} vezes : {' ,'.join(current_user['reasons'])}")
                        break
            else:
                await ctx.send(f"{user.name} nunca recebeu um warn!")


    @warnings.error
    async def warnings_handler(self, ctx, error):
        if isinstance(error, MissingPermissions):
            embed = discord.Embed(title="Comando $warnings:", colour=discord.Colour(0x370c5e),
                                  description="Diz quantos warnings o usuário levou"
                                              "\n \n**Como usar: $warnings <usuário>**")

            embed.set_author(name="Betina#9182",
                             icon_url=betina_icon)
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url=betina_icon)
            embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                            "ter a permissão de* ``"
                                                            "Expulsar membros`` *para utilizar este comando!*",
                            inline=False)
            embed.add_field(name="📖**Exemplos:**", value="$warnings @fulano\n$warnings @sicrano", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$avisos, $wrns.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")

        elif isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'user':
                embed = discord.Embed(title="Comando $warnings:", colour=discord.Colour(0x370c5e),
                                      description="Diz quantos warnings o usuário levou"
                                                  "\n \n**Como usar: $warnings <usuário>**")

                embed.set_author(name="Betina#9182",
                                 icon_url=betina_icon)
                embed.set_footer(text="Betina Brazilian Bot",
                                 icon_url=betina_icon)
                embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                                "ter a permissão de* ``"
                                                                "Expulsar membros`` *para utilizar este comando!*",
                                inline=False)
                embed.add_field(name="📖**Exemplos:**", value="$warnings @fulano\n$warnings @sicrano", inline=False)
                embed.add_field(name="🔀**Outros Comandos**", value="``$avisos, $wrns.``", inline=False)

                msg = await ctx.send(embed=embed)
                await msg.add_reaction("❓")


    @commands.guild_only()
    @commands.command(name='mute', aliases=['mutar', 'silenciar'])
    @has_permissions(kick_members=True, manage_roles=True)
    async def mute(self, ctx, member: discord.Member, time: int = 1):
        await ctx.message.delete()
        roles = [cargos.name for cargos in member.roles if cargos.name != "@everyone"]
        cargos_dos_mutados[str(member.id)] = roles
        for cargos in roles:
            atirar = discord.utils.get(ctx.guild.roles, name=str(cargos))
            await member.remove_roles(atirar)

        role = discord.utils.get(ctx.guild.roles, name='Mutado')
        if role not in ctx.guild.roles:
            await ctx.guild.create_role(name='Mutado', colour=discord.Colour(0x36393F), reason='Foi criado para mutar os usuários')
            await member.add_roles(role)

        await member.add_roles(role)

        with open('mutados.json', 'w') as file:
            json.dump(cargos_dos_mutados, file)

    @mute.error
    async def mute_handler(self, ctx, error):
        if isinstance(error, MissingPermissions):
            embed = discord.Embed(title="Comando $mute:", colour=discord.Colour(0x370c5e),
                                  description="Muta o usuário"
                                              "\n \n**Como usar: $mute <usuário>**")

            embed.set_author(name="Betina#9182",
                             icon_url=betina_icon)
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url=betina_icon)
            embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                            "ter a permissão de* ``"
                                                            "Expulsar membros e Gerenciar cargos"
                                                            "`` *para utilizar este comando!\n"
                                                            "Eu também preciso de estar com o cargo acima do usuário"
                                                            " a ser mutado!*",
                            inline=False)
            embed.add_field(name="📖**Exemplos:**", value="$mute @fulano\n$mute @sicrano", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$mutar, $silenciar.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")

        elif isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'member':
                embed = discord.Embed(title="Comando $mute:", colour=discord.Colour(0x370c5e),
                                      description="Muta o usuário"
                                                  "\n \n**Como usar: $mute <usuário>**")

                embed.set_author(name="Betina#9182",
                                 icon_url=betina_icon)
                embed.set_footer(text="Betina Brazilian Bot",
                                 icon_url=betina_icon)
                embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                                "ter a permissão de* ``"
                                                                "Expulsar membros e Gerenciar cargos"
                                                                "`` *para utilizar este comando!\n"
                                                                "Eu também preciso de estar com o cargo acima do usuário"
                                                                " a ser mutado!*",
                                inline=False)
                embed.add_field(name="📖**Exemplos:**", value="$mute @fulano\n$mute @sicrano", inline=False)
                embed.add_field(name="🔀**Outros Comandos**", value="``$mutar, $silenciar.``", inline=False)

                msg = await ctx.send(embed=embed)
                await msg.add_reaction("❓")


    @commands.guild_only()
    @commands.command(name='unmute', aliases=['desmutar', 'semsilenciar'])
    @has_permissions(kick_members=True, manage_roles=True)
    async def unmute(self, ctx, member: discord.Member, time: int = 1):
        await ctx.message.delete()
        if str(member.id) not in cargos_dos_mutados:
            return
        for cargos in cargos_dos_mutados[str(member.id)]:
            adicionar = discord.utils.get(ctx.guild.roles, name=str(cargos))
            await member.add_roles(adicionar)
        mute = discord.utils.get(ctx.guild.roles, name='Mutado')
        await member.remove_roles(mute)
        del cargos_dos_mutados[str(member.id)]
        with open('mutados.json', 'w') as file:
            json.dump(cargos_dos_mutados, file)

    @unmute.error
    async def mute_handler(self, ctx, error):
        if isinstance(error, MissingPermissions):
            embed = discord.Embed(title="Comando $unmute:", colour=discord.Colour(0x370c5e),
                                  description="Tira o mute do usuário"
                                              "\n \n**Como usar: $unmute <usuário>**\n \n"
                                              "Para utilizar corretamente, redefina as permissões do cargo ``everyone``"
                                              " para nenhuma permissão.")

            embed.set_author(name="Betina#9182",
                             icon_url=betina_icon)
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url=betina_icon)
            embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                            "ter a permissão de* ``"
                                                            "Expulsar membros e Gerenciar"
                                                            " cargos`` *para utilizar este comando!*",
                            inline=False)
            embed.add_field(name="📖**Exemplos:**", value="$unmute @fulano\n$unmute @sicrano", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$desmutar, $semsilenciar.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")

        elif isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'member':
                embed = discord.Embed(title="Comando $unmute:", colour=discord.Colour(0x370c5e),
                                      description="Tira o mute do usuário"
                                                  "\n \n**Como usar: $unmute <usuário>**\n \n"
                                                  "Para utilizar corretamente, redefina as permissões do cargo ``everyone``"
                                                  " para nenhuma permissão.")

                embed.set_author(name="Betina#9182",
                                 icon_url=betina_icon)
                embed.set_footer(text="Betina Brazilian Bot",
                                 icon_url=betina_icon)
                embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                                "ter a permissão de* ``"
                                                                "Expulsar membros e Gerenciar"
                                                                " cargos`` *para utilizar este comando!*",
                                inline=False)
                embed.add_field(name="📖**Exemplos:**", value="$unmute @fulano\n$unmute @sicrano", inline=False)
                embed.add_field(name="🔀**Outros Comandos**", value="``$desmutar, $semsilenciar.``", inline=False)

                msg = await ctx.send(embed=embed)
                await msg.add_reaction("❓")


    @commands.guild_only()
    @commands.command(name='sugestão', aliases=['suggestion', 'sug'])
    async def suggestion(self, ctx, *, arg: str):
        if ctx.message.author.avatar_url_as(static_format='png')[54:].startswith('a_'):
            avi = ctx.message.author.avatar_url.rsplit("?", 1)[0]
        else:
            avi = ctx.message.author.avatar_url_as(static_format='png')

        await ctx.message.delete()
        embed = discord.Embed(title="Sugestão: ", colour=discord.Colour(0x370c5e),
                              description=f"{arg}")
        embed.set_footer(text="{}".format(ctx.message.author), icon_url=avi)
        mensagem = await ctx.send(embed=embed)
        await mensagem.add_reaction('✅')
        await mensagem.add_reaction('❌')


    @suggestion.error
    async def suggestion_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'arg':
                embed = discord.Embed(title="Comando $sugestão:", colour=discord.Colour(0x370c5e),
                                      description="Começa a votação sobre uma sugestão!"
                                                  "\n \n**Como usar: $sugestão <mensagem>**")

                embed.set_author(name="Betina#9182",
                                 icon_url=betina_icon)
                embed.set_footer(text="Betina Brazilian Bot",
                                 icon_url=betina_icon)

                embed.add_field(name="📖**Exemplos:**", value="$sugestão que tal adicionar uma função e sugestão"
                                                              "\n$sugestão criar um canal de jogos", inline=False)
                embed.add_field(name="🔀**Outros Comandos**", value="``$sug, $suggestion.``", inline=False)

                msg = await ctx.send(embed=embed)
                await msg.add_reaction("❓")


def setup(client):
    client.add_cog(Administração(client))
