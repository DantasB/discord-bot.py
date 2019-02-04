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
