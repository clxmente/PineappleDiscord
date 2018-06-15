#Bot by clemente#7106 :D

import discord
import asyncio
import math
import datetime
import requests
import json
import string
import time
import os
import os.path
import traceback

from discord.ext import commands
from discord.ext.commands import Bot
from datetime import datetime, date
from random import randint
from io import StringIO
from os import listdir
from os.path import isfile, join

dab1 = '<:dab1:451466188925698058>'
dab2 = '<:dab2:451466199725899797>'
upvote = '<:upvote:452583845305384981>'
downvote = '<:downvote:452583859532333067>'


bot = commands.Bot(command_prefix="!")
bot.remove_command("help")
client = discord.Client()

with open('db/admin.json') as admn:
    admin = json.load(admn)

with open('db/privlogs.json') as admn:
    privlogs = json.load(admn)

with open('db/users.json') as fp:
    users = json.load(fp)


@bot.event
async def on_ready():
    number_of_servers = len(bot.servers) # List the number of things inside the dict value for bot.servers. This comes out to the number of servers the bot is on.
    await bot.change_presence(game=discord.Game(name='on {} servers'.format(number_of_servers))) # set the playing status to the number of servers the bot is on
    print ("Launched...")
    print ("My name is " + bot.user.name)
    print ("ID: " + bot.user.id)

@bot.command(pass_context=True)
async def status(ctx, *, message): #Changing the playing status of bot with a command
    if str(ctx.message.author.id) == '393069508027351051': #Only the bot owner can use this command
        if message == "servers": # Use the '!status servers' command to set the playing status back to number of servers the bot is on.
            number_of_servers = len(bot.servers)
            await bot.change_presence(game=discord.Game(name='on {} servers'.format(number_of_servers)))
        elif message == "members":
            guild_members = len(set(bot.get_all_members()))
            await bot.change_presence(game=discord.Game(name='with {} children'.format(guild_members)))
        else:
            await bot.change_presence(game=discord.Game(name='{}'.format(message)))
    else:
        userID = ctx.message.author.id
        await bot.say("<@%s>: Sorry, you aren't my owner." % (userID))


@bot.command(pass_context=True)
async def reload(ctx):
        if ctx.message.author.id == "393069508027351051":
            # Loading
            for extension in [f.replace('.py', "") for f in listdir("cogs") if isfile(join("cogs", f))]:
                try:
                    if not "__init__" in extension:
                        print("Reloading {}...".format(extension))
                        bot.unload_extension("cogs." + extension)
                        loadingCogMessage = await bot.say("Loading {}..".format(extension))
                        bot.load_extension("cogs." + extension)
                        await bot.edit_message(loadingCogMessage, "✅ | {} has been loaded.".format(extension))
                except Exception as e:
                    print("Failed to load cog {}".format(extension))
                    await bot.say("⛔️ | Failed to load cog {}".format(extension))
                    traceback.print_exc()
        else:
            print("Unauthorized user has attempted to reload modules.. Stopped :)")
            await bot.say("⛔️ | Bot owner only!")

@bot.event
async def on_command(cmd, ctx): # Log commands used in a private logging channel.
    server = ctx.message.server
    userID = ctx.message.author.id
    if (server.id in privlogs["servers"]):
        log_channel = server.get_channel(privlogs["servers"][server.id])
    embed = discord.Embed(title='Command Used', color = 0xf6d025)
    embed.add_field(name='Content', value = ctx.message.content, inline=False)
    embed.add_field(name='Channel', value = "#{}".format(ctx.message.channel), inline=False)
    embed.add_field(name='User', value="{} ".format(ctx.message.author) + "(<@{}>)".format(userID), inline=False)
    embed.timestamp = datetime.utcnow()
    embed.set_thumbnail(url=ctx.message.author.avatar_url)

    await bot.send_message(log_channel, embed=embed)

@bot.event
async def on_message_edit(before, after):

    server = before.author.server
    userID = before.author.id

    if (server.id in privlogs["servers"]):
        log_channel = server.get_channel(privlogs["servers"][server.id]) # Oh yea, we're logging it too :)
    
    embed = discord.Embed(title='Message Edited', color = 0xD24D26)
    embed.add_field(name='User', value = '{} '.format(before.author) + "(<@{}>)".format(userID), inline=False)
    embed.add_field(name='Channel', value = "#{}".format(before.channel), inline=False)
    embed.add_field(name='Content Before', value = before.content, inline=True)
    embed.add_field(name='Content After', value = after.content, inline=True)
    embed.timestamp = datetime.utcnow()
    embed.set_thumbnail(url=before.author.avatar_url)
    
    await bot.send_message(log_channel, embed=embed)

@bot.event
async def on_message_delete(message):
    
    server = message.author.server
    userID = message.author.id
    
    if (server.id in privlogs["servers"]):
        log_channel = server.get_channel(privlogs["servers"][server.id])

    embed = discord.Embed(title='Message Deleted', color = 0x1E3F8C)
    embed.add_field(name='User', value="{} ".format(message.author) + "(<@{}>)".format(userID), inline=False)
    embed.add_field(name='Channel', value =message.channel,inline=False)
    embed.add_field(name='Content', value=message.content, inline=False)
    embed.timestamp = datetime.utcnow()
    embed.set_thumbnail(url=message.author.avatar_url)
    
    await bot.send_message(log_channel, embed=embed)

@bot.event
async def on_member_join(member):
    server = member.server
    userID = member.id
    
    if (server.id in privlogs["servers"]):
        log_channel = server.get_channel(privlogs["servers"][server.id])

    embed = discord.Embed(title='Member Joined', color = 0xFD2F48)
    embed.add_field(name="Member", value="{} ".format(member) + "(<@{}>)".format(userID),  inline=True)

    embed.add_field(name='User ID', value=userID)

    memMade = member.created_at
    memMade2 = memMade.strftime("%B %d, %Y %I:%M %p")
    embed.add_field(name='Created At', value=memMade2)

    memJoin = member.joined_at.strftime("%B %d, %Y %I:%M %p")
    embed.add_field(name='Joined', value=memJoin, inline=True)
    
    embed.timestamp = datetime.utcnow()
    embed.set_thumbnail(url=member.avatar_url)
    
    await bot.send_message(log_channel, embed=embed)

@bot.event
async def on_member_remove(member):
    server = member.server
    userID = member.id
    
    if (server.id in privlogs["servers"]):
        log_channel = server.get_channel(privlogs["servers"][server.id])

    embed = discord.Embed(title='Member Left', color = 0xFD2F48)
    embed.add_field(name="Member", value="{} ".format(member) + "(<@{}>)".format(userID),  inline=True)

    embed.add_field(name='User ID', value=userID)

    memMade = member.created_at
    memMade2 = memMade.strftime("%B %d, %Y %I:%M %p")
    embed.add_field(name='Created At', value=memMade2)

    memJoin = member.joined_at.strftime("%B %d, %Y %I:%M %p")
    embed.add_field(name='Joined', value=memJoin, inline=True)

    embed.timestamp = datetime.utcnow()
    embed.set_thumbnail(url=member.avatar_url)
    
    await bot.send_message(log_channel, embed=embed)



def updateDatabase(db, name):
    with open("db/{}.json".format(name), 'w') as dbfile:
        json.dump(db, dbfile, indent=4)


async def LoadCogs():
    for extension in [f.replace('.py', "") for f in listdir("cogs") if isfile(join("cogs", f))]:
        try:
            if not "__init__" in extension:
                print("Loading {}...".format(extension))
                bot.load_extension("cogs." + extension)
        except Exception as e:
            print("Failed to load cog {}".format(extension))
            traceback.print_exc()


@bot.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(title='Help Command', description="**Invite Link:** https://discordapp.com/api/oauth2/authorize?client_id=456247418288209922&permissions=8&scope=bot", color = 0xf6d025)
    
    embed.add_field(name="privatelogging", value = "**Description:** Sets the channel for private logging for message edits, command uses, and deleted messages.\n**Permission Required:** Administrator\n**Arguments:** `None`\n```!privatelogging```", inline=False)
    embed.add_field(name="enablelogging", value = "**Description:** Sets the channel for mod logging.\n**Permission Required:** Administrator\n**Arguments:** `None`\n```!enablelogging```", inline=False)
    embed.add_field(name="xpstats", value = "**Description:** Displays your current level and xp.\n**Permission Required:** None\n**Arguments:** `None`\n```!xpstats```", inline=False)
    embed.add_field(name="staffvote", value = "**Description:** Sends an embed to vote for staff position through reacting with an upvote or downvote.\n**Permission Required:** Administrator\n**Arguments:** `member`\n```!staffvote Eric```", inline=False)
    embed.add_field(name="channelid", value = "**Description:** Sends the channel id of the current channel.\n**Permission Required:** None\n**Arguments:** `None`\n```!channelid```", inline=False)
    embed.add_field(name="mute/unmute", value = "**Description:** Mute/Unmute a user.\n**Permission Required:** Manage Roles\n**Arguments:** `user` `reason`\n```[!mute | !unmute] @user this is a reason```", inline=False)
    embed.add_field(name="info", value = "**Description:** Gives you info on a user.\n**Permission Required:** @Moderators\n**Arguments:** `user`\n```!info @user```", inline=False)
    embed.add_field(name="serverinfo", value = "**Description:** Gives you info on the current server.\n**Permission Required:** Administrator\n**Arguments:** `None`\n```!serverinfo```", inline=False)
    embed.add_field(name="kick", value = "**Description:** Kicks a user from the server.\n**Permission Required:** Kick Members\n**Arguments:** `user`\n```!kick @user```", inline=False)
    embed.add_field(name="ban", value = "**Description:** Bans a user.\n**Permission Required:** Ban Members\n**Arguments:** `user`\n```!ban @user```", inline=False)
    embed.add_field(name="clear", value = "**Description:** Clears messages from a channel. Can only delete messages in the range of [2, 100]\n**Permission Required:** Administrator\n**Arguments:** `integer`\n```!clear 50```", inline=False)
    embed.add_field(name="Create Role", value = "**Description:** Creates a new role and assigns a random color to it.\n**Permission Required:** Manage Roles\n**Arguments:** `Role Name`\n```!cr [role name]```", inline=False)
    embed.add_field(name="Edit Role", value = "**Description:** Takes an existing role and assigns a random color to it.\n**Permission Required:** Manage Roles\n**Arguments:** `Role Name`\n```!er [role name]```", inline=False)
    embed.add_field(name="spam", value = "**Description:** Spams a user with a message of your choice.\n**Permission Required:** Ban Members\n**Arguments:** `Integer`, `Message`\n```!spam @user [int][message]```", inline=False)
    embed.add_field(name="hmmcount", value = "**Description:** Shows a count of how many times Pineapple has replied with a thonk.\n**Permission Required** None\n**Arguments:** `None`\n```hmmcount```", inline=False)
    embed.add_field(name="duck", value = "**Description:** Loads a random picture of a duck\n**Permission Required** None\n**Arguments:** `None`\n```!duck```", inline=False)
    embed.add_field(name="dog", value = "**Description:** Loads a random picture of a dog\n**Permission Required** None\n**Arguments:** `None`\n```!dog```", inline=False)
    embed.add_field(name="shib", value = "**Description:** Loads a random picture of a shiba\n**Permission Required** None\n**Arguments:** `None`\n```!shib```", inline=False)
    embed.add_field(name="dab", value = "**Description:** Dab\n**Permission Required** None\n**Arguments:** `None`\n```!dab```", inline=False)
    embed.add_field(name="Created By", value="\n**clemente#7106**\nWith help from\n**exofeel#3333**\nTry `!trackrr` !\n:)", inline=False)

    await bot.say("Check your DMs!")
    await bot.send_message(ctx.message.author, embed=embed)
    await bot.delete_message(ctx.message)

@bot.command(pass_context=True)
async def pineapple(ctx):
    embed = discord.Embed(colour=discord.Colour(0x676767))

    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/430563327907725312/454868030854397952/PineappleBot.png")
    embed.set_author(name="PineappleBot", icon_url="https://cdn.discordapp.com/attachments/430563327907725312/454868030854397952/PineappleBot.png")
    embed.set_footer(text="PineappleBot | Created by clemente")

    embed.add_field(name="Invite Link:", value="[Invite PineappleBot to your server](https://discordapp.com/api/oauth2/authorize?client_id=456247418288209922&permissions=8&scope=bot)")
    embed.add_field(name="What is PineappleBot?", value="PineappleBot is a general purpose moderation bot built on the discord.py library. The bot began as a fun project and will continue to have updates pushed out as I learn more.")
    embed.add_field(name="Need help on how to use it?", value="You can check the help command by doing \n\n``!help`` \n\n Updates will constantly be pushed out with more features and new commands.")
    embed.add_field(name="<:TrackrrTwitter:452765661484285952>", value="Follow me on twitter\n[@clxmente](https://twitter.com/clxmente)", inline=True)


    await bot.say(embed=embed)

#-----------------------------------------------------------------PING-------------------------------------------------------------------------------
@bot.command(pass_context=True)
@commands.cooldown(1, 7, commands.BucketType.user)
async def ping(ctx):
    time_then = time.monotonic()
    pinger = await bot.send_message(ctx.message.channel, 'Pong | Loading latency..')
    ping = '%.2f' % (1000*(time.monotonic()-time_then))
    #await bot.edit_message(pinger, 'ℹ️ | **Pong!** ``' + ping + 'ms``') # you can edit this to say whatever you want really. Hope this helps.
    embed = discord.Embed(colour=discord.Colour(0x989898))

    embed.add_field(name="PineappleBot Ping", value="Ping: **{}ms** ".format(ping))
    await bot.delete_message(pinger)
    await bot.say(embed=embed)

@ping.error
async def ping_error(error, ctx):
    if isinstance(error, discord.ext.commands.errors.CommandOnCooldown):
        msg = await bot.send_message(ctx.message.channel, "{} You're doing that too fast, please slow down.".format(ctx.message.author.mention))
        await asyncio.sleep(6)
        await bot.delete_message(msg)
        

@bot.command(pass_context=True)
async def hexcode(ctx):
    r = lambda: randint(0,255)
    await bot.say('#%02X%02X%02X' % (r(),r(),r()))


@bot.command(pass_context=True)
async def trackrr(ctx):
    embed = discord.Embed(colour=discord.Colour(0x676767))

    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/452763485743349761/452763574503211008/trackrr.png")
    embed.set_author(name="Trackrr Music Search", icon_url="https://cdn.discordapp.com/attachments/452763485743349761/452763575878942720/TrackrrLogo.png")
    embed.set_footer(text="Trackrr Music Search | Created by exofeel")
    embed.add_field(name="Invite Link:", value="[Invite Trackrr to your server](https://discordapp.com/api/oauth2/authorize?client_id=449305030802145280&permissions=8&scope=bot)")
    embed.add_field(name="What is Trackrr?", value="Trackrr is a discord bot that searches through the most important streaming websites and find the song that you have asked.")
    embed.add_field(name="What services does this search through?", value="Currently, Trackrr searches through **Spotify, Apple Music, Soundcloud and YouTube**. With other streaming websites coming soon. (Depending on the websites API)")
    embed.add_field(name="Need help on how to use it?", value="You can check the help command by doing \n\n``^help`` \n\n Currently, there is no way to change the prefix.")
    embed.add_field(name="<:TrackrrTwitter:452765661484285952>", value="Follow me on twitter\n[@exofeel_dev](https://twitter.com/exofeel_dev)", inline=True)
    embed.add_field(name="<:TrackrrPayPal:452765247581847562>", value="Feeling generous?\nDonate to me on PayPal\n[me@exofeel.com](https://www.paypal.com/us/webapps/mpp/send-money-online)", inline=True)

    await bot.say(embed=embed)


# Add Command
@bot.command()
async def add(*left : int, right : int):
    # Simple command to add numbers
    await bot.say(left + right)

# ---------------------------------------------------------------CHANNEL ID----------------------------------------------------------------------
@bot.command(pass_context=True)
async def channelid(ctx):
    await bot.say('the channel id is: {}'.format(ctx.message.channel.id))

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
        await bot.send_message(ctx.message.channel,"<@%s>: **Can only delete messages in the range of [2, 100]**" % (userID))
        await bot.delete_message(ctx.message)


# ---------------------------------------------------------------ON_MESSAGE EVENT----------------------------------------------------------------------
chat_filter = [] #put words here in CAPS or it wont work. Strings seperated by commas.

@bot.event
async def on_message(message):
    await bot.process_commands(message)

#Adds a reaction if the user says 'hmm'
    if message.content.upper().startswith('HMM'):
	    if str(message.channel.id) == '368299513489915904': #staff channel
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
        await bot.send_message(message.channel, '**INVITE PINEAPPLEBOT TO YOUR OWN SERVER:** \nhttps://discordapp.com/oauth2/authorize?client_id=456247418288209922&scope=bot')

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
bot.run(" ")