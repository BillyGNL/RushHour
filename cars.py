import csv
import random

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

    def move(self):
        
        test_count = 0
        # check if won
        while self.won() != True:
            test_count += 1

            if (test_count % 200000) == 0:
                self.print_board()
            
            # pick random number to move
            car = random.choice(self.carlist)

                
            # check if there is space to the right of horizontal cars to move to
            if car.direction == "H":
                if car.x < (self.dimensions - 2) and self.board[car.y][car.x + 2] == 0:
                    self.board[car.y][car.x + 2] = self.board[car.y][car.x]
                    self.board[car.y][car.x] = 0
                    car.x = car.x + 1

                # if horizontal car can't move to right, check if space to the left to move to
                elif car.x > 0 and self.board[car.y][car.x - 1] == 0 and car.name != "X":
                    self.board[car.y][car.x - 1] = self.board[car.y][car.x]
                    self.board[car.y][car.x + 1] = 0
                    car.x = car.x - 1

            # if car vertical check if there is space to the top to move to
            if car.direction == "V":
                if car.y < (self.dimensions - 2) and self.board[car.y + 2][car.x] == 0:
                    self.board[car.y + 2][car.x] = self.board[car.y][car.x]
                    self.board[car.y][car.x] = 0
                    car.y = car.y + 1

                # if vertical car can't move up, check if space to the bottom to move to
                elif car.y > 0 and self.board[car.y - 1][car.x] == 0:
                    self.board[car.y - 1][car.x] = self.board[car.y][car.x]
                    self.board[car.y + 1][car.x] = 0
                    car.y = car.y - 1

        print("won")
        self.print_board()

    def won(self):
        for car in self.carlist:
            if car.name == "X":
                red_car = car
        
        if red_car.x == ((self.dimensions / 2) + 1):
            return True
        return False
    
    def print_board(self):
        for i in range(self.dimensions -1, -1, -1):
            for j in range(self.dimensions):
                print(self.board[i][j] ,end = " ")
            print()
    

        

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
