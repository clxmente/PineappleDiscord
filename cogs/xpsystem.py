import discord
import os
import json
import os.path
import datetime

from random import randint
from os import listdir
from os.path import isfile, join
from discord.ext import commands
from datetime import datetime

client = discord.Client()

with open('db/admin.json') as admn:
    admin = json.load(admn)

with open('db/privlogs.json') as admn:
    privlogs = json.load(admn)

with open('db/users.json') as fp:
    users = json.load(fp)

def userAddXP(userID: int, xp: int):
    if os.path.isfile("db/users.json"):
        try:
            with open('db/users.json', 'r') as fp:
                users = json.load(fp)
            users[userID]['xp'] += xp
            with open('db/users.json', 'w') as fp:
                json.dump(users, fp, sort_keys=True, indent=4)
        except KeyError:
            with open('db/users.json', 'r') as fp:
                users = json.load(fp)
            users[userID] = {}
            users[userID]['xp'] = xp
            with open('db/users.json', 'w') as fp:
                json.dump(users, fp, sort_keys=True, indent=4)

    else:
        users = {userID: {}}
        users[userID]['xp'] = xp
        with open('db/users.json', 'w') as fp:
            json.dump(users, fp, sort_keys=True, indent=4)

def getXP(userID: int):
    if os.path.isfile('db/users.json'):
        with open('db/users.json', 'r') as fp:
            users = json.load(fp)
        return users[userID]['xp']
    else:
        return 0

def setLevel(userID: int, level: int):
    if os.path.isfile('db/users.json'):
        with open('db/users.json', 'r') as fp:
            users = json.load(fp)
        users[userID]["Level"] = level
        with open('db/users.json', 'w') as fp:
            json.dump(users, fp, sort_keys=True, indent=4)

def getLevel(userID: int):
    if os.path.isfile('db/users.json'):
        try:
            with open('db/users.json', 'r') as fp:
                users = json.load(fp)
            return users[userID]['Level']
        except KeyError:
            return 0


class XpSystem(object):
    def __init__(self, bot):
        self.bot = bot

    @client.event
    async def on_message(self, message):
        if str(message.author.id) == '456247418288209922':
            return

        user_id= message.author.id
        userLevel = getLevel(message.author.id)
        userXP = getXP(message.author.id)

        if userLevel == 0 and userXP >= 1000:
            setLevel(user_id, 1)

        if userLevel == 1 and userXP >= 2000:
            setLevel(user_id, 2)

        if userLevel == 2 and userXP >= 3000:
            setLevel(user_id, 3)

        if userLevel == 3 and userXP >= 4000:
            setLevel(user_id, 4)

        if userLevel == 4 and userXP >= 5000:
            setLevel(user_id, 5)
            await client.send_message(message.channel, "{}: You just leveled up to level 5".format(message.author.mention))
 
        if userLevel == 5 and userXP >= 6000:
            setLevel(user_id, 6)
 
        if userLevel == 6 and userXP >= 7000:
            setLevel(user_id, 7)
 
        if userLevel == 7 and userXP >= 8000:
            setLevel(user_id, 8)
 
        if userLevel == 8 and userXP >= 9000:
            setLevel(user_id, 9)
 
        if userLevel == 9 and userXP >= 10000:
            setLevel(user_id, 10)
            await client.send_message(message.channel, "{}: You just leveled up to level 10".format(message.author.mention))


        randomXP = randint(2, 7)
        userAddXP(message.author.id, randomXP)


    @commands.command(pass_context=True)
    async def xpstats(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.message.author
        embed = discord.Embed(title="Leveling Stats - {}".format(user), description='Currently Level {}'.format(getLevel(user.id)), color = 0x25C740)
        embed.set_thumbnail(url=user.avatar_url)
        #embed.add_field(name="Experience Points", value="XXXX/XXXX ({})".format(getXP(ctx.message.author.id)), inline=True)
        embed.add_field(name="Experience Points", value="{}".format(getXP(user.id)), inline=True)
        #embed.add_field(name="Rank", value = "XX/XXXX", inline = True)
        embed.set_footer(text="Requested by {}".format(ctx.message.author))
        embed.timestamp = datetime.utcnow()
        
        await self.bot.send_message(ctx.message.channel, embed=embed)

    
def setup(bot):
    bot.add_cog(XpSystem(bot))
