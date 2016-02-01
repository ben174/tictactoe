class Board(object):
    """ Represents a stateless tic-tac-toe board. """

    def __init__(self, grid=None):
        if grid:
            self.grid = grid
        else:
            self.grid = [[0] * 3 for _ in xrange(3)]

    def move(self):
        """
        Attempts to make a move by iterating through a list of rules.
        """
        rules = [
            self.try_win,
            self.try_block,
            self.try_fork,
            self.try_block_fork,
            self.try_center,
            self.try_opposite_corner,
            self.try_corner,
            self.try_side,
            self.try_draw,
        ]
        for rule in rules:
            if rule():
                print "Hit rule: " + rule.__name__
                return
        # should never happen
        raise RuntimeError('No rules resulted in a move!')

    def get_cols(self):
        """ Returns a 3x3 list of cols X rows """
        return zip(*self.grid)

    def get_cells(self):
        """ Returns a flat list of cells for easy searching. """
        return sum(self.grid, [])

    def get_sequences(self, omit_cols=False):
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

        if not omit_cols:
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
        forks = self.locate_fork(1)
        if forks:
            fork = forks[0]
            self.grid[fork[0]][fork[1]] = 1
            return True

    def try_block_fork(self):
        """
        Block Opponent's Fork:

        Option 1: Create two in a row to force the opponent into defending, as
        long as it doesn't result in them creating a fork or winning. For
        example, if "X" has a corner, "O" has the center, and "X" has the opposite
        corner as well, "O" must not play a corner in order to win. (Playing a
        corner in this scenario creates a fork for "X" to win.)

        Option 2: If there is a configuration where the opponent can fork, block
        that fork.
        """
        forks = self.locate_fork(2)
        if forks:
            for sequence in self.get_sequences(omit_cols=True):
                vals, coords = sequence
                if vals.count(0) == 2 and 1 in vals:
                    my_spot = vals.index(1)
                    neighbor_coords = coords[1 if my_spot == 2 else my_spot + 1]
                    self.grid[neighbor_coords[0]][neighbor_coords[1]] = 1
                    return True

    def locate_fork(self, player):
        """ Looks through the board, finding fork opportunities. """
        trouble = []
        for sequence in self.get_sequences(omit_cols=(player==1)):
            vals, coords = sequence
            if vals.count(0) == 2 and player in vals:
                my_spot = vals.index(player)
                new_threats = [c for i, c in enumerate(coords) if i != my_spot]
                trouble.extend(new_threats)
        return [x for x in trouble if trouble.count(x) > 1]

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
        cells = self.get_cells()
        if 0 not in self.get_cells():
            # game is a draw, fail silently
            return True
        elif cells.count(0) == 1:
            # fill the final cell, resulting in a draw
            for sequence in self.get_sequences():
                vals, coords = sequence
                if 0 in vals:
                    x, y = coords[vals.index(0)]
                    self.grid[x][y] = 1
                    return True

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

    def __repr__(self):
        ret = ""
        for row in self.grid:
            col_str = ""
            for col in row:
                col_str += '{} '.format(col)
            ret += '{}\n'.format(col_str)
            ret.replace('1', 'O')
            ret.replace('2', 'X')
            ret.replace('0', ' ')
        return ret
