import discord

from discord.ext import commands
from discord.utils import get
from discord.ext.commands import has_permissions, MissingPermissions
from horario import*

betina_icon = "https://images.discordapp.net/avatars/527565353199337474/4c21db45f96d92a2b8214b5f93d059c4.png?size=256"


class Donate:
    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.command()
    async def donateinfo(self, ctx):
        embed = discord.Embed(title="<:Panda_Pensando:536892775556317184> Sua ajuda será de bom grado ",
                              colour=discord.Colour(0xcfe0ff), description="Para aqueles que"
                                                                           " sabem a história da betina"
                                                                           " também sabem"
                                                                           " o quão difícil hostear "
                                                                           "um bot no discord. Então, "
                                                                           "preciso da ajuda de vocês "
                                                                           "com o menor custo que seja, "
                                                                           "somente para mostrar que é possível "
                                                                           "fazer o melhor para uma comunidade "
                                                                           "com pouco dinheiro. Todo o dinheiro "
                                                                           "será revertido em pagamento para um "
                                                                           "novo servidor, onde a betina deixará "
                                                                           "de ser hosteada em minha casa e irá "
                                                                           "para um local com mais internet e suporte "
                                                                           "24h de modo a ajudar vocês.")

        embed.set_image(url="https://media.giphy.com/media/hol56wxuWmRrO/giphy.gif")

        embed.set_footer(icon_url=betina_icon,
                         text="Usado às {} Horário de Brasília | © {} {} .".format(hora(),
                                                                                   self.client.user.name,
                                                                                   year()))

        embed.add_field(name="<:picpay:539988602692567051> **Picpay**", value="", inline=True)
        embed.add_field(name="<:PayPal:539988258839592971> **Paypal**", value="", inline=True)
        embed.add_field(name="**Outras formas:**", value="Basta me mandarem inbox que"
                                                                             " ficarei muito feliz"
                                                                             " com a mensagem de vocês"
                                                                             " ()", inline=True)
        embed.add_field(name="**Dicas, Artes ou Sugestões"
                             " para a Betina:**", value="[Servidor de Suporte](https://discord.gg/eZrzDfs)", inline=True)

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Donate(client))
