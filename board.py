#!/usr/bin/env python


class Board(object):
    """ Represents a stateless tic-tac-toe board. """

    def __init__(self, grid=None):
        if grid:
            self.grid = grid
        else:
            self.init_grid()

    def move(self):
        """
        Attempts to make a move by iterating through a list of rules.
        """
        rules = [
            self.try_win,
            self.try_block,
            self.try_fork,
            self.try_center,
            self.try_opposite_corner,
            self.try_corner,
            self.try_side,
            self.try_draw,
        ]
        for rule in rules:
            if rule():
                return
        # should never happen
        raise RuntimeError('No rules resulted in a move!')

    def get_cols(self):
        """ Returns a 3x3 list of cols X rows """
        return zip(*self.grid)

    def get_cells(self):
        """ Returns a flat list of cells for easy searching. """
        return sum(self.grid, [])

    def get_sequences(self):
        """
        Returns a tuple of (vals, ((x, y)*3)) for all valid sequences
        (left to right, top to bottom, diagonal ltr, diagonal rtl)

        Example:
        (
            [0, 0, 1][(0, 0), (0, 1), (0, 2)],
            [0, 0, 0][(1, 0), (1, 1), (1, 2)],
            [0, 0, 0][(2, 0), (2, 1), (2, 2)],
        )
        """
        # rows
        for row_num, row in enumerate(self.grid):
            yield (row, ((row_num, 0), (row_num, 1), (row_num, 2)))

        # columns
        for col_num, col in enumerate(self.get_cols()):
            yield (col, ((0, col_num), (1, col_num), (2, col_num)))

        # diag ltr
        yield ((self.grid[0][0], self.grid[1][1], self.grid[2][2]),
               ((0, 0), (1, 1), (2, 2)))

        # diag rtl
        yield ((self.grid[0][2], self.grid[1][1], self.grid[2][0]),
               ((0, 2), (1, 1), (2, 0)))

    def get_status(self):
        """
        Returns a string representing the status of the game, from the
        opponent's point of view.
        """
        for sequence in self.get_sequences():
            vals, coords = sequence
            svals = list(set(vals))
            if len(svals) == 1:
                if svals[0] == 1:
                    return 'Lose'
                if svals[0] == 2:
                    return 'Win'
        if 0 not in self.get_cells():
            return 'Draw'
        return 'Playing'

    def try_win(self):
        """
        Win: If the player has two in a row, they can place a third to get
        three in a row.
        """
        for sequence in self.get_sequences():
            vals, coords = sequence
            if 2 not in vals and vals.count(1) == 2:
                x, y = coords[vals.index(0)]
                self.grid[x][y] = 1
                return True

    def try_block(self):
        """
        Block: If the opponent has two in a row, the player must play the
        third themselves to block the opponent.
        """
        for sequence in self.get_sequences():
            vals, coords = sequence
            if 1 not in vals and vals.count(2) == 2:
                x, y = coords[vals.index(0)]
                self.grid[x][y] = 1
                return True

    def try_fork(self):
        """
        Fork: Create an opportunity where the player has two threats to win
        (two non-blocked lines of 2).
        """
        threat_seqs = []
        for sequence in self.get_sequences():
            vals, coords = sequence
            if 1 in vals and 2 not in vals:
                threat_seqs.append(sequence)
        if len(threat_seqs) > 1:
            vals, coords = threat_seqs[0]
            x, y = coords[vals.index(0)]
            self.grid[x][y] = 1
            return True

    def try_center(self):
        """
        Center: A player marks the center.
        """
        if self.grid[1][1] == 0:
            self.grid[1][1] = 1
            return True

    def try_opposite_corner(self):
        """
        Opposite corner: If the opponent is in the corner, the player plays
        the opposite corner.
        """
        if self.grid[0][0] == 2 and self.grid[2][2] == 0:
            self.grid[2][2] = 1
            return True
        if self.grid[0][2] == 2 and self.grid[2][0] == 0:
            self.grid[2][0] = 1
            return True
        if self.grid[2][0] == 2 and self.grid[0][2] == 0:
            self.grid[0][2] = 1
            return True
        if self.grid[2][2] == 2 and self.grid[0][0] == 0:
            self.grid[0][2] = 1
            return True

    def try_corner(self):
        """
        Empty corner: The player plays in a corner square.
        """
        coords = ((0, 0), (0, 2), (2, 0), (2, 2))
        for corner in coords:
            x, y = corner
            if self.grid[x][y] == 0:
                self.grid[x][y] = 1
                return True

    def try_side(self):
        """
        Empty side: The player plays in a middle square on any of the 4
        sides.
        """
        coords = ((0, 1), (1, 2), (2, 1), (1, 1))
        for side in coords:
            x, y = side
            if self.grid[x][y] == 0:
                self.grid[x][y] = 1
                return True

    def try_draw(self):
        if 0 not in self.get_cells():
            # game is a draw, fail silently
            return True

    def init_grid(self):
        self.grid = [[0] * 3 for _ in xrange(3)]

    @staticmethod
    def create_board():
        """ Creates an empty board. """
        return Board([[0] * 3 for _ in xrange(3)])

    def __repr__(self):
        ret = ""
        for row in self.grid:
            col_str = ""
            for col in row:
                col_str += '{} '.format(col)
            ret += '{}\n'.format(col_str)
        return ret

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
