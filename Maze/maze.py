import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpathes


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

    def drawMap(self):
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
                elif self.map[row, col] == 9:
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
        # Save maze image.
        plt.show()
        # plt.savefig('./maze.png')

    def __next_grid(self, s):
        # return all possible new states for state s
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
        return s == (self.m - 1, self.n - 1)

    def __BFS(self):
        layer = [(0, 0)]
        parent = {(0, 0): None}  # visited
        dist = 0
        while layer:
            next_layer = []
            for grid in layer:
                if self.__is_end(grid):
                    x = grid
                    while parent[x]:
                        self.map[x] = 9
                        x = parent[x]
                    self.min_dist = min(dist, self.min_dist)
                    return dist
                for new_grid in self.__next_grid(grid):
                    if new_grid in parent.keys():
                        continue
                    parent[new_grid] = grid
                    next_layer.append(new_grid)
            dist += 1
            layer = next_layer
        # if no solution found
        return None

    def solve(self, algorithm="BFS"):
        self.map = self.init_map.copy()
        algorithm = algorithm.lower()
        if algorithm not in self.algorithms.keys():
            raise Exception("Unsupported algorithm: " + algorithm)
        print("Shortest distance:", self.algorithms[algorithm]())


if __name__ == "__main__":
    Solution = MazeProblem(maze_file='maze.txt')
    Solution.solve("BFS")
    Solution.drawMap()
