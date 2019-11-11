# Chessboard Game

Now we have a board game in which a white piece and a black piece are placed on a `n × n (2 ≤ n ≤ 20) `board. Player A and player B take turns moving the piece with the rules as follow and player A goes first:

-	Rule for player A: A can only move the white piece into the next grid in the up, down, left, right, four directions.
-	Rule for player B: B can only move the black piece into the next first or
second grid in the up, down, left, right, four directions.

To win the game, the player have to move his piece into the grid where the other piece stand to eat it. Both of the two players are clever so that they will do their best to win the game with the least steps or try to delay the end of the game when he is doomed to loose.

For example, `n = 2`, the white piece is located in `(1,1)`, while the black piece in `(2,2)`. Despite of two different ways that A could choose, B will win the game in the 2nd round.

## Usage

Just run the command in this folder and enter `n r1 c1 r2 c2`.
```bash
$ python3 chessboard.py
```

## Result

For example, `n = 8` and the initial coordinates are `(1, 1)` `(8, 8)`:

```bash
Please input n r1 c1 r2 c2:
8 1 1 8 8
Round 00: (1, 1) (8, 8)
Round 01: (2, 1) (8, 8)
Round 02: (2, 1) (6, 8)
Round 03: (1, 1) (6, 8)
Round 04: (1, 1) (4, 8)
Round 05: (2, 1) (4, 8)
Round 06: (2, 1) (4, 6)
Round 07: (3, 1) (4, 6)
Round 08: (3, 1) (4, 5)
Round 09: (4, 1) (4, 5)
Round 10: (4, 1) (4, 4)
Round 11: (5, 1) (4, 4)
Round 12: (5, 1) (4, 2)
Round 13: (6, 1) (4, 2)
Round 14: (6, 1) (5, 2)
Round 15: (7, 1) (5, 2)
Round 16: (7, 1) (6, 2)
Round 17: (8, 1) (6, 2)
Round 18: (8, 1) (7, 2)
Round 19: (7, 1) (7, 2)
BLACK 20
```

As for this program's efficiency, it can find the result **almost instantly** when `n <= 12` and it takes **about 20 seconds** to compute when `n = 20` (on my computer).

```bash
$ time python chessboard.py
Please input n r1 c1 r2 c2:
20 1 1 20 20
Round 00: (1, 1) (20, 20)
Round 01: (2, 1) (20, 20)
# some output is omitted
Round 55: (19, 1) (19, 2)
BLACK 56

real    0m21.051s
user    0m0.000s
sys     0m0.015s
```
