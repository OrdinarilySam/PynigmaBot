import discord
from discord.ext import commands
from googletrans import Translator

# NOT WORKING RIGHT NOW


translator = Translator(service_urls='translate.google.com')

class Translate(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def translate(self, ctx, *, message):
        #await ctx.send("Hello")
        await ctx.send(type(message))
        #await ctx.send(str(translator.translate(message)))

    
def setup(client):
    client.add_cog(Translate(client))