# COMMAND: rushhour(0, ["--B---","--B---","XXB---","--AA--","------","------"])

EMPTY_SPACE = '-'
HORIZONTAL = "horizontal"
VERTICAL = "vertical"

class Car:
    def __init__(self, char, orient, length):
        self.character = char
        self.orientation = orient
        self.length = length

    def printCar(self):
        print("Character: ", self.character)
        print("Orientation: ", self.orientation)
        print("Length: ", self.length)

class Board:
    def __init__(self, start):
        self.board = start
        self.width = 6
        self.height = 6
        self.cars = []

    def parseBoard(self):
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
                    
                    car = Car(character, orientation, length)
                    self.cars.append(car)

                visitedBoard[i][j] = True
        
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
        for row in self.board:
            print(row)


def rushhour(heuristic, start):
    game = Board(start)
    game.parseBoard()
