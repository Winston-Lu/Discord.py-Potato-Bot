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
                 [rookblack,knightblack,bishopblack,queenblack,kingblack,bishopblack,knightblack,rookblack],
        ]

        # Game variables
        player1 = ctx.message.mentions[0].name
        player2 = ctx.message.author.name
        currentPlayer = player1
        otherPlayer = player2
        player1badInput = 0
        player2badInput = 0
        currentPlayerId=1
        prevMove = ""
        turn = 0
        #Castling check
        castlingDict = {
            "isWhiteKingMove": False,
            "isWhiteRookMoveL": False,
            "isWhiteRookMoveR": False,
            "isBlackKingMove": False,
            "isBlackRookMoveL": False,
            "isBlackRookMoveR": False,
        }
        
        #Bunch of helper functions
        def getDisplay():
            toDisplay = ""
            for y in range(0,8):
                toDisplay+=(f'{y+1} |')
                for x in range(8):
                    if(board[y][x]==''):
                        toDisplay+=space+'|'
                    else:
                        toDisplay+=board[y][x]+'|'
                toDisplay+='\n'
            toDisplay+="  A | B | C | D | E | F | G | H |"
            return(toDisplay)

        def parseMove(msg: str):
            msg = msg.lower()
            try:
                if (msg[0].isalpha() and msg[1].isdigit()):
                    x = ord(msg[0])-97
                    y = int(msg[1])-1
                    if(x < 8 and y < 8 and x >= 0 and y >= 0):
                        return ((y,x))
                else:
                    raise ValueError
            except:
                pass
            return ((None,None))

        def validateMove(src: tuple, dst: tuple, castlingDict: dict):
            piece = board[src[0]][src[1]]
            dx = dst[1]-src[1]
            dy = dst[0]-src[0]
            #check if the shape/direction of travel is valid
            if(piece == pawnwhite):
                if(dx==0):
                    if(dy==1): #can move down 1 if spot above is empty
                        return (board[dst[0]][dst[1]]=="" and not inCheck(src,dst))
                    elif(dy==2): #double move if space between is empty and destination is empty
                        return(emptySpaceBetween(src,dst) and board[dst[0]][dst[1]]=="" and not inCheck(src,dst))
                    return False
                #if moving diagonally
                elif(abs(dx)==1 and dy==1):
                    #en passant at right spot, to an empty space, and passing an opponent pawn
                    if(dst[0]==5 and board[dst[0]][dst[1]]=="" and board[dst[0]-1][dst[1]]==pawnblack):
                        #check if pervious move before was a double move
                        prevMoveCoordsSrc = parseMove(prevMove.split(" ")[0])
                        prevMoveCoordsDst = parseMove(prevMove.split(" ")[1])
                        #if x move is 0, y move is 2, and prevMoveCoordsDst x is dst x 
                        if(abs(prevMoveCoordsSrc[0]-prevMoveCoordsDst[0])==2 and prevMoveCoordsSrc[1]-prevMoveCoordsDst[1]==0 and prevMoveCoordsDst[1] == dst[1] and not inCheck(src,dst)):
                            board[prevMoveCoordsDst[0]][prevMoveCoordsDst[1]] = ""
                            return True
                        return False
                    return (isOpponentPiece(src,dst) and not inCheck(src,dst))
                return False

            elif(piece == pawnblack):
                if(dx==0):
                    if(dy==-1): #can move up 1 if spot above is empty
                        return (board[dst[0]][dst[1]]=="" and not inCheck(src,dst))
                    elif(dy==-2): #double move if space between is empty and destination is empty
                        return(emptySpaceBetween(src,dst) and board[dst[0]][dst[1]]=="" and not inCheck(src,dst))
                    return False
                #if moving diagonally
                elif(abs(dx)==1 and dy==-1):
                    #en passant at right spot, to an empty space, and passing an opponent pawn
                    if(dst[0]==2 and board[dst[0]][dst[1]]=="" and board[dst[0]+1][dst[1]]==pawnwhite):
                        #check if pervious move before was a double move
                        prevMoveCoordsSrc = parseMove(prevMove.split(" ")[0])
                        prevMoveCoordsDst = parseMove(prevMove.split(" ")[1])
                        #if x move is 0, y move is 2, and prevMoveCoordsDst x is dst x 
                        if (abs(prevMoveCoordsSrc[0]-prevMoveCoordsDst[0])==2 and prevMoveCoordsSrc[1]-prevMoveCoordsDst[1]==0 and prevMoveCoordsDst[1] == dst[1] and not inCheck(src,dst)):
                            board[prevMoveCoordsDst[0]][prevMoveCoordsDst[1]] = ""
                            return True
                        return False
                    return(isOpponentPiece(src,dst) and not inCheck(src,dst))
                return False

            elif(piece == rookwhite or piece == rookblack):
                if((dy==0 and dx!=0) or (dy!=0 and dx==0)):
                    if(emptySpaceBetween(src,dst) and (board[dst[0]][dst[1]]=="" or isOpponentPiece(src,dst)) and not inCheck(src,dst)):
                        if(src[0]==0 and src[1]==0):
                            castlingDict["isWhiteRookMoveL"] = True
                        elif(src[0]==0 and src[1]==7):
                            castlingDict["isWhiteRookMoveR"] = True
                        elif(src[0]==7 and src[1]==0):
                            castlingDict["isBlackRookMoveL"] = True
                        elif(src[0]==7 and src[1]==7):
                            castlingDict["isBlackRookMoveR"] = True
                        return True
                    return False

            elif(piece == knightblack or piece == knightwhite):
                return (
                        (   #L-moves
                            (abs(dy)==1 and abs(dx)==2) 
                            or 
                            (abs(dy)==2 and abs(dx)==1)
                        ) 
                        and #destination is a capture or empty
                        (   board[dst[0]][dst[1]]=="" or isOpponentPiece(src,dst)  )
                        and
                            not inCheck(src,dst)
                       )

            elif(piece == bishopwhite or piece == bishopblack):
                if(abs(dy)==abs(dx)):
                    return(emptySpaceBetween(src,dst) and (board[dst[0]][dst[1]]=="" or isOpponentPiece(src,dst)) and not inCheck(src,dst))
                return False

            elif(piece == queenblack or piece == queenwhite):
                if( (dy==0 and dx!=0) or #horizontal
                    (dy!=0 and dx==0) or #vertucak
                    (abs(dy)==abs(dx))): #diagonal
                    return(emptySpaceBetween(src,dst) and (board[dst[0]][dst[1]]=="" or isOpponentPiece(src,dst)) and not inCheck(src,dst))
                return False

            elif(piece == kingblack or piece == kingwhite):
                if(abs(dx)<=1 and abs(dy)<=1 and not inCheck(src,dst)):
                    if(src[0]==7 and src[1] == 4):
                        castlingDict["isBlackKingMove"] = True
                    elif(src[0]==0 and src[1] == 4):
                        castlingDict["isWhiteKingMove"] = True
                    return (board[dst[0]][dst[1]]=="" or isOpponentPiece(src,dst) and not inCheck(src,dst))
                elif(abs(dx)>1 and dy==0 and not inCheck(src,dst)):
                    #possible castling
                    #move the rook as well since we are only moving the king
                    if(src[0]==0 and src[1]==4 and dx==-3 and not castlingDict["isWhiteRookMoveL"] and not castlingDict["isWhiteKingMove"] and board[0][0]==rookwhite):
                        board[0][0] = ""
                        board[0][2] = rookwhite
                        return True
                    elif (src[0]==0 and src[1]==4 and dx==2 and not castlingDict["isWhiteRookMoveR"] and not castlingDict["isWhiteKingMove"] and board[0][7]==rookwhite):
                        board[0][7] = ""
                        board[0][5] = rookwhite
                        return True
                    elif(src[0]==7 and src[1]==4 and dx==-3 and not castlingDict["isBlackRookMoveL"] and not castlingDict["isBlackKingMove"] and board[7][0]==rookblack):
                        board[7][0] = ""
                        board[7][2] = rookblack
                        return True
                    elif(src[0]==7 and src[1]==4 and dx==2 and not castlingDict["isBlackRookMoveR"] and not castlingDict["isBlackKingMove"] and board[7][7]==rookblack):
                        board[7][7] = ""
                        board[7][5] = rookblack
                        return True
                    return False

        def emptySpaceBetween(src: tuple, dst: tuple):
            dx = dst[1]-src[1]
            dy = dst[0]-src[0]
            dxDir = 1 if (dx > 0) else -1
            dyDir = 1 if (dy > 0) else -1
            if(dy==0 and dx != 0):
                #move from source x to destination x, ignoring itself (hence the src[1] +- 1)
                for x in range(src[1]+dxDir,dst[1],dxDir):
                    if(board[src[0]][x] != ""): 
                        return False #if piece between src and dst, return false
                return True
            elif(dx==0 and dy != 0):
                #move from source x to destination x, ignoring itself (hence the src[1] +- 1)
                for y in range(src[0]+dyDir,dst[0],dyDir):
                    if(board[y][src[1]] != ""): 
                        return False #if piece between src and dst, return false
                return True
            elif(abs(dy)==abs(dx)):
                for i in range (1,abs(dx)):
                    if(board[src[0]+i*dyDir][src[1]+i*dxDir] != ""):
                        return False
                return True
            return False

        def isOpponentPiece(src: tuple, dst: tuple):
            if(board[src[0]][src[1]] in whitepieces):
                return (board[dst[0]][dst[1]] in blackpieces)
            elif (board[src[0]][src[1]] in blackpieces):
                return (board[dst[0]][dst[1]] in whitepieces)
            return False

        def movePiece(msg: str):
            src = parseMove(msg.split(" ")[0])
            dst = parseMove(msg.split(" ")[1])
            board[dst[0]][dst[1]] = board[src[0]][src[1]]
            board[src[0]][src[1]] = ""

        def checkPlayerMove(msg: str, castlingDict: dict):
            coords = msg.split(" ")
            if(len(coords) != 2):
                return "Please give 2 coordinates separated by spaces. Ex: a2 a4"
            src = parseMove(coords[0])
            dst = parseMove(coords[1])
            if(src[0]==None):
                return "The first coordinate entered is in an invalid format (a-h)(1-8). Ex: A5 or a5"
            if(dst[0]==None):
                return "The second coordinate entered is in an invalid format (a-h)(1-8). Ex: A5 or a5"
            if((currentPlayerId == 2 and board[src[0]][src[1]] in whitepieces) or (currentPlayerId == 1 and board[src[0]][src[1]] in blackpieces)):
                return "You can not move your opponent's pieces"
            if(validateMove(src,dst,castlingDict)):
                return f"Turn {turn}: {currentPlayer} moved from {coords[0].upper()} to {coords[1].upper()}\n{otherPlayer}, Type two coordinates to move"
            if(board[src[0]][src[1]] == ""):
                return ("You did not select a valid piece")
            return "That piece can not move there"
       
        def inCheck(src: tuple, dst: tuple, player=None):
            if(player==None): #check player dependinbg on src piece
                pass
            elif (player == player1): #if player is defined, check if white is in check
                pass
            elif (player == player2): #if player is defined, check if black is in check
                pass
            return False #placeholder
        ### Send Message
        boardMessage = None #the message so that it can be deleted and altered when a move is made
        # Create Message
        em = discord.Embed()
        em.title = f'{player2} challenged {player1} to a game of chess'
        em.description = f"{getDisplay()}"
        em.color = 0x444444
        em.add_field(name=f"{player1}", value=f"Type two coordinates (piece -> destination), or type 'decline' to refuse\nYou are playing white", inline=False)
        em.add_field(name="Example", value="a2 a3", inline=False)
        await ctx.send(embed=em)
        # Add message to edit later
        async for x in ctx.channel.history(limit = 1):
            boardMessage = x

        for x in range(4):
            try:
                em = discord.Embed()
                em.title = f'{player2} challenged {player1} to a game of chess'
                msg = await self.bot.wait_for('message',check=lambda message: message.author.name == player1, timeout=30)
                if(msg.content=='decline'):
                    em.description = f"{getDisplay()}"
                    em.add_field(name=f"{player1}", value="Challenge refused", inline=False)
                    await boardMessage.edit(embed=em)
                    return
                gameMsg = checkPlayerMove(msg.content,castlingDict)
                if(gameMsg[0:4]!="Turn"):
                    player1badInput+=1
                    em.description = f"{getDisplay()}"
                    em.color = 0xFF0000
                    em.add_field(name="Error", value=f"{gameMsg}", inline=False)
                    await boardMessage.edit(embed=em)
                    continue
                await ctx.channel.delete_messages(await self.getMessages(ctx,1))
                turn += 1
                movePiece(msg.content)
                em.color = 0x00FF00
                em.description = f"{getDisplay()}"
                em.add_field(name=f"{otherPlayer}'s turn:", value=f"{gameMsg}", inline=False)
                await boardMessage.edit(embed=em)
                gameLoop = True
                currentPlayer,otherPlayer = otherPlayer,currentPlayer
                currentPlayerId = 2 if (currentPlayerId == 1) else 1
                player1badInput = 0
                prevMove = msg.content
                break;
            except asyncio.exceptions.TimeoutError:
                em.description = f"{getDisplay()}"
                em.color = 0xFF0000
                em.add_field(name=f"{player1}", value="Game timed out", inline=False)
                await boardMessage.edit(embed=em)
                return
            if(player1badInput==3):
                em.description = f"{getDisplay()}"
                em.color = 0xFF0000
                em.add_field(name=f"{player1}", value="Did not enter a valid move in 3 tries. Game ended.", inline=False)
                await boardMessage.edit(embed=em)
                return
        #Main game loop
        while gameLoop:
            try:
                em = discord.Embed()
                em.title = f'Chess match between {player2} and {player1}'
                em.add_field(name="Moves:", value=f"Type the 2 coordinates for the piece you want to move and the spot to move to, or type 'quit' to stop the game.", inline=False)
                msg = await self.bot.wait_for('message',check=lambda message: message.author.name == currentPlayer, timeout=30)
                gameMsg = checkPlayerMove(msg.content,castlingDict)
                if(msg.content[0:4]=="quit"):
                    em.color = 0x770000
                    em.description = f"{getDisplay()}"
                    em.add_field(name=f"{currentPlayer} Quits", value=f"{otherPlayer} wins!", inline=False)
                    await boardMessage.edit(embed=em)
                    return
                elif(gameMsg == "That piece can not move there"):
                    coords = msg.content.split(" ")
                    if(inCheck(parseMove(coords[0]),parseMove(coords[1]))):
                        em.color = 0xFF0000
                        em.description = f"{getDisplay()}"
                        em.add_field(name="Error", value=f"Can not move into check", inline=False)
                    else:
                        em.color = 0x770000
                        em.description = f"{getDisplay()}"
                        em.add_field(name="Invalid Move", value=f"{gameMsg}", inline=False)
                    await boardMessage.edit(embed=em)
                    continue
                elif(gameMsg[0:4]!="Turn"):
                    if(currentPlayer == player1):
                        player1badInput+=1
                    else:
                        player2badInput+=1
                    em.color = 0x770000
                    em.description = f"{getDisplay()}"
                    em.add_field(name="Invalid Move", value=f"{gameMsg}", inline=False)
                    await boardMessage.edit(embed=em)
                    continue
                await ctx.channel.delete_messages(await self.getMessages(ctx,1))
                turn += 1
                movePiece(msg.content)
                em.description = f"{getDisplay()}"
                em.color = 0x00FF00
                em.add_field(name=f"{otherPlayer}'s turn:", value=f"{gameMsg}", inline=False)
                if(currentPlayerId == 1):
                    player1badInput = 0
                elif(currentPlayerId == 2):
                    player2badInput = 0
                currentPlayer,otherPlayer = otherPlayer,currentPlayer
                currentPlayerId = 2 if (currentPlayerId == 1) else 1
                prevMove = msg.content
                await boardMessage.edit(embed=em)
            except asyncio.exceptions.TimeoutError:
                em.description = f"{getDisplay()}"
                em.color = 0x770000
                em.add_field(name=f"{currentPlayer} Forfeit", value="Didn't make a move within 30 seconds", inline=False)
                await boardMessage.edit(embed=em)
                return
            if(player1badInput==3):
                em.description = f"{getDisplay()}"
                em.color = 0x770000
                em.add_field(name=f"{player1} Forfeit", value="Did not enter a valid move in 3 tries. Game ended.", inline=False)
                await boardMessage.edit(embed=em)
                return
            if(player2badInput==3):
                em.description = f"{getDisplay()}"
                em.color = 0x770000
                em.add_field(name=f"{player2} Forfeit", value="Did not enter a valid move in 3 tries. Game ended.", inline=False)
                await boardMessage.edit(embed=em)
                return

       #ToDO
       #Finish castling (move the rook)
       #check

        




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

#for running in vscode coderunner
if __name__ == '__main__':
    import sys, os
    sys.path.append(os.path.abspath('.'))
    import bot