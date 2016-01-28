import unittest

from board import Board

class TestBoard(unittest.TestCase):
    def test_diags(self):
        board = Board.create_test_board()
        diags = Board.get_diags(board)
        # left to right
        assert diags[0] == [0, 4, 8]
        # right to left
        assert diags[1] == [2, 4, 6]


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
        print board
        assert board.try_win()
        print board


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
