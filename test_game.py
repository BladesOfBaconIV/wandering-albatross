
import unittest

from game import Game, Piece

class TestGame(unittest.TestCase):

    def setUp(self):
        self.game = Game()

    def test_make_move(self):
        self.game.make_move(1, Piece.RED)
        self.assertEqual(self.game.board[-1][0], Piece.RED, f"Piece not played correctly\n{self.game}")
        self.game.make_move(1, Piece.YELLOW)
        self.assertEqual(self.game.board[-2][0], Piece.YELLOW, f"Pieces not stacking\n{self.game}")

    def test_invalid_move(self):
        self._make_moves(1, 1, 1, 1, 1)  # fill first column
        self.assertFalse(
            self.game.is_move_valid(1), 
            f"Should not be able to place piece in full column\n{self.game}"
        )

    def test_board_full(self):
        self.assertFalse(self.game.is_full(), f"New board is not full\n{self.game}")
        self._make_moves(*[r for r in range(1, 10) for _ in range(5)])  # fill board
        self.assertTrue(self.game.is_full(), f"Board is full\n{self.game}")

    def test_row_wins(self):
        self._make_moves(4, 5, 6, 7, 8)
        self.assertEqual(
            self.game.is_won(), Piece.RED,
            f"Red has connect 5 in a row\n{self.game}"
        )

    def test_column_wins(self):
        self._make_moves(2, 2, 2, 2, 2, piece=Piece.YELLOW)
        self.assertEqual(
            self.game.is_won(), Piece.YELLOW,
            f"Yellow has connected 5 in a column\n{self.game}"
        )

    def test_diagonal_wins(self):
        self._make_moves(3, 4, 5, 6)
        self._make_moves(4, 5, 6)
        self._make_moves(5, 6)
        self._make_moves(6)
        self.assertEqual(self.game.is_won(), Piece.EMPTY, f"No one has won yet\n{self.game}")
        self._make_moves(2, 3, 4, 5, 6, piece=Piece.YELLOW)
        self.assertEqual(self.game.is_won(), Piece.YELLOW, f"Yellow has won on the diagonal\n{self.game}")

    def _make_moves(self, *moves, piece=Piece.RED):
        """
        Make a list of moves in the current game (all with the same piece)
        """
        for move in moves:
            self.game.make_move(move, piece)


if __name__ == "__main__":
    unittest.main()