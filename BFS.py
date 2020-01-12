from cars.py import Board


class Node():
    """ create node for algorithm"""

    def __init__(self, carlist):
        self.carlist = carlist

    # def connection(self):

class Bfs():
    """ BFS algorithm"""

    def __init__(self, start_node):
        self.queue = []
        self.visited_list = []
        self.start_node = start_node
        self.dimensions = Board.dimensions
        self.filled_board = Board.filled_board()
        self.board = Board.board
        

    def search(self, node):

        if self.won(node) == True:
            return node
        
        children = self.get_children(node)
        self.queue.append(children)
        self.queue.pop(node)
        self.visited_list.append(node)

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


    # search(Node(carlist))

    def add_children(self, node):
        
        for car in node.carlist:

            original_carlist = node.carlist
            original_car = car

            if car.direction == "H":

                if original_car.x < (self.dimensions - car.length) and self.board[original_car.y][original_car.x + car.length] == 0:
                    car.x = car.x + 1
                    child = Node()  

                if original_car.x > 0 and self.board[original_car.y][original_car.x - 1] == 0:
                    car.x = car.x - 1
            
            if car.direction == "V":

                if original_car.y < (self.dimensions - car.length) and self.board[original_car.y + car.length][original_car.x] == 0:
                    car.y = car.y + 1

                if original_car.y > 0 and self.board[original_car.y - 1][original_car.x] == 0:
                    car.y = car.y - 1
            

    
    def algorithm(self):
        




        
