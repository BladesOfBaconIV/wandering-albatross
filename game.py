
import itertools

from enum import Enum

class Piece(str, Enum):
    EMPTY = " "
    RED = "x"
    YELLOW = "o"

class Game:

    ROWS, COLS = 5, 9

    def __init__(self) -> None:
        self.board = [[Piece.EMPTY for _ in range(self.COLS)] for _ in range(self.ROWS)]

    def make_move(self, col: int, piece: Piece) -> None:
        """
        Make a move on the board, assumes move is valid before trying to make it
        
        :param col: col to place the piece in
        :param piece: piece to play
        """
        col -= 1  # Convert to 0 indexing
        for row in self.board[::-1]:  # reverse rows as they are stored top -> bottom
            if row[col] is Piece.EMPTY:
                row[col] = piece
                return 
        
    def is_won(self) -> Piece:
        """
        Check if the game is won, returning the colour of the winner (or EMPTY if there is no winner)
        """
        # check columns
        print("--------------")
        for col in range(self.COLS):
            pieces_in_column = set(row[col] for row in self.board)
            if len(pieces_in_column) == 1 and Piece.EMPTY not in pieces_in_column:
                return pieces_in_column.pop()
        # check rows
        for row in self.board:
            groups = [(piece, len(list(group))) for piece, group in itertools.groupby(row)]
            longest_group = max(groups, key=lambda x: x[1])   # get the longest group sorted by len
            if longest_group[0] is not Piece.EMPTY and longest_group[1] == 5:
                return longest_group[0]
        # check forward (/) diagonals
        for col in range(self.COLS - 4):   # can't be less than 4 from right edge
            diagonal = set(self.board[offset][col + offset] for offset in range(self.ROWS))  # start on [row=0][col] go to [row=4][col+4]
            if len(diagonal) == 1 and Piece.EMPTY not in diagonal:
                return diagonal.pop()
        # check backwards (\) diagonals
        for col in range(4, self.COLS):   # must be at least 4 from left edge
            diagonal = set(self.board[offset][col - offset] for offset in range(self.ROWS))  # start on [row=0][col] go to [row=4][col-4]
            if len(diagonal) == 1 and Piece.EMPTY not in diagonal:
                return diagonal.pop()
        # if no winner return EMPTY
        return Piece.EMPTY

    def is_full(self) -> bool:
        """
        Return if the board is full
        """
        return not any(piece == Piece.EMPTY for row in self.board for piece in row )

    def is_move_valid(self, col: int) -> bool:
        """
        Return if a move is valid, i.e. any row in that column is empty

        :param col: col to try place piece in
        """
        col -= 1  # Change to 0 indexing
        return any(row[col] is Piece.EMPTY for row in self.board)

    def __str__(self) -> str:
        return "\n".join(" ".join(f"[{p}]" for p in row) for row in self.board)
