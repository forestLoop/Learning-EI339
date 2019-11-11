# Triangle War

> More detailed description: [Triangle War on POJ](http://poj.org/problem?id=1085)

Two players, A and B, take turns filling in any dotted line connecting two dots, with A starting first. Once a line is filled, it cannot be filled again. If the line filled by a player completes one or more triangles, she owns the completed triangles and she is awarded another turn (i.e. the opponent skips a turn). The game ends after all dotted lines are filled in, and the player with the most triangles wins the game. The difference in the number of triangles owned by the two players is not important. 

## Usage

Just run the command in this folder and enter `n` and then `n` existing edges  .
```bash
$ python3 triangle_war.py
```

## Result

Here are some samples:

```bash
$ python3 triangle_war.py
number of existing edges:6
2 4
4 5
5 9
3 6
2 5
3 5
B wins.
number of existing edges:7
2 4
4 5
5 9
3 6
2 5
3 5
7 8
A wins.
```

Note that the larger `n` is, the smaller the total search space is and hence the less time it takes to compute. For example, when `n = 1`, it may take quite a long time to compute:

```bash
$ time python triangle_war.py
number of existing edges:1
1 2
B wins.

real    0m9.638s
user    0m0.000s
sys     0m0.031s
```

