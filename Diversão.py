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

dead = [] #giphy dead links
alive = [] #giphy alive links


class Diversão:
    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.command(name='ppt', aliases=['Rsp', 'jogo'])
    async def ppt(self, ctx, msg: str):
        t = ['pedra', 'papel', 'tesoura']
        channel = ctx.channel
        computer = t[random.randint(0, 2)]
        player = msg.lower()
        await ctx.send('``Você escolheu {}{}``'.format(player[:1].upper(), player[1:]))
        await ctx.channel.trigger_typing()
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
    async def ppt_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'msg':
                embed = discord.Embed(title="Comando $ppt:", colour=discord.Colour(0x370c5e),
                                      description="Inicia um jogo de Pedra, Papel ou tesoura com o bot\n \n**Como usar"
                                                  ": $ppt <Pedra, Papel ou Tesoura>**")

                embed.set_author(name="Betina#9182",
                                 icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
                embed.set_footer(text="Betina Brazilian Bot",
                                 icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")

                embed.add_field(name="📖**Exemplos:**", value="$ppt pedra\n$ppt tesoura", inline=False)
                embed.add_field(name="🔀**Outros Comandos**", value="``$Rsp, $jogo.``", inline=False)

                msg = await ctx.send(embed=embed)
                await msg.add_reaction("❓")

    @commands.guild_only()
    @commands.command(name='rola', aliases=['roll', 'dice'])
    async def rola(self, ctx, a: int):
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
    async def rola_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'a':
                embed = discord.Embed(title="Comando $rola:", colour=discord.Colour(0x370c5e),
                                      description="Rola um dado de n lados\n \n**Como usar"
                                                  ": $rola <n>**")

                embed.set_author(name="Betina#9182",
                                 icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
                embed.set_footer(text="Betina Brazilian Bot",
                                 icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
                embed.add_field(name="❗**Atenção:**", value="Escolha um dado que existe!", inline=False)
                embed.add_field(name="📖**Exemplos:**", value="$rola 10\n$rola 4", inline=False)
                embed.add_field(name="🔀**Outros Comandos**", value="``$roll, $dice.``", inline=False)

                msg = await ctx.send(embed=embed)
                await msg.add_reaction("❓")

    @commands.guild_only()
    @commands.command(name='roletarussa', aliases=['roulette', 'rr'])
    async def roletarussa(self, ctx, a: int):
        gif1 = random.choice(dead)
        gif2 = random.choice(alive)
        msg1 = '``Que pena, você morreu!``'
        msg2 = '``Parabéns, você ainda não morreu!``'
        numero = random.randint(1, 6)
        if a < 1 or a > 6:
            embed = discord.Embed(title="Comando $roletarussa:", colour=discord.Colour(0x370c5e),
                                  description="Inicia um jogo de roleta russa contra o bot\n \n**Como usar"
                                              ": $rola <n>**")

            embed.set_author(name="Betina#9182",
                             icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
            embed.set_footer(text="Betina Brazilian Bot",
                             icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
            embed.add_field(name="❗**Atenção:**", value="Escolha um número entre 1 e 6", inline=False)
            embed.add_field(name="📖**Exemplos:**", value="$roletarussa 6\n$roletarussa 1", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``$roulette, $rr.``", inline=False)

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❓")
        else:
            if (a == numero):
                embed = discord.Embed(title="**Morte!**", colour=discord.Colour(0x370c5e),
                                      description="{}".format(msg1))
                embed.set_image(url="{}".format(gif1))
                embed.set_footer(text="Betina Brazilian Bot",
                                 icon_url="https://images.discordapp.net/avatars/"
                                          "527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
                msg = await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="**Sobreviveu!**", colour=discord.Colour(0x370c5e),
                                      description="{}".format(msg2))
                embed.set_image(url="{}".format(gif2))
                embed.set_footer(text="Betina Brazilian Bot",
                                 icon_url="https://images.discordapp.net/avatars/"
                                          "527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
                msg = await ctx.send(embed=embed)

    @roletarussa.error
    async def roletarussa_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'a':
                embed = discord.Embed(title="Comando $roletarussa:", colour=discord.Colour(0x370c5e),
                                      description="Inicia um jogo de roleta russa contra o bot\n \n**Como usar"
                                                  ": $rola <n>**")

                embed.set_author(name="Betina#9182",
                                 icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
                embed.set_footer(text="Betina Brazilian Bot",
                                 icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
                embed.add_field(name="❗**Atenção:**", value="Escolha um número entre 1 e 6", inline=False)
                embed.add_field(name="📖**Exemplos:**", value="$roletarussa 6\n$roletarussa 1", inline=False)
                embed.add_field(name="🔀**Outros Comandos**", value="``$roulette, $rr.``", inline=False)

                msg = await ctx.send(embed=embed)
                await msg.add_reaction("❓")

    @commands.guild_only()
    @commands.command()
    async def faustao(self, ctx):
        with open("faustop.png", "rb") as imageFile:
            file = bytearray(imageFile.read())
        channel = ctx.channel
        async with aiohttp.ClientSession() as session:
            webhook = await channel.create_webhook(name='Faustão', avatar=file)

        await webhook.send("Esta Fera Bicho!")

    @commands.guild_only()
    @commands.command()
    async def bolsonaro(self, ctx):
        with open("bolsoboy.png", "rb") as imageFile:
            file = bytearray(imageFile.read())
        channel = ctx.channel
        async with aiohttp.ClientSession() as session:
            webhook = await channel.create_webhook(name='Bolsonaro', avatar=file)

        await webhook.send("Taokei?")

    @commands.guild_only()
    @commands.command(name='moeda', aliases=['coin', 'ht'])
    async def moeda(self, ctx):
        """Heads and Tails!"""
        resultado = random.randint(1, 2)
        if resultado == 1:
            await ctx.send('😃')
        else:
            await ctx.send('👑')


def setup(client):
    client.add_cog(Diversão(client))
