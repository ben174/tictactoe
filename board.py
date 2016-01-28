#!/usr/bin/env python

class Board(object):
    """ Represents a stateless tic-tac-toe board. """

    def __init__(self, grid=None):
        if grid:
            self.grid = grid
        else:
            self.grid = Board.create_grid()

    def get_cols(self):
        """ Returns a 3x3 list of cols x rows """
        return zip(*self.grid)

    def get_diags(self):
        """ Returns a tuple of diagonal (left-to-right, right-to-left) """
        ret = []
        ltr = []
        rtl = []
        for i in xrange(3):
            ltr.append(self.grid[i][i])
            rtl.append(self.grid[i][-(i+1)])
        return (ltr, rtl)

    def get_sequences(self):
        """
        Returns a tuple of ((x, y), value) for all valid sequences
        (left to right, top to bottom, diagonal ltr, diagonal rtl)
        """
        # rows
        for row_num, row in enumerate(self.grid):
            yield [((i, row_num), cell) for i, cell in enumerate(row)]
        # cols
        for col_num, col in enumerate(self.get_cols()):
            yield [((col_num, i), cell) for i, cell in enumerate(col)]
        # diags
        yield (
            ((0, 0), self.grid[0][0]),
            ((1, 1), self.grid[1][1]),
            ((2, 2), self.grid[2][2]),
        )
        yield (
            ((0, 2), self.grid[0][2]),
            ((1, 1), self.grid[1][1]),
            ((2, 0), self.grid[2][0]),
        )

    def __repr__(self):
        ret = ""
        for row in self.grid:
            col_str = ""
            for col in row:
                col_str += '{} '.format(col)
            ret += '{}\n'.format(col_str)
        return ret

    def try_win(self):
        '''
        1. Win: If the player has two in a row, they can place a third to get
        three in a row.
        '''
        for row in self.grid:
            if 2 not in row and row.count(1) == 2:
                row[row.index(0)] = 1
                return True
        for col_num, col in enumerate(self.get_cols()):
            if 2 not in col and col.count(1) == 2:
                row_num = col.index(0)
                self.grid[row_num][col_num] = 1
                return True
        #TODO diag

    def try_block(self):
        '''
        2. Block: If the opponent has two in a row, the player must play the
        third themselves to block the opponent.
        '''
        for row in self.grid:
            if 1 not in row and row.count(2) == 2:
                row[row.index(0)] = 1
                return True
        for col_num, col in enumerate(self.get_cols()):
            if 1 not in col and col.count(2) == 2:
                row_num = col.index(0)
                self.grid[row_num][col_num] = 1
                return True
        #for diag in _get_diags(grid):
        #TODO diag

    def try_fork(self):
        '''
        3. Fork: Create an opportunity where the player has two threats to win
        (two non-blocked lines of 2).
        '''
        threat_rows = []
        threat_col_nums = []
        cols = self.get_cols()
        for row in self.grid:
            if 1 in row and 2 not in row:
                threat_rows.append(row)
        for col_num, col in enumerate(cols):
            if 1 in col and 2 not in col:
                threat_col_nums.append(col_num)
        if len(threat_rows) + len(threat_col_nums) >= 2:
            if threat_rows:
                row = threat_rows[0]
                row[row.index(0)] = 1


            pass

    @staticmethod
    def create_board():
        """ Creates an empty board. """
        return  Board([[0] * 3 for x in xrange(3)])

    @staticmethod
    def create_test_board():
        """ Creates an empty board, enumerated with unique numbers. """
        cols = []
        for i in xrange(3):
            row = []
            for j in xrange(3):
                row.append(j + (i * 3))
            cols.append(row)
        return Board(cols)

if __name__ == '__main__':
    main()
