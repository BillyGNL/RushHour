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

        board = [[0 for x in range(dimensions)] for y in range(dimensions)]

        for car in carlist:
            if car.direction == "H":
                for i in range(car.length):
                    board[car.y - 1][car.x + i - 1] = car.name
            else:
                for i in range(car.length):
                    board[car.y + i - 1][car.x - 1] = car.name

        for r in board:
            for c in r:
                print(c,end = " ")
            print()

if __name__ == '__main__':

    with open('Rushhour6x6_1.csv') as input:
        reader = csv.reader(input, delimiter=',')

        row_count = 0
        carlist = []
        for row in reader:
            if row_count != 0:
                x = int(row[2].strip(' "'))
                y = int(row[3].strip('"'))
                length = int(row[4].strip())
                direction = row[1].strip()
                car = Car(row[0], direction, x, y, length)
                carlist.append(car)
            row_count += 1

    board = Board(6, carlist)
