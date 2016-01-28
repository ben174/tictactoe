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
