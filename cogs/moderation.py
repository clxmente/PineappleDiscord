import discord
import datetime
import asyncio
import json

from discord.ext import commands
from random import randint
from datetime import datetime

with open('db/admin.json') as admn:
    admin = json.load(admn)

with open('db/privlogs.json') as admn:
    privlogs = json.load(admn)


def updateDatabase(db, name):
        with open(f"db/{name}.json", 'w') as dbfile:
            json.dump(db, dbfile, indent=4)

class Moderation(object):
    def __init__(self, bot):
        self.bot = bot


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
            await self.bot.send_message(ctx.message.channel,"<@%s>: **Make sure to give the role a name.```!cr [role name]```" % (userID))
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
    async def staffvote(self, ctx, *, person: str):
        emoji1 = discord.utils.get(self.bot.get_all_emojis(), name = "upvote")
        emoji2 = discord.utils.get(self.bot.get_all_emojis(), name = "downvote")
        embed = discord.Embed(title='Staff vote for {}'.format(person), description='Vote whether we allow {} access to staff channels'.format(person), color=0xf6d025)
        embed.add_field(name='Note:', value="Allowing anyone into staff is a risky move. Vote yes only if you trust the person. If you're not comfortable with them being here, then vote no.\nMessage will be deleted after the vote is finished.", inline=False)
        embed.add_field(name='Vote below', value="Reply with <:upvote:452583845305384981> to vote **Yes**\n \nReact with <:downvote:452583859532333067> to vote **No**")
        embed.set_footer(text="Requested by {}".format(ctx.message.author))
        embed.timestamp = datetime.utcnow()

        msg = await self.bot.say(embed=embed)
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
            await self.bot.send_message(ctx.message.channel,"<@%s>: **Make to sure to specify who the vote is for. ```!staffvote Brandon```" % (userID))
            await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_roles=True)
    async def timeout(self, ctx, user: discord.Member, *, reason: str = "No reason specified"):
        server = ctx.message.server
        if (server.id in admin["servers"]):
            log_channel = server.get_channel(admin["servers"][server.id]) # Get the channel from the database
            print(log_channel)
        
        #log_channel = discord.utils.get(ctx.message.server.channels, name = 'public-mod-logs')
        # Specify  what role your adding. In this case its the muted role since we're muting/unmuting the user
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
        # Specify  what role your adding. In this case its the muted role since we're muting/unmuting the user
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
    async def mute(self, ctx, user: discord.Member, *, reason: str = "No reason specified"):
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
    #   embed.add_field(name="Duration", value="{} seconds".format(time), inline=True)
        embed.add_field(name="Reason", value="{}".format(reason), inline=True)


        embed.set_thumbnail(url=user.avatar_url)
        embed.timestamp = datetime.utcnow()

    #   await bot.send_message(discord.Object(id=log_channel), embed=embed)
        await self.bot.send_message(log_channel, embed=embed)
        await self.bot.add_roles(user, role)
        print("muted")
        await self.bot.delete_message(ctx.message)

    """ await asyncio.sleep(time)
        try:
            await bot.remove_roles(user, role)
            print("unmuted")
        except:
            pass"""

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

    #   await bot.send_message(discord.Object(id=log_channel), embed=embed)
        await self.bot.send_message(log_channel, embed=embed)
        await self.bot.kick(user)
        await self.bot.delete_message(ctx.message)

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