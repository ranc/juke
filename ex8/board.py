import copy
from typing import Dict

import car
import helper


class Board:
    """
    Add a class description here.
    Write briefly about the purpose of the class
    """
    car_dict: Dict[str, car.Car]
    SIZE = 7

    def __init__(self):
        # implement your code and erase the "pass"
        # Note that this function is required in your Board implementation.
        # However, is not part of the API for general board types.
        self.car_dict = {}
        self._update_board()

    def _update_board(self):
        """
        I chose to update the board by rebuilding it after each legal move,
        this is easier than just empty cells before and after each move
        :return:
        """
        # we need to use copy, else each row is repeated with the same instance.
        # if we use the '*' operator on mutable objects, they are duplicated by reference
        # (all copies points to the same location)
        self.board = [copy.copy(['_'] * Board.SIZE) for _ in range(Board.SIZE)]
        for cn, car in self.car_dict.items():
            for (r, c) in car.car_coordinates():
                if r < Board.SIZE and c < Board.SIZE:  # car can exit the board on the target coordinates
                    self.board[r][c] = cn

    def __str__(self):
        """
        This function is called when a board object is to be printed.
        :return: A string of the current status of the board
        """
        _str = '\n'.join("".join(row) for row in self.board[:3])
        _str += '\n'
        _str += "".join(self.board[3])+"-->\n"
        _str += '\n'.join("".join(row) for row in self.board[4:])
        return _str

    def cell_list(self):
        """ This function returns the coordinates of cells in this board
        :return: list of coordinates
        """
        # In this board, returns a list containing the cells in the square
        # from (0,0) to (6,6) and the target cell (3,7)
        list_coordinates = []
        for i in range(Board.SIZE):
            for j in range(Board.SIZE):
                list_coordinates.append((i, j))

        # The exit cell/target is added to the end
        list_coordinates.append(self.target_location())
        return list_coordinates

    def possible_moves(self):

        """ This function returns the legal moves of all cars in this board
        :return: list of tuples of the form (name,movekey,description) 
                 representing legal moves
        """
        # From the provided example car_config.json file, the return value could be
        # [('O','d',"some description"),('R','r',"some description"),('O','u',"some description")]
        pos_move = []
        for car_name, _car in self.car_dict.items():
            car_moves = _car.possible_moves()  # dict of move: desc
            for move, desc in car_moves.items():
                pos_move.append((car_name, move, car_name + ": " + desc))

        return pos_move

    def target_location(self):
        """
        This function returns the coordinates of the location which is to be filled for victory.
        :return: (row,col) of goal location
        """
        return Board.SIZE // 2, Board.SIZE

    def cell_content(self, coordinate):
        """
        Checks if the given coordinates are empty.
        :param coordinate: tuple of (row,col) of the coordinate to check
        :return: The name if the car in coordinate, None if empty
        """
        if not self._legal_cell(coordinate):
            return False  # error
        row, col = coordinate
        cell = self.board[row][col]
        if cell == '_':
            return None
        return cell

    def add_car(self, car):
        # Remember to consider all the reasons adding a car can fail.
        # You may assume the car is a legal car object following the API.
        # implement your code and erase the "pass"

        self.car_dict[car.get_name()] = car
        list_coor_car = car.car_coordinates()
        for cor in list_coor_car:
            if self.cell_content(cor) is not None:
                return False
        for (r, c) in list_coor_car:
            self.board[r][c] = car.get_name()

        return True

    def move_car(self, name, movekey) -> bool:
        """
        moves car one step in given direction.
        :param name: name of the car to move
        :param movekey: Key of move in car to activate
        :return: True upon success, False otherwise
        """

        if name not in self.car_dict:
            return False
        car = self.car_dict[name]  # the details of the car

        for cell in car.movement_requirements(movekey):
            if cell != self.target_location() and self.cell_content(cell) is not None:  # cell is not empty or illegal
                return False
        # move is allowed from board perspective
        if car.move(movekey):
            self._update_board()
            return True
        return False

    @staticmethod
    def _legal_cell(cell):
        r, c = cell
        if r < 0 or c < 0:
            return False
        if r >= Board.SIZE or c >= Board.SIZE:
            return False
        return True
