#!/usr/bin/env python3
import discord
from discord.ext import commands
import asyncio

import random
import math 
import numpy as np
import platform
#Image manipulation
from PIL import Image
import PIL
import cv2 as cv

# parse image from URL
import requests
from io import BytesIO
import io
# Music stuff
import music

bot = commands.Bot(command_prefix='/',description="Gaem suxs")
bot.remove_command('help')


removedMessages = {} #removed by bot
userDeletedMessages = {} #removed by user
MAXUSERDELETEDMESSAGES=50

@bot.event
async def on_connect():
    from time import strftime
    import time
    print("Started up on " + strftime("%B-%d-%Y %H:%M:%S", time.localtime()))
    random.seed(time.time())

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, afk=False, activity=discord.Game(name='HuniePop 2: Double Date'))

## ------------------------------------------------------------------------------------------------ General commands  ------------------------------------------------------------------------------------------------------- ##
@bot.event
async def on_message(message):
    import re
    if(message.author == bot.user): #if message is from bot itself
        return
    elif (re.search('^8=+D$',message.content)):
        length = len(message.content)-1
        if(length>1985):
            await message.channel.send("You win this time")
            return(0)
        await message.channel.send('Mine is longer\n8'+ '='*length + 'D')
    elif (message.content.lower().find("loli")!=-1):
        await message.channel.send('WEE WOO WEE WOO NO LEWDING LOLIS\nhttps://cdn.discordapp.com/attachments/569020987710898217/665355402199826463/53muboc5hv941.jpg')
    elif (message.content!="" and message.content[0]=='/'):
        await bot.process_commands(message)

@bot.command(pass_context=True)
async def say(ctx,*command):
    if(len(command)==0):
        em = discord.Embed()
        em.title = f'Usage: /say [x]'
        em.description = f'Says whatever is after /say'
        em.add_field(name="Example", value="/say hello\n\n>hello", inline=False)
        em.color = 0x22BBFF
        await ctx.send(embed=em)
        return
    phrase = ""
    for word in command:
        phrase += word + " "
    await ctx.send(phrase)

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
        
## -------------------------------------------------------------------------------------------------- Bro-gramming -----------------------------------------------------------------------------------------------------------##
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
    bannedModules = ["functools","itertools","youtube_dl",'StringIO','requests.','io.','BytesIO(','platform.','sys.','open(']
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

@python.error
async def python_error(ctx,error):
    em = discord.Embed()
    em.title = 'Error'
    em.description = f'Command failed due to error:\n{error}'
    em.color = 0xEE0000
    await ctx.send(embed=em)
    return

## ------------------------------------------------------------------------------------------- Chat moderation/manipulation ------------------------------------------------------------------------------------------------- ##
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
            em.description = f'Enter a length between 1-100'
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
            mgs = await getMessages(ctx,int(length)+2)
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
        mgs = await getMessages(ctx,int(length)+2)
    removedMessages[ctx.channel.id] = mgs
    await ctx.channel.delete_messages(mgs)

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
        em.description = f'Could not delete that many messages. Maximum is 98 (+2 including the /clear and bot prompt already added)'
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
    await ctx.send(message[0].attachments[0].url) 

@bot.command(pass_context=True)
async def undo(ctx,help=""):
    #-------------- Help section ------------------#
    if(help=="" or help.find('help')!=-1):
        em = discord.Embed()
        em.title = f'Usage: /undo'
        em.description = f'Resend the deleted messages'
        em.add_field(name="Example", value="/undo", inline=False)
        em.color = 0x22BBFF
        await ctx.send(embed=em)
        return
    #----------------------------------------------#
    if (ctx.channel.id in removedMessages):
        for msg in reversed(removedMessages.get(ctx.channel.id)):
            em = discord.Embed()
            em.title = f'{msg.author} (Deleted)'
            em.description = f'{msg.content}\n'
            try:
                em.add_field(name="Deleted image (image should no longer exist)", value=f"{msg.attachments[0].url}", inline=True)
            except IndexError:
                pass
            em.color = 0xFF6622
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
        em.description = f'Restores [x] previously deleted messages by a user in the order they were deleted up to {MAXUSERDELETEDMESSAGES} per text channel'
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
        for msg in reversed(messageList):
            em = discord.Embed()
            em.title = f'{msg[0]} (Deleted)'
            em.description = f'{msg[1]}'
            if(len(msg)==3):
                em.add_field(name="Deleted image (image should no longer exist)", value=f"{msg[3]}", inline=True)
            em.color = 0xFF6622
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

## ----------------------------------------------------------------------------------------------------- Games  ------------------------------------------------------------------------------------------------------------- ##
@bot.command(pass_context=True)
async def connect4(ctx,opponent="",width=7,height=6):
    #-------------- Help section ------------------#
    if(opponent=="" or opponent.find('help')!=-1):
        em = discord.Embed()
        em.title = f'Usage: /connect4 opponent [width] [height]'
        em.description = f'Challenges opponent to a game of connect 4. The Opponent should be @mentoned to start\nBoard is default 7x6 large if not specified, though you usually wont need any board larger than that.\nMax board volume is 95 due to character limitations'
        em.add_field(name="Example", value="/connect4 @Username\n/connect4 @Username 10 9", inline=False)
        em.color = 0x22BBFF
        await ctx.send(embed=em)
        return
    #----------------------------------------------#
    # Remove challenge message
    await ctx.channel.delete_messages(await getMessages(ctx,1))
    
    # Game init
    resized = False
    if(width*height > 95):
        width = 7
        height = 6
        resized = True
    player1 = ctx.message.mentions[0].name
    player2 = ctx.message.author.name
    s = ':black_large_square:'
    p1 = ':blue_circle:'
    p2 = ':red_circle:'
    board = []
    for column in range(height):
        rowArr = []
        for row in range(width):
            rowArr.append(s)
        board.append(rowArr)
    def getDisplay():
        toDisplay = ""
        for y in range(height):
            for x in range(width-1):
                toDisplay+=board[y][x]+'|'
            toDisplay+=board[y][width-1] + '\n'
        return(toDisplay)
    
    boardMessage = None
    em = discord.Embed()
    if(player1==player2):
        em.title = f"{player2} challenged themselves to a game of Connect 4 \n(wow you're lonely)"
    else:
        em.title = f'{player2} challenged {player1} to a game of Connect 4'
    em.description = f"{getDisplay()}"
    em.color = 0x444444
    em.add_field(name=f"{player1}", value=f"Type a number from 1-{width} to accept and place your first piece, or type 'decline' to refuse", inline=False)
    if resized:
        em.add_field(name="Note", value=f"Original board length was too large, defaulted to 7x6", inline=False)
    await ctx.send(embed=em)
    async for x in ctx.channel.history(limit = 1):
        boardMessage = x
    badInput = 0
    turns = 1
    currentPlayer = player1
    otherPlayer = player2
    currentPlayerId=1
    while True:
        try:
            msg = await bot.wait_for('message',check=lambda message: message.author.name == player1, timeout=30)
            if(msg.content=='decline'):
                em = discord.Embed()
                if(player1==player2):
                    em.title = f"{player2} challenged themselves to a game of Connect 4 (wow you're lonely)"
                else:
                    em.title = f'{player2} challenged {player1} to a game of Connect 4'
                em.description = f"{getDisplay()}"
                em.color = 0x444444
                em.add_field(name=f"{player1}", value="Challenge refused", inline=False)
                await boardMessage.edit(embed=em)
                return
            
            slot = int(msg.content)
            if(slot<1 or slot>width):
                raise ValueError
            await ctx.channel.delete_messages(await getMessages(ctx,1))
            board[height-1][slot-1] = p1
            gameLoop = True
            currentPlayer = player2
            otherPlayer = player1
            turns +=1
            currentPlayerId=2
            break;
        except asyncio.exceptions.TimeoutError:
            em = discord.Embed()
            if(player1==player2):
                em.title = f"{player2} challenged themselves to a game of Connect 4 (wow you're lonely)"
            else:
                em.title = f'{player2} challenged {player1} to a game of Connect 4'
            em.description = f"{getDisplay()}"
            em.color = 0x444444
            em.add_field(name=f"{player1}", value="Game timed out", inline=False)
            await boardMessage.edit(embed=em)
            return
        except ValueError:
            em = discord.Embed()
            if(player1==player2):
                em.title = f"{player2} challenged themselves to a game of Connect 4 (wow you're lonely)"
            else:
                em.title = f'{player2} challenged {player1} to a game of Connect 4'
            em.description = f"{getDisplay()}"
            em.color = 0x444444
            em.add_field(name=f"{player1}", value=f"Enter a valid number from 1-{width}", inline=False)
            await boardMessage.edit(embed=em)
            badInput+=1
        if(badInput==3):
            em = discord.Embed()
            if(player1==player2):
                em.title = f"{player2} challenged themselves to a game of Connect 4 (wow you're lonely)"
            else:
                em.title = f'{player2} challenged {player1} to a game of Connect 4'
            em.description = f"{getDisplay()}"
            em.color = 0x444444
            em.add_field(name=f"{player1}", value="Did not enter a valid number in 3 tries. Game ended.", inline=False)
            await boardMessage.edit(embed=em)
            return
    winningComment=""
    winner=""
    while gameLoop:
        if(turns==width*height):
            winner=None
            break;
        ################################
        #check for winning combinations#
        ################################
        # Horizontal
        for y in range(height):
            for x in range(width-3):
                if(board[y][x]==board[y][x+1] and board[y][x]==board[y][x+2] and board[y][x]==board[y][x+3] and board[y][x]!=s):
                    if(board[y][x]==p1):
                        board[y][x] = ':large_blue_diamond:'
                        board[y][x+1] = ':large_blue_diamond:'
                        board[y][x+2] = ':large_blue_diamond:'
                        board[y][x+3] = ':large_blue_diamond:'
                    elif(board[y][x]==p2):
                        board[y][x]=":diamonds:"
                        board[y][x+1]=":diamonds:"
                        board[y][x+2]=":diamonds:"
                        board[y][x+3]=":diamonds:"
                    print("winner")
                    winner=otherPlayer
                    winningComment = f"{otherPlayer} connected 4 in a horizontal row"
                    break
            if(winner!=""):
                break
        #Vertical
        for y in range(height-3):
            for x in range(width):
                if(board[y][x]==board[y+1][x] and board[y][x]==board[y+2][x] and board[y][x]==board[y+3][x] and board[y][x]!=s):
                    if(board[y][x]==p1):
                        board[y][x] = ':large_blue_diamond:'
                        board[y+1][x] = ':large_blue_diamond:'
                        board[y+2][x] = ':large_blue_diamond:'
                        board[y+3][x] = ':large_blue_diamond:'
                    elif(board[y][x]==p2):
                        board[y][x]=":diamonds:"
                        board[y+1][x]=":diamonds:"
                        board[y+2][x]=":diamonds:"
                        board[y+3][x]=":diamonds:"
                    winner = otherPlayer
                    winningComment = f"{otherPlayer} connected 4 in a vertical row"
                    break
            if(winner!=""):
                break      
        # diagonal \
        for y in range(height-3):
            for x in range(width-3):
                if(board[y][x]==board[y+1][x+1] and board[y][x]==board[y+2][x+2] and board[y][x]==board[y+3][x+3] and board[y][x]!=s):
                    if(board[y][x]==p1):
                        board[y][x] = ':large_blue_diamond:'
                        board[y+1][x+1] = ':large_blue_diamond:'
                        board[y+2][x+2] = ':large_blue_diamond:'
                        board[y+3][x+3] = ':large_blue_diamond:'
                    elif(board[y][x]==p2):
                        board[y][x]=":diamonds:"
                        board[y+1][x+1]=":diamonds:"
                        board[y+2][x+2]=":diamonds:"
                        board[y+3][x+3]=":diamonds:"
                    winner = otherPlayer
                    winningComment = f"{otherPlayer} connected 4 in a \ diagonal"
                    break
            if(winner!=""):
                break    
        # diagonal /
        for y in range(height-3):
            for x in range(3,width):
                if(board[y][x]==board[y+1][x-1] and board[y][x]==board[y+2][x-2] and board[y][x]==board[y+3][x-3] and board[y][x]!=s):
                    if(board[y][x]==p1):
                        board[y][x] = ':large_blue_diamond:'
                        board[y+1][x-1] = ':large_blue_diamond:'
                        board[y+2][x-2] = ':large_blue_diamond:'
                        board[y+3][x-3] = ':large_blue_diamond:'
                    elif(board[y][x]==p2):
                        board[y][x]=":diamonds:"
                        board[y+1][x-1]=":diamonds:"
                        board[y+2][x-2]=":diamonds:"
                        board[y+3][x-3]=":diamonds:"
                    winner = otherPlayer
                    winningComment = f"{otherPlayer} connected 4 in a / diagonal"
                    break
            if(winner!=""):
                break    
        if(winner!=""):
            break
        ################################
        em = discord.Embed()
        em.title = f'Connect 4'
        em.description = f"{getDisplay()}"
        em.color = 0x444444
        em.add_field(name=f"Turn {turns}: {currentPlayer} turn", value=f"Enter a value from 1-{width}. You have 30 seconds to make a choice", inline=True)
        await boardMessage.edit(embed=em)
        gotValidInput = False
        badInput = 0
        while not gotValidInput:
            try:
                msg = await bot.wait_for('message',check=lambda message: message.author.name == currentPlayer, timeout=30)
                await ctx.channel.delete_messages(await getMessages(ctx,1))
                slot = int(msg.content)
                if(slot<1 or slot>width):
                    raise ValueError
                # Place piece in slot
                for y in range(height-1,-1,-1):
                    if(board[y][slot-1]==s):
                        if(currentPlayerId == 1):
                            board[y][slot-1] = p1
                            break;
                        else:
                            board[y][slot-1] = p2
                            break;
                    elif(y==0): #if column is full
                        raise ValueError
                # switch player
                if(currentPlayerId == 1):
                    currentPlayer = player1
                    otherPlayer = player2
                    currentPlayerId = 2
                else:
                    currentPlayer = player1
                    otherPlayer = player2
                    currentPlayerId = 1
                gotValidInput=True
                turns+=1
                break
            except asyncio.exceptions.TimeoutError:
                winner=otherPlayer
                winningComment=f"{currentPlayer} took too much time"
                gameLoop = False
                break
            except ValueError:
                em = discord.Embed()
                em.title = f'Connect 4'
                em.description = f"{getDisplay()}"
                em.color = 0x444444
                em.add_field(name=f"Turn {turns}: {currentPlayer}", value=f"Enter a valid number from 1-{width}", inline=False)
                await boardMessage.edit(embed=em)
                badInput+=1
            if(badInput==3):
                winner=otherPlayer
                winningComment=f"{currentPlayer} had too many bad inputs"
                gameLoop = False
                break
    if(winner==None):
        em = discord.Embed()
        em.title = f'Connect 4 - Tie, No Winners'
        em.description = f"{getDisplay()}"
        em.color = 0x444444
        await boardMessage.edit(embed=em)
    elif(winner==player1):
        em = discord.Embed()
        em.title = f'Connect 4 - {player1} wins!'
        em.description = f"{getDisplay()}"
        em.add_field(name="Reason:", value=f"{winningComment}", inline=False)
        if(player1==player2):
            em.add_field(name="Also:", value=f"They won against themself", inline=False)
        em.color = 0x444444
        await boardMessage.edit(embed=em)
    elif(winner==player2):
        em = discord.Embed()
        em.title = f'Connect 4 - {player2} wins!'
        em.description = f"{getDisplay()}"
        em.add_field(name="Reason:", value=f"{winningComment}", inline=False)
        if(player1==player2):
            em.add_field(name="Also:", value=f"They won against themself", inline=False)
        em.color = 0x444444
        await boardMessage.edit(embed=em)

## --------------------------------------------------------------------------------------------- Image Helper functions ----------------------------------------------------------------------------------------------------- ##
async def getImage(ctx,command="",help="",amount="30"):
    if(help=="help"):
        return(("",1,False)) #help command
    if(help!=""): #if given url or number
        if(validateURL(help)): #check if given url
            url = help
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}) #use safari user agent in case they are blocking python UA
            img = Image.open(BytesIO(response.content))
            if(validateNum(amount,command)):
                amount = int(amount)
                return((img,amount,True))
            else:
                return("Invalid Number. Make sure the number is in a valid range. Type 'help' after the command to check the range",0,False)
        else: 
            if(validateNum(help,command)): #check if given number
                amount = help
                help = ""
            else:
                return("Invalid URL/Number. The 1st parameter you gave was invalid. Check if the link has an image or if the number is in a valid range",0,False)
    if(help==""):
        try: #get image from attachment
            url = ctx.message.attachments[0].url
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            return((img,int(amount),True))
        except IndexError: #get image above if no image attached
            imgCache = await getMessages(ctx,2)
            for x in range(1,len(imgCache)):
                try:
                    url = imgCache[x].attachments[0].url
                    response = requests.get(url)
                    img = Image.open(BytesIO(response.content))
                    return((img,int(amount),True))
                except IndexError:
                    continue
            return(("No image found. Did you mean to show the help menu? Type 'help' after the command to show (without quotation marks)",0,False))

def validateURL(url):
    try:
        if not requests.get(url).status_code == 200:
            return False
        image_formats = ("image/png", "image/jpeg", "image/jpg")
        h = requests.head(url, timeout=1)
        if not (h.headers["content-type"] in image_formats):
            return(False)
        return True
    except requests.exceptions.MissingSchema:
        return False

def validateNum(num,command):
    if(command=="radial"):
        min,max = -100,100
    elif(command=="blur"):
        min,max = 1,50
    try:
        return(int(num)>=min and int(num)<=max)
    except ValueError:
        return(False)

## ----------------------------------------------------------------------------------------------- Image manipulation: ------------------------------------------------------------------------------------------------------ ##
@bot.command(pass_context=True,aliases=['deepfry'])
async def fry(ctx,help="",amount="0"):
    img,amount,successful = await getImage(ctx,"radial",help,amount)
    if not successful:
        if(amount==0): #Error command
            em = discord.Embed()
            em.title = f'Error when running command'
            em.description = f"Error: {img}."
            em.color = 0xEE0000
            await ctx.send(embed=em)
            return
        else: #Help Command
            em = discord.Embed()
            em.title = f'Usage: /fry [img|imgURL]'
            em.description = f'Deep-fries the image attached, url in the message, or the image attached before the command'
            em.add_field(name="Aliases", value="/deepfry", inline=False)
            em.add_field(name="Examples", value="/fry https://imgur.com/a/wUChw7w | /deepfry (imageAttachment)", inline=False)
            em.color = 0x22BBFF
            await ctx.send(embed=em)
            return
    await ctx.send("Processing...")
    toDelete = await getMessages(ctx,1)
    # Processing
    img = np.array(img) #convert PIL image to Numpy (CV2 works with numpy BRG arrays)
    # Convert RGB to BGR 
    img = cv.cvtColor(np.array(img), cv.COLOR_RGB2BGR)
    width, height = img.shape[:2]

    #Sharpen
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]) #how to modify a pixel based on surrounding pixels
    img = cv.filter2D(img, -1, kernel)
    #Increase brightness
    value = 30 #default value, change during testing
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    h, s, v = cv.split(hsv)
    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value
    final_hsv = cv.merge((h, s, v))
    img = cv.cvtColor(final_hsv, cv.COLOR_HSV2BGR)
    #Change gamma and make it crusty
    gamma = 30
    table = np.array([((i / 255.0) ** gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    img = cv.LUT(img, table)
    #Now deform the image a bit
    from skimage.transform import swirl, PiecewiseAffineTransform, warp #import works here but if at the beginning, breaks the code for some reason
    #swirl the image at random places
    for x in range(8):
        img = swirl(img, strength=((random.random()+1)*-1**x), radius=width/1.4,center=(random.randint(int(width/4),int(width-width/4)),random.randint(int(height/4),int(height-height/4))))
        img = (img*255).astype('uint8')
    #convert CV2 Numpy array to PIL
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB) #Change CV2 BGR to RGB
    im_pil = Image.fromarray(img)   #Convert to PIL
    # Convert to an attachable Discord Format
    arr = io.BytesIO() #convert to bytes array
    im_pil.save(arr, format='PNG')
    arr.seek(0) #seek back to beginning of file
    # Send
    await ctx.send(file=discord.File(arr,'fry.png'))
    await ctx.channel.delete_messages(toDelete)

@bot.command(pass_context=True,aliases=['radialblur','blur','funny'])
async def radial(ctx,help="",amount="10"):
    img,amount,successful = await getImage(ctx,"radial",help,amount)
    if not successful:
        if(amount==0): #Error command
            em = discord.Embed()
            em.title = f'Error when running command'
            em.description = f"Error: {img}."
            em.color = 0xEE0000
            await ctx.send(embed=em)
            return
        else: #Help Command
            em = discord.Embed()
            em.title = f'Usage: /radial [img|imgURL] [amount]'
            em.description = f'Adds radial blur to the image attached, url in the message, or the image attached before the command by [amount] from 1 to 50'
            em.add_field(name="Aliases", value="/blur /radialblur /funny", inline=False)
            em.add_field(name="Examples", value="/radialblur https://imgur.com/a/wUChw7w | /blur (imageAttachment) 30", inline=False)
            em.color = 0x22BBFF
            await ctx.send(embed=em)
            return()
    await ctx.send("Processing...")
    toDelete = await getMessages(ctx,1)
    # Processing
    img = np.array(img) #convert PIL image to Numpy (CV2 works with numpy BRG arrays)
    # Convert RGB to BGR 
    img = cv.cvtColor(np.array(img), cv.COLOR_RGB2BGR)
    w, h = img.shape[:2]
    # Radial Blur
    center_x = w / 2
    center_y = h / 2
    blur = amount/1000
    iterations = 5
    growMapx = np.tile(np.arange(h) + ((np.arange(h) - center_x)*blur), (w, 1)).astype(np.float32)
    shrinkMapx = np.tile(np.arange(h) - ((np.arange(h) - center_x)*blur), (w, 1)).astype(np.float32)
    growMapy = np.tile(np.arange(w) + ((np.arange(w) - center_y)*blur), (h, 1)).transpose().astype(np.float32)
    shrinkMapy = np.tile(np.arange(w) - ((np.arange(w) - center_y)*blur), (h, 1)).transpose().astype(np.float32)

    for i in range(iterations):
        tmp1 = cv.remap(img, growMapx, growMapy, cv.INTER_LINEAR)
        tmp2 = cv.remap(img, shrinkMapx, shrinkMapy, cv.INTER_LINEAR)
        img = cv.addWeighted(tmp1, 0.5, tmp2, 0.5, 0)

    #convert CV2 Numpy array to PIL
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB) #Change CV2 BGR to RGB
    im_pil = Image.fromarray(img)   #Convert to PIL
    # Convert to an attachable Discord Format
    arr = io.BytesIO() #convert to bytes array
    im_pil.save(arr, format='PNG')
    arr.seek(0) #seek back to beginning of file
    # Send
    await ctx.send(file=discord.File(arr,'radial.png'))
    await ctx.channel.delete_messages(toDelete)

@bot.command(pass_context=True)
async def swirl(ctx,help="",amount="10"):
    img,amount,successful = await getImage(ctx,"radial",help,amount)
    if not successful:
        if(amount==0): #Error command
            em = discord.Embed()
            em.title = f'Error when running command'
            em.description = f"Error: {img}."
            em.color = 0xEE0000
            await ctx.send(embed=em)
            return
        else: #Help Command
            em = discord.Embed()
            em.title = f'Usage: /swirl [img|imgURL] [amount]'
            em.description = f'Swirls the image attached, url in the message, or the image attached before the command by [amount] from -100 to 100'
            em.add_field(name="Examples", value="/swirl https://imgur.com/a/wUChw7w | /swirl (imageAttachment) 30", inline=False)
            em.color = 0x22BBFF
            await ctx.send(embed=em)
            return()
    await ctx.send("Processing...")
    toDelete = await getMessages(ctx,1)
    # Processing
    from skimage.transform import swirl #import works here but not at the beginning
    w,h = img.size
    img = np.array(img) #convert PIl image to Numpy
    # Swirl
    img = swirl(img, strength=amount, radius=w/1.3)
    img = (img*255).astype('uint8')
    #convert numpy array to Pillow img
    im_pil=Image.fromarray(img)
    # Convert to an attachable Discord Format
    arr = io.BytesIO() #convert to bytes array
    im_pil.save(arr, format='PNG')
    arr.seek(0) #seek back to beginning of file
    # Send
    await ctx.send(file=discord.File(arr,'swirl.png'))
    await ctx.channel.delete_messages(toDelete)

## ------------------------------------------------------------------------------------------------------- Music ------------------------------------------------------------------------------------------------------------ ##
bot.add_cog(music.Music(bot)) #very simple, 2 lines of code to add music (import music), not including the lines in music.py that someone painstakingly wrote that isnt myself

## ----------------------------------------------------------------------------------------------------- Help Menu ---------------------------------------------------------------------------------------------------------- ##
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
    em.add_field(name="/restore NUM", value=f"Restores NUM messages previously deleted by users, up to\n[up to {MAXUSERDELETEDMESSAGES} per text channel]", inline=True)
    em.add_field(name="/say PHRASE", value="Makes bot say what you put in PHRASE", inline=True)

    em.add_field(name="\u200b", value="__**Games**__", inline=False)
    em.add_field(name="/connect4 OPPONENT [width] [height]", value="Challenges OPPONENT to a game of connect 4 on a [width]x[height] board", inline=True)

    em.add_field(name="\u200b", value="__**Images**__", inline=False)
    em.add_field(name="/fry [IMG | IMG_URL]", value="Deepfries an image attachemnt, image at the url given, or the iamge attachemnt before the command is executed", inline=True)
    em.add_field(name="/radial [IMG | IMG_URL] [amount]", value="Radial blurs an image attachemnt, image at the url given, or the iamge attachemnt before the command is executed", inline=True)
    em.add_field(name="/swirl [IMG | IMG_URL] [amount]", value="Swirls an image attachemnt, image at the url given, or the iamge attachemnt before the command is executed", inline=True)

    em.add_field(name="\u200b", value="__**Other**__", inline=False)
    em.add_field(name="/python CODE", value="```diff\n-Runs CODE as Python code, only works for specific users due to some security and execution concerns```", inline=True)
    em.add_field(name="On Messages", value="Longer phallic emojis\nAdded warning for mentioning underage children", inline=False)
    await ctx.send(embed=em)
    ## Message cuts off soon due to max embed size capacity, start a new embed
    em = discord.Embed()
    em.title = '__**Music/Voice Commands**__'
    em.description = "Thanks to vbe0201's for this example framework"
    em.color = 0x22BBFF
    em.add_field(name="/play URL|SEARCH", value="Plays audio from Youtube URL or search a video", inline=True)
    em.add_field(name="/volume NUM", value="Sets volume from 0% to 200%", inline=True)
    em.add_field(name="/mute", value="Sets volume to 0%", inline=True)
    em.add_field(name="/unmute", value="Restores volume to original value", inline=True)
    em.add_field(name="/stop", value="Stops currently playing song", inline=True)
    em.add_field(name="/join", value="Joins voice channel", inline=True)
    em.add_field(name="/leave | /disconnect", value="Leaves voice channel", inline=True)
    em.add_field(name="/info | /current | /playing", value="Gets info about the currently playing track", inline=True)
    em.add_field(name="/pause", value="Pauses the currently playing track", inline=True)
    em.add_field(name="/resume", value="Resumes the currently playing track", inline=True)
    em.add_field(name="/skip", value="Skips the currently playing track", inline=True)
    em.add_field(name="/queue", value="Shows the video queue", inline=True)
    em.add_field(name="/shuffle", value="Shuffles the video queue around", inline=True)
    em.add_field(name="/remove INDEX", value="Removes the video in the queue at INDEX (starts at 1)", inline=True)
    em.add_field(name="/loop", value="Loops the currently playing track. Run again to unloop", inline=True)
    await ctx.send(embed=em)

## ----------------------------------------------------------------------------------------------------- Others ------------------------------------------------------------------------------------------------------------ ##
@bot.command(pass_context=True)
async def test(ctx,help="",amount="10"):
    pass

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












###=============== Get bot token ================###
file = open("token.txt",'r')
token = file.read()
file.close()
bot.run(token)
###==============================================###

# Image manipulation resources:
# CV2 kernel examples: https://towardsdatascience.com/python-opencv-building-instagram-like-image-filters-5c482c1c5079