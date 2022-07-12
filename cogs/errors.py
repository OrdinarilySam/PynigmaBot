import discord
from discord.ext import commands

class Errors(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('Missing permissions')

    
def setup(client):
    client.add_cog(Errors(client))