VERTICAL = 0
HORIZONTAL = 1


class Car:
    """
    Add class description here
    """

    def __init__(self, name, length, location, orientation):
        """
        A constructor for a Car object
        :param name: A string representing the car's name
        :param length: A positive int representing the car's length.
        :param location: A tuple representing the car's head (row, col) location
        :param orientation: One of either 0 (VERTICAL) or 1 (HORIZONTAL)
        """
        self.name = name
        self.length = length
        self.location = tuple(location)
        self.orientation = orientation
        # Note that this function is required in your Car implementation.
        # However, is not part of the API for general car types.
        # implement your code and erase the "pass"

    def car_coordinates(self):
        list_coor = []
        if self.orientation == VERTICAL:
            for i in range(self.length):
                t = (self.location[0] + i, self.location[1])
                list_coor.append(tuple(t))
        else:
            for j in range(self.length):
                t = (self.location[0], self.location[1] + j)
                list_coor.append(tuple(t))

        """
        :return: A list of coordinates the car is in
        """
        return list_coor

    def possible_moves(self):
        """
        :return: A dictionary of strings describing possible movements permitted by this car.
        """
        # For this car type, keys are from 'udrl'
        # The keys for vertical cars are 'u' and 'd'.
        # The keys for horizontal cars are 'l' and 'r'.
        # You may choose appropriate strings.
        # implement your code and erase the "pass"
        # The dictionary returned should look something like this:
        # result = {'f': "cause the car to fly and reach the Moon",
        #          'd': "cause the car to dig and reach the core of Earth",
        #          'a': "another unknown action"}
        # A car returning this dictionary supports the commands 'f','d','a'.

        r = {}
        if self.orientation == VERTICAL:
            r.update({'u': "car can move one step up"})
            r.update({'d': "car can move one step down"})
        elif self.orientation == HORIZONTAL:
            r.update({'l': "car can move one step left"})
            r.update({'r': "car can move one step right"})
        return r

    def movement_requirements(self, movekey):
        """ 
        :param movekey: A string representing the key of the required move.
        :return: A list of cell locations which must be empty in order for this move to be legal.
        """
        # For example, a car in locations [(1,2),(2,2)] requires [(3,2)] to
        # be empty in order to move down (with a key 'd').
        moves = {
            'u': lambda: [(self.location[0] - 1, self.location[1])] if self.orientation == VERTICAL else [],
            'd': lambda: [(self.location[0] + self.length, self.location[1])] if self.orientation == VERTICAL else [],
            'l': lambda: [(self.location[0], self.location[1]-1)] if self.orientation == HORIZONTAL else [],
            'r': lambda: [(self.location[0], self.location[1]+self.length)] if self.orientation == HORIZONTAL else [],
        }
        return moves[movekey]()

    def move(self, movekey) -> bool:
        """
        :param movekey: A string representing the key of the required move.
        :return: True upon success, False otherwise
        """
        new_loc_moves = {
            'u': lambda: (self.location[0] - 1, self.location[1]) if self.orientation == VERTICAL else False,
            'd': lambda: (self.location[0] + 1, self.location[1]) if self.orientation == VERTICAL else False,
            'l': lambda: (self.location[0], self.location[1]-1) if self.orientation == HORIZONTAL else False,
            'r': lambda: (self.location[0], self.location[1]+1) if self.orientation == HORIZONTAL else False,
        }

        new_loc = new_loc_moves[movekey]()
        if not new_loc:
            return False

        self.location = new_loc
        return True

    def get_name(self):
        """
        :return: The name of this car.
        """
        return self.name
