import discord
import datetime
import asyncio
import json

from discord.ext import commands
from random import randint
from datetime import datetime

with open('db/admin.json') as admn:
    admin = json.load(admn)

class Fun(object):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def padraig(self, ctx):
        if str(ctx.message.author.id) == '285305801911042049':
            await self.bot.say("What can I say, he's sexy.")
        else:
            await self.bot.say("Only the goat Padraig can use this command.")

    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def spam(self, ctx, user: discord.Member, amount: int, *, content):
        messages = 0 
        while messages < amount:
            await self.bot.say('<@{}> {}'.format(user.id, content))
            messages = messages + 1
            await asyncio.sleep(0.2)

        # example of command is '!spam @user 10 wake up'
        # this will make the bot ping the user 10 times and say wake up.

    @spam.error
    async def spam_error(self, error, ctx):
        if isinstance(error, discord.ext.commands.CheckFailure):
            userID = (ctx.message.author.id)
            await self.bot.send_message(ctx.message.author,"<@%s>: **You don't have permission to perform this action**" % (userID))
            await self.bot.delete_message(ctx.message)
        
        elif isinstance(error, discord.ext.commands.MissingRequiredArgument):
            await self.bot.say('Missing Required Argument. ```!spam @user 10 wake up```')
            await self.bot.delete_message(ctx.message)




def setup(bot):
    bot.add_cog(Fun(bot))
