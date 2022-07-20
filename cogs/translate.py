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

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id == 983516379619672154:
            return
        if payload.channel_id == 983390210987548702:
            return
        client = self.client
        channel = client.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        file = open("data/languages.json", "r")
        data = json.load(file)
        file.close()
        for language in data:
            for emoji in language['emojis']:
                if str(payload.emoji) == emoji:
                    await channel.send(str(ts.google(str(message.content), to_language=language['code'])))
                    return

    
def setup(client):
    client.add_cog(Translate(client))