from cars import Board, Car
import csv
from os import path
import re
import copy
import hashlib

class Node():
    """ Create node for BFS algorithm which holds current carlist for node """

    def __init__(self, carlist, movelist):

        # each node contains the carlist, or current layout of the board, at the phase of the specific node
        self.carlist = carlist

        self.movelist = movelist

    def __eq__(self, other):
        if isinstance(other, Node):
            for car1, car2 in zip(self.carlist, other.carlist):
                if car1.x != car2.x:
                    return False
                if car.y != car2.y:
                    return False
            return True

class Bfs():
    """ BFS algorithm"""

    def __init__(self, start_node, dimensions):

        # the root node, the first layout or carlist
        self.start_node = start_node
        self.dimensions = dimensions

        # the queue will contain all to be checked discovered nodes which are not already in the visited list
        self.queue = [self.start_node]

        # the visited will contain all checked discovered nodes
        self.visited = set()
        start_node_string = ""
        for car in start_node.carlist:
            start_node_string += str(car.name)
            start_node_string += str(car.x)
            start_node_string += str(car.y)

        self.visited.add(start_node_string)

        # constructing first board
        self.board = self.construct_board(self.start_node)

    def check(self):

        while True:

            # pop first item in queue from queue and check if node holds winning carlist
            node = self.queue.pop(0)
            print(len(node.movelist))

            # construct board to check for all availabe moves
            self.board = self.construct_board(node)

            # check if node has winning setup
            if self.won(node) == True:
                self.view_node(node)
                print("succes")
                print(node.movelist)
                print(len(node.movelist))
                exit()

            # if not winning node, generate all children for node which are automatically added to queue
            self.get_children(node)


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

            if car.direction == "H":

                # while space to right to move to, move and create new node
                if car.x < (self.dimensions - car.length) and self.board[car.y][car.x + car.length] == 0:

                    car.x = car.x + 1
                    node.movelist.append(f"{car.name} + 1")
                    child = copy.deepcopy(Node(node.carlist, node.movelist))
                    node.movelist.pop()

                    string = ""
                    for cara in child.carlist:
                        string += str(cara.name)
                        string += str(cara.x)
                        string += str(cara.y)

                    # childhash = hashlib.md5(string.encode()).hexdigest()

                    if string in self.visited:
                        pass
                    else:
                        self.visited.add(string)
                        self.queue.append(child)

                    # set car.x back to value of node currently making children
                    car.x = car.x - 1

                # while space to left to move to, move and create new node
                if car.x > 0 and self.board[car.y][car.x - 1] == 0:

                    car.x = car.x - 1
                    node.movelist.append(f"{car.name} - 1")
                    child = copy.deepcopy(Node(node.carlist, node.movelist))
                    node.movelist.pop()

                    string = ""
                    for cara in child.carlist:
                        string += str(cara.name)
                        string += str(cara.x)
                        string += str(cara.y)

                    # childhash = hashlib.md5(string.encode()).hexdigest()

                    if string in self.visited:
                        pass
                    else:
                        self.visited.add(string)
                        self.queue.append(child)

                    # set car.x back to value of node currently making children
                    car.x = car.x + 1

            if car.direction == "V":

                # while space to the top to move to, move and create new node
                if car.y < (self.dimensions - car.length) and self.board[car.y + car.length][car.x] == 0:
                    car.y = car.y + 1

                    node.movelist.append(f"{car.name} + 1")
                    child = copy.deepcopy(Node(node.carlist, node.movelist))
                    node.movelist.pop()

                    string = ""
                    for cara in child.carlist:
                        string += str(cara.name)
                        string += str(cara.x)
                        string += str(cara.y)

                    # childhash = hashlib.md5(string.encode()).hexdigest()

                    if string in self.visited:
                        pass
                    else:
                        self.visited.add(string)
                        self.queue.append(child)

                    # set car.x back to value of node currently making children
                    car.y = car.y - 1

                # while space to bottom to move to, move and create new node
                if car.y > 0 and self.board[car.y - 1][car.x] == 0:
                    # print("move down")
                    car.y = car.y - 1
                    node.movelist.append(f"{car.name} - 1")
                    child = copy.deepcopy(Node(node.carlist, node.movelist))
                    node.movelist.pop()

                    string = ""
                    for cara in child.carlist:
                        string += str(cara.name)
                        string += str(cara.x)
                        string += str(cara.y)

                    # childhash = hashlib.md5(string.encode()).hexdigest()

                    if string in self.visited:
                        pass
                    else:
                        self.visited.add(string)
                        self.queue.append(child)

                    # set car.x back to value of node currently making children
                    car.y = car.y + 1


    def view_node(self, node):
        """ Prints the carlist of the node for testing purposes """

        view = self.construct_board(node)
        for i in range(self.dimensions -1, -1, -1):
            for j in range(self.dimensions):
                print(view[i][j] ,end = " ")
            print()

    def view_queue(self):
        for node in self.queue:
            self.view_node(node)
            print("\n")

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

    movelist = []
    start_node = Node(carlist, movelist)
    algorithm = Bfs(start_node, dimensions)
    algorithm.check()
