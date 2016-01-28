#!/usr/bin/env python

'''
From Wikipedia: Tic-Tac-Toe
https://en.wikipedia.org/wiki/Tic-tac-toe

(hope this isn't cheating)

1. Win: If the player has two in a row, they can place a third to get three
   in a row.

2. Block: If the opponent has two in a row, the player must play the third
   themselves to block the opponent.

3. Fork: Create an opportunity where the player has two threats to win (two
   non-blocked lines of 2).

4. Blocking an opponent's fork:

    - Option 1: The player should create two in a row to force the opponent
      into defending, as long as it doesn't result in them creating a fork.
      For example, if "X" has a corner, "O" has the center, and "X" has the
      opposite corner as well, "O" must not play a corner in order to win.
      (Playing a corner in this scenario creates a fork for "X" to win.)

    - Option 2: If there is a configuration where the opponent can fork,
      the player should block that fork.

5. Center: A player marks the center. (If it is the first move of the game,
   playing on a corner gives "O" more opportunities to make a mistake and
   may therefore be the better choice; however, it makes no difference between
   perfect players.)

6. Opposite corner: If the opponent is in the corner, the player plays the
   opposite corner.

7. Empty corner: The player plays in a corner square.

8. Empty side: The player plays in a middle square on any of the 4 sides.

'''


class Board(object):
    @staticmethod
    def create_board():
        return  Board([[0] * 3 for x in xrange(3)])

    @staticmethod
    def create_test_board():
        cols = []
        for i in xrange(3):
            row = []
            for j in xrange(3):
                row.append(j + (i * 3))
            cols.append(row)
        return Board(cols)

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
        1. Win: If the player has two in a row, they can place a third to get three
        in a row.
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
        2. Block: If the opponent has two in a row, the player must play the third
        themselves to block the opponent.
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
        3. Fork: Create an opportunity where the player has two threats to win (two
        non-blocked lines of 2).
        '''
        threat_rows = []
        threat_col_nums = []
        for row in self.grid:
            if 1 in row and 2 not in row:
                threat_rows.append(row)
        for col_num, col in enumerate(self.get_cols()):
            if 1 in col and 2 not in col:
                threat_col_nums.append(col_num)
        if len(threat_rows) + len(threat_col_nums) >= 2:
            pass



if __name__ == '__main__':
    main()
