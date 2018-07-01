import discord
import datetime
import asyncio
import json
import praw
import requests

from discord.ext import commands
from random import randint
from datetime import datetime

with open('db/admin.json') as admn:
    admin = json.load(admn)


reddit = praw.Reddit(client_id='',
                    client_secret='',
                    user_agent='')

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
        if amount > 20:
            await self.bot.say("Can't spam over 20.")
            return
        elif '@everyone' in content:
            await self.bot.say("Nice try.")
            return
        elif '@here' in content:
            await self.bot.say("Nice try.")
            return
            
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
        
    @commands.command(pass_context=True)
    async def say(self, ctx, *, message):
        if '@everyone' in message: # Checking to make sure the user isn't trying to ping everyone or here
            await self.bot.say('Nice try.')
            await self.bot.delete_message(ctx.message)
            return
        elif '@here' in message:
            await self.bot.say('Nice try.')
            await self.bot.delete_message(ctx.message)
            return
        else:
            await self.bot.send_message(ctx.message.channel, message)
            await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def reverse(self, ctx, *, message):
        if 'enoyreve@' in message:
            await self.bot.say("Haha nice try but u r gay.")
            await self.bot.delete_message(ctx.message)
            return

        elif 'ereh@' in message:
            await self.bot.say("Haha nice try but u r gay.")
            await self.bot.delete_message(ctx.message)
            return

        elif message == message[::-1]:
            await self.bot.say("{} ".format(message) + "(It's a Palindrome)")

        else:
            await self.bot.say("{}".format(message)[::-1])

    @commands.command(pass_context=True)
    async def fortune(self, ctx):
        cookie = requests.get("http://fortunecookieapi.herokuapp.com/v1/cookie").json()

        embed = discord.Embed(title="Fortune Cookie")
        embed.add_field(name="Fortune", value="{}".format(cookie[0]["fortune"]["message"]), inline=True)
        embed.add_field(name="Lucky Numbers", value="{0},{1},{2},{3},{4},{5}".format(cookie[0]["lotto"]["numbers"][0],cookie[0]["lotto"]["numbers"][1],cookie[0]["lotto"]["numbers"][2],cookie[0]["lotto"]["numbers"][3],cookie[0]["lotto"]["numbers"][4],cookie[0]["lotto"]["numbers"][5]), inline=True)
        embed.add_field(name="Lesson", value="**Chinese**:{0} ({1})\n**English**: {2}".format(cookie[0]["lesson"]["chinese"],cookie[0]["lesson"]["pronunciation"],cookie[0]["lesson"]["english"]),inline=False)
        embed.set_thumbnail(url="https://images.emojiterra.com/twitter/512px/1f960.png")

        await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    async def r(self, ctx, theSubreddit):
        print("reddit command recieved")
        print("----------------------")
        reddit_submissions = reddit.subreddit('{}'.format(theSubreddit)).hot()
        post_to_pick = random.randint(1, 10)
        for x in range(0, post_to_pick):
            submission = next(x for x in reddit_submissions if not x.stickied)

        self.bot.say(submission.url)


def setup(bot):
    bot.add_cog(Fun(bot))
