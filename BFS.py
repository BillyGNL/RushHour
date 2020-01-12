from cars import Board, Car
import csv
from os import path
import re

class Node():
    """ Create node for BFS algorithm which holds current carlist for node """

    def __init__(self, carlist):

        # each node contains the carlist, or current layout of the board, at the phase of the specific node
        self.carlist = carlist

class Bfs():
    """ BFS algorithm"""

    def __init__(self, start_node, dimensions):

        # the root node, the first layout or carlist
        self.start_node = start_node
        self.dimensions = dimensions

        # the queue will contain all to be checked discovered nodes which are not already in the visited list
        self.queue = [self.start_node]

        # the visited will contain all checked discovered nodes
        self.visited = []

        # constructing first board
        self.board = self.construct_board(self.start_node)

    def check(self):

        count = 0

        for i in range(self.dimensions -1, -1, -1):
            for j in range(self.dimensions):
                print(self.board[i][j] ,end = " ")
            print()

        print()

        while True:

            print("LENGTH", len(self.queue))

            # pop first item in queue from queue and check if node holds winning carlist
            node = self.queue.pop(0)

            # construct board to check for all availabe moves
            self.board = self.construct_board(node)

            for i in range(self.dimensions -1, -1, -1):
                for j in range(self.dimensions):
                    print(self.board[i][j] ,end = " ")
                print()

            print()

            # check if node has winning setup
            if self.won(node) == True:
                for i in range(self.dimensions -1, -1, -1):
                    for j in range(self.dimensions):
                        print(self.board[i][j] ,end = " ")
                    print()
                print(count)
                return node

            # if not winning node, generate all children for node which are automatically added to queue
            self.get_children(node)

            # add node to list of visited carlists
            self.visited.append(node)

            count += 1

    def construct_board(self, node):

        # create empty board with correct dimensions
        self.board = [[0 for x in range(self.dimensions)] for y in range(self.dimensions)]

        # fill in all cars on correct places in board
        for car in node.carlist:
            if car.direction == "H":
                for i in range(car.length):
                    self.board[car.y][car.x + i] = car.name
            if car.direction == "V":
                for i in range(car.length):
                    self.board[car.y + i][car.x] = car.name

        return self.board

    def won(self, node):

        # select red car
        for car in node.carlist:
            if car.name == "X":
                red_car = car

        # if all tiles to right of red_car are 0, win
        for i in range(red_car.x + 2, self.dimensions):
            if self.board[red_car.y][i] != 0:
                return False
        return True

    def get_children(self, node):

        for car in node.carlist:

            original_board = self.board
            original_car = car
            not_visited = True

            if car.direction == "H":

                # while space to right to move to, move and create new node
                while car.x < (self.dimensions - car.length) and self.board[car.y][car.x + car.length] == 0:

                    self.board[car.y][car.x + car.length] = self.board[car.y][car.x]
                    self.board[car.y][car.x] = 0
                    car.x = car.x + 1

                    # check every carlist in visited list, if carlists match break out of loop and check for next move
                    for visited_node in self.visited:
                        if visited_node.carlist == node.carlist:
                            not_visited = False
                            break

                    # if carlist not in visited, create node and add to queue
                    if not_visited == True:
                        self.queue.append(Node(node.carlist))
                    not_visited = True

                # set car.x back to value of node currently making children
                car = original_car
                self.board = original_board

                # while space to left to move to, move and create new node
                while car.x > 0 and self.board[car.y][car.x - 1] == 0:

                    self.board[car.y][car.x - 1] = self.board[car.y][car.x]
                    self.board[car.y][car.x + (car.length - 1)] = 0
                    car.x = car.x - 1

                    for visited_node in self.visited:
                        if visited_node.carlist == node.carlist:
                            not_visited = False
                            break
                    if not_visited == True:
                        self.queue.append(Node(node.carlist))
                    not_visited = True

                # set car.x back to value of node currently making children
                car = original_car
                self.board = original_board

            if car.direction == "V":

                # while space to the top to move to, move and create new node
                while car.y < (self.dimensions - car.length) and self.board[car.y + car.length][car.x] == 0:

                    self.board[car.y + car.length][car.x] = self.board[car.y][car.x]
                    self.board[car.y][car.x] = 0
                    car.y = car.y + 1

                    for visited_node in self.visited:
                        if visited_node.carlist == node.carlist:
                            not_visited = False
                            break
                    if not_visited == True:
                        self.queue.append(Node(node.carlist))
                    not_visited = True

                # set car.y back to value of node currently making children
                car = original_car
                self.board = original_board

                # while space to bottom to move to, move and create new node
                while car.y > 0 and self.board[car.y - 1][car.x] == 0:

                    self.board[car.y - 1][car.x] = self.board[car.y][car.x]
                    self.board[car.y + (car.length - 1)][car.x] = 0
                    car.y = car.y - 1

                    for visited_node in self.visited:
                        if visited_node.carlist == node.carlist:
                            not_visited = False
                            break
                    if not_visited == True:
                        self.queue.append(Node(node.carlist))
                    not_visited = True

                # set car.y back to value of node currently making children
                car = original_car
                self.board = original_board

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
        print(reader)
        row_count = 0
        carlist = []

        # construct carlist
        for row in reader:
            if row_count != 0:
                x = int(row[2].strip(' "')) - 1
                y = int(row[3].strip('"')) - 1
                length = int(row[4].strip())
                direction = row[1].strip()
                car = Car(row[0], direction, x, y, length)
                carlist.append(car)
            row_count += 1

    start_node = Node(carlist)
    algorithm = Bfs(start_node, dimensions)
    algorithm.check()
