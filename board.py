import copy
import logging


class Board(object):
    """ Represents a stateless tic-tac-toe board. """

    def __init__(self, grid=None):
        if grid:
            self.grid = grid
        else:
            self.grid = self.get_blank_grid()

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
        fork_seqs = []
        has_threat = False
        for sequence in self.get_sequences():
            vals, coords = sequence
            if 2 not in vals:
                if vals.count(1) == 1:
                    fork_seqs.append(sequence)
                elif vals.count(1) > 1:
                    has_threat = True
        if has_threat and fork_seqs:
            vals, coords = fork_seqs[0]
            x, y = coords[vals.index(0)]
            self.grid[x][y] = 1
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
        for sequence in self.get_sequences():
            vals, coords = sequence
            # Create two in a row to force the opponent into defending...
            for index, val in enumerate(vals):
                if val == 0:
                    test_board = Board()
                    test_board.grid = copy.deepcopy(self.grid)
                    x, y = coords[index]
                    test_board.grid[x][y] = 1
                    # ...as long as it doesn't result in them creating a fork or winning.
                    if not test_board.opponent_can_fork():
                        # if "X" has a corner, "O" has the center,
                        # and "X" has the opposite corner as well,
                        # "O" must not play a corner in order to win.
                        # if self.grid[1][1] == 2:
                        #     # put it somewhere where it blocks two possibilites
                        #     pass
                        # if (self.grid[0][0] == 2 and self.grid[2][2] == 2) or \
                        #     (self.grid[0][2] == 2 and self.grid[2][0] == 2):
                        #        print 'DANGER ZONE!!!!!!'
                        #        if x == 1 or y == 1 or (x == 1 and x == 1):
                        #            self.grid[x][y] = 1
                        #            return True
                        self.grid[x][y] = 1
                        return True
            #raise RuntimeError("I'm doomed. Player can fork")

    def opponent_can_fork(self):
        """
        Determines if the grid is a situation in which a fork can be generated.
        """
        trouble_count = 0
        for sequence in self.get_sequences():
            vals, coords = sequence
            if vals.count(1) == 0 and vals.count(2) > 0:
                trouble_count += 1
        print 'Opp can fork: ' + str(vals) + ' ' + str(coords)
        if self.grid[2][0] == 1:
            print 'This should work!'
            print self.__repr__()
        print 'Trouble count: ' + str(trouble_count)
        print self.__repr__()
        if self.try_win():
            print 'Lots of trouble but i can win in one move, look above'
            print self.__repr__()
            # top-left middle-right bottom-middle is still broken
            # UNLESS it's corner corner center
            if (self.grid[0][0] == 2 and self.grid[2][2] == 2) or \
                 (self.grid[0][2] == 2 and self.grid[2][0] == 2):
                if (self.grid[0][0] == 1 or self.grid[2][2] == 1 or \
                        self.grid[0][2] == 1 and self.grid[2][0] == 1):
                    if self.grid[1][1] == 1:
                        print 'NOPE this is that one crazy case'
                        return True
            return False
        return trouble_count >= 2


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

    def get_blank_grid(self):
        return [[0] * 3 for _ in xrange(3)]

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

