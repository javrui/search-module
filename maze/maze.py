"""================================================================ JRM 2024.02
Python script that finds maze exit using 'search' module

Usage:
    python3 maze.py <maze .txt file path>

Dependencies:
    search module

===============================================================================
Maze layout must be utf-8 text file (.txt) to be supplied as argument, where:
    - space characters form open paths
    - walls are any character except 'start_char' or 'goal_char' (see vars)
    - 'start_char' is the start point and 'goal_char' is the goal point
============================================================================"""

import sys
from search import Node, SearchProblem

class Maze(SearchProblem):
    """Defines a maze object to be solved by search algorithms."""

    def __init__(self, filename, start_char='A', goal_char='B',
                 path_char=' ', solution_char='*', explored_char = '·'):
        """Reads maze definition (including and initial and goal states) from
        utf-8 file 'filename' to initialize a maze object.

        Args:
            filename (str): name of utf-8 text file .txt defining maze
        """
        super().__init__()

        # name of utf-8 text file defining maze
        self.filename = filename

        # Characters thar define maze in file.txt
        # (wall_character = any other character in file)
        self.start_char = start_char # start_char = start point character in file
        self.goal_char = goal_char  # goal_char = end point character in file

        self.path_char = path_char # path_char = open path character in file

        # Solution path and explored nodes
        self.solution_char = solution_char  # character to mark solution path
        self.explored_char = explored_char  # character to mark explored nodes

        # Maze layout: (True value -> wall, False value -> open path))
        self.walls = []

        self.height = None      # Number of rows in the maze
        self.width = None       # Number of columns in the maze
        self.walls = None       # walls in the maze as boolean list of lists

        # offset: dictionary to calculate new position after action (movement)
        self.offset = { "up":   (-1, 0), # up
                        "right":(0, 1), # right
                        "down": (1, 0), # down
                        "left": (0, -1) # left
        }

        self._load_maze_from_file()

    def _load_maze_from_file(self):
        """."""
        # Read file and check start and goal points exist
        try:
            with open(self.filename, encoding="utf-8") as f:
                contents = f.read()
        except FileNotFoundError:
            sys.exit(f"File '{self.filename}' not found.")

        if contents.count(self.start_char) != 1:
            raise ValueError("maze must have exactly one start point")
        if contents.count(self.goal_char) != 1:
            raise ValueError("maze must have exactly one goal")

        # Define height and width of maze (ignores empty lines)
        contents = [line for line in contents.splitlines()
                    if line.strip('\n')]
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        self.walls = []
        # Creates wall values
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == self.start_char:
                        self.start_node = MazeNode(state=(i, j))
                        row.append(False)
                    elif contents[i][j] == self.goal_char:
                        self.goal_node = MazeNode(state=(i, j))
                        row.append(False)
                    elif contents[i][j] == self.path_char:
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)

            self.walls.append(row)

    def show_solution(self):
        """Prints the maze and its solution.
        Returns:
            Maze layout and solution as string.
        """

        # Generate maze layout, with solution path if exists
        string = "\n"
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                position = (i, j)
                if col:
                    string += "█"
                elif position == self.start_node.state:
                    string += self.start_char
                elif position == self.goal_node.state:
                    string += self.goal_char
                elif self.solution and position in self.solution:
                    string += self.solution_char
                elif self.solution and position in self.explored_nodes:
                    string += self.explored_char
                else:
                    string += self.path_char
            string += '\n'

        print(30*'-')
        print(f"- Solving: {self.filename}")
        print(f"- Algorithm: {self.algorithm}")
        print(
            f"- Explored nodes ({self.explored_char}, {self.solution_char}): "
            f"{len(self.explored_nodes)}"
        )
        print(
            f"- Solution nodes ({self.solution_char}): "
            f"{len(self.solution) if self.solution else '-'}"
        )

        if self.solution is None:
            print("- Solution: No Solution found!")
        else:
            print("- Solution:")
        print(string)

        return string # in case we want to use it in a GUI

    def show_algorithm_steps(self):
        if self.algorithm_log.not_empty():
            print("- Algorithm steps:")
            self.algorithm_log.show_log()


class MazeNode(Node):
    """ Node is mainly the position in the maze. Also previous position +
    direction taken to get there (those last 2 only used sparsely)
    """

    def actions(self, search_problem:SearchProblem):
        """List of valid movements (actions) to occupy contiguous cells."""

        valid_actions = []      # directions blank cell can 'move' to

        # these are all possible movements regardless of actual position
        initial_row, initial_col = self.state
        moved = {action: search_problem.offset [action] for action in search_problem.offset.keys()}

        # we choose the ones really possible considering position
        for action, (row_offset, col_offset) in moved.items():
            new_row = initial_row + row_offset
            new_col = initial_col + col_offset
            if (0 <= new_row < search_problem.height) \
                and (0 <= new_col < search_problem.width) \
                and not search_problem.walls[new_row][new_col]:
                valid_actions.append(action)

        return valid_actions

    def result (self, action, search_problem:SearchProblem):
        """Returns the node that results from performing 'action' on self.

        Calculates new position in maze.
        """
        initial_row, initial_col = self.state

        if action not in search_problem.offset:
            raise ValueError(f"Invalid action: {action}")

        new_position = (initial_row + search_problem.offset[action][0],# row
                        initial_col + search_problem.offset[action][1])# column

        return MazeNode(state=new_position, parent=self, action=action)

    def __repr__(self) -> str:
        """Simple view omitting details"""
        return f"{self.state}'{self.action}'"


if __name__ == '__main__':
    # Test for maze.py

    if len(sys.argv) != 2:
        sys.exit("Usage: python maze.py <path to utf-8 .txt maze layout file>")

    maze_filename = sys.argv[1]
    maze = Maze(maze_filename)

    maze.solve('BFS', keep_algorithm_log=False)
    maze.show_solution()
    maze.show_algorithm_steps()

    maze.solve('DFS', keep_algorithm_log=True)
    maze.show_solution()
    maze.show_algorithm_steps()
