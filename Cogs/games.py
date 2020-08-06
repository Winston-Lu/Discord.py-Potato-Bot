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

    @commands.command(name='chess')
    async def chess(self, ctx: commands.Context,opponent=""):
        #-------------- Help section ------------------#
        if(opponent=="" or opponent.find('help')!=-1):
            em = discord.Embed()
            em.title = f'Usage: /chess opponent'
            em.description = f'Challenges opponent to a game of chess. The Opponent should be @mentoned to start\nOpponent will make the first move, and thus be controlling the white pieces.'
            em.add_field(name="Example", value="/chess @Username", inline=False)
            em.color = 0x22BBFF
            await ctx.send(embed=em)
            return
        #----------------------------------------------#
        # Remove challenge message
        await ctx.channel.delete_messages(await self.getMessages(ctx,1))
        # Game init
        pawnwhite = "♟︎"
        knightwhite = "♞"
        bishopwhite = "♝"
        rookwhite = "♜"
        queenwhite = "♛"
        kingwhite = "♚"
        whitepieces = (pawnwhite,knightwhite,bishopwhite,rookwhite,queenwhite,kingwhite)
        pawnblack = "♙"
        knightblack = "♘"
        bishopblack = "♗"
        rookblack = "♖"
        queenblack = "♕"
        kingblack = "♔"
        blackpieces = (pawnblack,knightblack,bishopblack,rookblack,queenblack,kingblack)
        space = " "

        board = [[rookwhite,knightwhite,bishopwhite,queenwhite,kingwhite,bishopwhite,knightwhite,rookwhite],
                 [pawnwhite,pawnwhite,pawnwhite,pawnwhite,pawnwhite,pawnwhite,pawnwhite,pawnwhite],
                 ['','','','','','','',''],
                 ['','','','','','','',''],
                 ['','','','','','','',''],
                 ['','','','','','','',''],
                 [pawnblack,pawnblack,pawnblack,pawnblack,pawnblack,pawnblack,pawnblack,pawnblack],
                 [rookblack,knightblack,bishopblack,queenblack,kingblack,bishopblack,knightblack,rookblack]
        ]

        player1 = ctx.message.mentions[0].name
        player2 = ctx.message.author.name
        def getDisplay():
            toDisplay = ""
            for y in range(0,8):
                toDisplay+=(f'{8-y} |')
                for x in range(8):
                    if(board[y][x]==''):
                        toDisplay+=space+'|'
                    else:
                        toDisplay+=board[y][x]+'|'
                toDisplay+='\n'
            toDisplay+="  A | B | C | D | E | F | G | H |"
            return(toDisplay)
        ### Send Message
        boardMessage = None #the message so that it can be deleted and altered when a move is made
        # Create Message
        em = discord.Embed()
        if(player1==player2):
            em.title = f"{player2} challenged themselves to a game of chess\n(wow you're lonely)"
        else:
            em.title = f'{player2} challenged {player1} to a game of chess'
        em.description = f"{getDisplay()}"
        em.color = 0x444444
        em.add_field(name=f"{player1}", value=f"Type two coordinates (piece -> destination), or type 'decline' to refuse\nYou are the the bottom player", inline=False)
        em.add_field(name="Example", value="a2 a3", inline=False)
        await ctx.send(embed=em)
        # Add message in the to-delete list
        async for x in ctx.channel.history(limit = 1):
            boardMessage = x
        # Game variables
        badInput = 0
        currentPlayer = player1
        otherPlayer = player2
        currentPlayerId=1
        
        #Castling check
        iswhitekingmove = False
        iswhiterookmove1 = False
        iswhiterookmove2 = False
        isblackkingmove = False
        isblackrookmove1 = False
        isblackrookmove2 = False


        # Validate move function (used later)
        def validMove(playerTurn,msg):
            move = msg.lower().split(" ")
            if(len(move)!=2): #should be 2 coordinates
                return "Did not find exactly 2 coordinates. Make sure they are seperated by a space. Ex: 'a2 a3'"
            if(len(move[0])!=2 and len(move[1])!=2): #should be 2 characters long
                return "Coordinates were not 2 characters long, did you mistype the coordinate?"
            try:
                coordOfPiece = (8-int(move[0][1]),ord(move[0][0])-97)
                coordOfDestination = (8-int(move[1][1]),ord(move[1][0])-97)
                pieceToMove = board[coordOfPiece[0]][coordOfPiece[1]]
                pieceAtDestination = board[coordOfDestination[0]][coordOfDestination[1]]
                dx = coordOfDestination[1] - coordOfPiece[1]
                dy = coordOfPiece[0] - coordOfDestination[0] ##switch around for a more cartesion coordinate-like system instead of 0 being at the top
                errorMsg = ""
                if(dx==0 and dy==0): #if src and dst are the same
                    return "you must move your piece"
                #a switch-case would have been a lot nicer
                if(playerTurn==player1):
                    if(pieceToMove == pawnwhite):
                        if(dy==1): ##if moving 1 up
                            ##------ standard move up
                            #    if horizontal movement is 0    and     space to move is empty
                            if(dx==0 and pieceAtDestination==''): #forward and no piece in front
                                return 'g'
                            ##------ pawn killing a piece
                            #       if horizontal movement is 1         and     spot to move is a black piece
                            elif(abs(dx)==1 and pieceAtDestination in blackpieces):
                                return 'g'
                            else:
                                return "not a valid move for pawn"
                        ##------ Double jump
                        #   if moving 2 spaces up and moving 0 spaces to the side and on start line and nothing between pawn and destination
                        elif(dy==2 and dx==0 and coordOfPiece[0] == 6 and board[5][coordOfPiece[1]]==''): 
                            return 'g'
                        else:
                            return "not a valid move for pawn"
                    elif(pieceToMove == knightwhite):
                        if not (pieceAtDestination in whitepieces): #only move restriction is if spot is not own piece
                            if ((abs(dy)==2 and abs(dx)==1) or (abs(dy)==1 and abs(dx)==2)):
                                return 'g'
                            else:
                                return 'invalid move for knight'
                        else:
                            return "invalid move for knight"
                    elif(pieceToMove == bishopwhite):
                        if ((not (pieceAtDestination in whitepieces)) and abs(dx)==abs(dy)): #dont move if spot is their own piece and is moving diagonally
                            checkdx = abs(dx)/dx # +-1
                            checkdy = abs(dy)/dy # +-1
                            checkx = coordOfPiece[1]
                            checky = coordOfPiece[0]
                            tilesToCheck = abs(dx) #abs(dy) works too
                            for _ in range(tilesToCheck-1):
                                if(board[checky+checkdy][checkx+checkdx]!=''): #if piece in the way of bishops move
                                    return "piece in the way of bishop's move"
                                #increment diagonal check coordinates, branchless would have been a cleaner implentation
                                if(checkdx<0):
                                    checkdx-=1
                                else:
                                    checkdx+=1
                                if(checkdy<0):
                                    checkdy-=1
                                else:
                                    checkdy+=1
                            return 'g' #if passed check, move should be good
                        else:
                            return "not a valid move for bishop"
                    elif(pieceToMove == rookwhite):
                        if ((not (pieceAtDestination in whitepieces)) and (dx==0 or dy==0)): #dont move if spot is their own piece and is moving horizontally/vertically
                            checkx = coordOfPiece[1]
                            checky = coordOfPiece[0]
                            tilesToCheck = abs(dx) #abs(dy) works too
                            if(dx!=0): #moving horizontally
                                checkdx=abs(dx)/dx
                                for _ in (tilesToCheck-1):
                                    if(board[checky][checkx+checkdx]!=''): #if piece in the way of bishops move
                                        return "piece in the way of rook's move"
                                    #increment check coordinates, branchless would have been a cleaner implentation
                                    if(checkdx<0):
                                        checkdx-=1
                                    else:
                                        checkdx+=1
                            else: #moving vertically
                                checkdy=abs(dy)/dy
                                for _ in (tilesToCheck-1):
                                    if(board[checky+checkdy][checkx]!=''): #if piece in the way of bishops move
                                        return "piece in the way of rook's move"
                                    #increment check coordinates, branchless would have been a cleaner implentation
                                    if(checkdy<0):
                                        checkdy-=1
                                    else:
                                        checkdy+=1
                            return 'g'
                        else:
                            return "not a valid move for rook"
                    elif(pieceToMove == queenwhite):
                        if ((not (pieceAtDestination in whitepieces)) and (abs(dx)==abs(dy) or (abs(dx)==0 or abs(dy)==0))): #dont move if spot is their own piece and is moving diagonally
                            checkx = coordOfPiece[1]
                            checky = coordOfPiece[0]
                            tilesToCheck = abs(dx) #abs(dy) works too
                            #if diagonal move
                            if(abs(dx)==abs(dy)):
                                checkdx = abs(dx)/dx # +-1
                                checkdy = abs(dy)/dy # +-1
                                for _ in range(tilesToCheck-1):
                                    if(board[checky+checkdy][checkx+checkdx]!=''): #if piece in the way of queens move
                                        return "piece in the way of queen's move"
                                    #increment diagonal check coordinates, branchless would have been a cleaner implentation
                                    if(checkdx<0):
                                        checkdx-=1
                                    else:
                                        checkdx+=1
                                    if(checkdy<0):
                                        checkdy-=1
                                    else:
                                        checkdy+=1
                                return 'g' #if passed check, move should be good
                            #if horizontal move
                            elif(dx==0 or dy==0):
                                if(dx!=0): #moving horizontally
                                    checkdx=abs(dx)/dx
                                    for _ in (tilesToCheck-1):
                                        if(board[checky][checkx+checkdx]!=''): #if piece in the way of queens move
                                            return "piece in the way of queen's move"
                                        #increment check coordinates, branchless would have been a cleaner implentation
                                        if(checkdx<0):
                                            checkdx-=1
                                        else:
                                            checkdx+=1
                                else: #moving vertically
                                    checkdy=abs(dy)/dy
                                    for _ in (tilesToCheck-1):
                                        if(board[checky+checkdy][checkx]!=''): #if piece in the way of bishops move
                                            return "piece in the way of queen's move"
                                        #increment check coordinates, branchless would have been a cleaner implentation
                                        if(checkdy<0):
                                            checkdy-=1
                                        else:
                                            checkdy+=1
                                return 'g'
                            else:
                                return "not a valid move for queen - not sure what went wrong"
                        else:
                            return "not a valid move for queen"
                    elif(pieceToMove == kingwhite):
                        if not pieceAtDestination in whitepieces:
                            if (abs(dx)<=1 and abs(dy)<=1): #if spot is 1 tile away
                                if not (isInCheck(player1,coordOfDestionation)):
                                    return 'g'
                                else:
                                    return 'king can not move into check'
                            #castle to the left
                            elif ( (not iswhitekingmove) and (not iswhiterookmove1) and coordOfDestination[0] == 7 and coordOfDestination[1] == 2):
                                if (board[7][1]=='' and board[7][2]=='' and board[7][3]==''):
                                    return 'g'
                                else:
                                    return 'can not castle with pieces in the way'
                            #castle to the right
                            elif ( (not iswhitekingmove) and (not iswhiterookmove2) and coordOfDestination[0] == 7 and coordOfDestination[1] == 6):
                                if (board[7][5]=='' and board[7][6]==''):
                                    return 'g'
                                else:
                                    return 'can not castle with pieces in the way'
                        else:
                            return "king can not kill their own piece"
                        ## if king hasnt moved and king is moving to (C1 and rook has not moved) 
                        ##      if no pieces in B1 C1 D1
                        ##          return 'g'
                        ##      else:
                        ##          return "Can not castle with pieces in the way"
                        ## elif king hasnt moved and king is moving to (G1 and rook2 has not moved)
                        ##      if no pieces in F1 G1
                        ##          return 'g'
                        ##      else:
                        ##          return "Can not castle with pieces in the way"
                    else:
                        return(f"Invalid move: {errorMsg}") #if chose empty space or opponent's piece
                elif(playerTurn==player2):
                    if(pieceToMove == pawnblack):
                        ## pawn double move
                        pass
                    elif(pieceToMove == knightblack):
                        pass
                    elif(pieceToMove == bishopblack):
                        pass
                    elif(pieceToMove == rookblack):
                        pass
                    elif(pieceToMove == queenblack):
                        pass
                    elif(pieceToMove == kingblack):
                        pass
                    else:
                        return(f"Invalid move: {errorMsg}") #if chose empty space or opponent's piece
                    return 'g' #for testing, assume all black player moves are okay
            except IndexError:
                return "Coordinates does not seem to exist on the board"


        def isInCheck(player,dest): #checks if that spot would be in check
            if(player==player1): #if white king in check
                pass
            elif(player==player2): #if black king in check
                pass


        ## Get Opponent's first move, if opponent accepts match
        while True:
            try:
                msg = await self.bot.wait_for('message',check=lambda message: message.author.name == player1, timeout=30)
                if(msg.content=='decline'):
                    em = discord.Embed()
                    if(player1==player2):
                        em.title = f"{player2} challenged themselves to a game of chess (wow you're lonely)"
                    else:
                        em.title = f'{player2} challenged {player1} to a game of chess 4'
                    em.description = f"{getDisplay()}"
                    em.color = 0x444444
                    em.add_field(name=f"{player1}", value="Challenge refused", inline=False)
                    await boardMessage.edit(embed=em)
                    return
                # Parse Message
                checkMove = validMove(currentPlayer,msg.content)
                if(len(checkMove)>1): #not 'g' 
                    raise ValueError
                #cleanup and start main game loop
                await ctx.channel.delete_messages(await self.getMessages(ctx,1))
                gameLoop = True
                currentPlayer = player2
                otherPlayer = player1
                turns +=1
                currentPlayerId=2
                break;
            except asyncio.exceptions.TimeoutError:
                em = discord.Embed()
                if(player1==player2):
                    em.title = f"{player2} challenged themselves to a game of chess (wow you're lonely)"
                else:
                    em.title = f'{player2} challenged {player1} to a game of chess'
                em.description = f"{getDisplay()}"
                em.color = 0x444444
                em.add_field(name=f"{player1}", value="Game timed out", inline=False)
                await boardMessage.edit(embed=em)
                return
            except ValueError:
                em = discord.Embed()
                if(player1==player2):
                    em.title = f"{player2} challenged themselves to a game of chess (wow you're lonely)"
                else:
                    em.title = f'{player2} challenged {player1} to a game of chess'
                em.description = f"{getDisplay()}"
                em.color = 0x444444
                em.add_field(name=f"{player1}", value=f"Enter a valid coordinate pair for the piece", inline=False)
                em.add_field(name=f"Error:", value=f"{checkmove}", inline=False)
                await boardMessage.edit(embed=em)
                badInput+=1
            if(badInput==3):
                em = discord.Embed()
                if(player1==player2):
                    em.title = f"{player2} challenged themselves to a game of chess (wow you're lonely)"
                else:
                    em.title = f'{player2} challenged {player1} to a game of chess'
                em.description = f"{getDisplay()}"
                em.color = 0x444444
                em.add_field(name=f"{player1}", value="Did not enter a valid move in 3 tries. Game ended.", inline=False)
                await boardMessage.edit(embed=em)
                return
        winningComment=""
        winner=""
        while gameLoop:
            pass




    async def getMessages(self,ctx: commands.Context,number: int=1):
        if(number==0):
            return([])
        toDelete = []
        async for x in ctx.channel.history(limit = number):
            toDelete.append(x)
        return(toDelete)

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        em = discord.Embed()
        em.title = f'Error: {__name__}'
        em.description = f"{error}"
        em.color = 0xEE0000
        await ctx.send(embed=em)