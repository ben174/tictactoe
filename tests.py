import unittest

from board import Board


class TestBoard(unittest.TestCase):
    def test_sequences(self):
        print 'Test Sequences'
        board = Board.create_test_board()
        for line in board.get_sequences():
            print line


    def test_try_win(self):
        # finish him!
        board = Board.create_board()
        board.grid[0][0] = 1
        board.grid[0][1] = 1
        print 'before:'
        print board
        assert board.try_win()
        print 'after:'
        print board

        # can't win, no-op
        board = Board.create_board()
        board.grid[0][0] = 1
        board.grid[0][1] = 2
        print 'before:'
        print board
        assert not board.try_win()
        print 'after:'
        print board

        # can win, column
        board = Board.create_board()
        board.grid[0][0] = 1
        board.grid[2][0] = 1
        print 'before:'
        print board
        assert board.try_win()
        print 'after:'
        print board

        # can win, diag ltr
        board = Board.create_board()
        board.grid[0][0] = 1
        board.grid[2][2] = 1
        print 'before:'
        print board
        assert board.try_win()
        print 'after:'
        print board

        # can win, diag rtl
        board = Board.create_board()
        board.grid[2][2] = 1
        board.grid[1][1] = 1
        print 'before:'
        print board
        assert board.try_win()
        print 'after:'
        print board


    def try_move(self):
        print 'Move try'
        # can win, diag rtl
        board = Board.create_board()
        board.grid[2][2] = 1
        board.grid[1][1] = 1
        print 'before:'
        print board
        assert board.move()
        print 'after:'
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
