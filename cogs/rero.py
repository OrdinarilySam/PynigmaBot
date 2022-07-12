from socket import timeout
from attr import fields
import discord
from discord.ext import commands
from discord.utils import get
import json
import os
import asyncio
from asyncio import sleep

test_role = 984555378962481213



    # addrole and remrole common checks
def checkjsonfile():
    if not os.path.exists("data/rero.json"):
        return False
    else:
        return True


def jsonrandw(data=None):
    if data == None:
        file = open("data/rero.json", "r")
        data = json.load(file)
        file.close()
        return data
    else:
        file = open("data/rero.json", "w")
        file.write(json.dumps(data, indent=2))
        file.close()




class Rero(commands.Cog):

    def __init__(self, client):
        self.client = client
    





# COMMANDS
    @commands.command()
    async def init(self, ctx):
        #deletes the original message
        await ctx.channel.purge(limit=1)


        #creates the embed
        embed_init = discord.Embed(
            title="Roles",
            description="React to this message to get some roles",
            colour = discord.Colour.blue()
        )
        # embed_test.add_field(name="✅", value="test role", inline=False)

        # sends the embed and adds a loading emoji
        message = await ctx.send(embed=embed_init)
        await message.add_reaction('🔄')

        # initializes the starting json values
        data = json.dumps(
            {
                "message_id": message.id,
                #"channel_id": ctx.channel.id,
                "roles": []
            },
            indent=2
        )
        # writes the file, if already written, overwrites it
        file = open("data/rero.json", "w")
        file.write(data)
        file.close()

        # removes loading emoji
        await message.clear_reaction('🔄')









    # ADD AND REMOVE ROLES FROM THE EMBED
    @commands.command()
    async def addrole(self, ctx, role : commands.RoleConverter=None):
        
        # checks for instance of json file
        if not checkjsonfile():
            await ctx.send("You must initialize first")

        #checks to ensure the value of role is not None
        if role == None:
            await ctx.send("You must specify a role")
            return

        # stores the data from the json file
        data = jsonrandw()

        await ctx.channel.purge(limit=1)

        # checks for the given role 
        for r in data['roles']:
            if role.id == r['role_id']:
                await ctx.send("Role already included.")
                return

        # checks for original user reaction
        def check(reaction, user):
          return user == ctx.author and str(reaction)

        #sends a message awaiting a reaction then closes.
        message = await ctx.send("React to this message with the emoji of your choice")
        to_add = {"role_id": role.id, "role_emoji": ""}
        while True:
            try:
                reaction, user = await self.client.wait_for("reaction_add", timeout=60, check=check)
                to_add['role_emoji'] = str(reaction.emoji)
                await message.delete()
                break

            except asyncio.TimeoutError:
                await message.delete()
                return

        # adds the role and emoji to the file
        data['roles'].append(to_add)
        jsonrandw(data)

        # edits the embed to add the reaction
        message = await ctx.fetch_message(id=data['message_id'])
        embed = message.embeds[0]
        embed.add_field(name=f"{str(reaction.emoji)}", value=str(role.name), inline=False)
        await message.edit(embed=embed)
        await message.add_reaction(reaction.emoji)




    @commands.command()
    async def remrole(self, ctx, role : commands.RoleConverter=None):

        # checks for instance of json file
        if not checkjsonfile():
            await ctx.send("You must initialize first")

        # checks to ensure the value of role is not None
        if role==None:
            await ctx.send("You must specify the role")
            return

        # stores the data from the json file
        data = jsonrandw()

        await ctx.channel.purge(limit=1)

        # checks for the given role and removes it
        found = False
        for r in data['roles']:
            if role.id == r['role_id']:
                found = True
                data['roles'].pop(data['roles'].index(r))

        # checks to make sure the role was found
        if not found:
            await ctx.send("Role not found")
            return

        # writes the json file with role removed
        jsonrandw(data)

        # edits the embed to add the reaction
        message = await ctx.fetch_message(id=data['message_id'])

        embed = message.embeds[0]
        index = 0
        for field in embed.fields:
            if field.value == str(role.name):
                await message.clear_reaction(field.name)
                break
            index += 1
        if index > len(embed.fields)-1:
            return
        
        embed.remove_field(index)
        await message.edit(embed=embed)



    @commands.command()
    async def checkroles(self, ctx):

        # checks for instance of json file
        if not os.path.exists("data/rero.json"):
            await ctx.send("You must initialize the reaction roles first")
            return

        # stores the data from the json file
        data = jsonrandw()

        # Creates a list of the role names then prints them
        role_list = []
        for r in data['roles']:
            temp_role = str(get(ctx.guild.roles, id=r['role_id']).name)
            role_list.append(temp_role)

        await ctx.send(role_list)




    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id == 983516379619672154:
            return
        client = self.client
        guild = client.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        data = jsonrandw()
        if payload.message_id == data['message_id']:
            for role in data['roles']:
                if str(payload.emoji) == role['role_emoji']:
                    await member.add_roles(get(guild.roles, id=role['role_id']))
   
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.user_id == 983516379619672154:
            return
        client = self.client
        guild = client.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        data = jsonrandw()
        if payload.message_id == data['message_id']:
            for role in data['roles']:
                if str(payload.emoji) == role['role_emoji']:
                    await member.remove_roles(get(guild.roles, id=role['role_id']))






    # ERRORS


def setup(client):
    client.add_cog(Rero(client))