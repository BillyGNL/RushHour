import csv
import random
from os import path
import re
import matplotlib.pyplot as plt


class Car():
    """ Make car objects """

    def __init__(self, name, direction, x, y, length):
        """ Initialize car """

        self.name = name
        self.direction = direction
        self.x = x
        self.y = y
        self.length = length

class Board():
    """ Make board object """

    def __init__(self, dimensions, carlist):
        """ Initialize board """

        self.dimensions = dimensions
        self.carlist = carlist
        self.counter = 0

        # fill in empty board with correct dimensions
        self.board = [[0 for x in range(dimensions)] for y in range(dimensions)]

        # fill in all cars on correct places in board
        for car in carlist:
            if car.direction == "H":
                for i in range(car.length):
                    self.board[car.y][car.x + i] = car.name
            if car.direction == "V":
                for i in range(car.length):
                    self.board[car.y + i][car.x] = car.name

    def move(self):
        """ Allows cars to move over the board """

        test_counter = 0


        self.print_board()
        print()

        # end loop if game is won
        while self.won() != True:
            test_counter += 1

            if (test_counter % 200000) == 0:
                self.print_board()
                print()

            # pick random number to move
            car = random.choice(self.carlist)
            self.old_car_x = car.x
            self.old_car_y = car.y


            # check if there is space to the right of horizontal cars to move to
            if car.direction == "H":

                count = 0

                while car.x < (self.dimensions - car.length) and self.board[car.y][car.x + car.length] == 0:

                    # move car over board and increment counter
                    self.board[car.y][car.x + car.length] = self.board[car.y][car.x]
                    self.board[car.y][car.x] = 0
                    car.x = car.x + 1
                    count += 1
                    print("rechts")

                    if random.random() > 0.5:
                        break

                # if horizontal car can't move right, check if space to the left to move to
                while car.x > 0 and self.board[car.y][car.x - 1] == 0 and count == 0:

                    # move car over board and increment counter
                    self.board[car.y][car.x - 1] = self.board[car.y][car.x]
                    self.board[car.y][car.x + (car.length - 1)] = 0
                    car.x = car.x - 1
                    print("links")

                    if random.random() > 0.5:
                        break

                self.print_board()
                print()

            # check if there is space to the top of vertical cars to move to
            if car.direction == "V":

                count = 0

                while car.y < (self.dimensions - car.length) and self.board[car.y + car.length][car.x] == 0:

                    # move car over board and increment counter
                    self.board[car.y + car.length][car.x] = self.board[car.y][car.x]
                    self.board[car.y][car.x] = 0
                    car.y = car.y + 1
                    count += 1
                    print("boven")

                    if random.random() > 0.5:
                        break

                    # if vertical car can't move up, check if space to the bottom to move to
                while car.y > 0 and self.board[car.y - 1][car.x] == 0 and count == 0:

                    # move car over board and increment counter
                    self.board[car.y - 1][car.x] = self.board[car.y][car.x]
                    self.board[car.y + (car.length - 1)][car.x] = 0
                    car.y = car.y - 1
                    print("beneden")

                    if random.random() > 0.5:
                        break

                self.print_board()
                print()

            # if self.car_moved(car):
            #     self.counter += 1

        self.print_board()
        print(f"Found solution! {self.counter} cars were moved before the solution was found.")

        return self.counter

    def won(self):
        """ Check if game is won """

        # select red car
        for car in self.carlist:
            if car.name == "X":
                red_car = car

        # check if red car is in right place
        if red_car.x == (self.dimensions - 2):
            return True
        return False

    def print_board(self):
        """ Print the board """

        # print board in correct order
        for i in range(self.dimensions -1, -1, -1):
            for j in range(self.dimensions):
                print(self.board[i][j] ,end = " ")
            print()

    def car_moved(self, car):
        x = car.x
        y = car.y

        if x != self.old_car_x or y != self.old_car_y:
            return True
        return False


if __name__ == '__main__':

    while True:

        # ask for input file
        input_name = input(f"Please enter the name of the input file: ")
        input_file = f"Rushhour{input_name}.csv"

        # check if file exists otherwise reprompt
        if path.exists(input_file) == False:
            print("File does not exist")
        else:
            break

    # get board dimensions from file title, which is the 8th character
    dimensions = int(re.search(r'\d+', input_name).group())

    with open(input_file) as input:
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


    # move = board.move()
    # move_list = []
    # y_as = []
    # total = 0

    board = Board(dimensions, carlist)
    move = board.move()

    # for i in range(20):

    #     with open(input_file) as input:
    #         reader = csv.reader(input, delimiter=',')
    #         row_count = 0
    #         carlist = []
    #         for row in reader:
    #             if row_count != 0:
    #                 x = int(row[2].strip(' "')) - 1
    #                 y = int(row[3].strip('"')) - 1
    #                 length = int(row[4].strip())
    #                 direction = row[1].strip()
    #                 car = Car(row[0], direction, x, y, length)
    #                 carlist.append(car)
    #             row_count += 1



    #     board = Board(dimensions, carlist)
    #     y_as.append(i)
    #     move = board.move()
    #     move_list.append(move)
    #     total += move
    #     print(move)

    # mean = total / 20
    # print(mean)
    # plt.scatter(y_as, move_list)
    # plt.show()
