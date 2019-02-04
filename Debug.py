import discord
import random
import json
import sys
import time

from datetime import datetime
from discord.ext import commands


class debug():
    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.command(name='eval')
    async def debug(self, ctx, *, args):
        if str(ctx.message.author.id) != '361993078938271759':
            await ctx.message.add_reaction("deny:540714208111755265")
            mensagem = f"<:stop:540852590083178497> **Você não tem permissão para utilizar esse comando**"
            return await ctx.send(mensagem)
        try:
            erro = f'```Python\n{eval(args)}```'
            await ctx.send(erro)

        except Exception as e:
            erro = f'```Python\n{str(e)}```'
            await ctx.send(erro)



def setup(client):
    client.add_cog(debug(client))
