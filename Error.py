import discord
import sys
import traceback
import math

from discord.ext import commands
from horario import *
from difflib import SequenceMatcher

betina_icon = ""


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


class Error:
    def __init__(self, client):
        self.client = client

    async def on_command_error(self, ctx, error):

        ignored = (commands.CommandNotFound)


        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            comandos = [x.name for x in self.client.commands]
            possiveis = []
            possivel = str(error).split(' ')[1]
            for comando in comandos:
                if similar(possivel, comando) > 0.4:
                    possiveis.append(comando)
            if not possiveis:
                return await ctx.message.add_reaction("deny:540714208111755265")
            else:
                await ctx.send(f'```Olá usuário, não encontrei o comando {possivel}.'
                               f'\nVocê quis dizer: 'f'{possiveis}```')
            return


        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == 'tag list':  # Check if the command being invoked is 'tag list'
                if ctx.message.author.avatar_url_as(static_format='png')[54:].startswith('a_'):
                    avi = ctx.message.author.avatar_url.rsplit("?", 1)[0]
                else:
                    avi = ctx.message.author.avatar_url_as(static_format='png')

                embed = discord.Embed(title=f"ERRO!", colour=discord.Colour(0x370c5e))

                embed.set_author(name=f"{ctx.message.author}", icon_url=f"{avi}")
                embed.set_footer(icon_url=betina_icon,
                                 text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                           self.client.user.name,
                                                                                           year()))

                return await ctx.send(embed=embed, delete_after=10)

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
