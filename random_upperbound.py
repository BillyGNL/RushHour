import csv
import random
from os import path, startfile
import re
import copy

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

    def __init__(self, dimensions, carlist, upperbound):
        """ Initialize board """

        self.dimensions = dimensions
        self.upperbound = upperbound
        self.move_list = []
        self.kut_moves = []
        self.carlist = copy.deepcopy(carlist)
        self.counter = 0

        # make and fill board using the provided dimensions
        self.board = [[0 for x in range(dimensions)] for y in range(dimensions)]

        # fill in all cars on correct places in board
        for car in carlist:

            # if car is positioned horizontally
            if car.direction == "H":
                for i in range(car.length):
                    self.board[car.y][car.x + i] = car.name

            # if car is positioned vertically
            if car.direction == "V":
                for i in range(car.length):
                    self.board[car.y + i][car.x] = car.name

    def move(self):
        """ Allows cars to move over the board, returns a counter of the number of moves made """

        previous_car = None
        # end loop if game is won
        while self.won() != True:

            # pick a random car to move
            car = random.choice(self.carlist)

            if previous_car:
                if previous_car.name == car.name:
                    continue


            print("CAR BEING CHECKED:", car.name)

            # remember the x and y coordinate before moving the car
            self.old_car_x = car.x
            self.old_car_y = car.y

            # h_moved = False
            # v_moved = False

            # check if there is space to the right of horizontal cars to move to
            if car.direction == "H":

                while car.x < (self.dimensions - car.length) and self.board[car.y][car.x + car.length] == 0:

                    # move car to the right on the board
                    self.board[car.y][car.x + car.length] = self.board[car.y][car.x]
                    self.board[car.y][car.x] = 0
                    car.x = car.x + 1
                    self.kut_moves.append(f"{car.name} + 1")
                    previous_car = car
                    if len(self.move_list) > 0 and (self.move_list[-1][0:2] == f"{car.name} " or self.move_list[-1][0:2] == car.name):
                        previous_move = self.move_list.pop().split(" ")
                        previous_move[-1] = str(int(previous_move[-1]) + 1)
                        new_move = ' '.join(previous_move)
                        self.move_list.append(new_move)
                    else:
                        self.move_list.append(f"{car.name} + 1")

                moved = self.car_moved(car)

                # if horizontal car can't move right, check if space to the left to move to
                while car.x > 0 and self.board[car.y][car.x - 1] == 0 and moved == False:

                    # move car to the left on the board
                    self.board[car.y][car.x - 1] = self.board[car.y][car.x]
                    self.board[car.y][car.x + (car.length - 1)] = 0
                    car.x = car.x - 1
                    self.kut_moves.append(f"{car.name} - 1")
                    previous_car = car
                    if len(self.move_list) > 0 and (self.move_list[-1][0:2] == f"{car.name} " or self.move_list[-1][0:2] == car.name):
                        previous_move = self.move_list.pop().split(" ")
                        previous_move[-1] = str(int(previous_move[-1]) + 1)
                        new_move = ' '.join(previous_move)
                        self.move_list.append(new_move)
                    else:
                        self.move_list.append(f"{car.name} - 1")


            # check if there is space to the top of vertical cars to move to
            if car.direction == "V":

                while car.y < (self.dimensions - car.length) and self.board[car.y + car.length][car.x] == 0:

                    # move car up on the board
                    self.board[car.y + car.length][car.x] = self.board[car.y][car.x]
                    self.board[car.y][car.x] = 0
                    car.y = car.y + 1
                    self.kut_moves.append(f"{car.name} + 1")
                    previous_car = car
                    if len(self.move_list) > 0 and (self.move_list[-1][0:2] == f"{car.name} " or self.move_list[-1][0:2] == car.name):
                        previous_move = self.move_list.pop().split(" ")
                        previous_move[-1] = str(int(previous_move[-1]) + 1)
                        new_move = ' '.join(previous_move)
                        self.move_list.append(new_move)
                    else:
                        self.move_list.append(f"{car.name} + 1")

                moved = self.car_moved(car)

                # if vertical car can't move up, check if space to the bottom to move to
                while car.y > 0 and self.board[car.y - 1][car.x] == 0 and moved == False:

                    # move car down on the board
                    self.board[car.y - 1][car.x] = self.board[car.y][car.x]
                    self.board[car.y + (car.length - 1)][car.x] = 0
                    car.y = car.y - 1
                    self.kut_moves.append(f"{car.name} - 1")
                    previous_car = car
                    if len(self.move_list) > 0 and (self.move_list[-1][0:2] == f"{car.name} " or self.move_list[-1][0:2] == car.name):
                        previous_move = self.move_list.pop().split(" ")
                        previous_move[-1] = str(int(previous_move[-1]) + 1)
                        new_move = ' '.join(previous_move)
                        self.move_list.append(new_move)
                    else:
                        self.move_list.append(f"{car.name} - 1")

            # increment counter by 1 if the car has moved
            if self.car_moved(car):
                self.counter += 1

            if self.counter > self.upperbound:
                break

        return self.counter

    def won(self):
        """ Returns True if the game is won """

        # select red car
        for car in self.carlist:
            if car.name == "X":
                red_car = car

        # if all tiles to right of red_car are 0 then the win condition has been met
        for i in range(red_car.x + 2, self.dimensions):
            if self.board[red_car.y][i] != 0:
                return False
        return True

    def car_moved(self, car):
        x = car.x
        y = car.y

        if x != self.old_car_x or y != self.old_car_y:
            return True
        return False

def read_file(input_file):
    """ Read board file and return a list of car objects """

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

    return carlist

def game_iteration(iterations):

    # set upperbound to a very high number
    upperbound = 1000000
    kut = []
    original_carlist = read_file(input_file)
    for iteration in range(iterations):

        board = Board(dimensions, original_carlist, upperbound)
        move = board.move()

        if move < board.upperbound:
            upperbound = move
            print(upperbound)
            shortest_kutlist = board.kut_moves
            shortest_list = board.move_list

    print(f"Fastest: {upperbound}")
    print(shortest_kutlist)
    print(len(shortest_list))
    print(shortest_list)

    with open ('solution.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["car", "move"])
        for i in range(len(shortest_list)):
            if "-" in shortest_list[i]:
                negative_value = "-"+str(shortest_list[i][-1])
                if shortest_list[1] == " ":
                    writer.writerow([shortest_list[i][0], negative_value])
                else:
                    writer.writerow([shortest_list[i][0:2], negative_value])
            else:
                if shortest_list[1] == " ":
                    writer.writerow([shortest_list[i][0], shortest_list[i][-1]])
                else:
                    writer.writerow([shortest_list[i][0:2], shortest_list[i][-1]])

        # open solution file
        startfile('solution.csv')

if __name__ == '__main__':

    valid_file = False
    while valid_file == False:

        # ask for input file
        input_name = input(f"Please enter the name of the input file: ")
        input_file = f"Boards/Rushhour{input_name}.csv"

        # check if file exists otherwise reprompt
        if path.exists(input_file) == False:
            print("File does not exist")
        else:
            valid_file = True

    # fetch a positive integer from the user
    valid_integer = False
    while valid_integer == False:

        try:
            iterations = int(input(f"How many iterations would you like to run? :"))
        except:
            print("Please provide a positive integer, try again")
            continue

        if iterations > 0:
            valid_integer = True

    # fetch dimensions from file title
    dimensions = int(re.search(r'\d+', input_name).group())

    # start the random algorithm
    game = game_iteration(iterations)
