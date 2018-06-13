import discord
import datetime
import asyncio

from discord.ext import commands
from random import randint
from datetime import datetime

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
    @commands.has_permissions(administrator=True)
    async def spam(self, ctx, user: discord.Member, amount: int):
        messages = 0 
        while messages < amount:
            await self.bot.say('<@{}> spam.'.format(user.id))
            messages = messages + 1
            await asyncio.sleep(0.2)

    @spam.error
    async def spam_error(self, error, ctx):
        if isinstance(error, discord.ext.commands.CheckFailure):
            userID = (ctx.message.author.id)
            await self.bot.send_message(ctx.message.author,"<@%s>: **You don't have permission to perform this action**" % (userID))
            await self.bot.delete_message(ctx.message)




def setup(bot):
    bot.add_cog(Fun(bot))
