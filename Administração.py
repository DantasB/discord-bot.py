import random
import time
import discord
import datetime
import aiohttp

from discord.ext import commands
from forex_python.converter import CurrencyRates
from dhooks import Webhook
from discord.utils import get
from discord.ext.commands import has_permissions, MissingPermissions

banhammer = ['https://media.giphy.com/media/fe4dDMD2cAU5RfEaCU/giphy.gif',
             'https://media.giphy.com/media/qPD4yGsrc0pdm/giphy.gif',
             'https://media.giphy.com/media/e3WNjAUKGNGoM/giphy.gif',
             'https://media.giphy.com/media/xT5LMDzs9xYtHXeItG/giphy.gif',
             'https://media.giphy.com/media/HXcALJVPgaR4A/giphy.gif',
             'https://media.giphy.com/media/3o751XbGLXpORSxtQY/giphy.gif',
             'https://media.giphy.com/media/uC9e2ojJn1ZXW/giphy.gif',
             'https://media.giphy.com/media/qpqgxqebabVjq/giphy.gif']
omg = ['https://media.giphy.com/media/5VKbvrjxpVJCM/giphy.gif',
       'https://media.giphy.com/media/ygCJ5Bul73NArGOSFN/giphy.gif',
       'https://media.giphy.com/media/oYtVHSxngR3lC/giphy.gif',
       'https://media.giphy.com/media/1ykTax6hrAKpTQ0Mnb/giphy.gif',
       'https://media.giphy.com/media/PUBxelwT57jsQ/giphy.gif',
       'https://media.giphy.com/media/6b9DUG33FIF74J9H2O/giphy.gif',
       'https://media.giphy.com/media/sR2YaENch4sog/giphy.gif',
       'https://media.giphy.com/media/bGPTxLislwm3u/giphy.gif',
       'https://media.giphy.com/media/WuGSL4LFUMQU/giphy.gif',
       'https://media.giphy.com/media/3ohzdMk3uz9WSpdTvW/giphy.gif',
       'https://media.giphy.com/media/vQqeT3AYg8S5O/giphy.gif',
       'https://media.giphy.com/media/57ZvMMkuBIVMlU88Yh/giphy.gif',
       'https://media.giphy.com/media/MuTenSRsJ7TQQ/giphy.gif',
       'https://media.giphy.com/media/fpXxIjftmkk9y/giphy.gif',
       'https://media.giphy.com/media/3o72F8t9TDi2xVnxOE/giphy.gif',
       'https://media.giphy.com/media/1yMQuIU3lQLPpXCK7t/giphy.gif',
       'https://media.giphy.com/media/5p2wQFyu8GsFO/giphy.gif',
       'https://media.giphy.com/media/xT9IgAmXNP23ftHIsM/giphy.gif',
       'https://media.giphy.com/media/QjrrSbYaqgi1q/giphy.gif',
       'https://media.giphy.com/media/26xBC0xYwcSWzTL2g/giphy.gif',
       'https://media.giphy.com/media/m48e80jhv4Kk/giphy.gif',
       'https://media.giphy.com/media/l1J9EBp9Dcd6jtsbu/giphy.gif',
       'https://media.giphy.com/media/hPUm88VMjUIM0/giphy.gif',
       'https://media.giphy.com/media/vmGJdiqLTG4lq/giphy.gif',
       'https://media.giphy.com/media/OzHKDlB6CqwZG/giphy.gif']


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
        await ctx.channel.purge(limit=amount + 1)

    @apaga.error
    async def apaga_handler(self, ctx, error):
        if isinstance(error, MissingPermissions):
            embed = discord.Embed(title="Comando $apaga:", colour=discord.Colour(0x370c5e),
                                  description="Apaga n+1 linhas acima da ultima mensagem\n \n**Como usar: $apaga <linhas>**")

            embed.set_author(name="Betina#9182",
                             icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
            embed.add_field(name="👮**Permissões:**", value="*Você precisa "
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
                                 icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
                embed.set_footer(text="Betina Brazilian Bot",
                                 icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
                embed.add_field(name="👮**Permissões:**", value="*Você precisa "
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
    async def ban(self, ctx, member: discord.User, *, arg):
        reason = arg
        gif1 = random.choice(banhammer)
        gif2 = random.choice(omg)
        msg1 = '**Você estava tentando se banir ?**'
        msg2 = '{} foi banido do servidor {} pelo seguinte motivo: {}'.format(member, ctx.guild.name, reason)
        if member == ctx.message.author:

            embed = discord.Embed(title="**Pensativa...**", colour=discord.Colour(0x370c5e),
                                  description="{}".format(msg1))
            embed.set_image(url="{}".format(gif2))
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url="https://images.discordapp.net/avatars/"
                                      "527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
            await ctx.channel.send(embed=embed)
            return
        else:
            embed = discord.Embed(title="**BAN!**", colour=discord.Colour(0x370c5e), description="{}".format(msg2))
            embed.set_image(url="{}".format(gif1))
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url="https://images.discordapp.net/avatars/"
                                      "527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
            if not member.bot:
                await member.send(embed=embed)
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
                                              "\n \n**Como usar: $bane <usuário> <motivo>**")

            embed.set_author(name="Betina#9182",
                             icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
            embed.add_field(name="👮**Permissões:**", value="*Você precisa "
                                                            "ter a permissão de* ``"
                                                            "Banir membros`` *para utilizar este comando!*",
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
                                                  "\n \n**Como usar: $bane <usuário> <motivo(opcional>**")

                embed.set_author(name="Betina#9182",
                                 icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
                embed.set_footer(text="Betina Brazilian Bot",
                                 icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
                embed.add_field(name="👮**Permissões:**", value="*Você precisa "
                                                                "ter a permissão de* ``"
                                                                "Banir membros`` *para utilizar este comando!*",
                                inline=False)
                embed.add_field(name="📖**Exemplos:**", value="$ban @fulano\n$ban @fulano xingou o moderador",
                                inline=False)
                embed.add_field(name="🔀**Outros Comandos**", value="``$bane, $banir.``", inline=False)

                msg = await ctx.send(embed=embed)
                await msg.add_reaction("❓")


            elif error.param.name == 'arg':
                embed = discord.Embed(title="Comando $ban:", colour=discord.Colour(0x370c5e),
                                      description="Bane o usuário do servidor por um motivo"
                                                  "\n \n**Como usar: $bane <usuário> <motivo(opcional>**")

                embed.set_author(name="Betina#9182",
                                 icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
                embed.set_footer(text="Betina Brazilian Bot",
                                 icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
                embed.add_field(name="👮**Permissões:**", value="*Você precisa "
                                                                "ter a permissão de* ``"
                                                                "Banir membros`` *para utilizar este comando!*",
                                inline=False)
                embed.add_field(name="📖**Exemplos:**", value="$ban @fulano\n$ban @fulano xingou o moderador",
                                inline=False)
                embed.add_field(name="🔀**Outros Comandos**", value="``$bane, $banir.``", inline=False)

                msg = await ctx.send(embed=embed)
                await msg.add_reaction("❓")

    @commands.guild_only()
    @commands.command(name='cargo', aliases=['CARGO'
        , 'Cargo', 'CArgo', 'CARgo', 'CARGo', 'cARGO', 'caRGO', 'carGO', 'cargO'])
    async def cargo(self, ctx):
        pass

    @commands.guild_only()
    @commands.command()
    async def ajuda(self, ctx):
        await ctx.invoke(self.client.get_command("help"))


def setup(client):
    client.add_cog(Administração(client))
