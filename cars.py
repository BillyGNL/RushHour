import csv

# create 2d array

class Car():
    """ Make car objects """

    def __init__(self, name, direction, x, y, length):
        self.name = name
        self.direction = direction
        self.x = x
        self.y = y
        self.length = length

class Board():
    """ Make board object """

    def __init__(self, dimensions, carlist):
        self.dimensions = dimensions
        self.carlist = carlist

        self.board = [[0 for x in range(dimensions)] for y in range(dimensions)]

        for car in carlist:
            if car.direction == "H":
                for i in range(car.length):
                    self.board[car.y][car.x + i] = car.name
            if car.direction == "V":
                for i in range(car.length):
                    self.board[car.y + i][car.x] = car.name

        for r in self.board:
            for c in r:
                print(c,end = " ")
            print()
        print()
    
    def move(self):

        for car in self.carlist:

            if car.direction == "H" and car.x < 4:
                if self.board[car.y][car.x + 2] == 0:
                    self.board[car.y][car.x + 2] = self.board[car.y][car.x]
                    self.board[car.y][car.x] = 0
                elif self.board[car.y][car.x - 1] == 0:
                    self.board[car.y][car.x - 1] = self.board[car.y][car.x]
                    self.board[car.y][car.x + 1] = 0
        
            for r in self.board:
                for c in r:
                    print(c,end = " ")
                print()
            print()
            # if car.direction == "V":


if __name__ == '__main__':

    with open('Rushhour6x6_1.csv') as input:
        reader = csv.reader(input, delimiter=',')

        row_count = 0
        carlist = []
        for row in reader:
            if row_count != 0:
                x = int(row[2].strip(' "')) - 1
                y = int(row[3].strip('"')) - 1
                length = int(row[4].strip())
                direction = row[1].strip()
                car = Car(row[0], direction, x, y, length)
                carlist.append(car)
            row_count += 1

    board = Board(6, carlist)
    move = board.move()
