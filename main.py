#Bot by clemente#7106 :D

import discord
import asyncio
import math
import datetime
import requests
import json

from discord.ext import commands
from discord.ext.commands import Bot
from datetime import datetime, time, date
from random import randint
from io import StringIO

dab1 = '<:dab1:451466188925698058>'
dab2 = '<:dab2:451466199725899797>'
upvote = '<:upvote:452583845305384981>'
downvote = '<:downvote:452583859532333067>'


bot = commands.Bot(command_prefix="!")
bot.remove_command("help")
client = discord.Client()

# Set the channel you're logging to. Do "\#your-channel-name-here" to get the ID for your channel and put it here.
"""a = open('loggingchannel.txt', 'r')
channel = a.read()
a.close()

log_channel = ('{}'.format(channel))"""



@bot.event
async def on_ready():
    number_of_servers = len(bot.servers) # List the number of things inside the dict value for bot.servers. This comes out to the number of servers the bot is on.
    await bot.change_presence(game=discord.Game(name='on {} servers'.format(number_of_servers))) # set the playing status to the number of servers the bot is on
    print ("Launched...")
    print ("My name is " + bot.user.name)
    print ("ID: " + bot.user.id)

@bot.command(pass_context=True)
async def status(ctx, *, message): # Change the status to whatever you want. Try '!status this is a cool bot'
    if message == "servers": # Use the '!status servers' command to set the playing status back to number of servers the bot is on.
        number_of_servers = len(bot.servers)
        await bot.change_presence(game=discord.Game(name='on {} servers'.format(number_of_servers)))
    elif message == "members":
        guild_members = len(set(bot.get_all_members()))
        await bot.change_presence(game=discord.Game(name='with {} children'.format(guild_members)))
    else:
        await bot.change_presence(game=discord.Game(name='{}'.format(message)))


@bot.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(title='Help Command', description="**Invite Link:** https://discordapp.com/api/oauth2/authorize?client_id=451978077745184785&permissions=8&scope=bot", color = 0xf6d025)
    embed.add_field(name="Status", value = "**Description:** Changes the status of the 'Playing' message for PineappleBot.\n**Permission Required:** None\n**Arguments:** `servers`, `members`, `any message here`\n```!status with legos```", inline=False)
    embed.add_field(name="StaffVote", value = "**Description:** Sends an embed to vote for staff position through reacting with an upvote or downvote.\n**Permission Required:** Administrator\n**Arguments:** `member`\n```!staffvote Eric```", inline=False)
    embed.add_field(name="Channelid", value = "**Description:** Sends the channel id of the current channel.\n**Permission Required:** None\n**Arguments:** None\n```!channelid```", inline=False)
    embed.add_field(name="Mute/Unmute", value = "**Description:** Mute/Unmute a user.\n**Permission Required:** Manage Roles\n**Arguments:** `user` `reason`\n```[!mute | !unmute] @user this is a reason```", inline=False)
    embed.add_field(name="Info", value = "**Description:** Gives you info on a user.\n**Permission Required:** @Moderators\n**Arguments:** `user`\n```!info @user```", inline=False)
    embed.add_field(name="ServerInfo", value = "**Description:** Gives you info on the current server.\n**Permission Required:** Administrator\n**Arguments:** None\n```!serverinfo```", inline=False)
    embed.add_field(name="Kick", value = "**Description:** Kicks a user from the server.\n**Permission Required:** Kick Members\n**Arguments:** `user`\n```!kick @user```", inline=False)
    embed.add_field(name="Ban", value = "**Description:** Bans a user.\n**Permission Required:** Ban Members\n**Arguments:** `user`\n```!ban @user```", inline=False)
    embed.add_field(name="Clear", value = "**Description:** Clears messages from a channel. Can only delete messages in the range of [2, 100]\n**Permission Required:** Administrator\n**Arguments:** `integer`\n```!clear 50```", inline=False)
    embed.add_field(name="hmmcount", value = "**Description:** Shows a count of how many times Pineapple has replied with a thonk.\n**Permission Required** None\n**Arguments:** None\n```hmmcount```", inline=False)
    embed.add_field(name="Duck", value = "**Description:** Loads a random picture of a duck\n**Permission Required** None\n**Arguments:** None\n```!duck```")
    embed.add_field(name="Dog", value = "**Description:** Loads a random picture of a dog\n**Permission Required** None\n**Arguments:** None\n```!dog```", inline=False)
    embed.add_field(name="Shib", value = "**Description:** Loads a random picture of a shiba\n**Permission Required** None\n**Arguments:** None\n```!shib```")
    embed.add_field(name="Dab", value = "**Description:** Dab\n**Permission Required** None\n**Arguments:** None\n```!dab```")
    embed.add_field(name="Created By", value="\n**clemente#7106**\nWith help from\n**exofeel#3333**\nTry `!trackrr` !\n:)")

    await bot.say("Check your DMs")
    await bot.send_message(ctx.message.author, embed=embed)
    await bot.delete_message(ctx.message)

    

@bot.command(pass_context=True)
async def trackrr(ctx):
    embed = discord.Embed(colour=discord.Colour(0x676767))

    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/452763485743349761/452763574503211008/trackrr.png")
    embed.set_author(name="Trackrr Music Search", icon_url="https://cdn.discordapp.com/attachments/452763485743349761/452763575878942720/TrackrrLogo.png")
    embed.set_footer(text="Trackrr Music Search | Created by exofeel")

    embed.add_field(name="Invite Link:", value="[Invite Trackrr to your server](https://cdn.discordapp.com/attachments/452763485743349761/452763574503211008/trackrr.png)")
    embed.add_field(name="What is Trackrr?", value="Trackrr is a discord bot that searches through the most important streaming websites and find the song that you have asked.")
    embed.add_field(name="What services does this search through?", value="Currently, Trackrr searches through **Spotify, Apple Music, Soundcloud and YouTube**. With other streaming websites coming soon. (Depending on the websites API)")
    embed.add_field(name="Need help on how to use it?", value="You can check the help command by doing \n\n``^help`` \n\n Currently, there is no way to change the prefix.")
    embed.add_field(name="<:TrackrrTwitter:452765661484285952>", value="Follow me on twitter\n[@exofeel_dev](https://twitter.com/exofeel_dev)", inline=True)
    embed.add_field(name="<:TrackrrPayPal:452765247581847562>", value="Feeling generous?\nDonate to me on PayPal\n[me@exofeel.com](https://www.paypal.com/us/webapps/mpp/send-money-online)", inline=True)

    await bot.say(embed=embed)



# STAFF VOTE COMMAND -------------------------------------------------------------------------------------------
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def staffvote(ctx, *, person: str):
    emoji1 = discord.utils.get(bot.get_all_emojis(), name = "upvote")
    emoji2 = discord.utils.get(bot.get_all_emojis(), name = "downvote")
    embed = discord.Embed(title='Staff vote for {}'.format(person), description='Vote whether we allow {} access to staff channels'.format(person), color=0xf6d025)
    embed.add_field(name='Note:', value="Allowing anyone into staff is a risky move. Vote yes only if you trust the person. If you're not comfortable with them being here, then vote no.\nMessage will be deleted after the vote is finished.", inline=False)
    embed.add_field(name='Vote below', value="Reply with <:upvote:452583845305384981> to vote **Yes**\n \nReact with <:downvote:452583859532333067> to vote **No**")
    embed.set_footer(text="Requested by {}".format(ctx.message.author))
    embed.timestamp = datetime.utcnow()

    msg = await bot.say(embed=embed)
    await bot.delete_message(ctx.message)
    await bot.add_reaction(msg, emoji1)
    await bot.add_reaction(msg, emoji2)

@staffvote.error
async def staffvote_error(ctx, error):
    if isinstance(error, discord.ext.commands.CheckFailure):
        userID = (ctx.message.author.id)
        await bot.send_message(ctx.message.author,"<@%s>: **You don't have permission to perform this action**" % (userID))
        await bot.delete_message(ctx.message)
    
    elif isinstance(error, discord.ext.commands.MissingRequiredArgument):
        userID = (ctx.message.author.id)
        await bot.send_message(ctx.message.channel,"<@%s>: **Make to sure to specify who the vote is for. ```!staffvote Brandon```" % (userID))
        await bot.delete_message(ctx.message)



# ---------------------------------------------------------------LOGGING CHANNEL----------------------------------------------------------------------
"""@bot.command(pass_context=True)
async def enablelogging(ctx):
    f = open('loggingchannel.txt', 'r')
    loggingChannel = f.read()
    f.close()
    loggingChannel = ctx.message.channel.id
    f = open('loggingchannel.txt', 'w')
    f.write(loggingChannel)
    f.close()
"""

# Add Command
@bot.command()
async def add(*left : int, right : int):
    # Simple command to add numbers
    await bot.say(left + right)

# ---------------------------------------------------------------CHANNEL ID----------------------------------------------------------------------
@bot.command(pass_context=True)
async def channelid(ctx):
    await bot.say('the channel id is: {}'.format(ctx.message.channel.id))

# ---------------------------------------------------------------MUTE/UNMUTE COMMAND----------------------------------------------------------------------
# Mute command
@bot.command(pass_context=True)
@commands.has_permissions(manage_roles=True)
async def mute(ctx, user: discord.Member, *, reason: str = "No reason specified"):
    
    log_channel = discord.utils.get(ctx.message.server.channels, name = 'public-mod-logs')
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
    await bot.send_message(log_channel, embed=embed)
    await bot.add_roles(user, role)
    print("muted")
    await bot.delete_message(ctx.message)

""" await asyncio.sleep(time)
    try:
        await bot.remove_roles(user, role)
        print("unmuted")
    except:
        pass"""

@mute.error
async def mute_error(error, ctx):
    if isinstance(error, discord.ext.commands.BadArgument):
        userID = (ctx.message.author.id)
        botMessage = await bot.send_message(ctx.message.channel,"<@%s>: **Sorry, I couldn't find this user**" % (userID))
        await bot.delete_message(ctx.message)        
        await asyncio.sleep(5)
        try:
            await bot.delete_message(botMessage)
        except:
            pass

    
    elif isinstance(error, discord.ext.commands.CheckFailure):
        userID = (ctx.message.author.id)
        await bot.send_message(ctx.message.author,"<@%s>: **You don't have permission to perform this action**" % (userID))
        await bot.delete_message(ctx.message)


# Unmute command
@bot.command(pass_context=True)
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, user: discord.Member, *, reason: str = "No reason specified"):

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
    await bot.send_message(log_channel, embed=embed)
    await bot.remove_roles(user, role)
    await bot.delete_message(ctx.message)

@unmute.error
async def unmute_error(error, ctx):
    if isinstance(error, discord.ext.commands.BadArgument):
        userID = (ctx.message.author.id)
        botMessage = await bot.send_message(ctx.message.channel,"<@%s>: **Sorry, I couldn't find this user**" % (userID))
        await bot.delete_message(ctx.message)        
        await asyncio.sleep(5)
        try:
            await bot.delete_message(botMessage)
        except:
            pass
    
    elif isinstance(error, discord.ext.commands.CheckFailure):
        userID = (ctx.message.author.id)
        await bot.send_message(ctx.message.author,"<@%s>: **You don't have permission to perform this action**" % (userID))
        await bot.delete_message(ctx.message)

# ---------------------------------------------------------------USER INFO----------------------------------------------------------------------
@bot.command(pass_context=True)
@commands.has_permissions(ban_members=True)
async def info(ctx, user: discord.Member):
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
    await bot.say(embed=embed)
    print("User's info requested")
    await bot.delete_message(ctx.message)

@info.error
async def info_error(error, ctx):
    if isinstance(error, discord.ext.commands.BadArgument):
        userID = (ctx.message.author.id)
        botMessage = await bot.send_message(ctx.message.channel,"<@%s>: **Sorry, I couldn't find this user**" % (userID))
        await bot.delete_message(ctx.message)        
        await asyncio.sleep(5)
        try:
            await bot.delete_message(botMessage)
        except:
            pass
    
    elif isinstance(error, discord.ext.commands.CheckFailure):
        userID = (ctx.message.author.id)
        await bot.send_message(ctx.message.author,"<@%s>: **You don't have permission to perform this action**" % (userID))
        await bot.delete_message(ctx.message)

# ---------------------------------------------------------------SERVER INFO----------------------------------------------------------------------
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def serverinfo(ctx):
    embed = discord.Embed(title="{}'s info".format(ctx.message.server.name), description="Information on the server", color=0xcc0000)
    embed.add_field(name="Server Name", value=ctx.message.server.name, inline=True)
    embed.add_field(name="Server ID", value=ctx.message.server.id, inline=True)
    embed.add_field(name="Members", value=len(ctx.message.server.members))
    embed.add_field(name="Owner", value=ctx.message.server.owner, inline=False)

    servMade = ctx.message.server.created_at
    servMade2 = servMade.strftime("%B %d, %Y %I:%M %p")
    embed.add_field(name="Created", value="{}".format(servMade2))

    embed.set_thumbnail(url=ctx.message.server.icon_url)
    embed.set_footer(text="Requested by {}".format(ctx.message.author))
    embed.timestamp = datetime.utcnow()
    await bot.say(embed=embed)
    print("Server Info requested")
    await bot.delete_message(ctx.message)


@serverinfo.error
async def serverinfo_error(error, ctx):
    if isinstance(error, discord.ext.commands.CheckFailure):
        userID = (ctx.message.author.id)
        await bot.send_message(ctx.message.author,"<@%s>: **You don't have permission to perform this action**" % (userID))
        await bot.delete_message(ctx.message)

# ---------------------------------------------------------------KICK COMMAND----------------------------------------------------------------------
@bot.command(pass_context=True)
@commands.has_permissions(kick_members=True) 
async def kick(ctx, user: discord.Member, *, reason: str = "No reason specified"):

    log_channel = discord.utils.get(bot.get_all_channels(), name = 'public-mod-logs')
    userID = (user.id)
    embed = discord.Embed(title="Member Kicked", color = 0x3C80E2)
    embed.add_field(name="Member", value="{} ".format(user) + "(<@{}>)".format(userID), inline=True)
    embed.add_field(name="Mod", value="{}".format(ctx.message.author), inline=True)
    embed.add_field(name="Reason", value="{}".format(reason), inline=False)
    embed.set_thumbnail(url=user.avatar_url)
    embed.timestamp = datetime.utcnow()

#   await bot.send_message(discord.Object(id=log_channel), embed=embed)
    await bot.send_message(log_channel, embed=embed)
    await bot.kick(user)
    await bot.delete_message(ctx.message)

@kick.error
async def kick_error(error, ctx):
    if isinstance(error, discord.ext.commands.BadArgument):
        userID = (ctx.message.author.id)
        botMessage = await bot.send_message(ctx.message.channel,"<@%s>: **Sorry, I couldn't find this user**" % (userID))
        await bot.delete_message(ctx.message)        
        await asyncio.sleep(5)
        try:
            await bot.delete_message(botMessage)
        except:
            pass
    
    elif isinstance(error, discord.ext.commands.CheckFailure): # Message to the user if they don't have perms
        userID = (ctx.message.author.id)
        await bot.send_message(ctx.message.author,"<@%s>: **You don't have permission to perform this action**" % (userID))
        await bot.delete_message(ctx.message)


# ---------------------------------------------------------------BAN COMMAND----------------------------------------------------------------------
@bot.command(pass_context=True)
@commands.has_permissions(ban_members=True) 
async def ban(ctx, user: discord.Member, *, reason: str = "No reason specified"):

    log_channel = discord.utils.get(ctx.message.server.channels, name = 'public-mod-logs')
    userID = (user.id) 
    embed = discord.Embed(title="Member Banned", color = 0xD82626)
    embed.add_field(name="Member", value="{} ".format(user) + "(<@{}>)".format(userID), inline=True)
    embed.add_field(name="Mod", value="{}".format(ctx.message.author), inline=True)
    embed.add_field(name="Reason", value="{}".format(reason), inline=False)
    embed.set_thumbnail(url=user.avatar_url)
    embed.timestamp = datetime.utcnow()

#   await bot.send_message(discord.Object(id=log_channel), embed=embed)
    await bot.send_message(log_channel, embed=embed)
    await bot.ban(user)
    await bot.delete_message(ctx.message)
 
@ban.error
async def ban_error(error, ctx):
    if isinstance(error, discord.ext.commands.BadArgument):
        userID = (ctx.message.author.id)
        botMessage = await bot.send_message(ctx.message.channel,"<@%s>: **Sorry, I couldn't find this user**" % (userID))
        await bot.delete_message(ctx.message)        
        await asyncio.sleep(5)
        try:
            await bot.delete_message(botMessage)
        except:
            pass
    
    elif isinstance(error, discord.ext.commands.CheckFailure): # Message to the user if they don't have perms
        userID = (ctx.message.author.id)
        await bot.send_message(ctx.message.author,"<@%s>: **You don't have permission to perform this action**" % (userID))
        await bot.delete_message(ctx.message)
        
    elif isinstance(error, discord.ext.commands.CommandInvokeError):
        userID = (ctx.message.author.id)
        await bot.send_message(ctx.message.channel,"<@%s>: **You can't ban yourself**" % (userID))
        await bot.delete_message(ctx.message)
        await asyncio.sleep(5)
        try:
            await bot.delete_message(botMessage)
        except:
            pass

# ---------------------------------------------------------------CLEAR COMMAND----------------------------------------------------------------------
@bot.command(pass_context = True)
@commands.has_permissions(ban_members=True)
async def clear(ctx, number):
    mgs = [] #Empty list to put all the messages in the log
    number = int(number) #Converting the amount of messages to delete to an integer
    async for x in bot.logs_from(ctx.message.channel, limit = number):
        mgs.append(x)
    await bot.delete_messages(mgs)

@clear.error
async def clear_error(error, ctx):
    if isinstance(error, discord.ext.commands.CheckFailure): # Message to the user if they don't have perms
        userID = (ctx.message.author.id)
        await bot.send_message(ctx.message.author,"<@%s>: **You don't have permission to perform this action**" % (userID))
        await bot.delete_message(ctx.message)

    elif isinstance(error, discord.ext.commands.MissingRequiredArgument):
        userID = (ctx.message.author.id)
        await bot.send_message(ctx.message.channel,"<@%s>: **Missing Required Argument:** *integer.* Try `!clear 50`" % (userID))
        await bot.delete_message(ctx.message)

    elif isinstance(error, discord.ext.commands.CommandInvokeError):
        userID = (ctx.message.author.id)
        await bot.send_message(ctx.message.channel,"<@%s>: **Can only delete messages in the range of [2, 100]" % (userID))
        await bot.delete_message(ctx.message)


# ---------------------------------------------------------------ON_MESSAGE EVENT----------------------------------------------------------------------
chat_filter = [] #put words here in CAPS or it wont work. Strings seperated by commas.

@bot.event
async def on_message(message):
    await bot.process_commands(message)

#Adds a reaction if the user says 'hmm'
    if message.content.upper().startswith('HMM'):
	    if str(message.channel.id) == '368299513489915904':
		    return
	    hmm = discord.utils.get(bot.get_all_emojis(), name = "thonk") #Get the thonk emoji from the server
	    await bot.add_reaction(message, hmm)
	    f = open('hmm.txt', 'r')
	    count = f.read()
	    f.close()
	    count = int(count)
	    count += 1
	    count = str(count)
	    f = open('hmm.txt', 'w')
	    f.write(count)
	    f.close()
    if message.content.lower().startswith('hmmcount'):
	    f = open('hmm.txt', 'r')
	    count = f.read()
	    f.close()
	    await bot.send_message(message.channel, '**{}** hmms'.format(count))


# Adds a reaction if a message contains all letters of the alphabet
    if 'a' in message.content.lower():
	    if 'b' in message.content.lower():
		    if 'c' in message.content.lower():
			    if 'd' in message.content.lower():
				    if 'e' in message.content.lower():
					    if 'f' in message.content.lower():
						    if 'g' in message.content.lower():
							    if 'h' in message.content.lower():
								    if 'i' in message.content.lower():
									    if 'j' in message.content.lower():
										    if 'k' in message.content.lower():
											    if 'l' in message.content.lower():
												    if 'm' in message.content.lower():
													    if 'n' in message.content.lower():
														    if 'o' in message.content.lower():
															    if 'p' in message.content.lower():
																    if 'q' in message.content.lower():
																	    if 'r' in message.content.lower():
																		    if 's' in message.content.lower():
																			    if 't' in message.content.lower():
																				    if 'u' in message.content.lower():
																					    if 'v' in message.content.lower():
																						    if 'w' in message.content.lower():
																							    if 'x' in message.content.lower():
																								    if 'y' in message.content.lower():
																									    if 'z' in message.content.lower():
																										    await bot.add_reaction(message, '\U0001F98A')
																										    f = open('az.txt', 'r')
																										    count = f.read()
																										    f.close()
																										    count = int(count)
																										    count += 1
																										    count = str(count)
																										    f = open('az.txt', 'w')
																										    f.write(count)
																										    f.close()
																										    log = open('log.txt', 'a')
																										    now = datetime.now()
																										    formatTime = now.strftime("%B %d, %Y %I:%M %p")
																										    msg = "Server:{}\nChannel:#{}\nAuthor:{}\nAuthorID:{}\nMessage:{}\nTime:{}\n -------------\n".format(message.server, message.channel, message.author, message.author.id, message.content, formatTime)
																										    log.write(msg)
																										    log.close()


    if message.content.lower().startswith('azcount'):
	    f = open('az.txt', 'r')
	    count = f.read()
	    f.close()
	    await bot.send_message(message.channel, "**{}** a-z's".format(count))

    if message.content.lower().startswith('!inv'):
        await bot.send_message(message.channel, '**INVITE PINEAPPLEBOT TO YOUR OWN SERVER:** \nhttps://discordapp.com/oauth2/authorize?client_id=451978077745184785&scope=bot')

    if message.content.lower().startswith('!duck'):
	    msg = await bot.send_message(message.channel, 'loading...')
	    num = randint(1, 114)
	    e = discord.Embed(colour=0xffffff,)
	    url = 'https://duckgroup.xyz/img/imagebot/duck/%d.jpg' % (num)
	    e.set_image(url=url)
	    e.set_footer(text='Duck #%d | requested by %s' % (num, message.author), icon_url='')
	    await bot.send_message(message.channel, embed=e, content='')
	    await bot.delete_message(msg)
	

    if message.content.lower().startswith('!shib'):
	    msg = await bot.send_message(message.channel, 'loading...')
	    e = discord.Embed(colour=0xffffff,)
	    url = requests.get("https://dog.ceo/api/breed/shiba/images/random").json()["message"]
	    e.set_image(url=url)
	    e.set_footer(text='shiba requested by %s' % (message.author), icon_url='')
	    await bot.send_message(message.channel, embed=e, content='')
	    await bot.delete_message(msg)
	
	
    if message.content.lower().startswith('!dog'):
	    msg = await bot.send_message(message.channel, 'loading...')
	    e = discord.Embed(colour=0xffffff,)
	    url = requests.get("https://dog.ceo/api/breeds/image/random").json()["message"]
	    e.set_image(url=url)
	    e.set_footer(text='dog requested by %s' % (message.author), icon_url='')
	    await bot.send_message(message.channel, embed=e, content='')
	    await bot.delete_message(msg)

	
    if message.content.startswith('!dab'):
        msg = await bot.send_message(message.channel, dab1)
        asyncio.sleep(0.4)
        await bot.edit_message(msg, dab2)
        asyncio.sleep(0.4)
        await bot.edit_message(msg, dab1)
        asyncio.sleep(0.4)
        await bot.edit_message(msg, dab2)
        asyncio.sleep(0.4)
        await bot.edit_message(msg, dab1)
        asyncio.sleep(0.4)
        await bot.edit_message(msg, dab2)
        asyncio.sleep(0.4)
        await bot.edit_message(msg, dab1)
        asyncio.sleep(0.4)
        await bot.edit_message(msg, dab2)
        asyncio.sleep(0.4)
        await bot.edit_message(msg, dab1)
        asyncio.sleep(0.4)
        await bot.edit_message(msg, dab2)
        asyncio.sleep(0.4)
        await bot.edit_message(msg, dab1)




    if message.content == 'ping': #useless ping command
        userID = (message.author.id)
        await bot.send_message(message.channel, "<@%s> Pong" % (userID))
    if message.content == 'h':
        await bot.send_message(message.channel, 'shoui is stupid')
    contents = message.content.split(" ") #contents is a list type
    for word in contents:
        if word.upper() in chat_filter:
            userID = (message.author.id) 
            await bot.delete_message(message)
            await bot.send_message(message.author, "<@%s>: **What you just said has caught our word filters and has been removed**." % (userID))

# Insert your token here
bot.run("insert_bot_token")