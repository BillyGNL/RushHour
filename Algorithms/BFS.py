"""
Billy Griep
Floris Kienhuis
Jan Elders

Minor Programmeren
Heuristieken

Vindt snelste oplossing voor Rush Hour met behulp van breadt-first search
"""

from random_algorithm import Board, Car
import csv
from os import path
import re
import copy

class Node():
    """ Creates nodes for BFS algorithm which hold carlist and movelist """

    def __init__(self, carlist, movelist):

        # each node contains the carlist, or current layout of the board, at the phase of the specific node
        self.carlist = carlist

        # each node contains a list of all previous moves which have led to the current carlist
        self.movelist = movelist

class BFS():
    """ Contains logic for breadt-first search algorithm used to solve Rush Hour """

    def __init__(self, root_node, dimensions):

        # each BFS starts from a root node, which as a carlist has the initial layout of the game
        self.root_node = root_node

        # BFS holds the value for the dimensions of the board being played
        self.dimensions = dimensions

        # the queue will contain all to be checked discovered nodes, starting with the root node
        self.queue = [self.root_node]

        # the visited set will contain all carlists which have been checked
        self.visited = set()

        # the set contains strings representing carlists
        root_node_string = ""
        for car in root_node.carlist:
            root_node_string += car.name
            root_node_string += str(car.x)
            root_node_string += str(car.y)
        self.visited.add(root_node_string)

        # constructing starting board
        self.board = self.construct_board(self.root_node)

    def check(self):
        """ Check method contains the iterative part of the BFS algorithm """

        while self.queue:

            # pop first item in queue and assign to node variable
            node = self.queue.pop(0)

            # construct board to check for all possible moves to make
            self.board = self.construct_board(node)

            # check if node has winning setup
            if self.won(node) == True:

                # write all moves leading to fastest solution into csv file
                with open ('solution.csv', 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["car", "move"])
                    for i in range(len(node.movelist)):
                        if node.movelist[i][2] == "-":
                            negative_value = "-"+str(node.movelist[i][4])
                            writer.writerow([node.movelist[i][0], negative_value])
                        else:
                            writer.writerow([node.movelist[i][0], node.movelist[i][4]])

                # exit program after writing into csv file
                print("Solved board, check solution.csv for solution!")
                exit()

            # if not winning node, generate all children for node which are automatically added to queue
            self.get_children(node)


    def construct_board(self, node):
        """ Construct_board method contains logic for constructing the board """

        # create empty board with correct dimensions
        self.board = [[0 for x in range(self.dimensions)] for y in range(self.dimensions)]

        # fill in all cars on correct places in board for given carlist
        for car in node.carlist:
            if car.direction == "H":
                for i in range(car.length):
                    self.board[car.y][car.x + i] = car.name
            if car.direction == "V":
                for i in range(car.length):
                    self.board[car.y + i][car.x] = car.name

        return self.board

    def won(self, node):
        """ Won method contains conditions for winning setup """

        # select red car
        for car in node.carlist:
            if car.name == "X":
                red_car = car

        # if all tiles to right of red_car are 0, game is won
        for i in range(red_car.x + 2, self.dimensions):
            if self.board[red_car.y][i] != 0:
                return False
        return True

    def get_children(self, node):
        """ Get_children method contains logic for creating all possible children for each node """

        # loop through every car in carlist
        for car in node.carlist:

            # check if direction of car is horizontal
            if car.direction == "H":

                # if space to the right of car availabe to move to, move 1 place to the right
                if car.x < (self.dimensions - car.length) and self.board[car.y][car.x + car.length] == 0:

                    # adjust x-coordinate in carlist
                    car.x = car.x + 1

                    # check if previous move was made by same car
                    if len(node.movelist) > 0 and node.movelist[-1][0] == car.name:

                        # if previous move was made my same car, add 1 to move
                        previous_move = node.movelist.pop().split(" ")
                        previous_move[2] = str(int(previous_move[2]) + 1)
                        new_move = ' '.join(previous_move)
                        node.movelist.append(new_move)

                    # if previous move was not made by same car, add new move to movelist
                    else:
                    	node.movelist.append(f"{car.name} + 1")

                    # make deepcopy of child
                    child = copy.deepcopy(Node(node.carlist, node.movelist))

                    # if previous move was made my same car, subtract 1 from last move for node currently making children
                    if node.movelist[-1][-1] != '1':
                        changed_move = node.movelist.pop().split(" ")
                        changed_move[2] = str(int(changed_move[2]) - 1)
                        original_move = ' '.join(changed_move)
                        node.movelist.append(original_move)

                    # else remove previously added move for node currently making children
                    else:
                        node.movelist.pop()

                    # construct string representing carlist of child
                    string = ""
                    for child_car in child.carlist:
                        string += child_car.name
                        string += str(child_car.x)
                        string += str(child_car.y)

                    # check if any node with carlist of child already exists
                    if string in self.visited:

                        # if exists, forget about child and pass to next iteration
                        pass

                    # if not exists, add child to set of visited carlists and to queue to be checked
                    else:
                        self.visited.add(string)
                        self.queue.append(child)

                    # set x-coordinate back to value of node currently making children
                    car.x = car.x - 1

                # if space to the left of car availabe to move to, move 1 place to the left
                if car.x > 0 and self.board[car.y][car.x - 1] == 0:
                    car.x = car.x - 1

                    if len(node.movelist) > 0 and node.movelist[-1][0] == car.name:
                        previous_move = node.movelist.pop().split(" ")
                        previous_move[2] = str(int(previous_move[2]) + 1)
                        new_move = ' '.join(previous_move)
                        node.movelist.append(new_move)
                    else:
                    	node.movelist.append(f"{car.name} - 1")

                    child = copy.deepcopy(Node(node.carlist, node.movelist))

                    if node.movelist[-1][-1] != '1':
                        changed_move = node.movelist.pop().split(" ")
                        changed_move[2] = str(int(changed_move[2]) - 1)
                        original_move = ' '.join(changed_move)
                        node.movelist.append(original_move)
                    else:
                        node.movelist.pop()

                    string = ""
                    for child_car in child.carlist:
                        string += child_car.name
                        string += str(child_car.x)
                        string += str(child_car.y)

                    if string in self.visited:
                        pass
                    else:
                        self.visited.add(string)
                        self.queue.append(child)

                    car.x = car.x + 1

            # check if direction of car is vertical
            if car.direction == "V":

                # if space to the top of car availabe to move to, move 1 place to the top
                if car.y < (self.dimensions - car.length) and self.board[car.y + car.length][car.x] == 0:

                    #adjust y-coordinate in carlist
                    car.y = car.y + 1

                    if len(node.movelist) > 0 and node.movelist[-1][0] == car.name:
                        previous_move = node.movelist.pop().split(" ")
                        previous_move[2] = str(int(previous_move[2]) + 1)
                        new_move = ' '.join(previous_move)
                        node.movelist.append(new_move)
                    else:
                    	node.movelist.append(f"{car.name} + 1")

                    child = copy.deepcopy(Node(node.carlist, node.movelist))

                    if node.movelist[-1][-1] != '1':
                        changed_move = node.movelist.pop().split(" ")
                        changed_move[2] = str(int(changed_move[2]) - 1)
                        original_move = ' '.join(changed_move)
                        node.movelist.append(original_move)
                    else:
                        node.movelist.pop()

                    string = ""
                    for child_car in child.carlist:
                        string += str(child_car.name)
                        string += str(child_car.x)
                        string += str(child_car.y)

                    if string in self.visited:
                        pass
                    else:
                        self.visited.add(string)
                        self.queue.append(child)

                    # set y-coordinate back to value of node currently making children
                    car.y = car.y - 1

                # if space to the bottom of car availabe to move to, move 1 place to the bottom
                if car.y > 0 and self.board[car.y - 1][car.x] == 0:
                    car.y = car.y - 1

                    if len(node.movelist) > 0 and node.movelist[-1][0] == car.name:
                        previous_move = node.movelist.pop().split(" ")
                        previous_move[2] = str(int(previous_move[2]) + 1)
                        new_move = ' '.join(previous_move)
                        node.movelist.append(new_move)
                    else:
                    	node.movelist.append(f"{car.name} - 1")

                    child = copy.deepcopy(Node(node.carlist, node.movelist))

                    if node.movelist[-1][-1] != '1':
                        changed_move = node.movelist.pop().split(" ")
                        changed_move[2] = str(int(changed_move[2]) - 1)
                        original_move = ' '.join(changed_move)
                        node.movelist.append(original_move)
                    else:
                        node.movelist.pop()

                    string = ""
                    for child_car in child.carlist:
                        string += str(child_car.name)
                        string += str(child_car.x)
                        string += str(child_car.y)

                    if string in self.visited:
                        pass
                    else:
                        self.visited.add(string)
                        self.queue.append(child)

                    car.y = car.y + 1

if __name__ == '__main__':

    # keep prompting for file as long as incorrect file is provided
    valid_file = False
    while valid_file == False:

        # access parent directory
        directory = path.dirname(path.dirname(path.abspath(__file__)))

        # ask for input file
        input_name = input(f"Please enter the name of the input file: ")
        input_file = f"{directory}/Boards/Rushhour{input_name}.csv"

        # check if file exists otherwise reprompt
        if path.exists(input_file) == False:
            print("File does not exist")
        else:
            valid_file = True

    # get board dimensions from title of input file
    dimensions = int(re.search(r'\d+', input_name).group())

    # read into file, which holds data for cars in game
    with open(input_file) as input:
        reader = csv.reader(input, delimiter=',')
        row_count = 0
        carlist = []

        # iterate over rows in file
        for row in reader:

            # skip over header row
            if row_count != 0:

                # construct Car objects to be used in games
                x = int(row[2].strip(' "')) - 1
                y = int(row[3].strip('"')) - 1
                length = int(row[4].strip())
                direction = row[1].strip()
                car = Car(row[0], direction, x, y, length)

                # add Car object to carlist of game
                carlist.append(car)
            row_count += 1

    # root_node contains empty movelist
    movelist = []

    # construct root_node, which holds starting carlist
    root_node = Node(carlist, movelist)

    # construct BFS object
    algorithm = BFS(root_node, dimensions)

    # start the algorithm
    algorithm.check()
