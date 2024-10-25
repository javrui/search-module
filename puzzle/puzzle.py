"""================================================================ JRM 2024.02
Puzzle solving script
===============================================================================
Sliding puzzle solver using search algorithms implementation from module 'search'

Sliding puzzle layouts must be utf-8 text file (.txt) to be supplied as
argument, where:
    - numbers separated by spaces,
    - numbers must appear one and only one time in file
    - one and only one non digit nor space character must be present, to
    represent the empty cell in the puzzle grid.

Both initial and goal puzzle layout files have to be provided as arguments
============================================================================"""

import sys
import os
from search import Node, SearchProblem


class SlidingPuzzle(SearchProblem):
    """
    Represents a sliding puzzle problem.

    This class inherits from the SearchProblem class and defines the necessary methods
    to solve a sliding puzzle using search algorithms.

    Attributes:
        <list any attributes here>
    """

    def __init__(self, initial_grid_filename, goal_grid_filename):
        """
        Initializes a SlidingPuzzle object.

        Args:
            initial_grid_filename (str): The name of the UTF-8 text file
            that defines the initial state of the sliding puzzle.
            goal_grid_filename (str): The name of the UTF-8 text file.
        """
        super().__init__()

        #self.blank_position = None # empty cell in the puzzle grid position
        #self.blank_char = blank_char # character representing empty cell in the puzzle grid
        self.num_grid_rows = None    #nr of rows in the puzzle grid
        self.num_grid_columns = None #nr of columns in the puzzle grid

        self.start_node = PuzzleNode()
        self.goal_node = PuzzleNode()

        self.offset = { "up":   (-1, 0), # up
                        "right":(0, 1), # right
                        "down": (1, 0), # down
                        "left": (0, -1) # left
        }


        # Read initial and goal grids from files
        self.start_node = PuzzleNode(self.grid_from_file(initial_grid_filename))
        self.goal_node = PuzzleNode(self.grid_from_file(goal_grid_filename))

        # Grids sizes (rows and columns)
        self.num_grid_rows = len(self.start_node.state)
        self.num_grid_columns = len(self.start_node.state[0])

        # Check if initial and goal grids have the same size
        if self.num_grid_rows != len(self.goal_node.state) or \
            self.num_grid_columns != len(self.goal_node.state[0]):
            raise ValueError("Initial and goal grids must have the same size")

        # Check same tiles in initial and goal grids:
        initial_numbers = set(elem for row in self.start_node.state for elem in row)
        goal_numbers = set(elem for row in self.goal_node.state for elem in row)
        if initial_numbers != goal_numbers:
            raise ValueError("Initial and goal grids must have the same tiles")


    def grid_from_file(self, filename):
        """Reads a grid from a file and returns a list of lists representing the grid.

        Blank tile is any not number nor space character.
        """

        # Read file
        try:
            with open(filename, encoding="utf-8") as f:
                contents = f.read()
        except FileNotFoundError:
            sys.exit(f"File '{filename}' not found.")


        # Set to store all stuff read from file (cleaning spaces, '\n', etc.)
        tiles = set(contents.split())
        numeric_tiles = set([x for x in tiles if x.isdigit()])
        blank_char = tiles - numeric_tiles

        # Check: Blank tile character must appear one and only one time in file
        if len(blank_char) != 1:
            raise ValueError("Blank character must appear one and only one time in file")

        # Check: All other elements must be numbers:
        if numeric_tiles == set():
            raise ValueError("All elements must be numbers or blank character")

        # Check: All lines must have the same number of elements
        for line in contents:
            if len(line) != len(contents[0]):
                raise ValueError("All lines must have the same number of elements")
        # Check: tile values only appear once in file
        numbers_in_file = [int(n) for n in contents.split() if n.isdigit()]
        nr_numbers_in_file = len(numbers_in_file)
        nr_distinct_numbers_in_file = len(set(numbers_in_file))

        if nr_numbers_in_file != nr_distinct_numbers_in_file:
            raise ValueError("All numbers must be distinct in puzzle")

        #return list of lists representing the grid
        return [line.split() for line in contents.splitlines()]


    def show_solution(self):
        """Prints the solution to the sliding puzzle problem."""

        print(100*'=')
        print(f"Puzzle initial state:\n{self.start_node}")
        print(f"\nPuzzle goal state:\n{self.goal_node}")
        print(100*'=')

        if self.solution:
            print(self.start_node)
            for nd in self.solution:
                print(nd)
            print(f"Solution steps: {len(self.solution)} "
                    f"({len(self.explored_nodes)} nodes tried)")
        else:
            print("\nNo Solution found!")


class PuzzleNode(Node):
    """ Node is mainly grid state, also parent node and action that lead to it."""

    def __init__(self, state=None, parent=None, action=None):
        """Initializes a PuzzleNode object.

        Args:
            state (list of lists, optional): The state of the puzzle grid.
            parent (PuzzleNode, optional): The parent node of the current node.
            action (str, optional): The action that led to the current node.
        """
        super().__init__(state=None, parent=parent, action=action)
        if state:
            self.state = [row[:] for row in state]


    def actions(self, search_problem:SearchProblem):
        """List of valid blank cell movements (actions) to occupy contiguous cells."""

        valid_actions = []      # directions blank cell can 'move' to

        blank_row, blank_col = self.blank_position()
        # Blank new position after action (movement):
        blank_after = {  "up": (blank_row - 1, blank_col), # up
                            "right": (blank_row, blank_col + 1), # right
                            "down": (blank_row + 1, blank_col), # down
                            "left": (blank_row, blank_col - 1) # left
        }

        for action, blank_new_pos in blank_after.items():
            b_row, b_column = blank_new_pos

            if  (0 <= b_row < search_problem.num_grid_rows) and \
                (0 <= b_column < search_problem.num_grid_columns):
                valid_actions.append(action)
        #print(f">> {valid_actions=}\n") #DBG

        return valid_actions


    def result (self, action, search_problem: SearchProblem):
        """Returns the node that results from performing 'action' on self.

        Calculates blank new position and swaps it with the tile in that position.
        """
        blank_row, blank_col = self.blank_position()
        blank_new_positions = { "up": (blank_row - 1, blank_col),   # up   (row - 1, column)
                                "right": (blank_row, blank_col + 1),   # right(row, column + 1)
                                "down": (blank_row + 1, blank_col),   # down (row + 1, column)
                                "left": (blank_row, blank_col - 1)}   # left (row, column - 1)

        if action not in blank_new_positions:
            raise ValueError(f"Invalid action: {action}")

        # Positions of the blank cell and moving cell
        blank_old_position = self.blank_position()
        blank_new_position = blank_new_positions[action]

        # Set new value in blank old position
        row, col = blank_new_position
        moving_tile_value = self.state[row][col]

        new_node = PuzzleNode(state=self.state, action=action, parent=self)
        row, col = blank_old_position
        new_node.state[row][col] = moving_tile_value

        # Set blank in blank new position
        row, col = blank_new_position
        new_node.state[row][col] = '_'

        return new_node


    def __repr__(self) -> str:
        """Simple view showing just state."""
        return '\n'.join(' '.join(sublist) for sublist in self.state) + '\n'


    def blank_position(self):
        """Returns the position of the blank cell in the grid, assuming as
        blank any non-digit character."""

        for row_idx, sublist in enumerate(self.state):
            for col_idx, elem in enumerate(sublist):
                if not elem.isdigit():
                    return (row_idx, col_idx)

        raise ValueError(f"Blank cell not found in node: {self}") # Blank cell not found


if __name__ == '__main__':

    PUZZLE_DIRECTORY = "puzzles"
    puzzle_file_path = []
    for arg_nr in range(1, 3):
        puzzle_filename = sys.argv[arg_nr]
        puzzle_file_path.append(os.path.join(PUZZLE_DIRECTORY, puzzle_filename))
        if not os.path.exists(puzzle_file_path[arg_nr-1]):
            print(f"File '{puzzle_filename}' not found in directory '{PUZZLE_DIRECTORY}'")
            sys.exit(1)
    initial_grid_filename_arg = puzzle_file_path[0]
    goal_grid_filename_arg = puzzle_file_path[1]

    puzzle = SlidingPuzzle(initial_grid_filename_arg, goal_grid_filename_arg)

    for algorithm in ['BSF', 'DSF', ]:
        try:
            puzzle.solve(algorithm, audit_trail=True)
        except ValueError as e:
            print(e)
            sys.exit(1)
        else:
            print(100*'=')
            print(f"Solving SlidingPuzzle with {algorithm} algorithm...")
            puzzle.show_solution()

            print(100*'=')
            print("Algorithm steps:")
            puzzle.audit_trail.show()
