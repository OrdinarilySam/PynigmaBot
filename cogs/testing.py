import discord
from discord.ext import commands

test_role_id = 984555378962481213

class Testing(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    #grants the test role to the user by default
    @commands.command()
    async def gr(self, ctx, member: commands.MemberConverter=None):
        if not member:
            await ctx.author.add_roles(discord.utils.get(ctx.guild.roles, id=test_role_id))
        else:
            await member.add_roles(discord.utils.get(ctx.guild.roles, id=test_role_id))

    #removes the test role to the user by default
    @commands.command()
    async def rr(self, ctx, member: commands.MemberConverter=None):
        if not member:
            await ctx.author.remove_roles(discord.utils.get(ctx.guild.roles, id=test_role_id))
        else:
            await member.remove_roles(discord.utils.get(ctx.guild.roles, id=test_role_id))

    
def setup(client):
    client.add_cog(Testing(client))