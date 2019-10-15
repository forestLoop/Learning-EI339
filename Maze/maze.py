import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpathes


class MazeProblem:
    def __init__(self, maze_file=''):
        self.map = self.loadMap(maze_file)

    def loadMap(self, file):
        # Load map txt as matrix.
        # 0: path, 1: obstacle, 2: start point, 3: end point
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
        plt.savefig('./maze.png')


if __name__ == "__main__":
    Solution = MazeProblem(maze_file='maze.txt')
    Solution.drawMap()
