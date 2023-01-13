from collections import Counter


class Grid:

    digits = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    # initialise the grid and length of each row and column
    def __init__(self, current_grid):
        self.current_grid = current_grid
        self.length = len(current_grid)

    # create lists of all the digits in the corresponding row, column or box
    def rowList(self, row_index):
        row_keys = [(row_index, col_index) for col_index in range(9)]
        return [self.current_grid[key][0] for key in row_keys]

    def colList(self, col_index):
        col_keys = [(row_index, col_index) for row_index in range(9)]
        return [self.current_grid[key][0] for key in col_keys]

    def boxList(self, index):
        box_row = index[0] // 3
        box_col = index[1] // 3
        box_list = [
            self.current_grid[(row, col)][0]
            for row in range(box_row * 3, box_row * 3 + 3)
            for col in range(box_col * 3, box_col * 3 + 3)
        ]
        return box_list

    # check if a digit can be placed in a particular square on the grid
    def checkDigit(self, digit, index):
        if (
            self.checkRow(digit, index[0])
            and self.checkCol(digit, index[1])
            and self.checkBox(digit, index)
        ):
            return True
        return False

    def checkRow(self, digit, row_index):
        row_list = self.rowList(row_index)
        if Counter(row_list)[digit] >= 2:
            return False
        else:
            return True

    def checkCol(self, digit, col_index):
        col_list = self.colList(col_index)
        if Counter(col_list)[digit] >= 2:
            return False
        else:
            return True

    def checkBox(self, digit, index):
        box_list = self.boxList(index)
        if Counter(box_list)[digit] >= 2:
            return False
        else:
            return True

    # check if any digit after the current one can be placed in a particular square on the grid
    def checkSquare(self, fromDigit, index):
        for digit in self.digits[fromDigit:]:
            self.current_grid[index] = [digit, False]
            if self.checkDigit(digit, index):
                return digit
        return 0

    def solve(self):
        current_square = 0
        current_digit = 0
        # iterate over all the indices
        while current_square != self.length:
            square_index = list(self.current_grid.keys())[current_square]
            # check if the square is fixed
            if not self.current_grid[square_index][1]:
                digit_added = False
                # check if we can add a digit to the square
                poss_digit = self.checkSquare(current_digit, square_index)
                # if there is a possible digit add it to the grid
                if poss_digit != 0:
                    digit_added = True
                    self.current_grid[square_index][0] = poss_digit
                    current_square += 1
                    current_digit = 0
                # if we were not able to we have to backtrack
                if not digit_added:
                    # set the current square to 0 as it still needs to be solved
                    self.current_grid[square_index][0] = 0
                    # go back one index
                    current_square -= 1
                    # keep going back until we reach a square we can change
                    while self.current_grid[
                        list(self.current_grid.keys())[current_square]
                    ][1]:
                        current_square -= 1
                    # start checking from this new square from digits after the current ones to avoid rechecking
                    new_square_index = list(self.current_grid.keys())[current_square]
                    current_digit = self.current_grid[new_square_index][0]

            else:
                current_square += 1

        print(self)

    # output the grid in a somewhat nice format
    def __str__(self):
        final_string = ""
        for row_index in range(9):
            new_line = ""
            if row_index in [3, 6]:
                final_string += " ------+-------+------\n"
            for col_index in range(9):
                if col_index in [3, 6]:
                    new_line += " |"
                new_line += f" {self.current_grid[(row_index, col_index)][0]}"
            new_line += "\n"
            final_string += new_line
        return final_string


def main():
    useSolver = input("Would you like to use the sudoku solver? y/n ")
    while useSolver not in ["y", "n"]:
        useSolver = input("That is not a valid input. Press y to use and n to quit: ")
    if useSolver == "n":
        quit()
    else:
        sudoku_input = []
        row_names = [
            "First",
            "Second",
            "Third",
            "Fourth",
            "Fifth",
            "Sixth",
            "Seventh",
            "Eighth",
            "Ninth",
        ]
        print(
            "Please enter your sudoku, use a 0 to indicate an empty square and leave a space between digits"
        )

        for row_name in row_names:
            row_input = input(f"{row_name} Row: ")
            row_list = list(map(int, row_input.split(" ")))

            while len(row_list) != 9:
                row_input = input(
                    f"Incorrect number of values given. Please try again.\n{row_name} Row: "
                )
                row_list = list(map(int, row_input.split(" ")))

            while not set(row_list).issubset([x for x in range(10)]):
                row_input = input(
                    f"One or more values was not a digit from 0 to 9. Please try again.\n{row_name} Row: "
                )
                row_list = list(map(int, row_input.split(" ")))

            else:
                sudoku_input.append(row_list)

    sudoku_dict = {}
    for row_index, row in enumerate(sudoku_input):
        for col_index, square in enumerate(row):
            sudoku_dict[(row_index, col_index)] = [square, square != 0]

    print()
    print("SOLUTION:")
    print()
    sudoku_grid = Grid(sudoku_dict)
    sudoku_grid.solve()


if __name__ == "__main__":
    main()


"""
trial sudoku

[
            [
                0,
                3,
                0,
                0,
                1,
                2,
                0,
                5,
                0,
            ],
            [
                0,
                7,
                0,
                0,
                0,
                0,
                8,
                0,
                0,
            ],
            [
                8,
                0,
                0,
                0,
                3,
                0,
                0,
                0,
                4,
            ],
            [
                0,
                8,
                4,
                0,
                0,
                0,
                0,
                0,
                6,
            ],
            [
                0,
                0,
                0,
                9,
                5,
                0,
                0,
                0,
                0,
            ],
            [
                0,
                0,
                0,
                0,
                0,
                0,
                9,
                7,
                3,
            ],
            [
                2,
                0,
                0,
                6,
                0,
                0,
                4,
                0,
                7,
            ],
            [
                0,
                0,
                0,
                0,
                0,
                5,
                0,
                0,
                1,
            ],
            [
                1,
                6,
                9,
                0,
                0,
                8,
                0,
                2,
                0,
            ],
        ]

"""
