import sys
import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('data/.env')
load_dotenv(dotenv_path=dotenv_path)

intents = discord.Intents.default()
intents.members = True

token = os.getenv('TOKEN')
prefix = '>'
client = commands.Bot(command_prefix=prefix, intents=intents)


# Checks if the user is me
def is_Sam(ctx):
    if ctx.author.id == 979408629595799562:
        return True
    else:
        ctx.send("Only Sam can use this command")
        return False
        

# What to do when the bot is ready
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('PUT THOSE GRIPPERS AWAY.'))
    print('Bot logged in as {0.user}'.format(client))

# Status Cycle  
#@tasks.loop(seconds=3)
#async def change_status():
#    await client.change_presence(activity=discord.Game(next(status)))


# Loads the cog
@client.command()
@commands.check(is_Sam)
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} loaded.')

# Unloads the cog
@client.command()
@commands.check(is_Sam)
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} unloaded.')

# Reloads the cog
@client.command()
@commands.check(is_Sam)
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} reloaded.')



# Loads cogs on startup
for filename in os.listdir('./cogs/'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

@client.command()
@commands.check(is_Sam)
async def kill(ctx):
    sys.exit(0)

@client.command()
@commands.check(is_Sam)
async def deljson(ctx):
    os.remove('data/rero.json')

client.run(token)

