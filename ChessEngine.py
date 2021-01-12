
class GameState():
    def __init__(self):

        #the board notation is : b -> Black, R -> Rock and -- -> empty space
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]

        self.moveFunctions = {'P': self.getPawnMoves, 'R': self.getRockMoves, 'N': self.getKnightMoves, 
                              'B': self.getBishopMoves, 'K' :self.getKingMoves, 'Q': self.getQueenMoves}

        self.whiteToMove = True 
        self.moveLog =[]
        self.WhiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False

    # takes a move as a marameter and executes it (that is not working for castling, pawn pormotion and en passant)    
    def makeMove(self, move):
        self.board[move.startRaw][move.startCol] = "--"
        self.board[move.endRaw][move.endCol] = move.pieceMoved
        self.moveLog.append(move) # Log the move so we can undo it later
        self.whiteToMove = not self.whiteToMove #swap players
        #update the king's location if moved
        if move.pieceMoved == "wK":
            self.WhiteKingLocation = (move.endRaw, move.endCol)
        if move.pieceMoved == "bK":
            self.WhiteKingLocation = (move.endRaw, move.endCol)


    # undo the last move
    def undoMove(self):
        if len(self.moveLog) != 0:     #make sure that there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRaw][move.startCol] = move.pieceMoved
            self.board[move.endRaw][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove  #switch turns back
            #update the king's location if moved
            if move.pieceMoved == "wK":
                self.WhiteKingLocation = (move.startRaw, move.startCol)
            if move.pieceMoved == "bK":
                self.WhiteKingLocation = (move.startRaw, move.startCol)



    # all moves considering checks 
    def getValidMoves(self):
        #.1) generate all possible moves
        moves = self.getAllPossibleMoves()
        #.2) for each move, make the move
        for i in range(len(moves)-1,-1,-1):     
            #.3) generate all oppenment's moves
            self.makeMove(moves[i])
            #.4) for each oppenment's move, see if they attack ur king
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                #.5) if they attack ur king, not a valid move
                moves.remove(moves[i])              
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
 
        if len(moves) == 0:           #checkmate or stalemate
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False



        return moves
    

    #if the current player is in check
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.WhiteKingLocation[0], self.WhiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])
            


    # if the enemy can attack the square (r,c)
    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove #switch to the opponment's turn
        oppMoves = self.getAllPossibleMoves() 
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRaw == r and move.endCol == c:
                return True
        return False


    # all moves without considernig checks
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):          #number of raws
            for c in range(len(self.board[r])):   #number of cols
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    #tabazor
                    self.moveFunctions[piece](r, c, moves)
        return moves




    """ ------------------------------------------------------------------------------------------------------"""
    #####################               get all Pawn moves                        ########################
    """ ------------------------------------------------------------------------------------------------------"""
    
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:        #white pawn move 
            if self.board[r-1][c] == "--":     #1 square pawn advance
                moves.append(Move((r, c), (r-1, c), self.board))    
                if r == 6 and self.board[r-2][c] == "--":    #2 square pawn advance
                    moves.append(Move((r, c), (r-2, c), self.board))  

            # a black piece to capture
            if c-1 >= 0:   #takes to the left
                if self.board[r-1][c-1][0] == "b":     
                    moves.append(Move((r, c), (r-1, c-1), self.board))
            if c+1 <= 7:   #takes to the right
                if self.board[r-1][c+1][0] == "b":
                    moves.append(Move((r, c), (r-1, c+1), self.board))


        else :                      #black pawn move
            if self.board[r+1][c] == "--":
                moves.append(Move((r,c), (r+1, c), self.board)) 
                if r == 1 and self.board[r+2][c] == "--":
                    moves.append(Move((r, c), (r+2, c), self.board))
                
            # a white piece to capture
            if c-1 >= 0:   #takes to the left
                if self.board[r+1][c-1][0] == "w":     
                    moves.append(Move((r, c), (r+1, c-1), self.board))
            if c+1 <= 7:   #takes to the right
                if self.board[r+1][c+1][0] == "w":
                    moves.append(Move((r, c), (r+1, c+1), self.board))





    """ ------------------------------------------------------------------------------------------------------"""
    #####################               get all Rock moves                        ########################
    """ ------------------------------------------------------------------------------------------------------"""
    
    def getRockMoves(self, r, c, moves):
        directions = ( (-1,0), (0,-1), (1,0), (0,1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range (1,8):
                endRaw = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRaw < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRaw][endCol]
                    if endPiece == "--" or endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRaw, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRaw, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break





    """ ------------------------------------------------------------------------------------------------------"""
    #####################               get all Knight moves                        ########################
    """ ------------------------------------------------------------------------------------------------------"""
    
    def getKnightMoves(self, r, c, moves):
        knightMoves = ((-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRaw = r + m[0] 
            endCol = c + m[1]
            if 0 <= endRaw < 8 and 0 <= endCol < 8:
                Knight = self.board[endRaw][endCol]
                if Knight[0] != allyColor:
                    moves.append(Move((r,c), (endRaw, endCol), self.board))




    """ ------------------------------------------------------------------------------------------------------"""
    #####################               get all Bishp moves                        ########################
    """ ------------------------------------------------------------------------------------------------------"""
  
    def getBishopMoves(self, r, c, moves):
        directions = ((-1,-1), (-1,1), (1,-1), (1,1))
        enemyColor = "b" if self.whiteToMove else  "w"
        for d in directions:
            for i in range (1,8):
                endRaw = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRaw < 8 and 0 <= endCol < 8 :
                    endPiece = self.board[endRaw][endCol]
                    if endPiece == "--":
                        moves.append(Move((r,c), (endRaw, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r,c), (endRaw, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break





    """ ------------------------------------------------------------------------------------------------------"""
    #####################               get all King moves                        ########################
    """ ------------------------------------------------------------------------------------------------------"""
    
    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1,-1), (-1,0), (-1,1), (0,1), (1,1), (1,0), (1,-1), (0,-1))
        allyColor = "w" if self.whiteToMove else "b"
        for i in range (8):
            endRaw = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endCol < 8 and 0 <= endRaw < 8:
                endPiece = self.board[endRaw][endCol]
                if endPiece != allyColor:
                    moves.append(Move((r,c), (endRaw, endCol), self.board))
                    






    """ ------------------------------------------------------------------------------------------------------"""
    #####################               get all Queen moves                        ########################
    """ ------------------------------------------------------------------------------------------------------"""
    
    def getQueenMoves(self, r, c, moves):
        self.getRockMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)


class Move():

    # maps keys to values
    # key : value
    ranksToRaws = {"1": 7, "2": 6, "3": 5, "4": 4,
                  "5": 3, "6": 2, "7": 1, "8": 0}
    rawsToRanks = {v: k for k, v in ranksToRaws.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                  "e": 4, "f": 5, "g": 6, "h": 7} 
    colsToFiles = {v: k for k, v in filesToCols.items()}


    def __init__(self, startSq, endSq, board):
        self.startRaw = startSq[0]
        self.startCol = startSq[1]
        self.endRaw = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRaw][self.startCol]
        self.pieceCaptured = board[self.endRaw][self.endCol]
        self.moveID = self.startRaw * 1000 + self.startCol * 100 + self.endRaw * 10 + self.endCol
        #print (self.moveID)


    #overriding the equals methode
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False


    def getChessNotation(self):
        return self.getRankFile(self.startRaw, self.startCol) + self.getRankFile(self.endRaw, self.endCol)


    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rawsToRanks[r]