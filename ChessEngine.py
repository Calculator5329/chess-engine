# This class stores information about the current state of the game
# It will also determine the valid moves at the current state and keep a move log

class GameState():
    def __init__(self):
        # Board will be a 2d list, each element has 2 chars.
        # First is color of piece, second is type of piece (ex: "bB" is black bishop)
        # "--" Represents empty space
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "bP", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.moveFunctions = {'P': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}

        self.whiteToMove = True
        self.moveLog = []

    '''
    Takes a move as a parameter and executes it. Will not work for castling, en passant, or promotions.
    '''

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  # Log move for later
        self.whiteToMove = not self.whiteToMove

    '''
    Undo the last move made
    '''

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove  # Switch turn back

    '''
    All moves considering checks
    '''

    def getValidMoves(self):
        return self.getAllPossibleMoves()

    '''
    All moves without considering checks
    '''

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)
        return moves

    '''
    Get all pawn moves for the piece located at r, c, and add these moves to the list
    '''

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
            if self.board[r-1][c] == "--":
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--":  # 2 square advance
                    moves.append(Move((r, c), (r-2, c), self.board))
            if c-1 >= 0:
                if self.board[r-1][c-1][0] == 'b':  # Enemy piece to capture
                    moves.append(Move((r, c), (r-1, c-1), self.board))
            if c+1 <= 7:
                if self.board[r-1][c+1][0] == 'b':  # Enemy piece to capture
                    moves.append(Move((r, c), (r-1, c+1), self.board))
        else:  # Black pawn moves
            if self.board[r+1][c] == "--":
                moves.append(Move((r, c), (r+1, c), self.board))
                if r == 1 and self.board[r+2][c] == "--":  # 2 square advance
                    moves.append(Move((r, c), (r+2, c), self.board))
            if c-1 >= 0:
                if self.board[r+1][c-1][0] == 'w':  # Enemy piece to capture
                    moves.append(Move((r, c), (r+1, c-1), self.board))
            if c+1 <= 7:
                if self.board[r+1][c+1][0] == 'w':  # Enemy piece to capture
                    moves.append(Move((r, c), (r+1, c+1), self.board))

    '''
    Get all rook moves for the piece located at r, c, and add these moves to the list
    '''

    def getRookMoves(self, r, c, moves):
        # Up, Down, Left, Right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        enemy_color = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8):  # Can move max 7 spaces in any direction
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:  # On board
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":  # Empty space
                        moves.append(
                            Move((r, c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:  # Enemy piece
                        moves.append(
                            Move((r, c), (end_row, end_col), self.board))
                        break  # Can't move past enemy piece
                    else:  # Friendly piece
                        break  # Can't move past friendly piece
                else:  # Off board
                    break

    '''
    Get all bishop moves for the piece located at r, c, and add these moves to the list
    '''

    def getBishopMoves(self, r, c, moves):
        # Up, Down, Left, Right
        directions = [(-1, -1), (1, 1), (1, -1), (-1, 1)]
        enemy_color = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8):  # Can move max 7 spaces in any direction
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:  # On board
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":  # Empty space
                        moves.append(
                            Move((r, c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:  # Enemy piece
                        moves.append(
                            Move((r, c), (end_row, end_col), self.board))
                        break  # Can't move past enemy piece
                    else:  # Friendly piece
                        break  # Can't move past friendly piece
                else:  # Off board
                    break

    '''
    Get all knight moves for the piece located at r, c, and add these moves to the list
    '''

    def getKnightMoves(self, r, c, moves):
        knight_directions = [(-2, 1), (-2, -1), (2, 1), (2, -1),
                             (-1, 2), (-1, -2), (1, 2), (1, -2)]
        ally_color = 'w' if self.whiteToMove else 'b'
        for d in knight_directions:
            end_row = r + d[0]
            end_col = c + d[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:  # On board
                end_piece = self.board[end_row][end_col]
                # Not an ally piece (empty or enemy)
                if end_piece[0] != ally_color:
                    moves.append(Move((r, c), (end_row, end_col), self.board))

    '''
    Get all queen moves for the piece located at r, c, and add these moves to the list
    '''

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    '''
    Get all king moves for the pawn located at r, c, and add these moves to the list
    '''

    def getKingMoves(self, r, c, moves):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                      (-1, -1), (1, 1), (1, -1), (-1, 1)]
        ally_color = 'w' if self.whiteToMove else 'b'
        for d in directions:
            end_row = r + d[0]
            end_col = c + d[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:  # On board
                end_piece = self.board[end_row][end_col]
                # Not an ally piece (empty or enemy)
                if end_piece[0] != ally_color:
                    moves.append(Move((r, c), (end_row, end_col), self.board))


class Move():

    # Map keys to values
    # key : value
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + \
            self.endRow * 10 + self.endCol  # Unique move id from 0000 - > 7777

    '''
    Overriding the equals method
    '''

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
