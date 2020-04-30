# COMMAND: rushhour(0, ["--B---","--B---","XXB---","--AA--","------","------"])
# COMMAND: rushhour(0, ["--B---","--B---","--B-XX","--AA--","------","------"])

EMPTY_SPACE = '-'
HORIZONTAL = "horizontal"
VERTICAL = "vertical"
RIGHT = "right"
LEFT = "left"
UP = "up"
DOWN = "down"


class Car:
    def __init__(self, char, orient, length, startPos, endPos):
        self.character = char
        self.orientation = orient
        self.length = length
        self.startPos = startPos
        self.endPos = endPos

    def printCar(self):
        print("Character: ", self.character)
        print("Orientation: ", self.orientation)
        print("Length: ", self.length)
        print("Start Position: ", self.startPos)
        print("End Position: ", self.endPos)


class Board:
    def __init__(self, start):
        self.board = self.parseBoard(start)
        self.width = 6
        self.height = 6
        self.cars = dict()

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
                    # self.cars.append(car)
                    self.cars[character] = car

                visitedBoard[i][j] = True

    def moveCar(self, char, direction):

        car = self.cars[char]
        startX = car.startPos[0]
        startY = car.startPos[1]
        endX = car.endPos[0]
        endY = car.endPos[1]

        if (direction == RIGHT):
            self.board[startX][startY] = EMPTY_SPACE
            self.board[endX][endY + 1] = char

            car.startPos = [startX, startY + 1]
            car.endPos = [endX, endY + 1]

        elif (direction == LEFT):
            self.board[endX][endY] = EMPTY_SPACE
            self.board[startX][startY - 1] = char

            car.startPos = [startX, startY - 1]
            car.endPos = [endX, endY - 1]
        elif (direction == UP):
            self.board[endX][endY] = EMPTY_SPACE
            self.board[startX - 1][startY] = char

            car.startPos = [startX - 1, startY]
            car.endPos = [endX - 1, endY]
        elif (direction == DOWN):
            self.board[startX][startY] = EMPTY_SPACE
            self.board[endX + 1][endY] = char

            car.startPos = [startX + 1, startY]
            car.endPos = [endX + 1, endY]

        print("After move: ")
        self.printBoard()
        car.printCar()

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


def rushhour(heuristic, start):
    game = Board(start)
    print("Start:")
    game.printBoard()
    game.parseCars()

# TODO: Check validity of moving car
