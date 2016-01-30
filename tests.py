import unittest

from board import Board


class TestBoard(unittest.TestCase):
    def test_sequences(self):
        board = Board.create_test_board()
        for line in board.get_sequences():
            print line

    def test_try_win(self):
        # finish him!
        board = Board.create_board()
        board.grid[0][0] = 1
        board.grid[0][1] = 1
        assert board.try_win()

        # can't win, no-op
        board = Board.create_board()
        board.grid[0][0] = 1
        board.grid[0][1] = 2
        assert not board.try_win()

        # can win, column
        board = Board.create_board()
        board.grid[0][0] = 1
        board.grid[2][0] = 1
        assert board.try_win()

        # can win, diag ltr
        board = Board.create_board()
        board.grid[0][0] = 1
        board.grid[2][2] = 1
        assert board.try_win()

        # can win, diag rtl
        board = Board.create_board()
        board.grid[2][2] = 1
        board.grid[1][1] = 1
        assert board.try_win()

    def try_move(self):
        # can win, diag rtl
        board = Board.create_board()
        board.grid[2][2] = 1
        board.grid[1][1] = 1
        assert board.move()

    def test_try_block(self):
        # can block
        board = Board.create_board()
        board.grid[0][0] = 2
        board.grid[0][1] = 2
        assert board.try_block()

        # can't block, no-op
        board = Board.create_board()
        board.grid[0][0] = 1
        board.grid[0][1] = 2
        assert not board.try_block()

    def test_cols(self):
        board = Board.create_test_board()
        assert board.get_cols() == [
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8)
        ]


if __name__ == '__main__':
    unittest.main()
