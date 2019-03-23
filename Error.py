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
import discord
import sys
import traceback
import math

from discord.ext import commands
from horario import *
from difflib import SequenceMatcher

betina_icon = "https://images.discordapp.net/avatars/527565353199337474/4c21db45f96d92a2b8214b5f93d059c4.png?size=256"


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


class Error(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def on_command_error(self, ctx, error):

        ignored = (commands.CommandNotFound)


        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            comandos = [x for x in self.client.all_commands]
            possiveis = []
            possivel = str(error).split(' ')[1]
            for comando in comandos:
                if similar(possivel, comando) > 0.4:
                    possiveis.append(comando)
            if not possiveis:
                return await ctx.message.add_reaction("deny:540714208111755265")
            else:
                valor = '\n-> $'.join([x for x in possiveis])
                return await ctx.send(f'```Olá usuário, não encontrei o comando {possivel}.'
                               f'\nVocê quis dizer:\n'f'-> ${valor}```')
            return


        elif isinstance(error, commands.BadArgument):
            mensagem = f"<:stop:540852590083178497> **Por favor, coloque um argumento válido!**\n **{error}**"
            return await ctx.send(mensagem)

        elif isinstance(error, commands.BotMissingPermissions):
            mensagem = f"<:stop:540852590083178497> **Eu não tenho permissão para executar esse comando.**"

            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                fmt = '{}, e {}'.format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = ' e '.join(missing)
            _message = "<:stop:540852590083178497> **Eu preciso dessas permissões" \
                       " para executar esse comando:** ``{}``".format(fmt)

            return await ctx.send(_message)

        elif isinstance(error, commands.CheckFailure):
            msg = f"<:stop:540852590083178497> **Você não tem permissão para" \
                f" executar esse comando.**"
            return await ctx.send(msg)

        elif isinstance(error, commands.CommandOnCooldown):
            msg = f"<:stop:540852590083178497> **Vamos com calma, " \
                f"apressadinho. Tente novamente em** ``{math.ceil(error.retry_after)}`` **segundos.**"
            return await ctx.send(msg)

        elif isinstance(error, discord.Forbidden):
            msg = f"<:stop:540852590083178497> **Eu não tenho permissão para" \
                f" executar esse comando.\n<:stop:540852590083178497> Tente colocar o meu cargo no topo" \
                f" dos outros cargos e checar minhas permissões**"
            return await ctx.send(msg)

        elif isinstance(error, commands.MissingPermissions):
            return

        elif isinstance(error, commands.MissingRequiredArgument):
            return

        elif isinstance(error, commands.UserInputError):
            msg = f"<:stop:540852590083178497> **Tente utilizar o argumento correto**"
            return await ctx.send(msg)

        elif isinstance(error, commands.TooManyArguments):
            return await ctx.send("<:stop:540852590083178497> Você colocou argumentos demais nessa função.")

        # All other Errors not returned come here... And we can just print the default TraceBack.
        print('Exception ignorada no comando: {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


def setup(client):
    client.add_cog(Error(client))
