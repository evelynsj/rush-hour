# COMMAND: rushhour(0, ["--B---","--B---","XXB---","--AA--","------","------"])
# COMMAND: rushhour(0, ["--B---","--B---","--B-XX","--AA--","------","------"])

import copy
import heapq

EMPTY_SPACE = '-'
HORIZONTAL = "horizontal"
VERTICAL = "vertical"
RIGHT = "right"
LEFT = "left"
UP = "up"
DOWN = "down"


class PriorityQueue:
    def __init__(self, heap=[]):
        self.heap = heap  # turn into max heap by making priority negative
        self.count = 0

    def push(self, state, value):
        # use count as a tiebreaker when priorities are the same
        heapq.heappush(self.heap, (value, self.count, state))
        self.count += 1

    def pop(self):
        return heapq.heappop(self.heap)

    def size(self):
        return len(self.heap)


class Car:
    def __init__(self, char, orient, length, startPos, endPos):
        self.character = char
        self.orientation = orient
        self.length = length
        self.startPos = startPos
        self.endPos = endPos

    def possibleMoves(self, state):
        moves = []
        startX = self.startPos[0]
        startY = self.startPos[1]
        endX = self.endPos[0]
        endY = self.endPos[1]

        if (self.orientation == HORIZONTAL):
            # can move right
            if (endY + 1 < state.width) and (state.isEmpty(endX, endY + 1)):
                moves.append(RIGHT)
            # can move left
            if (startY - 1 >= 0) and (state.isEmpty(startX, startY - 1)):
                moves.append(LEFT)

        elif (self.orientation == VERTICAL):
            # can move up
            if (startX - 1 >= 0) and (state.isEmpty(startX - 1, startY)):
                moves.append(UP)
            # can move down
            if (endX + 1 < state.height) and (state.isEmpty(endX + 1, endY)):
                moves.append(DOWN)

        # print(moves)
        return moves

    def moveCar(self, direction, state):
        board = state.board
        startX = self.startPos[0]
        startY = self.startPos[1]
        endX = self.endPos[0]
        endY = self.endPos[1]

        if (direction == RIGHT):
            board[startX][startY] = EMPTY_SPACE
            board[endX][endY + 1] = self.character

            self.startPos = [startX, startY + 1]
            self.endPos = [endX, endY + 1]
        elif (direction == LEFT):
            board[endX][endY] = EMPTY_SPACE
            board[startX][startY - 1] = self.character

            self.startPos = [startX, startY - 1]
            self.endPos = [endX, endY - 1]
        elif (direction == UP):
            board[endX][endY] = EMPTY_SPACE
            board[startX - 1][startY] = self.character

            self.startPos = [startX - 1, startY]
            self.endPos = [endX - 1, endY]
        elif (direction == DOWN):
            board[startX][startY] = EMPTY_SPACE
            board[endX + 1][endY] = self.character

            self.startPos = [startX + 1, startY]
            self.endPos = [endX + 1, endY]

    def printCar(self):
        print("***Print Car***")
        print("Character: ", self.character)
        print("Orientation: ", self.orientation)
        print("Length: ", self.length)
        print("Start Position: ", self.startPos)
        print("End Position: ", self.endPos)


class Board:
    def __init__(self, start, width=6, height=6, cars=dict(), gn=0, hn=0):
        self.board = self.parseBoard(start)
        self.width = width
        self.height = height
        self.cars = cars
        self.gn = gn
        self.hn = hn

    def parseBoard(self, start):
        board = []

        for row in start:
            board.append(list(row))

        return board

    def parseCars(self):
        # create boolean board
        visitedBoard = self.createBooleanBoard()

        # parse to get car position
        for i in range(self.height):
            for j in range(self.width):
                if visitedBoard[i][j]:  # tile has been visited
                    continue
                if self.board[i][j] != EMPTY_SPACE:  # tile contains car

                    # get car character
                    character = self.board[i][j]

                    # get car orientation
                    orientation = self.getCarOrientation(
                        i, j, character, visitedBoard)

                    # get car length and mark visited
                    length = self.getCarLength(
                        i, j, orientation, character, visitedBoard)

                    # get start and end positions
                    startPos = [i, j]
                    endPos = self.getEndPos(i, j, orientation, length)

                    car = Car(character, orientation, length, startPos, endPos)
                    self.cars[character] = car

                visitedBoard[i][j] = True

    def getEndPos(self, i, j, orient, length):
        if (orient == HORIZONTAL):
            return [i, j + length - 1]
        elif (orient == VERTICAL):
            return [i + length - 1, j]

    def getCarLength(self, i, j, orient, char, visited):
        length = 1
        if (orient == HORIZONTAL):
            for y in range(j + 1, self.width):
                if self.board[i][y] != char or visited[i][y]:
                    break
                length += 1
                visited[i][y] = True
        elif (orient == VERTICAL):
            for x in range(i + 1, self.height):
                # if board has different car or has been visited
                if self.board[x][j] != char or visited[x][j]:
                    break
                length += 1
                visited[x][j] = True

        return length

    def getCarOrientation(self, i, j, char, visited):  # TODO: check -1 too??
        # check horizontal
        if j + 1 < self.width and not visited[i][j + 1] and self.board[i][j + 1] == char:
            return HORIZONTAL
        # check vertical
        elif i + 1 < self.height and not visited[i + 1][j] and self.board[i + 1][j] == char:
            return VERTICAL

    def isGoal(self):
        GOAL_END = [2, 5]
        specialCar = self.cars["X"]

        return specialCar.endPos == GOAL_END

    def isEmpty(self, i, j):
        return self.board[i][j] == EMPTY_SPACE

    def createBooleanBoard(self):
        board = []

        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            board.append(row)

        return board

    def printBoard(self):
        for i, row in enumerate(self.board):
            print(i, "".join(row))


class Game:
    def __init__(self, start, heuristic, path=[]):
        self.frontier = PriorityQueue()
        self.generated = [start.board]
        self.heuristic = heuristic
        self.path = path

    def play(self, start):

        self.evaluateHeuristic(start, self.heuristic)
        fn = start.gn + start.hn

        explored = 0
        self.frontier.push(start, fn)

        # maxI = 2
        # i = 0

        # while frontier is not empty
        while (self.frontier.size()):
            # if (i == maxI):
            #     break
            state = self.frontier.pop()[2]  # pop from frontier
            # print("Popped state:")
            # state.printBoard()
            explored += 1
            # self.path.append(state.board)

            if (state.isGoal()):  # check if it's a winning state
                print("Goal found")
                # return self.path, explored
                return explored
            else:
                newStates = self.generateNewStates(
                    state)  # generate new states
                # print("New states:")
                for newState in newStates:
                    newState.gn = state.gn + 1
                    self.evaluateHeuristic(newState, self.heuristic)
                    fn = newState.gn + newState.hn
                    self.frontier.push(newState, fn)
            # i += 1
        # print(explored)

    def generateNewStates(self, state):
        new = []

        for key in state.cars:
            car = state.cars[key]

            # if there is/are possible move(s), create a new state and add that to the list
            # check possible moves for each car in the state
            moves = car.possibleMoves(state)
            if (moves):
                for move in moves:
                    newState = copy.deepcopy(state)  # create a new state
                    newCar = newState.cars[key]
                    newCar.moveCar(move, newState)

                    if (newState.board not in self.generated):
                        new.append(newState)  # add new state
                        self.generated.append(newState.board)

        return new

    def evaluateHeuristic(self, state, heuristic):
        if (heuristic == 0):  # implement blocking heuristic
            state.hn = self.calculateBlocking(state)
        # TODO: custom heuristic

        # return state.gn + state.hn

    def calculateBlocking(self, state):
        board = state.board
        endY = state.cars['X'].endPos[1]
        blocked = set()

        for j in range(endY + 1, state.width):
            # check if there is car blocking X to the right
            if (board[2][j] != EMPTY_SPACE and board[2][j not in blocked]):
                blocked.add(state.board[2][j])

        return 1 + len(blocked)

    def printGenerated(self):
        print("***Generated list***")
        for board in self.generated:
            print("State")
            for i, row in enumerate(board):
                print(i, "".join(row))

    def printFrontier(self):
        print("***Frontier list***")
        for state in self.frontier.heap:
            print("State heuristic:", state[0])
            state[2].printBoard()


def rushhour(heuristic, start):
    startBoard = Board(start)
    startBoard.parseCars()
    game = Game(startBoard, heuristic)
    explored = game.play(startBoard)
    # path, explored = game.play(startBoard)
    # for state in path:
    #     for row in state:
    #         print("".join(row))
    #     print("\n")

    # print("Total moves:", len(path) - 1)
    print("Total states explored:", explored)

# TODO: Check validity of moving car
