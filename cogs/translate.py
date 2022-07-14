from asyncio import to_thread
import discord
from discord.ext import commands
import translators as ts
import json



class Translate(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def translate(self, ctx, language, *, message=None):
        print("command started with language", language)
        file = open("data/languages.json", "r")
        data = json.load(file)
        file.close()
        print(language)
        for lang in data:
            print("starting detection on language", lang['name'])
            if lang['code'] == language.lower() or lang['name'].lower() == language.lower():
                print("match found")
                await ctx.send(str(ts.google(message, to_language=lang['code'])))
                return
        if not message:
            message = language
        else:
            message = language + message
        await ctx.send(str(ts.google(message, to_language='en')))

    
def setup(client):
    client.add_cog(Translate(client))