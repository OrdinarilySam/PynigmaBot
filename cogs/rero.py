import discord
from discord.ext import commands
from discord.utils import get
import json
import os
import asyncio

test_role = 984555378962481213



    # addrole and remrole common checks
def checkjsonfile():
    if not os.path.exists("data/rero.json"):
        return False
    if os.path.getsize("data/rero.json") < 21:
        return False
    return True
    


def json_rw(needed='data', inp=None, remove=False):
    if needed == 'data':
        if not inp:
            if checkjsonfile():
                file = open("data/rero.json", "r")
                data = json.load(file)
                file.close()
                return data
        else:
            file = open("data/rero.json", "w")
            file.write(json.dumps(inp, indent=2))
            file.close()
            return
    else:
        file = open("data/rero.json", "r")
        data = json.load(file)
        file.close()
        for init in data['inits']:
            if init['category_name'].lower() == needed.lower():
                if not remove:
                    if not inp:
                        return init
                    else:
                        data['inits'][data['inits'].index(init)] = inp
                else:
                    data['inits'].pop(data['inits'].index(init))
                file = open("data/rero.json", "w")
                file.write(json.dumps(data, indent=2))
                file.close()
                return



class Rero(commands.Cog):

    def __init__(self, client):
        self.client = client
    



# COMMANDS
    @commands.command()
    async def init(self, ctx, *, embed_category='default'):
        #deletes the original message
        await ctx.channel.purge(limit=1)
        with ctx.channel.typing():
            #creates the embed
            if embed_category == 'default':
                embed_init = discord.Embed(
                    title=f"Roles",
                    description="React to this message to receive roles",
                    colour = discord.Colour.blue()
                )
            else:
                embed_init = discord.Embed(
                    title=f"{embed_category}",
                    description="React to this message to receive roles",
                    colour = discord.Colour.blue()
                )
            message = await ctx.send(embed=embed_init)
            if checkjsonfile():
                data = json_rw()
                new_data = {
                            "category_name": embed_category,
                            "message_id": message.id,
                            "channel_id": ctx.channel.id,
                            "roles": []
                    }
                data['inits'].append(new_data)
            else:
                data = {
                        "inits": [{
                            "category_name": embed_category,
                            "message_id": message.id,
                            "channel_id": ctx.channel.id,
                            "roles": []
                    }]    
                    }
            json_rw(inp=data)

    @commands.command()
    async def remcat(self, ctx, *, embed_category='default'):
        init = json_rw(embed_category)
        if init['category_name'].lower() == embed_category.lower():
            channel = get(ctx.guild.text_channels, id=init["channel_id"])
            message = await channel.fetch_message(id=init['message_id'])
            await message.delete()
            json_rw(embed_category, remove=True)
            await ctx.channel.purge(limit=1)




    # ADD AND REMOVE ROLES FROM THE EMBED
    @commands.command()
    async def addrole(self, ctx, role : commands.RoleConverter=None, *, embed_category='default'):
        
        # checks for instance of json file
        if not checkjsonfile():
            await ctx.send("You must initialize first")

        #checks to ensure the value of role is not None
        if role == None:
            await ctx.send("You must specify a role")
            return

        # stores the data from the json file
        init = json_rw(embed_category)

        await ctx.channel.purge(limit=1)

        # checks for the given role 
        for r in init['roles']:
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
        
        init['roles'].append(to_add)
        json_rw(embed_category, init)

        # edits the embed to add the reaction
        channel = get(ctx.guild.text_channels, id=init['channel_id'])
        message = await channel.fetch_message(id=init['message_id'])
        embed = message.embeds[0]
        embed.add_field(name=f"{str(reaction.emoji)}", value=str(role.name), inline=False)
        await message.edit(embed=embed)
        await message.add_reaction(reaction.emoji)




    @commands.command()
    async def remrole(self, ctx, role : commands.RoleConverter=None, *, embed_category='default'):

        # checks for instance of json file
        if not checkjsonfile():
            await ctx.send("You must initialize first")

        # checks to ensure the value of role is not None
        if role==None:
            await ctx.send("You must specify the role")
            return

        # stores the data from the json file
        init = json_rw(embed_category)

        await ctx.channel.purge(limit=1)

        # checks for the given role and removes it
        found = False
        for r in init['roles']:
            if role.id == r['role_id']:
                found = True
                init['roles'].pop(init['roles'].index(r))

        # checks to make sure the role was found
        if not found:
            await ctx.send("Role not found")
            return

        # writes the json file with role removed
        json_rw(embed_category, init)

        # edits the embed to add the reaction
        channel = get(ctx.guild.text_channels, id=init['channel_id'])
        message = await channel.fetch_message(id=init['message_id'])

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
    async def checkroles(self, ctx, *, embed_category=None):

        # checks for instance of json file
        if not os.path.exists("data/rero.json"):
            await ctx.send("You must initialize the reaction roles first")
            return

        if not embed_category:
            data = json_rw()
            role_list = {}
            for init in data['inits']:
                role_list.update({init['category_name']: []})
                for role in init['roles']:
                    role_list[init['category_name']].append(str(get(ctx.guild.roles, id=role['role_id']).name))
        else:
            init = json_rw(embed_category)
            role_list = []
            for role in init['roles']:
                role_list.append(str(get(ctx.guild.roles, id=role['role_id']).name))

        await ctx.send(role_list)




    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id == 983516379619672154:
            return
        client = self.client
        guild = client.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        data = json_rw()

        for init in data['inits']:
            if payload.message_id == init['message_id']:
                for role in init['roles']:
                    if str(payload.emoji) == role['role_emoji']:
                        await member.add_roles(get(guild.roles, id=role['role_id']))
                        return

        
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.user_id == 983516379619672154:
            return
        client = self.client
        guild = client.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        data = json_rw()

        for init in data['inits']:
            if payload.message_id == init['message_id']:
                for role in init['roles']:
                    if str(payload.emoji) == role['role_emoji']:
                        await member.remove_roles(get(guild.roles, id=role['role_id']))
                        return






    # ERRORS
    @init.error
    async def init_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please specify the category name")

    @addrole.error
    async def addrole_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Usage: >addrole [role] [category]")
    
    @remrole.error
    async def remrole_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Usage: >remrole [role] [category]")


def setup(client):
    client.add_cog(Rero(client))