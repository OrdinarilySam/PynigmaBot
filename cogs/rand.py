import discord
import random
from discord.ext import commands

class Rand(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def rand(self, ctx):
        await ctx.send(f'Random Number: {random.randint(0, 1000)}')

    @commands.command(aliases=['8ball', 'eightball'])
    async def _8ball(self, ctx, *, question):
        responses = ['It is certain.',
                    'It is decidedly so.',
                    'Without a doubt.',
                    'Yes definitely.',
                    'You may rely on it.',
                    'As I see it, yes.',
                    'Most likely.',
                    'Outlook good.',
                    'Yes.',
                    'Signs point to yes.',
                    'Reply hazy, try again.',
                    'Ask again later.',
                    'Better not tell you now.',
                    'Cannot predict now.',
                    'Concentrate and ask again.',
                    'Don\'t count on it.',
                    'My reply is no.',
                    'My sources say no.',
                    'Outlook not so good.',
                    'Very doubtful.']
        await ctx.send(f'Question: {question}\n Answer: {random.choice(responses)}')

    @_8ball.error
    async def _8ball_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('You can\'t have me predict nothing.')

def setup(client):
    client.add_cog(Rand(client))