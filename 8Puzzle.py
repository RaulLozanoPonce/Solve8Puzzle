import marshal
import os
from time import time


def loadData(path):
    if os.path.isfile(path):
        fileIn = open(path, "br")
        dataLoad = marshal.load(fileIn)
        fileIn.close()
        return dataLoad
    else:
        return {}


def saveData(path, data):
    fileOut = open(path, "bw")
    marshal.dump(data, fileOut)
    fileOut.close()


class Board:

    def __init__(self, init_state):
        # Serialization
        self.directory = "map.txt"
        self.map = loadData(self.directory)

        # Board
        self.board = init_state
        self.path = [init_state]
        self.manhattan = self.calculateManhattan()
        self.possibilities = ((-1, 0), (0, -1), (1, 0), (0, 1))

        # Lists
        self.open_list = []
        self.closed_list = []

        # 0's attributes
        self.zx = -1
        self.zy = -1
        self.searchZero()

    def searchZero(self):
        for i in range(0, 3):
            if self.board[i].__contains__(0):
                self.zx = i
                self.zy = self.board[i].index(0)

    def calculateManhattan(self):
        count = 0
        for i in range(0, 3):
            for j in range(0, 3):
                aux = self.board[i][j] - 1
                if aux == -1:
                    count += 4 - i - j
                else:
                    count += abs(aux // 3 - i) + abs(aux % 3 - j)
        return count

    def manhattanChange(self, currentManhattan, pos1x, pos1y, pos2x, pos2y):
        aux1 = self.board[pos1x][pos1y] - 1
        aux2 = self.board[pos2x][pos2y] - 1

        if aux1 == -1:
            count1 = pos1x + pos1y - pos2x - pos2y
        else:
            count1 = - (abs(aux1 // 3 - pos1x) + abs(aux1 % 3 - pos1y)) + (
                    abs(aux1 // 3 - pos2x) + abs(aux1 % 3 - pos2y))

        if aux2 == -1:
            count2 = pos2x + pos2y - pos1x - pos1y
        else:
            count2 = - (abs(aux2 // 3 - pos2x) + abs(aux2 % 3 - pos2y)) + (
                    abs(aux2 // 3 - pos1x) + abs(aux2 % 3 - pos1y))

        currentManhattan += count1 + count2
        return currentManhattan

    def searchNodes(self):
        for i in range(0, 4):
            posx = self.zx + self.possibilities[i][0]
            posy = self.zy + self.possibilities[i][1]
            if 0 <= posx <= 2 and 0 <= posy <= 2:
                manhaux = self.manhattanChange(self.manhattan, self.zx, self.zy, posx, posy)
                cpy = [self.board[0].copy(), self.board[1].copy(), self.board[2].copy()]
                cpy[self.zx][self.zy] = cpy[posx][posy]
                cpy[posx][posy] = 0
                if not self.closed_list.__contains__(cpy):
                    pathaux = self.path.copy()
                    pathaux.append(cpy)
                    self.open_list.append([pathaux.copy(), manhaux, posx, posy])
        self.open_list.sort(key=lambda manh: manh[1] + len(manh[0]), reverse=True)

    def forPath(self):
        for i in range(0, len(self.path) - 1):
            self.map[str(self.path[i])] = self.path[i + 1]
            for j in range(0, 3):
                for k in range(0, 3):
                    if self.path[i][j][k] == 0:
                        print(i + 1, ": ", self.path[i + 1][j][k])

    def execute(self):
        while True:
            if self.manhattan == 0:
                self.forPath()
                saveData("map.txt", self.map)
                return

            self.closed_list.append(self.board)
            if str(self.board) in self.map:
                self.path.append(self.map[str(self.board)])
                self.board = self.map[str(self.board)]
                self.manhattan = self.calculateManhattan()
            else:
                self.searchNodes()
                aux = self.open_list.pop()
                self.path = aux[0].copy()
                self.board = self.path[len(self.path) - 1].copy()
                self.manhattan = aux[1]
                self.zx = aux[2]
                self.zy = aux[3]


class Main:
    start_time = time()
    b = Board([[6, 7, 1],
               [5, 2, 3],
               [8, 4, 0]])
    b.execute()
    elapsed_time = time() - start_time
    print(elapsed_time)
