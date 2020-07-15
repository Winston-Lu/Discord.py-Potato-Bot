import discord
from discord.ext import commands
import asyncio


class Games(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='connect4')
    async def connect4(self,ctx: commands.Context,opponent="",width=7,height=6):
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
        await ctx.channel.delete_messages(await self.getMessages(ctx,1))
        
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
                msg = await self.bot.wait_for('message',check=lambda message: message.author.name == player1, timeout=30)
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
                await ctx.channel.delete_messages(await self.getMessages(ctx,1))
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
                    msg = await self.bot.wait_for('message',check=lambda message: message.author.name == currentPlayer, timeout=30)
                    await ctx.channel.delete_messages(await self.getMessages(ctx,1))
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




    async def getMessages(self,ctx: commands.Context,number: int=1):
        if(number==0):
            return([])
        toDelete = []
        async for x in ctx.channel.history(limit = number):
            toDelete.append(x)
        return(toDelete)

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        em = discord.Embed()
        em.title = 'Error: Games'
        em.description = f"{error}"
        em.color = 0xEE0000
        await ctx.send(embed=em)
        return