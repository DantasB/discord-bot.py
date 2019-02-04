import discord
import json

from discord.utils import get
from discord.ext.commands import has_permissions, MissingPermissions
from horario import*
from discord.ext import commands


betina_icon = "https://images.discordapp.net/avatars/527565353199337474/4c21db45f96d92a2b8214b5f93d059c4.png?size=256"

numero = {}


class Tickets:
    def __init__(self, client):
        self.client = client

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name='openticket', aliases=['newticket'])
    @commands.guild_only()
    async def criaticket(self, ctx, nome: discord.Member = None):
        if 'criaticket' not in numero:
            numero['criaticket'] = 1
        else:
            numero['criaticket'] += 1
        resultado = numero['criaticket']
        if nome is None:
            overwrites = {
                ctx.message.guild.default_role: discord.PermissionOverwrite(read_messages=False, add_reactions=False,
                                                                            send_messages=False, attach_files=False),
                ctx.message.author: discord.PermissionOverwrite(read_messages=True, add_reactions=False,
                                                                send_messages=True, attach_files=True)
            }
            await ctx.message.guild.create_text_channel(f'ticket número {resultado}', overwrites=overwrites)
        else:
            overwrites = {
                ctx.message.guild.default_role: discord.PermissionOverwrite(read_messages=False, add_reactions=False,
                                                                            send_messages=False, attach_files=False),
                ctx.message.author: discord.PermissionOverwrite(read_messages=True, add_reactions=False,
                                                                send_messages=True, attach_files=True),
                nome: discord.PermissionOverwrite(read_messages=True, add_reactions=False,
                                                                send_messages=True, attach_files=True)
            }
            await ctx.message.guild.create_text_channel(f'ticket número {resultado}', overwrites=overwrites)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name='closeticket', aliases=['fechaticket'])
    @commands.guild_only()
    async def delticket(self, ctx):
        resultado = numero['criaticket']
        if ctx.message.channel.name != f'ticket-número-{resultado}':
            mensagem = f"<:stop:540852590083178497> **Este comando só pode deletar o canal de nome:" \
                f" ``ticket-número-{resultado}``. Para isso você precisa estar nele.**"
            return await ctx.send(mensagem)
        await ctx.message.channel.delete()

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name='infoticket', aliases=['ticketinfo'])
    @commands.guild_only()
    async def info(self, ctx):
        resultado = numero['criaticket']
        f = open(f"information{resultado}.txt", "w+")
        resultado = numero['criaticket']
        c = 0
        author = ctx.author
        async for message in ctx.message.channel.history(reverse=True):
            c += 1
            if ctx.message.channel.name != f'ticket-número-{resultado}':
                mensagem = f"<:stop:540852590083178497> **Este comando só pode obter informações do canal de nome:" \
                    f" ``Ticket número: 45021``. Para isso você precisa estar nele.**"
                return await ctx.send(mensagem)
                break
            f.write(f"Mensagem {c}: {message.author} disse: {message.content}\n")
        f.close()
        await author.send(file=discord.File(f'information{resultado}.txt'))


def setup(client):
    client.add_cog(Tickets(client))
