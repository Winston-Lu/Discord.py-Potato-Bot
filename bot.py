#!/usr/bin/env python3
import os
import discord
from discord.ext import commands
import asyncio
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option

import random
import math 
import time
import numpy as np
import platform
import threading

# Music stuff
from musicconfig import config
from musicbot.audiocontroller import AudioController
from musicbot.settings import Settings
from musicbot.utils import guild_to_audiocontroller, guild_to_settings
initial_extensions = ['musicbot.commands.music',
                      'musicbot.commands.general', 'musicbot.plugins.button']
        
# Import additional modules
from Cogs import games
from Cogs import images
from Cogs import google

bot = commands.Bot(command_prefix='/',pm_help=True,description="Gaem suxs")
config.ABSOLUTE_PATH = os.path.dirname(os.path.abspath(__file__))
config.COOKIE_PATH = config.ABSOLUTE_PATH + config.COOKIE_PATH
bot.remove_command('help')
slash = SlashCommand(bot, sync_commands=True)
guild_ids = [393652537733152768]
for extension in initial_extensions:
    try:
        bot.load_extension(extension)
    except Exception as e:
        print("Extension loading error: " + e)

removedMessages = {} #removed by bot
userDeletedMessages = {} #removed by user

MAX_USER_DELETED_MESSAGES=50
MAX_BULK_MESSAGES=100
#if you want to save removed messages and user deleted messages even after rebooting the bot, as well as see currently purged messages
PERSISTENT_STORAGE = True   
SAVE_TIMER = 600 #in seconds

@bot.event
async def on_connect(): #Running this during on_connect since bots can parse commands after on_connect, which occurs before on_ready
    from time import strftime
    print("Started up on " + strftime("%B-%d-%Y %H:%M:%S", time.localtime()))
    random.seed(time.time())
    await bot.change_presence(status=discord.Status.online, afk=False, activity=discord.Game(name='HuniePop 2: Double Date'))
    

async def register(guild):
    guild_to_settings[guild] = Settings(guild)
    guild_to_audiocontroller[guild] = AudioController(bot, guild)
    sett = guild_to_settings[guild]
    try:
        await guild.me.edit(nick=sett.get('default_nickname'))
    except:
        pass
    if config.GLOBAL_DISABLE_AUTOJOIN_VC == True:
        return
        vc_channels = guild.voice_channels
    if sett.get('vc_timeout') == False:
        if sett.get('start_voice_channel') == None:
            try:
                await guild_to_audiocontroller[guild].register_voice_channel(guild.voice_channels[0])
            except Exception as e:
                print(e)
        else:
            for vc in vc_channels:
                if vc.id == sett.get('start_voice_channel'):
                    try:
                        await guild_to_audiocontroller[guild].register_voice_channel(vc_channels[vc_channels.index(vc)])
                    except Exception as e:
                        print(e)

@bot.event
async def on_ready():
    for guild in bot.guilds:
        await register(guild)
        print(f"Joined {guild.name}")

@bot.event
async def on_guild_join(guild):
    await register(guild)

## ----------------------------- General commands ------------------------------------------- ##
@bot.event
async def on_message(message):
    import re
    if(message.author == bot.user or message.author.bot): #if message is from bot itself
        return
    elif (re.search('8=+D',message.content)):
        p = re.compile("8=+D")
        maxLen = 0
        for m in p.finditer(message.content):
            if(len(m.group()) > maxLen):
                maxLen = len(m.group())
        if(maxLen>1985):
            await message.channel.send("You win this time")
            return(0)
        await message.channel.send('Mine is longer\n8'+ '='*(maxLen-1) + 'D')
    elif (message.content.lower().find("loli")!=-1):
        await message.channel.send('WEE WOO WEE WOO NO LEWDING LOLIS\nhttps://cdn.discordapp.com/attachments/569020987710898217/665355402199826463/53muboc5hv941.jpg')
    
    elif (message.content!="" and message.content[0]=='/'):
        await bot.process_commands(message)

@slash.slash(name="say",
             description="Makes the bot say something",
             options=[
               create_option(
                 name="message",
                 description="Whatever you want it to say",
                 option_type=3, #3=str, 4=int, 5=bool, 6=user, 7=channel, 8=role
                 required=True
               )
             ])
@bot.command(pass_context=True)
async def say(ctx,message):
    if(len(message)==0):
        em = discord.Embed()
        em.title = f'Usage: /say [x]'
        em.description = f'Says whatever is after /say'
        em.add_field(name="Example", value="/say hello\n\n>hello", inline=False)
        em.color = 0x22BBFF
        await ctx.send(embed=em)
        return
    phrase = ""
    for word in message:
        phrase += word
    await ctx.send(phrase)

@slash.slash(name="ping", description="Prints the latency to the Discord server",)
@bot.command(pass_context=True)
async def ping(ctx,help=""):
    if(help.find('help')!=-1):
        em = discord.Embed()
        em.title = f'Usage: /ping'
        em.description = f'Prints the bot latency from the host server to Discord servers'
        em.add_field(name="Example", value="/ping", inline=False)
        em.color = 0x22BBFF
        await ctx.send(embed=em)
        return
    import platform
    em = discord.Embed()
    em.title = f'{platform.platform()}   Latency:'
    em.description = f'{bot.ws.latency * 1000:.4f} ms'
    em.color = 0xFFA400
    await ctx.send(embed=em)
        
## ------------------------------- Bro-gramming ---------------------------------------------##
# @slash.slash(name="python",
#          guild_ids = guild_ids,
#          description="Executes python code",
#          options=[
#            create_option(
#              name="command",
#              description="Python code",
#              option_type=3, #3=str, 4=int, 5=bool, 6=user, 7=channel, 8=role
#              required=True
#            )
#          ]) 
@bot.command(pass_context=True)
async def python(ctx,*,command=""):
    #-------------- Help section ------------------#
    if(len(command)==0 or command.find('help')!=-1):
        em = discord.Embed()
        em.title = 'Usage: /python *code*'
        em.description = f'code: Python3 code to run\nAlso accepts \`\`\`codeblock\`\`\` notation. Dont specify "Python" for syntax highlighting, as it will interpret it as part of the code'
        em.add_field(name="Example", value="Python\n\`\`\`\nprint('Hello World!')\n\`\`\`\n\n>Hello World!", inline=False)
        em.color = 0x22BBFF
        await ctx.send(embed=em)
        return
    #----------------------------------------------#
    bannedModules = ["functools","itertools","youtube_dl",'StringIO','requests.','io.','BytesIO(','platform.','sys.','open(','threading.']
    if(ctx.author.id==164559470343487488): #only allow myself to run this command for now
        import re
        if(command.find('```')!=-1 and command.find('```',3)):
            command = command[3:-3].strip()
        if(command.find('import')!=-1): #if allowed imports, a reverse shell could spawn. Be careful of what others can import. I just disallowed it
            em = discord.Embed()
            em.title = 'Import Error'
            em.description = 'Additional Imports not allowed for security reasons.'
            em.color = 0xEE3333
            await ctx.send(embed=em)
            return
        if any (x in command for x in bannedModules): #Some commands that could interact with the host system for enumation
            em = discord.Embed()
            em.title = 'Illegal module call'
            em.description = 'Certain library calls are not allowed'
            em.color = 0xEE3333
            await ctx.send(embed=em)
            return
        #Could encode disallowed functions/imports and run it with exec/eval. Also finding variable names isnt harmful, but still could find info that shouldnt be needed
        if(command.find('dir(')!=-1 or command.find('globals(')!=-1 or command.find('locals(')!=-1 or command.find('eval(')!=-1 or command.find('exec(')!=-1 or command.find('compile(')!=-1):
            em = discord.Embed()
            em.title = 'Disallowed function errors'
            em.description = 'Certain functions are not allowed such as those viewing variables or a nested code execution'
            em.color = 0xEE3333
            await ctx.send(embed=em)
            return
        from io import StringIO
        import sys
        old_stdout = sys.stdout
        redirected_output = sys.stdout = StringIO()

        try:
            exec(command)  #will stop bot if there is a infinite or very long loop
        except Exception as err:
            em = discord.Embed()
            em.title = 'Error'
            em.description = f'{err}'
            em.color = 0xEE3333
            await ctx.send(embed=em)
            return

        sys.stdout = old_stdout
        em = discord.Embed()
        em.title = 'Console Output'
        em.description = f'{redirected_output.getvalue()}'
        em.color = 0x22EE22
        await ctx.send(embed=em)
        return


async def python_error(ctx,error):
    em = discord.Embed()
    em.title = 'Error'
    em.description = f'Command failed due to error:\n{error}'
    em.color = 0xEE0000
    await ctx.send(embed=em)
    return

## ----------------------- Chat moderation/manipulation ------------------------------------ ##
@slash.slash(name="clear",
             guild_ids = guild_ids,
             description="Deletes multiple messages",
             options=[
               create_option(
                 name="length",
                 description="How many messages to delete",
                 option_type=3, #3=str, 4=int, 5=bool, 6=user, 7=channel, 8=role
                 required=True
               )
             ])
@bot.command(pass_context=True,aliases=['delete','purge'])
@commands.has_permissions(manage_messages=True)
async def clear(ctx,length=""):
    #-------------- Help section ------------------#
    if(len(length)==0 or str(length).find('help')!=-1):
        em = discord.Embed()
        em.title = 'Usage: /clear length | /delete *length* | /purge *length*'
        em.description = f'length: (integer) number of messages to delete'
        em.add_field(name="Example", value="/clear 10\n/purge 20\n/delete 4", inline=False)
        em.color = 0x22BBFF
        await ctx.send(embed=em)
        return
    #----------------------------------------------#
    try:
        if(int(length)<1 or int(length)>100):
            em = discord.Embed()
            em.title = 'Command Argument Error'
            em.description = f'Enter a length between 1-97'
            em.color = 0xEE0000
            await ctx.send(embed=em)
            return
    except ValueError:
        em = discord.Embed()
        em.title = 'Command Argument Error'
        em.description = f'Enter valid positive integer for length'
        em.color = 0xEE0000
        await ctx.send(embed=em)
        return
    mgs=[]
    if (int(length)>=10):
        em = discord.Embed()
        em.title = 'Warning'
        em.description = f"You are about to delete {length} messages, continue? [y/n]"
        em.color = 0xEE9900
        await ctx.send(embed=em)
        mgs = await getMessages(ctx,2)
        msg = ""
        additionalMgsToDelete = 1
        try:
            msg = await bot.wait_for('message',check=lambda message: message.author == ctx.author, timeout=5)
        except asyncio.exceptions.TimeoutError:
            None
        try:
            msg = msg.content.lower().strip()
        except AttributeError: #if no message is sent, cant lowercase nothing so throws error
            msg = 'n'
            additionalMgsToDelete -= 1
        if(msg=='y'):
            mgs = await getMessages(ctx,int(length)+3)
        else:
            if(additionalMgsToDelete==1):
                await ctx.channel.delete_messages(await getMessages(ctx,1))
            await ctx.channel.delete_messages(mgs)
            em = discord.Embed()
            em.title = 'Clear Cancelled'
            em.description = f"\u200b"
            em.color = 0xEE9900
            await ctx.send(embed=em)
            return
    else:
        mgs = await getMessages(ctx,int(length)+1)
    ## Store deleted messages in a cache
    messageCache = []
    for m in mgs:
        try:
            messageCache.append((m.author,m.content,m.attachments[0].url))
        except IndexError:
            messageCache.append((m.author,m.content))
    #Limit the amount of messages cached to MAXBULKMESSAGES. Messages are stored as a stack
    existingMsgs = removedMessages.get(ctx.channel.id)
    if existingMsgs is not None:
        for existingMsg in existingMsgs:
            messageCache.append(existingMsg)
        if(len(existingMsgs)>MAX_BULK_MESSAGES):
            messageCache = messageCache[:MAX_BULK_MESSAGES] #say you have 25 msg max and you have a 28 msg cache. We take from [0:25), (0-indexed, so 25 is the 26th element)
    removedMessages[ctx.channel.id] =  messageCache
    ##delete messages specified by the user
    await ctx.channel.delete_messages(mgs)
"""
@clear.error
async def clear_error(ctx,error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        #-------------- Help section ------------------#
        em = discord.Embed()
        em.title = 'Usage: /clear *length*'
        em.description = f'length: (integer) number of messages to delete'
        em.color = 0x22BBFF
        await ctx.send(embed=em)
        return
        #----------------------------------------------#
    elif isinstance(error, commands.errors.CommandInvokeError):
        em = discord.Embed()
        em.title = 'Error'
        em.description = f'Could not delete that many messages. Maximum is 97 (+3 including the /clear, bot prompt, and  already added)'
        em.color = 0xEE0000
        await ctx.send(embed=em)
        return
    elif isinstance(error, commands.errors.CheckFailure):
        em = discord.Embed()
        em.title = 'Insufficient Privileges'
        em.description = f'You do not have sufficient privileges to run this command'
        em.color = 0xEE0000
        await ctx.send(embed=em)
        return
    else:
        em = discord.Embed()
        em.title = 'Error'
        em.description = f'Command failed due to error:\n{error}'
        em.color = 0xEE0000
        await ctx.send(embed=em)
        return


    message = await getMessages(ctx,1)
    await ctx.send(message[0].attachments[0].url) """

@bot.command(pass_context=True)
async def undo(ctx,help=""):
    #-------------- Help section ------------------#
    if(help.find('help')!=-1):
        em = discord.Embed()
        em.title = f'Usage: /undo'
        em.description = f'Resend the deleted messages'
        em.add_field(name="Example", value="/undo", inline=False)
        em.color = 0x22BBFF
        await ctx.send(embed=em)
        return
    #----------------------------------------------#
    if (ctx.channel.id in removedMessages):
        if(len(removedMessages.get(ctx.channel.id))==0):
            await ctx.send("No deleted messages found on this channel since last restart")
            return
        field = 0 
        em = discord.Embed()
        em.title = "Deleted messages"
        em.description = f"Messages restored: {len(removedMessages.get(ctx.channel.id))}"
        em.color = 0xFF6622
        for msg in reversed(removedMessages.get(ctx.channel.id)):
            if(field >= 23):
                 field = 0
                 await ctx.send(embed=em)
                 em = discord.Embed()
                 em.title = "Deleted messages"
                 em.description = f"Continued:"
                 em.color = 0xFF6622
            if (len(msg[1])==0): #usually embeds have no msg content
                msg[1] = "[No Msg Found, Likely an embed]"
            if (len(msg)==3):
                if(len(msg[1])>1020):
                    em.add_field(name=f'{msg[0]}',value=f'{msg[1][:1020]} {msg[2]}',inline=False)
                    em.add_field(name=f'{msg[0]} cont.',value=f'{msg[1][1020:]} {msg[2]}',inline=False)
                    field+=1
                else:
                    em.add_field(name=f'{msg[0]}',value=f'{msg[1]} {msg[2]}',inline=False)
            else:
                if(len(msg[1])>1020):
                    em.add_field(name=f'{msg[0]}',value=f'{msg[1][:1020]}',inline=False)
                    em.add_field(name=f'{msg[0]} cont.',value=f'{msg[1][1020:]}',inline=False)
                    field+=1
                else:
                    em.add_field(name=f'{msg[0]}',value=f'{msg[1]}',inline=False)
            field += 1
        await ctx.send(embed=em)
    else:
        await ctx.send("No deleted messages found on this channel since last restart")

@bot.command(pass_context=True)
@commands.has_permissions(manage_messages=True)
async def undo_error(ctx,error):
    if isinstance(error, commands.errors.CheckFailure):
        em = discord.Embed()
        em.title = 'Insufficient Privileges'
        em.description = f'You do not have sufficient privileges to run this command'
        em.color = 0xEE0000
        await ctx.send(embed=em)
        return
    else:
        em = discord.Embed()
        em.title = 'Error'
        em.description = f'Command failed due to error:\n{error}'
        em.color = 0xEE0000
        await ctx.send(embed=em)
        return

@bot.command(pass_context=True)
async def restore(ctx,value=""):
    #-------------- Help section ------------------#
    if(value=="" or value.find('help')!=-1):
        em = discord.Embed()
        em.title = f'Usage: /restore [x]'
        em.description = f'Restores [x] previously deleted messages by a user in the order they were deleted up to {MAX_USER_DELETED_MESSAGES} per text channel'
        em.add_field(name="Example", value="/restore 5", inline=False)
        em.color = 0x22BBFF
        await ctx.send(embed=em)
        return
    #----------------------------------------------#
    try:
        if(int(value)<1):
            await ctx.send("Enter a valid number greater or equal to 1")
            return
        value = int(value)
    except ValueError:
        await ctx.send("Enter a valid number")
        return
    if(ctx.channel.id in userDeletedMessages):
        messages = userDeletedMessages.get(ctx.channel.id)
        messageLength = len(messages)
        if(value > messageLength):
            value = messageLength
        messageList = messages[messageLength-value:]
        field = 0 
        em = discord.Embed()
        em.title = "Deleted messages"
        em.description = f"Restoring {value} messages"
        em.color = 0xFF6622
        for msg in reversed(messageList):
            try:
                if(field >= 23):
                     field = 0
                     await ctx.send(embed=em)
                     em = discord.Embed()
                     em.title = "Deleted messages"
                     em.description = f"Continued:"
                     em.color = 0xFF6622
                if (len(msg[1])==0): #usually embeds have no msg content
                    msg[1] = "[No Msg Found, Likely an embed]"
                if (len(msg)==3):
                    if(len(msg[1])>1020):
                        em.add_field(name=f'{msg[0]}',value=f'{msg[1][:1020]} {msg[2]}',inline=False)
                        em.add_field(name=f'{msg[0]} cont.',value=f'{msg[1][1020:]} {msg[2]}',inline=False)
                        field+=1
                    else:
                        em.add_field(name=f'{msg[0]}',value=f'{msg[1]} {msg[2]}',inline=False)
                else:
                    if(len(msg[1])>1020):
                        em.add_field(name=f'{msg[0]}',value=f'{msg[1][:1020]}',inline=False)
                        em.add_field(name=f'{msg[0]} cont.',value=f'{msg[1][1020:]}',inline=False)
                        field+=1
                    else:
                        em.add_field(name=f'{msg[0]}',value=f'{msg[1]}',inline=False)
                field += 1
            except Exception as e:
                await ctx.send(f"Error: {e}")
        await ctx.send(embed=em)
    else:
        await ctx.send("Did not find any deleted messages since last restart")
    
@bot.command(pass_context=True)
@commands.has_permissions(manage_messages=True)
async def restore_error(ctx,error):
    if isinstance(error, commands.errors.CheckFailure):
        em = discord.Embed()
        em.title = 'Insufficient Privileges'
        em.description = f'You do not have sufficient privileges to run this command'
        em.color = 0xEE0000
        await ctx.send(embed=em)
        return
    else:
        em = discord.Embed()
        em.title = 'Error'
        em.description = f'Command failed due to error:\n{error}'
        em.color = 0xEE0000
        await ctx.send(embed=em)
        return

@bot.event
async def on_message_delete(message):
    if (message.channel.id in userDeletedMessages): #if entry for channel exists
        existing = userDeletedMessages.get(message.channel.id)
        try:
            attachmenturl = message.attachments[0].url
            existing.append((str(message.author),message.content,attachmenturl))
            userDeletedMessages[message.channel.id] = existing
        except IndexError:
            existing.append((str(message.author),message.content))
            userDeletedMessages[message.channel.id] = existing
    else:
        try:
            attachmenturl = message.attachments[0].url
            userDeletedMessages[message.channel.id] = [(str(message.author),message.content,attachmenturl)]
        except IndexError:
            userDeletedMessages[message.channel.id] = [(str(message.author),message.content)]

## --------------- Image manipulation: ---------------------- ##
bot.add_cog(images.Images(bot))
## ---------------------- Games  ---------------------------- ##
bot.add_cog(games.Games(bot))
## ---------------------- Music ----------------------------- ##
#bot.load_extension('music')
## ----------------- Google Searches ------------------------ ##
bot.add_cog(google.Google(bot))

## ------------------- Help Menu ---------------------------- ##

@bot.command(pass_context=True,aliases=['commands','commandlist','command','h'])
async def help(ctx):
    em = discord.Embed()
    em.title = '__**Available Commands**__'
    em.description = f"For more information on a command, run '/command help' or '/command'\nAll Caps mean that argument is required, while [square brackets] means that argument is optional"
    em.color = 0x22BBFF
    em.add_field(name="\u200b", value="__**General Commands**__", inline=False)
    em.add_field(name="/ping", value="Gets latency from bot host to Discord servers", inline=True)
    em.add_field(name="/clear NUM", value="Deletes NUM amount of messages. /delete and /purge also execute this command", inline=True)
    em.add_field(name="/undo", value="Restores messages that was previously deleted by /clear", inline=True)
    em.add_field(name="/restore NUM", value=f"Restores NUM messages previously deleted by users, up to\n[up to {MAX_USER_DELETED_MESSAGES} per text channel]", inline=True)
    em.add_field(name="/say PHRASE", value="Makes bot say what you put in PHRASE", inline=True)

    em.add_field(name="\u200b", value="__**Games**__", inline=False)
    em.add_field(name="/connect4 OPPONENT [width] [height]", value="Challenges OPPONENT to a game of connect 4 on a [width]x[height] board", inline=True)
    em.add_field(name="/chess OPPONENT", value="Challenges OPPONENT to a game of chess", inline=True)

    em.add_field(name="\u200b", value="__**Images**__", inline=False)
    em.add_field(name="/fry [img | img_url] [gamma]", value="Deepfries an image attachemnt, image at the url given, or the iamge attachemnt before the command is executed", inline=True)
    em.add_field(name="/radial [img | img_url] [amount]", value="Radial blurs an image attachemnt, image at the url given, or the iamge attachemnt before the command is executed", inline=True)
    em.add_field(name="/swirl [img | img_url] [amount]", value="Swirls an image attachemnt, image at the url given, or the iamge attachemnt before the command is executed", inline=True)
    em.add_field(name="/warp [img | img_url]", value="Randomly warps an image attachemnt, image at the url given, or the iamge attachemnt before the command is executed", inline=True)

    em.add_field(name="\u200b", value="__**Google Stuff**__", inline=False)
    em.add_field(name="/translate SRC", value="Translates SRC to english", inline=True)
    em.add_field(name="/translateto LANG SRC", value="Translate SRC to LANG", inline=True)
    em.add_field(name="/translatefromto LANG LANG2 SRC", value="Translates SRC in LANG to LANG2. /translatetofrom does the opposite", inline=True)

    em.add_field(name="\u200b", value="__**Other**__", inline=False)
    #em.add_field(name="/python CODE", value="```diff\n-Runs CODE as Python code, only works for specific users due to some security and execution concerns```", inline=True)
    em.add_field(name="On Messages", value="Longer phallic emojis\nAdded warning for mentioning underage children", inline=False)
    await ctx.send(embed=em)
    ## Message cuts off soon due to max embed size capacity, start a new embed
    em = discord.Embed()
    em.title = '__**Music/Voice Commands**__'
    em.description = "Thanks to vbe0201's for this example framework"
    em.color = 0x22BBFF
    em.add_field(name="/play URL|SEARCH", value="Plays audio from Youtube URL or search a video", inline=True)
    em.add_field(name="/pause", value="Pauses the current song", inline=True)
    em.add_field(name="/resume", value="Resumes the currently playing track", inline=True)
    em.add_field(name="/volume", value="Sets the global bot volume [0-200]", inline=True)
    em.add_field(name="/repeat", value="Repeats the currently playing song. Type again to toggle off", inline=True)
    em.add_field(name="/reset", value="Starts the current song from the start", inline=True)
    em.add_field(name="/skip", value="Stops currently playing song", inline=True)
    em.add_field(name="/stop", value="Stops the song and clear the queue", inline=True)
    em.add_field(name="/join ", value="Leaves voice channel", inline=True)
    em.add_field(name="/leave ", value="Leaves voice channel", inline=True)
    em.add_field(name="/queue", value="Shows the video queue", inline=True)
    em.add_field(name="/song-info", value="Shows the video information", inline=True)
    await ctx.send(embed=em)

## --------------------- Others ------------------------------ ##
@bot.command(pass_context=True)
async def test(ctx,help="",amount="10"):
    print(ctx.author.id)
    
@bot.command(pass_context=True)
async def spam(ctx,help="",amount="10"):   
    for x in range (26):
        await ctx.send(str(x))

@bot.event
async def on_command_error(ctx,error):
    if(str(error).find("Command")!=-1 and str(error).find("is not found")!=-1): #command not found
        em = discord.Embed()
        em.title = 'Error'
        em.description = f"{error}"
        em.color = 0xEE0000
        await ctx.send(embed=em)
        return
    elif(str(error).find("'NoneType' object has no attribute '")!=-1):
        pass; #likely from music.py, already handled
    elif(str(error).find("ClientException: Can only bulk delete messages up to")!=-1):
        pass; #likely from /clear, already handled
    else:
        from time import strftime
        import time
        print("Error at time: " + strftime("%B-%d-%Y %H:%M:%S", time.localtime()))
        raise error

async def getMessages(ctx,number: int=1):
    if(number==0):
        return([])
    toDelete = []
    async for x in ctx.channel.history(limit = number):
        toDelete.append(x)
    return(toDelete)

@bot.command(pass_context=True)
async def exit(ctx):
    if(ctx.author.id==164559470343487488): #only allow myself to run this command for now
        exit()


# Read from file
def readCache():
    try:
        with open("cached/usermsg.txt",encoding="UTF-8") as f:
            line = f.readline()
            while(len(line)!=0):
                elements = line.split("ʒ")
                msgList = []
                for msg in elements[1:]:
                    newMsg = msg.split("ˤ")
                    msgList.append(newMsg)
                userDeletedMessages[int(elements[0])] = msgList
                line = f.readline()
            f.close()
    except FileNotFoundError:
        import os
        try:
            os.makedirs('cached')
        except FileExistsError:
            pass
        with open(os.path.join('cached', 'usermsg.txt'), 'w') as temp_file:
            temp_file.write("")
    try:
        with open("cached/bulkmsg.txt",encoding="UTF-8") as f:
            line = f.readline()
            while(len(line)!=0):
                elements = line.split("ʒ")
                msgList = []
                for msg in elements[1:]:
                    newMsg = msg.split("ˤ")
                    msgList.append(newMsg)
                removedMessages[int(elements[0])] = msgList
                line = f.readline()
            f.close()
    except FileNotFoundError:
        import os
        try:
            os.makedirs('cached')
        except FileExistsError:
            pass
        with open(os.path.join('cached', 'bulkmsg.txt'), 'w') as temp_file:
            temp_file.write("")

# Save to file
runningThreads = [None]
def saveCache(firstRun = False):
    try:
        if(runningThreads[0].is_alive()): #prevent conflicting file IO if this function is called
            runningThreads[0].cancel()
    except AttributeError: #no threads.
        pass

    if not firstRun: #no need to write on init
        # Write userDeletedMessages
        with open("cached/usermsg.txt",'wb') as f:
            f.truncate() #clear file
            channels = userDeletedMessages.keys()
            for channel in channels:
                toWrite = f"{channel}".encode("UTF-8") #should just be strings, but sticking to the format
                for msg in userDeletedMessages.get(channel):
                    if(len(msg)==3):
                        toWrite += (f"ʒ{msg[0]}ˤ{' '.join(msg[1].splitlines())}ˤ{msg[2]}").encode("UTF-8")  #use ˤ as a seperation character, as it isnt used very much in normal messages
                    else:
                        toWrite += (f"ʒ{msg[0]}ˤ{' '.join(msg[1].splitlines())}").encode("UTF-8")
                f.write(toWrite)
            f.close()
        # Write removedMessages
        with open("cached/bulkmsg.txt",'wb') as f:
            f.truncate() #clear file
            channels = removedMessages.keys()
            for channel in channels:
                toWrite = f"{channel}".encode("UTF-8") #should just be strings, but sticking to the format
                for msg in removedMessages.get(channel):
                    if(len(msg)==3):
                        toWrite += (f"ʒ{msg[0]}ˤ{' '.join(msg[1].splitlines())}ˤ{msg[2]}").encode("UTF-8")  #use ˤ as a seperation character, as it isnt used very much in normal messages
                    else:
                        toWrite += (f"ʒ{msg[0]}ˤ{' '.join(msg[1].splitlines())}").encode("UTF-8")
                f.write(toWrite)
            f.close()
    timer = threading.Timer(SAVE_TIMER, saveCache)
    timer.start()
    runningThreads[0] = timer

#If enabled storing deleted messages
if(PERSISTENT_STORAGE):
    readCache()
    saveCache()



###=============== Get bot token ================###
try:
    file = open("token.txt",'r')
    token = file.read()
    file.close()
    bot.run(token, bot=True, reconnect=True)
except:
    print("Token.txt not found")
###==============================================###

# Image manipulation resources:
# CV2 kernel examples: https://towardsdatascience.com/python-opencv-building-instagram-like-image-filters-5c482c1c5079
