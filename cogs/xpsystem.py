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
            return users[userID]['level']
        except KeyError:
            return 0


class XpSystem(object):
    def __init__(self, bot):
        self.bot = bot

    @client.event
    async def on_message(self, message):
        if str(message.author.id) == '456247418288209922':
            return
        randomXP = randint(5, 25)
        userAddXP(message.author.id, randomXP)

    @commands.command(pass_context=True)
    async def xpstats(self, ctx):
        embed = discord.Embed(title="Leveling Stats - {}".format(ctx.message.author), description='Currently Level //Working on this', color = 0x25C740)
        embed.set_thumbnail(url=ctx.message.author.avatar_url)
        embed.add_field(name="Experience Points", value="XXXX/XXXX ({})".format(getXP(ctx.message.author.id)), inline=True)
        embed.add_field(name="Rank", value = "XX/XXXX", inline = True)
        embed.set_footer(text="Requested by {}".format(ctx.message.author))
        embed.timestamp = datetime.utcnow()
        
        await self.bot.send_message(ctx.message.channel, embed=embed)

    
def setup(bot):
    bot.add_cog(XpSystem(bot))
