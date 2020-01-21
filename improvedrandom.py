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

    def car_in_front(self):
        for car in self.carlist:
            if car.name == "X":
                red_car = car

        for i in range(red_car.x + 2, self.dimensions):
            if self.board[red_car.y][i] != 0:
                letter = self.board[red_car.y][i]

                for car in self.carlist:
                        if car.name == letter:
                            if (car.y > 0 and self.board[red_car.y - 1][car.x] == 0) or (red_car.y < (self.dimensions - car.length) and self.board[red_car.y + car.length][car.x] == 0):
                                # self.print_board()
                                # print(car.name)
                                # print()
                                self.car_in_fron = car
                                return True

            return False

    def move(self):
        """ Allows cars to move over the board """

        # end loop if game is won
        while self.won() != True:

            # pick random number to move
            car = random.choice(self.carlist)
            if self.car_in_front() == True and self.car_in_fron != previous_car:
                car = self.car_in_fron
            previous_car = car
            self.old_car_x = car.x
            self.old_car_y = car.y

            # check if there is space to the right of horizontal cars to move to
            if car.direction == "H":

                while car.x < (self.dimensions - car.length) and self.board[car.y][car.x + car.length] == 0:

                    # move car over board and increment counter
                    self.board[car.y][car.x + car.length] = self.board[car.y][car.x]
                    self.board[car.y][car.x] = 0
                    car.x = car.x + 1

                    # if random.random() > 0.3:
                    #     break

                moved = self.car_moved(car)
                # if horizontal car can't move right, check if space to the left to move to
                while car.x > 0 and self.board[car.y][car.x - 1] == 0 and moved == False:

                    # move car over board and increment counter
                    self.board[car.y][car.x - 1] = self.board[car.y][car.x]
                    self.board[car.y][car.x + (car.length - 1)] = 0
                    car.x = car.x - 1

                    # if random.random() > 0.3:
                    #     break

            # check if there is space to the top of vertical cars to move to
            if car.direction == "V":

                while car.y < (self.dimensions - car.length) and self.board[car.y + car.length][car.x] == 0:

                    # move car over board and increment counter
                    self.board[car.y + car.length][car.x] = self.board[car.y][car.x]
                    self.board[car.y][car.x] = 0
                    car.y = car.y + 1

                    # if random.random() > 0.3:
                    #     break

                moved = self.car_moved(car)
                # if vertical car can't move up, check if space to the bottom to move to
                while car.y > 0 and self.board[car.y - 1][car.x] == 0 and moved == False:

                    # move car over board and increment counter
                    self.board[car.y - 1][car.x] = self.board[car.y][car.x]
                    self.board[car.y + (car.length - 1)][car.x] = 0
                    car.y = car.y - 1

                    # if random.random() > 0.3:
                    #     break

            if self.car_moved(car):
                self.counter += 1

            # self.print_board()
            # print()
        # print(f"Found solution! {self.counter} cars were moved before the solution was found.")

        return self.counter

    def won(self):
        """ Check if game is won """

        # select red car
        for car in self.carlist:
            if car.name == "X":
                red_car = car

        # if all tiles to right of red_car are 0, win
        for i in range(red_car.x + 2, self.dimensions):
            if self.board[red_car.y][i] != 0:
                return False
        return True

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

    def animation(self):
        colors = {'A': "#cc3399",
              'B': "#FFF000",
              'C': "#008000",
              'D': "#0000FF",
              'E': "#000000",
              'F': "#00FFFF",
              'G': "#FF00FF",
              'H': "#FFA500",
              'I': "#FFE455",
              'J': "#BC8F8F",
              'K': "#DA70D6",
              'L': "#00ff00",
              'M': "#0066ff",
              'N': "#663300",
              'O': "#003366",
              'P': "#660066",
              'Q': "#666699",
              'R': "#339966",
              'S': "#666633",
              'T': "#00cc00",
              'U': "#ff0066",
              'V': "#cc3300",
              'W': "#ff9999",
              'X': "#FF0000",
              'Y': "#99cc00"
            }

        plt.figure()
        axis = plt.axes()

        for x in range(dimensions):
            for y in range(dimensions):
                if self.board[y][x] != 0:
                    block = plt.Rectangle((x, y), 1, 1, fc=colors[self.board[y][x]])
                    axis.add_patch(block)

        plt.xlim(0, dimensions)
        plt.ylim(0, dimensions)
        plt.grid()
        plt.show()
        plt.cla()

        # plt.rectangle
        # add_patch


def game_iteration():

    move_list = []
    total = 0
    iterations = 100

    for iteration in range(iterations):

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

        board = Board(dimensions, carlist)
        move = board.move()

        move_list.append(move)
        total += move

    sort = sorted(move_list)

    mean = total / iterations
    median = sort[int((iterations / 2) - 1)]
    fastest = sort[0]
    print("mean:", mean)
    print("median:", median)
    print("fastest:", fastest)
    plt.hist(move_list, bins=50)
    plt.show()


if __name__ == '__main__':

    while True:

        # ask for input file
        input_name = input(f"Please enter the name of the input file: ")
        input_file = f"Boards/Rushhour{input_name}.csv"

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

    game = game_iteration()
