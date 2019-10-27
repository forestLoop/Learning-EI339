import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.patches as mpathes
from matplotlib.pyplot import MultipleLocator


class Environment(object):
    def __init__(self, rows=5, cols=8, barrier_num=3, reward_num=5):
        self.rows = rows
        self.cols = cols
        self.barrier_num = barrier_num
        self.reward_num = reward_num
        self.create_env_default()

    def create_env_default(self):
        # the final matrix of environment in our problem
        # start node = 1, terminal node = 2, cliff = -1, barrier = -2, reward = 3
        # [[1. - 1. - 1. - 1. - 1. - 1. - 1.  2.]
        # [0.  0.  0.  0.  0.  0. - 2.  0.]
        # [0.  0.  0.  3. - 2.  0.  0.  0.]
        # [3.  0.  0.  0. - 2.  0.  0.  3.]
        # [0.  0.  3.  0.  0.  0.  0.  0.]]

        self.env = np.zeros([self.rows, self.cols])
        # start node = 1, terminal node = 2, cliff = -1
        self.env[0][0] = 1
        self.env[0][self.cols-1] = 2
        self.env[0][1:self.cols-1] = -1

        # set barrier pos
        barrier_pos = [[3, 4], [2, 4], [1, 6]]
        # set barrier = -2
        for pos in barrier_pos:
            self.env[pos[0]][pos[1]] = -2

        # set reward pos
        reward_pos = [[3, 0], [2, 3], [4, 2], [3, 7]]
        # set reward = 3
        for pos in reward_pos:
            self.env[pos[0]][pos[1]] = 3

    def create_env(self):
        self.env = np.zeros([self.rows, self.cols])
        # start node = 1, terminal node = 2, cliff = -1
        self.env[0][0] = 1
        self.env[0][self.cols-1] = 2
        self.env[0][1:self.cols-1] = -1

        # randomly set barrier pos
        barrier_pos = []
        while(len(barrier_pos) < self.barrier_num):
            i = random.randint(1, self.rows-1)
            j = random.randint(0, self.cols-1)
            if [i, j] not in barrier_pos and [i, j] not in [[1, 0], [1, self.cols-1]]:
                barrier_pos.append([i, j])

        # set barrier = -2
        for pos in barrier_pos:
            self.env[pos[0]][pos[1]] = -2

        # randomly set reward pos
        reward_pos = []
        while (len(reward_pos) < self.reward_num):
            i = random.randint(1, self.rows - 1)
            j = random.randint(0, self.cols - 1)
            if [i, j] not in reward_pos and [i, j] not in barrier_pos:
                reward_pos.append([i, j])

        # set reward = 3
        for pos in reward_pos:
            self.env[pos[0]][pos[1]] = 3

    def show_env(self):
        # fig = plt.figure()
        ax = plt.subplot()
        plt.xlim((0, self.cols))
        plt.ylim((0, self.rows))
        # name: start, terminal, cliff, barrier, reward, others
        # number: 1, 2, -1, -2, 3, 0
        # color: yellow, orange, gray, black, red, white
        color_dict = {-1: "gray", 1: "yellow", 2: "orange", -2: "black", 3: "red", 0: "white", 9: "blue"}
        my_x_ticks = np.arange(0, self.cols, 1)
        my_y_ticks = np.arange(0, self.rows, 1)
        plt.xticks(my_x_ticks)
        plt.yticks(my_y_ticks)
        x_major_locator = MultipleLocator(1)
        y_major_locator = MultipleLocator(1)
        ax.xaxis.set_major_locator(x_major_locator)
        ax.yaxis.set_major_locator(y_major_locator)
        ax.xaxis.set_ticks_position('top')
        ax.invert_yaxis()

        plt.grid()
        for i in range(self.rows):
            for j in range(self.cols):
                color = color_dict[int(self.env[i][j])]
                rect = mpathes.Rectangle([j, i], 1, 1, color=color)
                ax.add_patch(rect)
        # plt.savefig('./cliffwalk.jpg')
        plt.show()

    def update_path(self, policy):
        x, y = 0, 0
        STEP = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        while (x, y) != (0, self.cols-1):
            self.env[x][y] = 9
            action = policy[x][y]
            print((x, y), action)
            x, y = x + STEP[action][0], y + STEP[action][1]


class Sarsa():

    UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3
    STEP = [[-1, 0], [1, 0], [0, -1], [0, 1]]

    def __init__(self, env):
        self.env = env.env
        self.rows = env.rows
        self.cols = env.cols

    def __all_actions(self, state):
        x, y = state[0], state[1]
        if x > 0 and self.env[x - 1][y] != -2:
            yield self.UP
        if x < self.rows - 1 and self.env[x + 1][y] != -2:
            yield self.DOWN
        if y > 0 and self.env[x][y - 1] != -2:
            yield self.LEFT
        if y < self.cols - 1 and self.env[x][y + 1] != -2:
            yield self.RIGHT

    def __is_terminal(self, state):
        return self.env[state[0]][state[1]] == 2

    def __choose_action(self, state, Q, epsilon):
        all_actions = list(self.__all_actions(state))
        # print("###", state, all_actions)
        if np.random.random() <= epsilon:  # exploration
            return np.random.choice(all_actions)
        else:  # exploitation
            return max(all_actions, key=lambda x: Q[state][x])

    def __take_action(self, state, action):
        new_state = (state[0] + self.STEP[action][0], state[1] + self.STEP[action][1])
        # print("###", state, action, new_state)
        reward = 0
        if self.__is_terminal(new_state):   # terminal
            reward = 10
        elif self.env[new_state] == -1:  # cliff
            reward = -100
        elif self.env[new_state] == 3:  # red
            reward = -1
        return new_state, reward

    def learning(self, max_episode_num, gamma=0.9, alpha=0.5, epsilon=0.8):
        # gamma: the discount factor
        # max_episode_num: total episode num
        # Initialize Q(s, a) randomly, except that Q(terminal, *) = 0
        # Q = np.random.rand(self.rows * self.cols, 4)
        Q = np.zeros((self.rows, self.cols, 4))
        Q[0, self.cols - 1, :] = 0
        # Loop for each episode
        while max_episode_num > 0:
            max_episode_num -= 1
            if max_episode_num % 100 == 0:
                epsilon /= 1.5
            state = (0, 0)
            action = self.__choose_action(state, Q, epsilon)
            # Loop until reaching terminal states
            while not self.__is_terminal(state):
                next_state, reward = self.__take_action(state, action)
                # print(next_state)
                next_action = self.__choose_action(next_state, Q, epsilon)
                # Update Q
                Q[state][action] += alpha * (reward + gamma * Q[next_state][next_action] - Q[state][action])
                state, action = next_state, next_action
            # print("-------")
        print(Q)
        policy = [[None, ] * self.cols for _ in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.cols):
                policy[i][j] = max(self.__all_actions((i, j)), key=lambda x: Q[i, j, x])
        return policy


if __name__ == "__main__":
    Env = Environment()
    print("the environment matrix:")
    print(Env.env)
    Env.show_env()
    sarsa = Sarsa(Env)
    policy = sarsa.learning(max_episode_num=300, gamma=0.9, alpha=0.1, epsilon=0.8)
    print(policy)
    Env.update_path(policy)
    Env.show_env()
