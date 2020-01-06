import csv

# create 2d array

class Car():
    """ Make car objects """

    def __init__(self, carname, length):
        self.carname = carname
        self.length = length


class Board():

    def __init__(self, dimensions):
        self.dimensions = dimensions
        board = [[0 for x in range(dimensions)] for y in range(dimensions)]

        # open csv file
        with open('Rushhour6x6_1.csv') as input:
            reader = csv.reader(input, delimiter=',')
            row_count = 0

            # # remove spaces from elements
            # for row in reader:
            #     for element in row:
            #         element.strip()
            #         print(element)

            for row in reader:
                if row_count != 0:
                    car = Car(row[0], row[4])
                    x = int(row[2].strip(' "'))
                    y = int(row[3].strip('"'))
                    if row[1] == " H":
                        board[x - 1][y - 1] = row[0]
                        board[x][y - 1] = row[0]
                    else:
                        board[x - 1][y - 1] = row[0]
                        board[x - 1][y] = row[0]

                row_count += 1
        print(board)


if __name__ == '__main__':

    game  = Board(6)
