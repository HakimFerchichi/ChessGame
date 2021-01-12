"""
this is our main driver. It will be responsable for handling user inpur and displaying the current GameState object
"""

import pygame as p
import ChessEngine


# 512 is an option
WIDTH =  HIGHT = 480
SQ_SIZE = 60

DIMENSION = 8               #dimension 8x8 
MAX_FPS = 15      
IMAGES = {}

"""
initialize a global dictionary of images. This will be called once exactly in the main  
"""

def loadImages():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bP", "wR", "wN", "wB", "wQ", "wK","wP"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale (p.image.load("packages/images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


"""
The main driver for our code. This will handle user input and updating the graphics
"""

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #flag variable for when a move is made
    print(gs.board)
    loadImages()                #only called once before the while loop
    running = True
    sqSelected = ()     # no square is selected, keep track of the last click of the user (tuple : (raw, col))
    playerClicks = []  #keep track of player clicks ( tow tuples: [(6, 4), (4, 4)]  )
    
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
                print('game is closed')
            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()         # location = (x,y)
                col = location[0]//SQ_SIZE
                raw = location[1]//SQ_SIZE
                if sqSelected  == (raw, col): #the user clicks in the same square twice
                    sqSelected = ()     #deselected
                    playerClicks = []   #clear playerClicks
                else:
                    sqSelected = (raw, col)
                    playerClicks.append(sqSelected)  #append for both 1st and 2nd click
                #was the user 2nd click?
                if len(playerClicks) > 1:      # after 2nd click
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                        sqSelected = () #reset user clicks
                        playerClicks = []
                    else:
                        sqSelected = ()
                        playerClicks = []
                         
            # key handlers
            elif e.type == p.KEYDOWN:
                if e.key != p.K_z:         # undo when z is pressed
                    gs.undoMove()
                    print("undo move")
                    moveMade = True


        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
                
        drawGameState(screen, gs)
        clock.tick (MAX_FPS)
        p.display.flip()

"""
Responsable of all graphics options
"""
def drawGameState(screen, gs):
    drawBoard(screen)                #draw squares in the board
    drawPieces(screen, gs.board)     #draw pieces on top of this squares   


# Draw the squares on the board 
def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range (DIMENSION):
        for c in range (DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect (screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))




# Draw the pieces on the board
def drawPieces(screen, board):
    for r in range (DIMENSION):
        for c in range (DIMENSION):
            piece = board[r][c]
            if piece != "--":                  # not empty
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
             






if __name__ == "__main__":
    main()
