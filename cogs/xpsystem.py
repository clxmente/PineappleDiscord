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

def user_add_xp(user_id: int, xp: int):
    if os.path.isfile("db/users.json"):
        try:
            with open('db/users.json', 'r') as fp:
                users = json.load(fp)
            users[user_id]['xp'] += xp
            with open('db/users.json', 'w') as fp:
                json.dump(users, fp, sort_keys=True, indent=4)
        except KeyError:
            with open('db/users.json', 'r') as fp:
                users = json.load(fp)
            users[user_id] = {}
            users[user_id]['xp'] = xp
            with open('db/users.json', 'w') as fp:
                json.dump(users, fp, sort_keys=True, indent=4)

    else:
        users = {user_id: {}}
        users[user_id]['xp'] = xp
        with open('db/users.json', 'w') as fp:
            json.dump(users, fp, sort_keys=True, indent=4)


def user_remove_xp(user_id: int, xp: int):
    if os.path.isfile("db/users.json"):
        try:
            with open('db/users.json', 'r') as fp:
                users = json.load(fp)
            users[user_id]['xp'] -= xp
            with open('db/users.json', 'w') as fp:
                json.dump(users, fp, sort_keys=True, indent=4)
        except KeyError:
            with open('db/users.json', 'r') as fp:
                users = json.load(fp)
            users[user_id] = {}
            users[user_id]['xp'] = 0
            with open('db/users.json', 'w') as fp:
                json.dump(users, fp, sort_keys=True, indent=4)
    else:
        users = {user_id: {}}
        users[user_id]['xp'] = 0
        with open('db/users.json', 'w') as fp:
            json.dump(users, fp, sort_keys=True, indent=4)

def getXP(user_id: int):
    if os.path.isfile('db/users.json'):
        with open('db/users.json', 'r') as fp:
            users = json.load(fp)
        return users[user_id]['xp']
    else:
        return 0

def setLevel(user_id: int, level: int):
    if os.path.isfile('db/users.json'):
        with open('db/users.json', 'r') as fp:
            users = json.load(fp)
        users[user_id]["Level"] = level
        with open('db/users.json', 'w') as fp:
            json.dump(users, fp, sort_keys=True, indent=4)

def getLevel(user_id: int):
    if os.path.isfile('db/users.json'):
        try:
            with open('db/users.json', 'r') as fp:
                users = json.load(fp)
            return users[user_id]['Level']
        except KeyError:
            return 0


class XpSystem(object):
    def __init__(self, bot):
        self.bot = bot

    @client.event
    async def on_message(self, message):
        if str(message.author.id) == '456247418288209922':
            return

        randomXP = randint(7, 25)
        user_add_xp(message.author.id, randomXP)

        if getXP(message.author.id) >= round(0.45 * (int(getLevel(message.author.id)) ** 3) + 80 * (int(getLevel(message.author.id)) ** 2) + 20 * int(getLevel(message.author.id))):
            setLevel(message.author.id, int(getLevel(message.author.id)) + 1)


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

    @commands.command(pass_context=True)
    async def givexp(self, ctx, user: discord.Member, amountxp: int):
        if str(ctx.message.author.id) == '393069508027351051':
            user_add_xp(user.id, int(amountxp))
            await self.bot.say("Increased {}'s XP by {}.".format(user.name, amountxp))
        else: 
            await self.bot.say("⛔️ | Bot Owner Only.")

    @commands.command(pass_context=True)
    async def removexp(self, ctx, user: discord.Member, amountxp: int):
        if str(ctx.message.author.id) == '393069508027351051':
            user_remove_xp(user.id, int(amountxp))
            await self.bot.say("Removed {} XP from {}.".format(amountxp, user.name))
        else: 
            await self.bot.say("⛔️ | Bot Owner Only.")
        

    
def setup(bot):
    bot.add_cog(XpSystem(bot))
