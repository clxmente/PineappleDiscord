import discord
import datetime
import asyncio
import json
import os 
import os.path


from discord.ext import commands
from os.path import isfile, join
from os import listdir
from random import randint
from datetime import datetime

with open('db/admin.json') as admn:
    admin = json.load(admn)

with open('db/privlogs.json') as admn:
    privlogs = json.load(admn)

with open('db/users.json') as fp:
    users = json.load(fp)


def updateDatabase(db, name):
        with open("db/{}.json".format(name), 'w') as dbfile:
            json.dump(db, dbfile, indent=4)

seconds_in_unit = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800} # Gives us the seconds per unit used for timed mutes.
def convertToSeconds(timeduration):
    return int(timeduration[:-1]) * seconds_in_unit[timeduration[-1]]



def addWarnPoints(user_id: int, warnpoints: int):
    if os.path.isfile("db/users.json"):
        try:
            with open('db/users.json', 'r') as fp:
                users = json.load(fp)
            users[user_id]['warnpoints'] += warnpoints
            with open('db/users.json', 'w') as fp:
                json.dump(users, fp, sort_keys=True, indent=4)
        except KeyError:
            with open('db/users.json', 'r') as fp:
                users = json.load(fp)
            users[user_id] = {}
            users[user_id]['warnpoints'] = warnpoints
            with open('db/users.json', 'w') as fp:
                json.dump(users, fp, sort_keys=True, indent=4)

    else:
        users = {user_id: {}}
        users[user_id]['warnpoints'] = warnpoints
        with open('db/users.json', 'w') as fp:
            json.dump(users, fp, sort_keys=True, indent=4)


def removeWarnPoints(user_id: int, warnpoints: int):
    if os.path.isfile("db/users.json"):
        try:
            with open('db/users.json', 'r') as fp:
                users = json.load(fp)
            users[user_id]['warnpoints'] -= warnpoints
            with open('db/users.json', 'w') as fp:
                json.dump(users, fp, sort_keys=True, indent=4)
        except KeyError:
            with open('db/users.json', 'r') as fp:
                users = json.load(fp)
            users[user_id] = {}
            users[user_id]['warnpoints'] = 0
            with open('db/users.json', 'w') as fp:
                json.dump(users, fp, sort_keys=True, indent=4)
    else:
        users = {user_id: {}}
        users[user_id]['warnpoints'] = 0
        with open('db/users.json', 'w') as fp:
            json.dump(users, fp, sort_keys=True, indent=4)


def getWarnPoints(user_id: int):
    if os.path.isfile('db/users.json'):
        try:
            with open('db/users.json', 'r') as fp:
                users = json.load(fp)
            return users[user_id]['warnpoints']
        except KeyError:
            return 0





class Moderation(object):
    def __init__(self, bot):
        self.bot = bot

    """async def log_to_channel(self, server, type, embed_color, duration, timeduration, increase, warnpoints, user, moderator, reason): #Function to log to channels without using so much repeated code
            if (server.id in admin["servers"]):
                log_channel = server.get_channel(admin["servers"][server.id])
                embed = discord.Embed(title="Member {}".format(type), colour = discord.Colour(embed_color))
                embed.add_field(name="Member", value="{} (<@{}>)".format(user, user.id), inline=True)
                embed.add_field(name="Mod", value=moderator, inline=True)
                if duration == True:
                    embed.add_field(name="Duration", value=timeduration, inline=True)
                    embed.add_field(name="Reason", value=reason, inline=True)
                elif duration == False:
                    embed.add_field(name="Reason", value=reason, inline=False)
                elif increase == True:
                    embed.add_field(name="Increase", value=warnpoints, inline=True)
                    embed.add_field(name="Reason", value=reason, inline=True)
                elif increase == False:
                    embed.add_field(name="Increase", value=warnpoints, inline=True)
                    embed.add_field(name="Reason", value=reason, inline=True)
                elif increase == None:
                    embed.add_field(name="Reason", value=reason, inline=False)
                else:
                    embed.add_field(name="Reason", value=reason, inline=False)
                embed.set_thumbnail(url=user.avatar_url)
                embed.timestamp = datetime.utcnow()

                await self.bot.send_message(log_channel, embed=embed)"""

    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def warn(self, ctx, user: discord.Member, warnpoints: int, *, reason: str = "No reason specified"):
        addWarnPoints(user.id, warnpoints)
        if int(getWarnPoints(user.id)) >= 1000:
            await self.bot.ban(user)
        else:
            pass
        
        server = ctx.message.server
        if (server.id in admin["servers"]):
            log_channel = server.get_channel(admin["servers"][server.id])
        
        userID = (user.id)
        embed = discord.Embed(title="Member Warned", color = 0xB657D1)
        embed.add_field(name="Member", value="{} ".format(user) + "(<@{}>)".format(userID), inline=False)
        embed.add_field(name="Mod", value="{}".format(ctx.message.author), inline=True)
        embed.add_field(name="Increase", value = warnpoints, inline=True)
        embed.add_field(name="Reason", value="{}".format(reason), inline=False)
        embed.set_thumbnail(url=user.avatar_url)
        embed.timestamp = datetime.utcnow()

        #await self.log_to_channel(ctx.message.server, "Warned", 0xb657d1, False, None, True, warnpoints, user, ctx.message.author, reason) 
        #async def log_to_channel(self, server, type, embed_color, duration, timeduration, thepoints, warnpoints, user, moderator, reason):

        await self.bot.send_message(log_channel, embed=embed)
        await self.bot.delete_message(ctx.message)


    @warn.error
    async def warn_error(self, error, ctx):
        if isinstance(error, discord.ext.commands.CheckFailure):
            userID = (ctx.message.author.id)
            await self.bot.send_message(ctx.message.author,"<@%s>: **You don't have permission to perform this action**" % (userID))
            await self.bot.delete_message(ctx.message)
        
        elif isinstance(error, discord.ext.commands.MissingRequiredArgument):
            userID = (ctx.message.author.id)
            await self.bot.send_message(ctx.message.channel,"<@%s>: **Missing Argument**. Example of command is: ```!warn @user 100 this is a reason```" % (userID))
            await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def dewarn(self, ctx, user: discord.Member, warnpoints: int, *, reason: str = "No reason specified"):
        removeWarnPoints(user.id, warnpoints)
        
        server = ctx.message.server
        if (server.id in admin["servers"]):
            log_channel = server.get_channel(admin["servers"][server.id])
        
        userID = (user.id)
        embed = discord.Embed(title="Member Dewarned", color = 0xFDB509)
        embed.add_field(name="Member", value="{} ".format(user) + "(<@{}>)".format(userID), inline=False)
        embed.add_field(name="Mod", value="{}".format(ctx.message.author), inline=True)
        embed.add_field(name="Decrease", value= warnpoints)
        embed.add_field(name="Reason", value="{}".format(reason), inline=False)
        embed.set_thumbnail(url=user.avatar_url)
        embed.timestamp = datetime.utcnow()

        await self.bot.send_message(log_channel, embed=embed)
        await self.bot.delete_message(ctx.message)

    @dewarn.error
    async def dewarn_error(self, error, ctx):
        if isinstance(error, discord.ext.commands.CheckFailure):
            userID = (ctx.message.author.id)
            await self.bot.send_message(ctx.message.author,"<@%s>: **You don't have permission to perform this action**" % (userID))
            await self.bot.delete_message(ctx.message)
        
        elif isinstance(error, discord.ext.commands.MissingRequiredArgument):
            userID = (ctx.message.author.id)
            await self.bot.send_message(ctx.message.channel,"<@%s>: **Missing Argument**. Example of command is: ```!dewarn @user 100 this is a reason```" % (userID))
            await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def warnpoints(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.message.author

        points = getWarnPoints(user.id)
        pointsleft = 1000 - int(points)

        await self.bot.say("<@{}> has **{}** warn points. ".format(user.id, points) + "Points left: **{}.**".format(pointsleft))


        

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_roles=True)
    async def cr(self, ctx, *, rolename):
        r = randint(0, 0xFFFFFF)

        author = ctx.message.author
        await self.bot.create_role(author.server, name="{}".format(rolename), colour = discord.Colour(r))
        embed = discord.Embed(title='New Role Created', color=0xf6d025)
        embed.add_field(name='Role:', value=rolename, inline=False)
        embed.add_field(name='Color:', value='#{}'.format(r), inline=False)
        embed.set_footer(text="Created by {}".format(ctx.message.author))
        await self.bot.say(embed=embed)
        await self.bot.delete_message(ctx.message)

    @cr.error
    async def cr_error(self, error, ctx):
        if isinstance(error, discord.ext.commands.CheckFailure):
            userID = (ctx.message.author.id)
            await self.bot.send_message(ctx.message.author,"<@%s>: **You don't have permission to perform this action**" % (userID))
            await self.bot.delete_message(ctx.message)
        
        elif isinstance(error, discord.ext.commands.MissingRequiredArgument):
            userID = (ctx.message.author.id)
            await self.bot.send_message(ctx.message.channel,"<@%s>: **Make sure to give the role a name.**```!cr [role name]```" % (userID))
            await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_roles=True)
    async def er(self, ctx, *, therole):
        author = ctx.message.author
        await self.bot.edit_role(author.server, role=discord.utils.get(author.server.roles, name=therole), colour=discord.Colour(randint(0, 0xFFFFFF)))
    
    @er.error
    async def er_error(self, error, ctx):
        if isinstance(error, discord.ext.commands.CheckFailure):
            userID = (ctx.message.author.id)
            await self.bot.send_message(ctx.message.author,"<@%s>: **You don't have permission to perform this action**" % (userID))
            await self.bot.delete_message(ctx.message)
        
        elif isinstance(error, discord.ext.commands.MissingRequiredArgument):
            userID = (ctx.message.author.id)
            await self.bot.send_message(ctx.message.channel,"<@%s>: **Specify which role you're editing.**```!er [role name]```" % (userID))
            await self.bot.delete_message(ctx.message)
        
        elif isinstance(error, discord.ext.commands.CommandInvokeError):
            userID = (ctx.message.author.id)
            await self.bot.send_message(ctx.message.channel, "<@%s>: **Invalid role.** Make sure to check that your spelling was right." % (userID))

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def staffvote(self, ctx, *, message: str):
        emoji1 = discord.utils.get(self.bot.get_all_emojis(), name = "upvote")
        emoji2 = discord.utils.get(self.bot.get_all_emojis(), name = "downvote")
        embed = discord.Embed(title='Staff Vote', description="{}".format(message), color=0xf6d025)
        embed.add_field(name='Vote below', value="Reply with <:upvote:452583845305384981> to vote **Yes**\n \nReact with <:downvote:452583859532333067> to vote **No**")
        embed.timestamp = datetime.utcnow()

        msg = await self.bot.say("@everyone", embed=embed)
        await self.bot.delete_message(ctx.message)
        await self.bot.add_reaction(msg, emoji1)
        await self.bot.add_reaction(msg, emoji2)

    @staffvote.error
    async def staffvote_error(self, error, ctx):
        if isinstance(error, discord.ext.commands.CheckFailure):
            userID = (ctx.message.author.id)
            await self.bot.send_message(ctx.message.author,"<@%s>: **You don't have permission to perform this action**" % (userID))
            await self.bot.delete_message(ctx.message)
        
        elif isinstance(error, discord.ext.commands.MissingRequiredArgument):
            userID = (ctx.message.author.id)
            await self.bot.send_message(ctx.message.channel,"<@%s>: **Make to sure to specify who the vote is for.** ```!staffvote [message]```" % (userID))
            await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_roles=True)
    async def timeout(self, ctx, user: discord.Member, *, reason: str = "No reason specified"):
        server = ctx.message.server
        if (server.id in admin["servers"]):
            log_channel = server.get_channel(admin["servers"][server.id]) # Get the channel from the database
            print(log_channel)
        
        #log_channel = discord.utils.get(ctx.message.server.channels, name = 'public-mod-logs')
        role = discord.utils.get(user.server.roles, name = "Timeout")
        # Send it to the logs
        userID = (user.id)
        embed = discord.Embed(title="Sent to Timeout", color = 0x74E27B)
        embed.add_field(name="Member", value="{} ".format(user) + "(<@{}>)".format(userID), inline=True)
        embed.add_field(name="Mod", value="{}".format(ctx.message.author), inline=True)
    #   embed.add_field(name="Duration", value="{} seconds".format(time), inline=True)
        embed.add_field(name="Reason", value="{}".format(reason), inline=True)


        embed.set_thumbnail(url=user.avatar_url)
        embed.timestamp = datetime.utcnow()

    #   await bot.send_message(discord.Object(id=log_channel), embed=embed)
        await self.bot.send_message(log_channel, embed=embed)
        await self.bot.add_roles(user, role)
        await self.bot.delete_message(ctx.message)

    @timeout.error
    async def timeout_error(self, error, ctx):
        if isinstance(error, discord.ext.commands.BadArgument):
            userID = (ctx.message.author.id)
            botMessage = await self.bot.send_message(ctx.message.channel,"<@%s>: **Sorry, I couldn't find this user**" % (userID))
            await self.bot.delete_message(ctx.message)        
            await asyncio.sleep(5)
            try:
                await self.bot.delete_message(botMessage)
            except:
                pass

        
        elif isinstance(error, discord.ext.commands.CheckFailure):
            userID = (ctx.message.author.id)
            await self.bot.send_message(ctx.message.author,"<@%s>: **You don't have permission to perform this action**" % (userID))
            await self.bot.delete_message(ctx.message)

        elif isinstance(error, discord.ext.commands.CommandInvokeError):
            userID = (ctx.message.author.id)
            await self.bot.send_message(ctx.message.channel, "<@%s>: **Try making sure the role you're adding isn't above PineappleBot.**" % (userID))
    
    @commands.command(pass_context=True)
    @commands.has_permissions(manage_roles=True)
    async def untimeout(self, ctx, user: discord.Member, *, reason: str = "No reason specified"):
        server = ctx.message.server
        if (server.id in admin["servers"]):
            log_channel = server.get_channel(admin["servers"][server.id])
        #log_channel = discord.utils.get(ctx.message.server.channels, name = 'public-mod-logs')
        role = discord.utils.get(user.server.roles, name = "Timeout")
        # Send it to the logs
        userID = (user.id)
        embed = discord.Embed(title="Left Timeout", color = 0xAB2573)
        embed.add_field(name="Member", value="{} ".format(user) + "(<@{}>)".format(userID), inline=True)
        embed.add_field(name="Mod", value="{}".format(ctx.message.author), inline=True)
        embed.add_field(name="Reason", value="{}".format(reason), inline=False)
        embed.set_thumbnail(url=user.avatar_url)
        embed.timestamp = datetime.utcnow()

    #   await bot.send_message(discord.Object(id=log_channel), embed=embed)
        await self.bot.send_message(log_channel, embed=embed)
        await self.bot.remove_roles(user, role)
        await self.bot.delete_message(ctx.message)

    @untimeout.error
    async def untimeout_error(self, error, ctx):
        if isinstance(error, discord.ext.commands.BadArgument):
            userID = (ctx.message.author.id)
            botMessage = await self.bot.send_message(ctx.message.channel,"<@%s>: **Sorry, I couldn't find this user**" % (userID))
            await self.bot.delete_message(ctx.message)        
            await asyncio.sleep(5)
            try:
                await self.bot.delete_message(botMessage)
            except:
                pass

        
        elif isinstance(error, discord.ext.commands.CheckFailure):
            userID = (ctx.message.author.id)
            await self.bot.send_message(ctx.message.author,"<@%s>: **You don't have permission to perform this action**" % (userID))
            await self.bot.delete_message(ctx.message)

    # Mute command
    @commands.command(pass_context=True)
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, user: discord.Member, timeduration, *, reason: str = "No reason specified"):
        server = ctx.message.server
        if (server.id in admin["servers"]):
            log_channel = server.get_channel(admin["servers"][server.id])        
        #log_channel = discord.utils.get(ctx.message.server.channels, name = 'public-mod-logs')
        # Specify  what role your adding. In this case its the muted role since we're muting/unmuting the user
        role = discord.utils.get(user.server.roles, name = "Muted")
        # Send it to the logs
        userID = (user.id)
        embed = discord.Embed(title="Member Muted", color = 0xB760F3)
        embed.add_field(name="Member", value="{} ".format(user) + "(<@{}>)".format(userID), inline=True)
        embed.add_field(name="Mod", value="{}".format(ctx.message.author), inline=True)
        embed.add_field(name="Duration", value=timeduration, inline=True)
        embed.add_field(name="Reason", value="{}".format(reason), inline=True)


        embed.set_thumbnail(url=user.avatar_url)
        embed.timestamp = datetime.utcnow()

    #   await bot.send_message(discord.Object(id=log_channel), embed=embed)
        await self.bot.send_message(log_channel, embed=embed)
        await self.bot.add_roles(user, role)
        print("muted")
        await self.bot.delete_message(ctx.message)

        theTime = convertToSeconds("{}".format(timeduration)) #convert our time argument to seconds
        print(theTime)
        await asyncio.sleep(int(theTime)) # pass the seconds to asyncio.sleep
        try:
            await self.bot.remove_roles(user, role)
            print("unmuted")
        except:
            pass

    @mute.error
    async def mute_error(self, error, ctx):
        if isinstance(error, discord.ext.commands.BadArgument):
            userID = (ctx.message.author.id)
            botMessage = await self.bot.send_message(ctx.message.channel,"<@%s>: **Sorry, I couldn't find this user**" % (userID))
            await self.bot.delete_message(ctx.message)        
            await asyncio.sleep(5)
            try:
                await self.bot.delete_message(botMessage)
            except:
                pass
        
        elif isinstance(error, discord.ext.commands.MissingRequiredArgument):
            userID = (ctx.message.author.id)
            await self.bot.send_message(ctx.message.author,"<@%s>: **Missing Required Argument.** Ex:```!mute @user 2h this is a reason```" % (userID))
            await self.bot.delete_message(ctx.message)
        elif isinstance(error, discord.ext.commands.CheckFailure):
            userID = (ctx.message.author.id)
            await self.bot.send_message(ctx.message.author,"<@%s>: **You don't have permission to perform this action**" % (userID))
            await self.bot.delete_message(ctx.message)

    # Unmute command
    @commands.command(pass_context=True)
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, user: discord.Member, *, reason: str = "No reason specified"):
        server = ctx.message.server
        if (server.id in admin["servers"]):
            log_channel = server.get_channel(admin["servers"][server.id])
        log_channel = discord.utils.get(ctx.message.server.channels, name = 'public-mod-logs')
        # Specify  what role your adding. In this case its the muted role since we're muting/unmuting the user
        role = discord.utils.get(user.server.roles, name = "Muted")
        # Send it to the logs
        userID = (user.id)
        embed = discord.Embed(title="Member Unmuted", color = 0x563F65)
        embed.add_field(name="Member", value="{} ".format(user) + "(<@{}>)".format(userID), inline=True)
        embed.add_field(name="Mod", value="{}".format(ctx.message.author), inline=True)
        embed.add_field(name="Reason", value="{}".format(reason), inline=False)
        embed.set_thumbnail(url=user.avatar_url)
        embed.timestamp = datetime.utcnow()

    #   await bot.send_message(discord.Object(id=log_channel), embed=embed)
        await self.bot.send_message(log_channel, embed=embed)
        await self.bot.remove_roles(user, role)
        await self.bot.delete_message(ctx.message)

    @unmute.error
    async def unmute_error(self, error, ctx):
        if isinstance(error, discord.ext.commands.BadArgument):
            userID = (ctx.message.author.id)
            botMessage = await self.bot.send_message(ctx.message.channel,"<@%s>: **Sorry, I couldn't find this user**" % (userID))
            await self.bot.delete_message(ctx.message)        
            await asyncio.sleep(5)
            try:
                await self.bot.delete_message(botMessage)
            except:
                pass
        
        elif isinstance(error, discord.ext.commands.CheckFailure):
            userID = (ctx.message.author.id)
            await self.bot.send_message(ctx.message.author,"<@%s>: **You don't have permission to perform this action**" % (userID))
            await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def info(self, ctx, user: discord.Member):
        embed = discord.Embed(title="{}'s Info".format(user.name), description="Here's what I found.", color=0x00cda1)
        embed.add_field(name="Username", value=user, inline=True)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="Status", value=user.status, inline=True)
        embed.add_field(name="Highest Role", value=user.top_role)

        userMade = user.created_at
        userMade2 = userMade.strftime("%B %d, %Y %I:%M %p")
        embed.add_field(name="Created", value="{}".format(userMade2))

        userJoin = user.joined_at
        userJoin2 = userJoin.strftime("%B %d, %Y %I:%M %p")
        embed.add_field(name="Joined", value="{}".format(userJoin2))

        embed.set_thumbnail(url=user.avatar_url)
        embed.set_footer(text="Requested by {}".format(ctx.message.author))
        embed.timestamp = datetime.utcnow()
        await self.bot.say(embed=embed)
        print("User's info requested")
        await self.bot.delete_message(ctx.message)

    @info.error
    async def info_error(self, error, ctx):
        if isinstance(error, discord.ext.commands.BadArgument):
            userID = (ctx.message.author.id)
            botMessage = await self.bot.send_message(ctx.message.channel,"<@%s>: **Sorry, I couldn't find this user**" % (userID))
            await self.bot.delete_message(ctx.message)        
            await asyncio.sleep(5)
            try:
                await self.bot.delete_message(botMessage)
            except:
                pass
        
        elif isinstance(error, discord.ext.commands.CheckFailure):
            userID = (ctx.message.author.id)
            await self.bot.send_message(ctx.message.author,"<@%s>: **You don't have permission to perform this action**" % (userID))
            await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def serverinfo(self, ctx):
        embed = discord.Embed(title="{}'s info".format(ctx.message.server.name), description="Information on the server", color=0xcc0000)
        embed.add_field(name="Server Name", value=ctx.message.server.name, inline=True)
        embed.add_field(name="Server ID", value=ctx.message.server.id, inline=True)
        embed.add_field(name="Members", value=len(ctx.message.server.members))
        embed.add_field(name="Owner", value=ctx.message.server.owner, inline=True)
        embed.add_field(name="Role Count", value=len(ctx.message.server.roles))

        servMade = ctx.message.server.created_at
        servMade2 = servMade.strftime("%B %d, %Y %I:%M %p")
        embed.add_field(name="Created", value="{}".format(servMade2))

        embed.set_thumbnail(url=ctx.message.server.icon_url)
        embed.set_footer(text="Requested by {}".format(ctx.message.author))
        embed.timestamp = datetime.utcnow()
        await self.bot.say(embed=embed)
        print("Server Info requested")
        await self.bot.delete_message(ctx.message)


    @serverinfo.error
    async def serverinfo_error(self, error, ctx):
        if isinstance(error, discord.ext.commands.CheckFailure):
            userID = (ctx.message.author.id)
            await self.bot.send_message(ctx.message.author,"<@%s>: **You don't have permission to perform this action**" % (userID))
            await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    @commands.has_permissions(kick_members=True) 
    async def kick(self, ctx, user: discord.Member, *, reason: str = "No reason specified"):
        server = ctx.message.server
        if (server.id in admin["servers"]):
            log_channel = server.get_channel(admin["servers"][server.id])
        #log_channel = discord.utils.get(ctx.message.server.channels, name = 'public-mod-logs')
        userID = (user.id)
        embed = discord.Embed(title="Member Kicked", color = 0x3C80E2)
        embed.add_field(name="Member", value="{} ".format(user) + "(<@{}>)".format(userID), inline=True)
        embed.add_field(name="Mod", value="{}".format(ctx.message.author), inline=True)
        embed.add_field(name="Reason", value="{}".format(reason), inline=False)
        embed.set_thumbnail(url=user.avatar_url)
        embed.timestamp = datetime.utcnow()

        #await bot.send_message(discord.Object(id=log_channel), embed=embed)
        
        
        await self.bot.send_message(log_channel, embed=embed)
        await self.bot.kick(user)
        await self.bot.delete_message(ctx.message)
        #(self, server, embed_color, user, moderator, reason)

    @kick.error
    async def kick_error(self, error, ctx):
        if isinstance(error, discord.ext.commands.BadArgument):
            userID = (ctx.message.author.id)
            botMessage = await self.bot.send_message(ctx.message.channel,"<@%s>: **Sorry, I couldn't find this user**" % (userID))
            await self.bot.delete_message(ctx.message)        
            await asyncio.sleep(5)
            try:
                await self.bot.delete_message(botMessage)
            except:
                pass
        
        elif isinstance(error, discord.ext.commands.CheckFailure): # Message to the user if they don't have perms
            userID = (ctx.message.author.id)
            await self.bot.send_message(ctx.message.author,"<@%s>: **You don't have permission to perform this action**" % (userID))
            await self.bot.delete_message(ctx.message)


    
    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True) 
    async def ban(self, ctx, user: discord.Member, *, reason: str = "No reason specified"):
        server = ctx.message.server
        if (server.id in admin["servers"]):
            log_channel = server.get_channel(admin["servers"][server.id])
        #log_channel = discord.utils.get(ctx.message.server.channels, name = 'public-mod-logs')
        userID = (user.id) 
        embed = discord.Embed(title="Member Banned", color = 0xD82626)
        embed.add_field(name="Member", value="{} ".format(user) + "(<@{}>)".format(userID), inline=True)
        embed.add_field(name="Mod", value="{}".format(ctx.message.author), inline=True)
        embed.add_field(name="Reason", value="{}".format(reason), inline=False)
        embed.set_thumbnail(url=user.avatar_url)
        embed.timestamp = datetime.utcnow()

    #   await bot.send_message(discord.Object(id=log_channel), embed=embed)
        await self.bot.send_message(log_channel, embed=embed)
        await self.bot.ban(user)
        await self.bot.delete_message(ctx.message)
    
    @ban.error
    async def ban_error(self, error, ctx):
        if isinstance(error, discord.ext.commands.BadArgument):
            userID = (ctx.message.author.id)
            botMessage = await self.bot.send_message(ctx.message.channel,"<@%s>: **Sorry, I couldn't find this user**" % (userID))
            await self.bot.delete_message(ctx.message)        
            await asyncio.sleep(5)
            try:
                await self.bot.delete_message(botMessage)
            except:
                pass
        
        elif isinstance(error, discord.ext.commands.CheckFailure): # Message to the user if they don't have perms
            userID = (ctx.message.author.id)
            await self.bot.send_message(ctx.message.author,"<@%s>: **You don't have permission to perform this action**" % (userID))
            await self.bot.delete_message(ctx.message)
            
        elif isinstance(error, discord.ext.commands.CommandInvokeError):
            userID = (ctx.message.author.id)
            await self.bot.send_message(ctx.message.channel,"<@%s>: **You can't ban yourself**" % (userID))
            await self.bot.delete_message(ctx.message)
            await asyncio.sleep(5)
            try:
                await self.bot.delete_message(botMessage)
            except:
                pass

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def enablelogging(self, ctx):
        await self.bot.say('\u2705: This channel is now used for public mod logs!')
        admin["servers"][ctx.message.server.id] = ctx.message.channel.id
        updateDatabase(admin, "admin")

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def privatelogging(self, ctx):
        await self.bot.say('\u2705: This channel is now used for private mod logs!')
        privlogs["servers"][ctx.message.server.id] = ctx.message.channel.id
        updateDatabase(privlogs, "privlogs")
        
            

def setup(bot):
    bot.add_cog(Moderation(bot))