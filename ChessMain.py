# This class will handle user input and display current gamestate object

import pygame as p
import ChessEngine
import math

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

'''
Intitialize a global dictionary of images. This should only be called once to reduce lag.
'''


def loadImages():
    pieces = ["wR", "wN", "wB", "wQ", "wK", "wP",
              "bQ", "bK", "bB", "bN", "bR", "bP"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(
            'images/' + piece + '.png'), (SQ_SIZE, SQ_SIZE))


'''
Main driver for code. Will handle user input and graphics
'''


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False  # Flag variable for when a move is made
    loadImages()  # Only doing this once
    running = True
    sqSelected = ()
    # Keeps track of player clicks (two tuples: [(6, 4), (4, 4)])
    playerClicks = []
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # Mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  # (x, y) location of mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row, col):  # User clicks same square twice
                    sqSelected = ()  # Deselect
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)  # Append both clicks
                if len(playerClicks) == 2:  # Was that the second click?
                    move = ChessEngine.Move(
                        playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                        sqSelected = ()
                        playerClicks = []
                    else:
                        playerClicks = [sqSelected]
            # Key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # Undo when z is pressed
                    gs.undoMove()
                    moveMade = True
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


'''
Responsible for all graphics within current game state.
'''


def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)


'''
Draw the squares on the board.
'''


def drawBoard(screen):
    colors = [p.Color('white'), p.Color("gray")]

    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r+c) % 2]
            p.draw.rect(screen, color, (r * SQ_SIZE,
                        c * SQ_SIZE, SQ_SIZE, SQ_SIZE))


'''
Draw the pieces on the board using the current GameState.board
'''


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":  # Not empty square
                screen.blit(IMAGES[piece], p.Rect(
                    c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()
