import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpathes
from queue import PriorityQueue


class MazeProblem:

    def __init__(self, maze_file=''):
        self.init_map = self.loadMap(maze_file)
        self.map = self.init_map.copy()
        self.m, self.n = self.map.shape
        self.algorithms = {
            "bfs": self.__BFS,
            "a star": self.__A_star,
            "a*": self.__A_star,
        }
        self.min_dist = float("inf")

    def loadMap(self, file):
        # Load map txt as matrix.
        # 0: path, 1: obstacle, 2: start point, 3: end point
        # 9: solution
        f = open(file)
        lines = f.readlines()
        numOfLines = len(lines)
        returnMap = np.zeros((numOfLines, 40))
        A_row = 0
        for line in lines:
            list = line.strip().split(' ')
            returnMap[A_row:] = list[0:40]
            A_row += 1
        print(np.shape(returnMap))
        return returnMap

    def drawMap(self, title="Maze"):
        # Visulize the maze map.
        # Draw obstacles(1) as red rectangles. Draw path(0) as white rectangles. Draw starting point(2) and ending point(3) as circles.
        # Draw solution(9) as blue rectangles.
        rowNum = len(self.map)
        print(rowNum)
        colNum = len(self.map[0])
        print(colNum)
        ax = plt.subplot()
        param = 1
        for col in range(colNum):
            for row in range(rowNum):
                if self.map[row, col] == 2:
                    circle = mpathes.Circle([param * col + param/2.0, param * row + param/2.0], param/2.0, color='g')
                    ax.add_patch(circle)
                elif self.map[row, col] == 3:
                    circle = mpathes.Circle([param * col + param/2.0, param * row + param/2.0], param/2.0, color='y')
                    ax.add_patch(circle)
                elif self.map[row, col] == 1:
                    rect = mpathes.Rectangle([param * col, param * row], param, param, color='r')
                    ax.add_patch(rect)
                elif self.map[row, col] == 9:   # color the solution path blue
                    rect = mpathes.Rectangle([param * col, param * row], param, param, color='b')
                    ax.add_patch(rect)
                else:
                    rect = mpathes.Rectangle([param * col, param * row], param, param, color='w')
                    ax.add_patch(rect)
        # Improve visualization
        plt.xlim((0, colNum))
        plt.ylim((0, rowNum))
        my_x_ticks = np.arange(0, colNum+1, 1)
        my_y_ticks = np.arange(0, rowNum+1, 1)
        plt.xticks(my_x_ticks)
        plt.yticks(my_y_ticks)
        axx = plt.gca()
        axx.xaxis.set_ticks_position('top')
        axx.invert_yaxis()
        plt.grid()
        plt.suptitle(title + " (distance: {})".format(self.min_dist), fontsize=20)
        # Save maze image.
        # plt.show()
        plt.savefig("./maze_{}.png".format(title))

    def __next_grid(self, s):
        # Return all possible new states for state s in a generator style
        x, y = s
        if x != 0 and self.map[x - 1, y] != 1:
            yield (x - 1, y)
        if x != self.m - 1 and self.map[x + 1, y] != 1:
            yield (x + 1, y)
        if y != 0 and self.map[x, y - 1] != 1:
            yield (x, y - 1)
        if y != self.n - 1 and self.map[x, y + 1] != 1:
            yield (x, y + 1)

    def __is_end(self, s):
        # Return True iff s is an ending state
        return s == (self.m - 1, self.n - 1)

    def __trace_back(self, dest, history):
        # Track back to find the path from the starting state to `dest`
        # history[x] is the state previous to x
        while history[dest] and history[history[dest]]:
            dest = history[dest]
            self.map[dest] = 9

    def __BFS(self):
        # Use BFS to find the shortest path in the maze self.map
        # If such path exists, color the path in the maze and return the distance
        # If not, return None
        layer = [(0, 0)]  # all states in the same layer, with a distance of `dist` from the starting state
        parent = {(0, 0): None}  # x is visited iff x is in parent, and also, parent[x] is the parent of x in the optimal path
        dist = 0
        while layer:
            next_layer = []
            for grid in layer:
                if self.__is_end(grid):
                    self.__trace_back(grid, parent)  # trace back to find the optimal path
                    assert(dist <= self.min_dist)  # sanity check: new distance must be lower than the previous one
                    self.min_dist = dist
                    return dist
                for new_grid in self.__next_grid(grid):
                    if new_grid in parent.keys():   # if visited
                        continue
                    parent[new_grid] = grid
                    next_layer.append(new_grid)
            # move to the next layer
            dist += 1
            layer = next_layer
        # if no solution found
        return None

    def __future_cost(self, s):
        # Return the heuristic future cost of state s (the L1 distiance from the destination)
        return abs(s[0] - self.m + 1) + abs(s[1] - self.n + 1)

    def __A_star(self):
        # Use A* Algorithm to find the shortest path in the maze self.map
        # If such path exists, color the path in the maze and return the distance
        # If not, return None
        parent = {(0, 0): None}  # parent[x] is the state previous to x in the optimal path
        cost = {(0, 0): 0}  # cost[x] is the minimum cost to reach x
        frontier = PriorityQueue()
        frontier.put((0, (0, 0)))   # (priority, state)
        while frontier:
            current_priority, current = frontier.get()
            if self.__is_end(current):  # if reaching the ending state
                self.__trace_back(current, parent)  # trace back to find the optimal path
                assert(cost[current] <= self.min_dist)  # sanity check: new distance must be lower than the previous one
                self.min_dist = cost[current]
                return cost[current]
            for next_grid in self.__next_grid(current):
                new_cost = cost[current] + 1
                if next_grid not in cost.keys() or new_cost < cost[next_grid]:  # next_grid hasn't been visited or needs to update
                    cost[next_grid] = new_cost
                    parent[next_grid] = current
                    priority = new_cost + self.__future_cost(next_grid) - self.__future_cost(current)   # heuristic future cost
                    frontier.put((priority, next_grid))
        # if there's no feasible solution
        return None

    def solve(self, algorithm="BFS"):
        # make a copy of the initial map
        self.map = self.init_map.copy()
        algorithm = algorithm.lower()
        if algorithm not in self.algorithms.keys():
            raise Exception("Unsupported algorithm: " + algorithm)
        print("Shortest distance:", self.algorithms[algorithm]())


if __name__ == "__main__":
    Solution = MazeProblem(maze_file='maze.txt')
    algorithms = ["BFS", "A star"]
    for algo in algorithms:
        Solution.solve(algo)
        Solution.drawMap(algo)
