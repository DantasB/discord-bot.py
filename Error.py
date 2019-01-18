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


class Error:
    def __init__(self, client):
        self.client = client

    async def on_command_error(self, ctx, error):

        if hasattr(ctx.command, 'on_error'):
            return

        ignored = (commands.CommandNotFound, commands.UserInputError)

        error = getattr(error, 'original', error)

        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            if ctx.message.author.avatar_url_as(static_format='png')[54:].startswith('a_'):
                avi = ctx.message.author.avatar_url.rsplit("?", 1)[0]
            else:
                avi = ctx.message.author.avatar_url_as(static_format='png')

            embed = discord.Embed(title=f"*Não consegui encontrar esse comando, {ctx.message.author}. "
            f"Tente utilizar o comando $ajuda para quais são os meus comandos*", colour=discord.Colour(0x370c5e))

            embed.set_author(name=f"{ctx.message.author}", icon_url=f"{avi}")
            embed.set_footer(text="Betina Brazilian Bot", icon_url='https://images.discordapp'
                                                                   '.net/avatars/527565353199337474/40042c09'
                                                                   'bb354a396928cb91e0288384.png?size=256')
            return await ctx.send(embed=embed)

        # For this error example we check to see where it came from...
        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == 'tag list':  # Check if the command being invoked is 'tag list'
                embed = discord.Embed(title=f"*Não consegui encontrar esse usuário, {ctx.message.author}. "
                f"Tente checar se utilizou o nome correto!*", colour=discord.Colour(0x370c5e))

                embed.set_author(name=f"{ctx.message.author}", icon_url=f"{avi}")
                embed.set_footer(text="Betina Brazilian Bot", icon_url='https://images.discordapp'
                                                                       '.net/avatars/527565353199337474/40042c09'
                                                                       'bb354a396928cb91e0288384.png?size=256')
                return await ctx.send(embed=embed)


        # All other Errors not returned come here... And we can just print the default TraceBack.
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


def setup(client):
    client.add_cog(Error(client))
