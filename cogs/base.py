import discord
from discord.ext import commands

class Base(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong!")

    
def setup(client):
    client.add_cog(Base(client))