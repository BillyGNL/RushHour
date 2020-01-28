"""
Billy Griep
Floris Kienhuis
Jan Elders

Minor Programmeren
Heuristieken

Vindt random oplossing voor Rush Hour gebruik makend van een upperbound
"""

import csv
import random
from os import path
import re
import copy
from random_algorithm import Car, read_file

class Board():
    """ Makes board object """

    def __init__(self, dimensions, carlist, upperbound):
        """ Initializes board """

        # each board contains dimensions to visualise the board in the correct format
        self.dimensions = dimensions

        # each board contains an upperbound which will be adjusted during running to prevent unneccesary runtime
        self.upperbound = upperbound

        # each board contains a movelist which is updated after every move
        self.movelist = []

        # each board contains a carlist, a list of car objects with coordinates, direction and length
        self.carlist = copy.deepcopy(carlist)

        # each board starts with a counter equal to 0, which is used to keep track of the number of moves made
        self.counter = 0

        # create empty board with correct dimensions
        self.board = [[0 for x in range(dimensions)] for y in range(dimensions)]

        # fill in all cars on correct places in board for given carlist
        for car in carlist:
            if car.direction == "H":
                for i in range(car.length):
                    self.board[car.y][car.x + i] = car.name
            if car.direction == "V":
                for i in range(car.length):
                    self.board[car.y + i][car.x] = car.name

    def move(self):
        """ Allows cars to move over the board, returns a counter of the number of moves made """

        # for the first iteration, previous_car should be equal to None
        previous_car = None

        # continue looping until game is won
        while self.won() != True:

            # pick a random car to move
            car = random.choice(self.carlist)

            # if car picked is car that last moved, choose another car
            if previous_car:
                if previous_car.name == car.name:
                    continue

            # remember the x and y coordinate before moving the picked car
            self.old_car_x = car.x
            self.old_car_y = car.y

            # check if there is space to the right of horizontal cars to move to
            if car.direction == "H":
                while car.x < (self.dimensions - car.length) and self.board[car.y][car.x + car.length] == 0:

                    # move car to the right on the board
                    self.board[car.y][car.x + car.length] = self.board[car.y][car.x]
                    self.board[car.y][car.x] = 0
                    car.x = car.x + 1

                    # after car moved, set previous_car to current car for next iteration
                    previous_car = car

                    # if move made is made by same car as previous move, combine moves into one move before appending to movelist
                    if len(self.movelist) > 0 and (self.movelist[-1][0:2] == f"{car.name} " or self.movelist[-1][0:2] == car.name):
                        previous_move = self.movelist.pop().split(" ")
                        previous_move[-1] = str(int(previous_move[-1]) + 1)
                        new_move = ' '.join(previous_move)
                        self.movelist.append(new_move)
                    else:
                        self.movelist.append(f"{car.name} + 1")

                # check if car moved to prevent car from moving back in opposite direction in same iteration
                moved = self.car_moved(car)

                # if horizontal car can't move right, check if space to the left to move to
                while car.x > 0 and self.board[car.y][car.x - 1] == 0 and moved == False:

                    # move car to the left on the board
                    self.board[car.y][car.x - 1] = self.board[car.y][car.x]
                    self.board[car.y][car.x + (car.length - 1)] = 0
                    car.x = car.x - 1
                    previous_car = car
                    if len(self.movelist) > 0 and (self.movelist[-1][0:2] == f"{car.name} " or self.movelist[-1][0:2] == car.name):
                        previous_move = self.movelist.pop().split(" ")
                        previous_move[-1] = str(int(previous_move[-1]) + 1)
                        new_move = ' '.join(previous_move)
                        self.movelist.append(new_move)
                    else:
                        self.movelist.append(f"{car.name} - 1")

            # check if there is space to the top of vertical cars to move to
            if car.direction == "V":
                while car.y < (self.dimensions - car.length) and self.board[car.y + car.length][car.x] == 0:

                    # move car up on the board
                    self.board[car.y + car.length][car.x] = self.board[car.y][car.x]
                    self.board[car.y][car.x] = 0
                    car.y = car.y + 1
                    previous_car = car
                    if len(self.movelist) > 0 and (self.movelist[-1][0:2] == f"{car.name} " or self.movelist[-1][0:2] == car.name):
                        previous_move = self.movelist.pop().split(" ")
                        previous_move[-1] = str(int(previous_move[-1]) + 1)
                        new_move = ' '.join(previous_move)
                        self.movelist.append(new_move)
                    else:
                        self.movelist.append(f"{car.name} + 1")
                moved = self.car_moved(car)

                # if vertical car can't move up, check if space to the bottom to move to
                while car.y > 0 and self.board[car.y - 1][car.x] == 0 and moved == False:

                    # move car down on the board
                    self.board[car.y - 1][car.x] = self.board[car.y][car.x]
                    self.board[car.y + (car.length - 1)][car.x] = 0
                    car.y = car.y - 1
                    previous_car = car
                    if len(self.movelist) > 0 and (self.movelist[-1][0:2] == f"{car.name} " or self.movelist[-1][0:2] == car.name):
                        previous_move = self.movelist.pop().split(" ")
                        previous_move[-1] = str(int(previous_move[-1]) + 1)
                        new_move = ' '.join(previous_move)
                        self.movelist.append(new_move)
                    else:
                        self.movelist.append(f"{car.name} - 1")

            # increment movecounter by 1 if current car has moved
            if self.car_moved(car):
                self.counter += 1

            # if movecounter is bigger than upperbound, break
            if self.counter > self.upperbound:
                break

        # return movecounter
        return self.counter

    def won(self):
        """ Returns True if the game is won """

        # select red car
        for car in self.carlist:
            if car.name == "X":
                red_car = car

        # if all tiles to right of red_car are 0, game is won
        for i in range(red_car.x + 2, self.dimensions):
            if self.board[red_car.y][i] != 0:
                return False
        return True

    def car_moved(self, car):
        """ Checks if car moved """

        # fetch current coordinates
        x = car.x
        y = car.y

        # compare current coordinates to old coordinates saved in move function
        if x != self.old_car_x or y != self.old_car_y:
            return True
        return False

def game_iteration(iterations):
    """ contains logic of 1 iteration """

    # set upperbound to a very high number, so it is overwritten in first iteration
    upperbound = 1000000

    # remember original carlist to construct board
    original_carlist = read_file(input_file)

    # loop for given amount of iterations
    for iteration in range(iterations):

        # initialize board
        board = Board(dimensions, original_carlist, upperbound)

        # execute move function to find solution, which breaks if movecounter exceeds upperbound provided
        move = board.move()

        # if faster solution is found, adjust upperbound
        if move < board.upperbound:
            upperbound = move
            fastest_solution = board.movelist

    # write all moves leading to fastest solution into csv file
    with open ('solution.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["car", "move"])
        for i in range(len(fastest_solution)):
            if "-" in fastest_solution[i]:
                negative_value = "-"+str(fastest_solution[i][-1])
                if fastest_solution[1] == " ":
                    writer.writerow([fastest_solution[i][0], negative_value])
                else:
                    writer.writerow([fastest_solution[i][0:2], negative_value])
            else:
                if fastest_solution[1] == " ":
                    writer.writerow([fastest_solution[i][0], fastest_solution[i][-1]])
                else:
                    writer.writerow([fastest_solution[i][0:2], fastest_solution[i][-1]])

        # exit program wghen solution found
        print("Solved board, check solution.csv for solution!")
        exit()

if __name__ == '__main__':

    # keep prompting for file as long as incorrect file is provided
    valid_file = False
    while valid_file == False:

        # prompt for input file
        input_name = input(f"Please enter the name of the input file: ")
        input_file = f"Boards/Rushhour{input_name}.csv"

        # check if file exists otherwise reprompt
        if path.exists(input_file) == False:
            print("File does not exist")
        else:
            valid_file = True

    # keep prompting until positive integer is provided
    valid_integer = False
    while valid_integer == False:
        try:
            iterations = int(input(f"How many iterations would you like to run?: "))
        except:
            print("Please provide a positive integer")
            continue

        # check if integer is positive
        if iterations > 0:
            valid_integer = True
        else:
            print("Please provide a positive integer")
            continue

    # fetch dimensions from file title
    dimensions = int(re.search(r'\d+', input_name).group())

    # run program
    game = game_iteration(iterations)
