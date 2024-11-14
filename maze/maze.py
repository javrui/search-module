"""================================================================ JRM 2024.02
Python script that finds maze exit using search algorithms


Usage:
    python3 maze.py <maze .txt file path>

Dependencies:
    search module





Algorithm implemented:

• Start with a frontier that contains the initial state.
• Start with an empty explored set.
• Repeat:
    • If the frontier is empty, then no solution.
    • Remove a node from the frontier.
    • If node contains goal state, return the solution.
    • Add the node to the explored set.
    • Expand node
    • Add resulting nodes to the frontier if they aren't already in the frontier or the explored set.


===============================================================================
Maze layout must be utf-8 text file (.txt) to be supplied as argument, where:
    - space characters form open paths
    - walls are any character except 'start_char' or 'goal_char' (see vars)
    - 'start_char' is the start point and 'goal_char' is the goal point
============================================================================"""

import sys
import os
from search import Node, SearchProblem


class Maze(SearchProblem):
    """Defines a maze object to be solved by search algorithms."""

    def __init__(self, filename, start_char='A', goal_char='B',
                 path_char=' ', solution_char='*', frontier_char='F',
                 explain=False):
        """Reads maze definition (including and initial and goal states) from
        utf-8 file 'filename' to initialize a maze object.

        Args:
            filename (str): name of utf-8 text file .txt defining maze
        """
        super().__init__()

        #----------------------------------------------------------------------
        # Attributes specific to Maze:
        #----------------------------------------------------------------------

        self.height = None      # Number of rows in the maze
        self.width = None       # Number of columns in the maze
        self.walls = None       # walls in the maze as boolean list of lists

        # offset: dictionary to calculate new position after action (movement)
        self.offset = { "up":   (-1, 0), # up
                        "right":(0, 1), # right
                        "down": (1, 0), # down
                        "left": (0, -1) # left
        }

        # Characters thar define maze in file.txt
        # wall_character = any other character in file
        self.start_char = start_char # start_char = start point character in file
        self.goal_char = goal_char  # goal_char = end point character in file
        self.path_char = path_char # path_char = open path character in file

        self.solution_char = solution_char  # solution_char = character to mark solution path
        self.frontier_char = frontier_char  # goal_char = end point character in file

        self.explain = explain  # Print explanations of the search process

        #----------------------------------------------------------------------
        # Read file and check start and goal points exist
        #----------------------------------------------------------------------
        try:
            with open(filename, encoding="utf-8") as f:
                contents = f.read()
        except FileNotFoundError:
            sys.exit(f"File '{filename}' not found.")

        if contents.count(self.start_char) != 1:
            raise ValueError("maze must have exactly one start point")
        if contents.count(self.goal_char) != 1:
            raise ValueError("maze must have exactly one goal")


        #----------------------------------------------------------------------
        # Define height and width of maze (ignores empty lines)
        #----------------------------------------------------------------------
        contents = [line for line in contents.splitlines() if line.strip('\n')]

        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        #----------------------------------------------------------------------
        # Define
        #   - walls (list of lists of booleans (wall present -0 True)
        #   - start_node and goal_node
        #----------------------------------------------------------------------
        self.walls = []
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
                except IndexError:      # Admits lines shorter than the longest
                    row.append(False)

            self.walls.append(row)


    def show_solution(self):
        """Prints the maze and its solution. Also returns it as string"""

        if self.solution is None:
            print("No Solution found!")


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
                    string += '·'
                else:
                    string += self.path_char
            string += '\n'

        print("Nodes Explored: ", self.nodes_explored)
        print(string)

        return string # in case we want to use it in a GUI


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
        sys.exit("Usage: python maze.py <utf-8 maze file (.txt)>")

    maze_filename = sys.argv[1]
    MAZE_DIRECTORY = "mazes"
    maze_file_path = os.path.join(MAZE_DIRECTORY, maze_filename)

    if not os.path.exists(maze_file_path):
        print(f"File '{maze_filename}' not found in directory '{MAZE_DIRECTORY}'")
        sys.exit(1)

    maze = Maze(maze_file_path, explain=False)

    for algorithm in ['BSF', 'DSF', ]:
        try:
            maze.solve(algorithm, audit_trail=True)
        except ValueError as e:
            print(e)
            sys.exit(1)
        else:
            print(f"\nSolving maze '{maze_filename}' with {algorithm} algorithm:")
            maze.show_solution()

            print(100*'=')
            print("Algorithm steps:")
            maze.audit_trail.show()
