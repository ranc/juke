import board
import car
import helper
from board import Board


class Game:
    """
    Add class description here
    """

    def __init__(self, board):
        """
        Initialize a new Game object.
        :param board: An object of type board
        """
        self.board = board
        self.cars_in_board = {}  # we need to keep track of cars to kow if the car have reached the target
        car_dict = helper.load_json('car_config.json')

        for name, (l, loc, _dir) in car_dict.items():
            new_car = car.Car(name, l, loc, _dir)  # create the car from details
            self.board.add_car(new_car)
            self.cars_in_board[name] = new_car

    def __single_turn(self) -> bool:
        """
                Note - this function is here to guide you and it is *not mandatory*
                to implement it.

                The function runs one round of the game :
                    1. Get user's input of: what color car to move, and what
                        direction to move it.
                    2. Check if the input is valid.
                    3. Try moving car according to user's input.

                Before and after every stage of a turn, you may print additional
                information for the user, e.g., printing the board. In particular,
                you may support additional features, (e.g., hints) as long as they
                don't interfere with the API.
                :return: True - stop the game, False - Continue to play
                """
        print(self.board)
        dirs = ['u', 'd', 'l', 'r']
        print("what color car to move, and what direction to move it?")
        inp = input().split(',')
        if inp[0] == '!':
            print("bye bye...")
            return True  # break
        if len(inp) != 2:
            print("please supply two arguments: Car Name, direction")
            return False
        car_name = inp[0]
        if car_name not in self.cars_in_board:
            print(f"car name '{car_name}' not in board")
            return False

        move = inp[1].lower()
        if move not in dirs:
            print("please supply direction as: u,d,l,r")
            return False

        if not self.board.move_car(car_name, move):
            print("Invalid move, please try again")
            return False

        moved_car = self.cars_in_board[car_name]
        target_loc = self.board.target_location()
        for loc in moved_car.car_coordinates():
            if loc == target_loc:
                print(f"Congratulations! car {car_name} managed to find the exit!")
                return True

        return False

    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """
        while True:
            if self.__single_turn():
                return


if __name__ == "__main__":
    game = Game(Board())
    game.play()

