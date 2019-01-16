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

# gifs
angry = ['https://media.giphy.com/media/l1J9u3TZfpmeDLkD6/giphy.gif',
         'https://media.giphy.com/media/11tTNkNy1SdXGg/giphy.gif',
         'https://media.giphy.com/media/10UHehEC098kAE/giphy.gif',
         'https://media.giphy.com/media/88i7NElG87uXGpjpBr/giphy.gif',
         'https://media.giphy.com/media/3Fkw8DCq4eUxp31E4n/giphy.gif',
         'https://media.giphy.com/media/DvNwi41Iqrzos/giphy.gif',
         'https://media.giphy.com/media/WH85q8e201wlO/giphy.gif',
         'https://media.giphy.com/media/ZebTmyvw85gnm/giphy.gif',
         'https://media.giphy.com/media/xTiTnF6v2Th2GPmZ7q/giphy.gif',
         'https://media.giphy.com/media/ntjBjvfnakKJ2/giphy.gif',
         'https://media.giphy.com/media/OOezqqxPB8aJ2/giphy.gif',
         'https://media.giphy.com/media/10juQ7fAaQjuHS/giphy.gif',
         'https://media.giphy.com/media/Vzku9jyuef09G/giphy.gif',
         'https://media.giphy.com/media/pYI1hSqUdcBiw/giphy.gif',
         'https://media.giphy.com/media/11u2JnMZwQVm3S/giphy.gif',
         'https://media.giphy.com/media/8pMS5BXOUVZyo/giphy.gif',
         'https://media.giphy.com/media/3GCeasnPeeImI/giphy.gif',
         'https://media.giphy.com/media/eXUlPn1gmZavu/giphy.gif',
         'https://media.giphy.com/media/H9Mm0ULO8AtMc/giphy.gif',
         'https://media.giphy.com/media/Zaeyj0lscMhA4/giphy.gif',
         'https://media.giphy.com/media/ySVKduoNNFoRy/giphy.gif',
         'https://media.giphy.com/media/3oJpyi7wBpo0sV9V9C/giphy.gif',
         'https://media.giphy.com/media/26ufixlZznOaDs3ja/giphy.gif',
         'https://media.giphy.com/media/eb4WGfjWeIsgM/giphy.gif']
cave = ['https://media.giphy.com/media/7U9Jw8lHCZTQQ/giphy.gif',
        'https://media.giphy.com/media/GLjbMKJdoob60/giphy.gif',
        'https://media.giphy.com/media/8UYMQ5MCmuqXu/giphy.gif',
        'https://media.giphy.com/media/t0Da5LwHxxZwA/giphy.gif']
slap = ['https://media.giphy.com/media/3XlEk2RxPS1m8/giphy.gif',
        'https://media.giphy.com/media/vxvNnIYFcYqEE/giphy.gif'
    , 'https://media.giphy.com/media/RrLbvyvatbi36/giphy.gif',
        'https://media.giphy.com/media/55TZk1pnXsBQA/giphy.gif',
        'https://media.giphy.com/media/6Fad0loHc6Cbe/giphy.gif'
    , 'https://media.giphy.com/media/jX708Wo6abfC8/giphy.gif',
        'https://media.giphy.com/media/3wtc9qlgBxaq4/giphy.gif',
        'https://media.giphy.com/media/uqSU9IEYEKAbS/giphy.gif'
    , 'https://media.giphy.com/media/zvDT09xBhcuMo/giphy.gif',
        'https://media.giphy.com/media/4Nphcg0CCOfba/giphy.gif',
        'https://media.giphy.com/media/mEtSQlxqBtWWA/giphy.gif'
    , 'https://media.giphy.com/media/uG3lKkAuh53wc/giphy.gif',
        'https://media.giphy.com/media/j3iGKfXRKlLqw/giphy.gif',
        'https://media.giphy.com/media/tV0HkQju9zHR6/giphy.gif'
    , 'https://media.giphy.com/media/w5FSoU86sXRFm/giphy.gif',
        'https://media.giphy.com/media/s5zXKfeXaa6ZO/giphy.gif',
        'https://media.giphy.com/media/wXgBk2fM696gM/giphy.gif'
    , 'https://media.giphy.com/media/kIagrwoLKaLYc/giphy.gif',
        'https://media.giphy.com/media/Y6c59hTH3TJoA/giphy.gif',
        'https://media.giphy.com/media/l0MYthTiOGtg1zsT6/giphy.gif',
        'https://media.giphy.com/media/q8AiNhQJVyDoQ/giphy.gif',
        'https://media.giphy.com/media/l1Avzvn1gWvk1pwsM/giphy.gif']
dance = ['https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif',
         'https://media.giphy.com/media/xJjs8eGVbjNYY/giphy.gif',
         'https://media.giphy.com/media/j3gsT2RsH9K0w/giphy.gif',
         'https://media.giphy.com/media/jzaZ23z45UxK8/giphy.gif',
         'https://media.giphy.com/media/l3V0lsGtTMSB5YNgc/giphy.gif',
         'https://media.giphy.com/media/RX7N03MEUafW8/giphy.gif',
         'https://media.giphy.com/media/TfKfqjt2i4GIM/giphy.gif',
         'https://media.giphy.com/media/3ornkdtVzQfIRpwfug/giphy.gif',
         'https://media.giphy.com/media/l0HUqsz2jdQYElRm0/giphy.gif',
         'https://media.giphy.com/media/fIXtW1VlTyPba/giphy.gif',
         'https://media.giphy.com/media/xUA7b2S7SxhM1cGdsQ/giphy.gif',
         'https://media.giphy.com/media/5xaOcLGvzHxDKjufnLW/giphy.gif',
         'https://media.giphy.com/media/SGkufeMafyuBhIw796/giphy.gif',
         'https://media.giphy.com/media/6fScAIQR0P0xW/giphy.gif',
         'https://media.giphy.com/media/BkL4Vyz0z2iYQMhwFw/giphy.gif',
         'https://media.giphy.com/media/Pjs1kqtH1KTaU/giphy.gif',
         'https://media.giphy.com/media/MVDPX3gaKFPuo/giphy.gif',
         'https://media.giphy.com/media/elbwkxVuAfGiQ/giphy.gif',
         'https://media.giphy.com/media/KPgOYtIRnFOOk/giphy.gif',
         'https://media.giphy.com/media/MLZYKauKxeqKk/giphy.gif']
hug = ['https://media.giphy.com/media/EvYHHSntaIl5m/giphy.gif',
       'https://media.giphy.com/media/42YlR8u9gV5Cw/giphy.gif',
       'https://media.giphy.com/media/llmZp6fCVb4ju/giphy.gif',
       'https://media.giphy.com/media/lXiRKBj0SAA0EWvbG/giphy.gif',
       'https://media.giphy.com/media/16bJmyPvRbCDu/giphy.gif',
       'https://media.giphy.com/media/6uEE79cXjssla/giphy.gif',
       'https://media.giphy.com/media/3oriNWfntn0yXfOW6A/giphy.gif',
       'https://media.giphy.com/media/l4FGy5UyZ1KnVZ7BC/giphy.gif',
       'https://media.giphy.com/media/8tpiC1JAYVMFq/giphy.gif',
       'https://media.giphy.com/media/QbkL9WuorOlgI/giphy.gif',
       ' https://media.giphy.com/media/3oEdv4hwWTzBhWvaU0/giphy.gif',
       'https://media.giphy.com/media/8KKRIP5ZHUo2k/giphy.gif',
       'https://media.giphy.com/media/fyx8vjZc2ZvoY/giphy.gif',
       ' https://media.giphy.com/media/gnXG2hODaCOru/giphy.gif',
       'https://media.giphy.com/media/oaQgdY6DCGKre/giphy.gif'
    , 'https://media.giphy.com/media/VGACXbkf0AeGs/giphy.gif',
       'https://media.giphy.com/media/3oz8xJfB6XGBwOA8HS/giphy.gif',
       'https://media.giphy.com/media/l0HlKDJgw54pm4hgY/giphy.gif',
       'https://media.giphy.com/media/kooPUWvhaGe7C/giphy.gif',
       'https://media.giphy.com/media/OiKAQbQEQItxK/giphy.gif']
kiss = ['https://media.giphy.com/media/l2Je2M4Nfrit0L7sQ/giphy.gif',
        'https://media.giphy.com/media/bCY7hoYdXmD4c/giphy.gif',
        'https://media.giphy.com/media/frHK797nhEUow/giphy.gif'
    , 'https://media.giphy.com/media/10UUe8ZsLnaqwo/giphy.gif',
        'https://media.giphy.com/media/HhPJIIpNIGXHq/giphy.gif',
        'https://media.giphy.com/media/124gj4XvM8f3fa/giphy.gif',
        'https://media.giphy.com/media/udiIFmPkJQzkI/giphy.gif',
        'https://media.giphy.com/media/lTQF0ODLLjhza/giphy.gif',
        'https://media.giphy.com/media/108M7gCS1JSoO4/giphy.gif',
        'https://media.giphy.com/media/TftAZamDxqUdq/giphy.gif',
        'https://media.giphy.com/media/rDSIz6yb2JIHe/giphy.gif',
        'https://media.giphy.com/media/tCWMUAuZLMvKg/giphy.gif',
        'https://media.giphy.com/media/wf4UuPMYnwBck/giphy.gif'
    , 'https://media.giphy.com/media/ROnAaM2l5Rayk/giphy.gif',
        'https://media.giphy.com/media/6uFetT0Kw9Isg/giphy.gif',
        'https://media.giphy.com/media/3o85xrApQMfuCr0D60/giphy.gif',
        'https://media.giphy.com/media/FjBnClwCFoity/giphy.gif',
        'https://media.giphy.com/media/KH1CTZtw1iP3W/giphy.gif'
    , 'https://media.giphy.com/media/wDEWXcisSjrQQ/giphy.gif',
        'https://media.giphy.com/media/xAVhxModUI2Pu/giphy.gif']
attack = ['https://media.giphy.com/media/Eq49yQGJL835K/giphy.gif',
          'https://media.giphy.com/media/rVYbN0uxznAaI/giphy.gif',
          'https://media.giphy.com/media/67tQ4947zCIQo/giphy.gif',
          'https://media.giphy.com/media/3o8doYRSVzXu3l000g/giphy.gif',
          'https://media.giphy.com/media/l0MYOheN243NvYkco/giphy.gif',
          'https://media.giphy.com/media/KZp3Mj1AoTHCo/giphy.gif',
          'https://media.giphy.com/media/hiOTu0M0ILSIU/giphy.gif',
          'https://media.giphy.com/media/o2Lwy4g7Dzptu/giphy.gif',
          'https://media.giphy.com/media/63MO9LTRoTXQk/giphy.gif',
          'https://media.giphy.com/media/q0cairP4p5MFG/giphy.gif',
          'https://media.giphy.com/media/3ornjXJUIDbLSlnZwQ/giphy.gif',
          'https://media.giphy.com/media/feoIvi3j0MxcFTazV8/giphy.gif',
          'https://media.giphy.com/media/l0MYz5lF8DEvLrYKQ/giphy.gif',
          'https://media.giphy.com/media/3o7btQ8jDTPGDpgc6I/giphy.gif',
          'https://media.giphy.com/media/vGLqAadWShT5m/giphy.gif']
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
rage = ['https://media.giphy.com/media/p8Uw3hzdAE2dO/giphy.gif',
        'https://media.giphy.com/media/13EjnL7RwHmA2Q/giphy.gif',
        'https://media.giphy.com/media/6hE3b5HSuMrMk/giphy.gif',
        'https://media.giphy.com/media/LTpmRMNSmZgIw/giphy.gif',
        'https://media.giphy.com/media/ntjBjvfnakKJ2/giphy.gif',
        'https://media.giphy.com/media/SiItwB3nrAZuRKl3vP/giphy.gif',
        'https://media.giphy.com/media/ZMJQEhBskQmQM/giphy.gif',
        'https://media.giphy.com/media/mRGsFJImjeXPW/giphy.gif',
        'https://media.giphy.com/media/vHcCevWbWkzwk/giphy.gif',
        'https://media.giphy.com/media/l0Iyo3JenZWJuEP0Q/giphy.gif',
        'https://media.giphy.com/media/qDfgfLkj47lDi/giphy.gif',
        'https://media.giphy.com/media/sN7VFBDZWCgjm/giphy.gif',
        'https://media.giphy.com/media/3o7ZeGtJoHORdUuPgA/giphy.gif',
        'https://media.giphy.com/media/6RoUMn34pqvcs/giphy.gif',
        'https://media.giphy.com/media/aaoG2VSbUdUe4/giphy.gif',
        'https://media.giphy.com/media/3o6ZsY8110mu207jvG/giphy.gif',
        'https://media.giphy.com/media/JWLp2eO1gdYFG/giphy.gif',
        'https://media.giphy.com/media/udv8jAcfnPaIU/giphy.gif',
        'https://media.giphy.com/media/KdKhwLw3CLH9u/giphy.gif']
end = ['https://media.giphy.com/media/DAtJCG1t3im1G/giphy.gif',
       'https://media.giphy.com/media/110IlProGBQgs8/giphy.gif',
       'https://media.giphy.com/media/l2JeaFDEUkyXjoULK/giphy.gif',
       'https://media.giphy.com/media/hRqxN8UbaaGuA/giphy.gif',
       'https://media.giphy.com/media/l46CrXrr945SmMA0g/giphy.gif',
       'https://media.giphy.com/media/AkLGHCYGv43uw/giphy.gif',
       'https://media.giphy.com/media/4ECepQbplGd0I/giphy.gif',
       'https://media.giphy.com/media/26Ff4PUGXu6OgoiWI/giphy.gif',
       'https://media.giphy.com/media/l1AszMouJ4dU9u3p6/giphy.gif',
       'https://media.giphy.com/media/13S0cgc6oDYqPK/giphy.gif',
       'https://media.giphy.com/media/SIPIe590rx6iA/giphy.gif',
       'https://media.giphy.com/media/l3vQXpNnRGaAVprjO/giphy.gif',
       'https://media.giphy.com/media/dkuZHIQsslFfy/giphy.gif',
       'https://media.giphy.com/media/oDxCE80IULQ6Q/giphy.gif',
       'https://media.giphy.com/media/LQDupOVfCgsSY/giphy.gif',
       'https://media.giphy.com/media/AIlrItaxPyivS/giphy.gif']


class Interação:
    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.command()
    async def treta(self, ctx):
        """Todas as tretas do grupo!"""
        pass

    @commands.guild_only()
    @commands.command(name='endeline')
    async def endeline(self, ctx):
        gif = random.choice(end)
        endmessage = '**Sem mais vai e vem!**'
        embed = discord.Embed(title="**FIM DE JOGO!**", colour=discord.Colour(0x370c5e),
                              description="{}".format(endmessage))

        embed.set_image(url="{}".format(gif))
        embed.set_footer(text="Betina Brazilian Bot",
                         icon_url="https://images.discordapp.net/avatars/"
                                  "527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
        await ctx.send(embed=embed, delete_after=10)

    @commands.guild_only()
    @commands.command(name='emputece', aliases=['angry', 'rage'])
    async def emputece(self, ctx, member: discord.Member, membro=None):
        if membro == None:
            membro = ctx.author
        else:
            if ctx.author == membro == member:
                await ctx.invoke(self.client.get_command('endeline'))
                await msg.delete()

        gif = random.choice(rage)

        emputece2 = '{} **Deixou** {} **PUTO!**'.format(membro.mention, member.mention)
        embed = discord.Embed(title="**EMPUTECEU!**", colour=discord.Colour(0x370c5e),
                                description="{}".format(emputece2))

        embed.set_image(url="{}".format(gif))
        embed.set_footer(text="Betina Brazilian Bot",
                            icon_url="https://images.discordapp.net/avatars/"
                                      "527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('😡')

        def check(reaction, user):
            return user == member and str(reaction.emoji) == "😡"

        try:
            reaction, user = await self.client.wait_for('reaction_add', check=check)
        except:
            return
        else:
            await msg.delete()
            await ctx.invoke(self.client.get_command('putin'), ctx.author, member)

    @emputece.error
    async def emputece_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'member':
                embed = discord.Embed(title="Comando $emputece:", colour=discord.Colour(0x370c5e),
                                      description="Emputece o usuário\n \n**Como usar: $emputece <usuário>**")

                embed.set_author(name="Betina#9182",
                                 icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
                embed.set_footer(text="Betina Brazilian Bot",
                                 icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")

                embed.add_field(name="📖**Exemplos:**", value="$emputece @fulano\n$emputece @sicrano", inline=False)
                embed.add_field(name="🔀**Outros Comandos**", value="``$rage, $angry.``", inline=False)

                msg = await ctx.send(embed=embed)
                await msg.add_reaction("❓")

    @commands.guild_only()
    @commands.command(name='putin')
    async def putin(self, ctx, member: discord.Member, membro=None):
        gif = random.choice(rage)

        emputece1 = '**SAI DA FRENTE QUE AGORA EU TO PUTA CONTIGO!**. \n\nEU VOU MATAR o ' \
                    'usuário {}'.format(ctx.author.mention)
        emputece2 = '{} **Deixou** {} **MAIS PUTO AINDA !**'.format(membro.mention, member.mention)

        embed = discord.Embed(title="**EMPUTECEU MAIS AINDA !**", colour=discord.Colour(0x370c5e),
                                description="{}".format(emputece2))

        embed.set_image(url="{}".format(gif))
        embed.set_footer(text="Betina Brazilian Bot",
                            icon_url="https://images.discordapp.net/avatars/"
                                      "527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('😡')

        def check(reaction, user):
            return user == member and str(reaction.emoji) == "😡"

        try:
            reaction, user = await self.client.wait_for('reaction_add', check=check)
        except:
            return
        else:
            await msg.delete()
            await ctx.invoke(self.client.get_command('endeline'))

    @commands.guild_only()
    @commands.command(name='bate', aliases=['hit', 'punch'])
    async def bate(self, ctx, member: discord.Member, membro=None):
        if membro == None:
            membro = ctx.author
        else:
            if ctx.author == member == membro:
                await ctx.invoke(self.client.get_command('endeline'))
                await msg.delete()

        """<membro>: Tome cuidado com isso."""
        gif = random.choice(slap)

        bate2 = '{} **deu um tapa em** {}'.format(membro.mention, member.mention)
        embed = discord.Embed(title="**Tapão!**", colour=discord.Colour(0x370c5e), description="{}".format(bate2))

        embed.set_image(url="{}".format(gif))
        embed.set_footer(text="Betina Brazilian Bot",
                            icon_url="https://images.discordapp.net/avatars/"
                                      "527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
        msg = await ctx.send(embed=embed)

        await msg.add_reaction("🔙")

        def check(reaction, user):
            return user == member and str(reaction.emoji) == "🔙"

        try:
            reaction, user = await self.client.wait_for('reaction_add', check=check)
        except:
            return
        else:
            await msg.delete()
            await ctx.invoke(self.client.get_command('bate'), ctx.author, member)

    @bate.error
    async def bate_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'member':
                embed = discord.Embed(title="Comando $bate:", colour=discord.Colour(0x370c5e),
                                      description="Bate no usuário\n \n**Como usar: $bate <usuário>**")

                embed.set_author(name="Betina#9182",
                                 icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
                embed.set_footer(text="Betina Brazilian Bot",
                                 icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")

                embed.add_field(name="📖**Exemplos:**", value="$bate @fulano\n$bate @sicrano", inline=False)
                embed.add_field(name="🔀**Outros Comandos**", value="``$hit, $punch.``", inline=False)

                msg = await ctx.send(embed=embed)
                await msg.add_reaction("❓")

    @commands.guild_only()
    @commands.command(name='abraça', aliases=['hug', 'abraço'])
    async def abraça(self, ctx, member: discord.Member, membro=None):
        if membro == None:
            membro = ctx.author
        else:
            if ctx.author == member == membro:
                await ctx.invoke(self.client.get_command('endeline'))
                await msg.delete()

        """<membro>: Use isso com amor <3."""
        gif = random.choice(hug)

        abraça2 = '{} **deu um abraço em** {}'.format(membro.mention, member.mention)

        embed = discord.Embed(title="**Abraço!**", colour=discord.Colour(0x370c5e),
                                  description="{}".format(abraça2))

        embed.set_image(url="{}".format(gif))
        embed.set_footer(text="Betina Brazilian Bot",
                            icon_url="https://images.discordapp.net/avatars/"
                                      "527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
        msg = await ctx.send(embed=embed)

        await msg.add_reaction("🔙")

        def check(reaction, user):
            return user == member and str(reaction.emoji) == "🔙"

        try:
            reaction, user = await self.client.wait_for('reaction_add', check=check)
        except:
            return
        else:
            await msg.delete()
            await ctx.invoke(self.client.get_command('abraça'), ctx.author, member)

    @abraça.error
    async def abraça_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'member':
                embed = discord.Embed(title="Comando $abraça:", colour=discord.Colour(0x370c5e),
                                      description="Abraça o usuário\n \n**Como usar: $abraça <usuário>**")

                embed.set_author(name="Betina#9182",
                                 icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
                embed.set_footer(text="Betina Brazilian Bot",
                                 icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")

                embed.add_field(name="📖**Exemplos:**", value="$abraça @fulano\n$abraça @sicrano", inline=False)
                embed.add_field(name="🔀**Outros Comandos**", value="``$hug, $abraço.``", inline=False)

                msg = await ctx.send(embed=embed)
                await msg.add_reaction("❓")

    @commands.guild_only()
    @commands.command(name='beija', aliases=['kiss', 'beijou'])
    async def beija(self, ctx, member: discord.Member, membro=None):
        if membro == None:
            membro = ctx.author
        else:
            if ctx.author == member == membro:
                await ctx.invoke(self.client.get_command('endeline'))
                await msg.delete()

        """<membro>: Use isso com amor <3."""
        gif1 = random.choice(slap)
        gif2 = random.choice(kiss)
        beija2 = '{} **deu um beijo em** {}'.format(membro.mention, member.mention)

        embed = discord.Embed(title="**Beijo!**", colour=discord.Colour(0x370c5e), description="{}".format(beija2))

        embed.set_image(url="{}".format(gif2))
        embed.set_footer(text="Betina Brazilian Bot",
                             icon_url="https://images.discordapp.net/avatars/"
                                      "527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
        msg = await ctx.send(embed=embed)

        await msg.add_reaction("🔙")

        def check(reaction, user):
            return user == member and str(reaction.emoji) == "🔙"

        try:
            reaction, user = await self.client.wait_for('reaction_add', check=check)
        except:
            return
        else:
            await msg.delete()
            await ctx.invoke(self.client.get_command('beija'), ctx.author, member)

    @beija.error
    async def beija_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'member':
                embed = discord.Embed(title="Comando $beija:", colour=discord.Colour(0x370c5e),
                                      description="Beija o usuário\n \n**Como usar: $beija <usuário>**")

                embed.set_author(name="Betina#9182",
                                 icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
                embed.set_footer(text="Betina Brazilian Bot",
                                 icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")

                embed.add_field(name="📖**Exemplos:**", value="$beija @fulano\n$beija @sicrano", inline=False)
                embed.add_field(name="🔀**Outros Comandos**", value="``$kiss, $beijou.``", inline=False)

                msg = await ctx.send(embed=embed)
                await msg.add_reaction("❓")

    @commands.command()
    async def tnc(self, ctx):
        gif1 = random.choice(angry)
        gif2 = random.choice(omg)

        person = random.choice(list(ctx.guild.members))

        tnc1 = '{} mandou {} tomar no cu!'.format(ctx.author.mention, person.mention)

        embed = discord.Embed(title="**Raiva!**", colour=discord.Colour(0x370c5e), description="{}".format(tnc1))
        embed.set_image(url="{}".format(gif2))
        embed.set_footer(text="Betina Brazilian Bot",
                             icon_url="https://images.discordapp.net/avatars/"
                                      "527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('😮')

    @commands.guild_only()
    @commands.command(name='voltapracaverna', aliases=['caverna', 'goback'])
    async def voltapracaverna(self, ctx, member: discord.Member, membro=None):
        if membro == None:
            membro = ctx.author
        else:
            if ctx.author == member == membro:
                await ctx.invoke(self.client.get_command('endeline'))
                await msg.delete()

        """<membro>: Use isso com amor <3."""
        gif = random.choice(cave)

        cave2 = '{} **mandou** {} **de volta pra caverna**'.format(membro.mention, member.mention)

        embed = discord.Embed(title="**Volta pra Caverna!**", colour=discord.Colour(0x370c5e),
                                  description="{}".format(cave2))
        embed.set_image(url="{}".format(gif))
        embed.set_footer(text="Betina Brazilian Bot",
                            icon_url="https://images.discordapp.net/avatars/"
                                      "527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
        msg = await ctx.send(embed=embed)

        await msg.add_reaction("🔙")

        def check(reaction, user):
            return user == member and str(reaction.emoji) == "🔙"

        try:
            reaction, user = await self.client.wait_for('reaction_add', check=check)
        except:
            return
        else:
            await msg.delete()
            await ctx.invoke(self.client.get_command('voltapracaverna'), ctx.author, member)

    @voltapracaverna.error
    async def voltapracaverna_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'member':
                embed = discord.Embed(title="Comando $voltapracaverna:", colour=discord.Colour(0x370c5e),
                                      description="Manda o usuário de volta pra caverna\n \n**Como usar: $volta pra caverna"
                                                  " <usuário>**")

                embed.set_author(name="Betina#9182",
                                 icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
                embed.set_footer(text="Betina Brazilian Bot",
                                 icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")

                embed.add_field(name="📖**Exemplos:**", value="$voltapracaverna @fulano\n$voltapracaverna"
                                                              " @sicrano", inline=False)
                embed.add_field(name="🔀**Outros Comandos**", value="``$caverna, $goback.``", inline=False)

                msg = await ctx.send(embed=embed)
                await msg.add_reaction("❓")

    @commands.guild_only()
    @commands.command(name='dança', aliases=['dance', 'dançar'])
    async def dança(self, ctx, member: discord.Member, membro=None):
        if membro == None:
            membro = ctx.author
        else:
            if ctx.author == member == membro:
                await ctx.invoke(self.client.get_command('endeline'))
                await msg.delete()

        """<membro>: Use isso com amor <3."""
        gif = random.choice(dance)

        dança2 = '{} **começou a dançar com** {}'.format(membro.mention, member.mention)

        embed = discord.Embed(title="**Dançante!**", colour=discord.Colour(0x370c5e),
                                  description="{}".format(dança2))
        embed.set_image(url="{}".format(gif))
        embed.set_footer(text="Betina Brazilian Bot",
                            icon_url="https://images.discordapp.net/avatars/"
                                      "527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
        msg = await ctx.send(embed=embed)

        await msg.add_reaction("🔙")

        def check(reaction, user):
            return user == member and str(reaction.emoji) == "🔙"

        try:
            reaction, user = await self.client.wait_for('reaction_add', check=check)
        except:
            return
        else:
            await msg.delete()
            await ctx.invoke(self.client.get_command('dança'), ctx.author, member)

    @dança.error
    async def dança_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'member':
                embed = discord.Embed(title="Comando $dança:", colour=discord.Colour(0x370c5e),
                                      description="Dança com o usuário\n \n**Como usar: $dança <usuário>**")

                embed.set_author(name="Betina#9182",
                                 icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
                embed.set_footer(text="Betina Brazilian Bot",
                                 icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")

                embed.add_field(name="📖**Exemplos:**", value="$dança @fulano\n$dança @sicrano", inline=False)
                embed.add_field(name="🔀**Outros Comandos**", value="``$dance, $dançar.``", inline=False)

                msg = await ctx.send(embed=embed)
                await msg.add_reaction("❓")

    @commands.guild_only()
    @commands.command(name='ataca', aliases=['attack', 'atacar'])
    async def ataca(self, ctx, member: discord.Member, membro=None):
        if membro == None:
            membro = ctx.author
        else:
            if ctx.author == member == membro:
                await ctx.invoke(self.client.get_command('endeline'))
                await msg.delete()
        """<membro>: Cuidado com isso!"""
        gif = random.choice(attack)
        ataca2 = '{} **deu um ataque em** {}'.format(membro.mention, member.mention)

        embed = discord.Embed(title="**Ataque!**", colour=discord.Colour(0x370c5e), description="{}".format(ataca2))
        embed.set_image(url="{}".format(gif))
        embed.set_footer(text="Betina Brazilian Bot",
                             icon_url="https://images.discordapp.net/avatars/"
                                      "527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
        msg = await ctx.send(embed=embed)

        await msg.add_reaction("🔙")

        def check(reaction, user):
            return user == member and str(reaction.emoji) == "🔙"

        try:
            reaction, user = await self.client.wait_for('reaction_add', check=check)
        except:
            return
        else:
            await msg.delete()
            await ctx.invoke(self.client.get_command('ataca'), ctx.author, member)

    @ataca.error
    async def ataca_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'member':
                embed = discord.Embed(title="Comando $ataca:", colour=discord.Colour(0x370c5e),
                                      description="ataca o usuário\n \n**Como usar: $ataca <usuário>**")

                embed.set_author(name="Betina#9182",
                                 icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")
                embed.set_footer(text="Betina Brazilian Bot",
                                 icon_url="https://images.discordapp.net/avatars/527565353199337474/40042c09bb354a396928cb91e0288384.png?size=256")

                embed.add_field(name="📖**Exemplos:**", value="$ataca @fulano\n$ataca @sicrano", inline=False)
                embed.add_field(name="🔀**Outros Comandos**", value="``$attack, $atacar.``", inline=False)

                msg = await ctx.send(embed=embed)
                await msg.add_reaction("❓")


def setup(client):
    client.add_cog(Interação(client))
