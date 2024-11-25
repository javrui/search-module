"""================================================================ JRM 2024.02
Python script that shows maze exploring and solving using 'search' module

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
import os
import time
import curses
from search import Node, SearchProblem


class Maze(SearchProblem):
    """Defines a maze object to be solved by search algorithms."""

    def __init__(self, filename, start_char='A', goal_char='B',
                 path_char=' '):
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
        self.start_char = start_char # start point character in maze file
        self.goal_char = goal_char  # end point character in maze file
        self.open_path_char = path_char # open path character in maze file

        # Maze layout in maze FILE: (True value -> wall, False value -> open path))
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

        # Solution and exploration layout elements for curses:
        self.layout_elements = {
            'walls':{'char':'█', 'color':243, 'wait':0},
            'exploration':{'char':'·', 'color':208, 'wait':0.01},
            'solution':{'char':'¤', 'color':118, 'wait':0.05},
            'start_goal':{'char':'_', 'color':7, 'wait':0.1},
            }

        # dictionary to store maze exploration and solution layout for curses
        self.maze_solution_layout = None

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
                    elif contents[i][j] == self.open_path_char:
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)

            self.walls.append(row)

    def show_solution(self):
        self._calculate_maze_and_solution_layout_elements()

        try:
            curses.wrapper(lambda stdscr: self._show_dynamic_solution(stdscr))
            return True
        except Exception:
            print("Error showing dynamic solution.\n")
            # Checks terminal size fits needed space for maze and info:
            (term_width, term_height) = os.get_terminal_size()

            display_height = 9 + self.height
            display_width = max(self.width +6, 26, 12+ len(self.filename))

            if display_height > term_height:
                print(f"Terminal height ({term_height}) < diplay height needed ({display_height})")
                print("Please, resize terminal, or try static solution instead.\n")

            if display_width > term_width:
                print(f"Terminal width ({term_width}) < diplay width needed ({display_width})")
                print("Please, resize terminal, or try static solution instead.\n")

            return False

    def _show_dynamic_solution(self, stdscr):

        self._set_curses_settings(stdscr)

        try:
            # Print Summary:
            stdscr.addstr(1, 2, f"- Solving: {self.filename}")
            stdscr.addstr(2, 2, f"- Algorithm: {self.algorithm}")

            expl_char = self.layout_elements['exploration']['char']
            sol_char = self.layout_elements['solution']['char']

            stdscr.addstr(3, 2, str(
                f"- Explored nodes ({expl_char}, {sol_char}): "
                f"{len(self.explored_nodes)}"
                ))

            stdscr.addstr(4, 2, str(
                f"- Solution nodes ({sol_char}): "
                f"{len(self.solution) if self.solution else '-'}"
                ))

            if self.solution is None:
                show_elements = ['walls', 'start_goal', 'exploration', 'start_goal']

                stdscr.addstr(5, 2, str(
                    "- Solution: No Solution found!"
                    f"{len(self.solution) if self.solution else '-'}"
                    ))
            else:
                show_elements = ['walls', 'start_goal', 'exploration', 'start_goal','solution', 'start_goal']

                stdscr.addstr(5, 2, "- Solution:")
                stdscr.addstr(7, 2, "")

            # Print layout:
            for element_name in show_elements:
                for (y, x, char) in self.maze_solution_layout[element_name]:

                    time.sleep(self.layout_elements[element_name]['wait'])

                    color = curses.color_pair(self.layout_elements[element_name]['color'])

                    stdscr.addch(y+7, x+6, char, color)
                    stdscr.refresh()

            # Print the end message
            stdscr.addstr(8+self.height, 2, "Press any key to exit")
            stdscr.refresh()
            # Wait for a key press to exit
            stdscr.getch()

        except KeyboardInterrupt:
            pass  # Handle Ctrl+C gracefully

    def _set_curses_settings(self, stdscr):
        # Disable cursor and enable instant character echoing
        curses.curs_set(0)
        # Blocking mode. getch() waits indefinitely for a key press.
        stdscr.timeout(-1)
        # Set the color pairs
        self._set_colors()
        stdscr.clear()

    def _set_colors(self):
        if not curses.has_colors():
            raise RuntimeError("Your terminal does not support colors.")

        curses.start_color()

        try:
            for _, components in self.layout_elements.items():
                curses.init_pair(components['color'], components['color'], curses.COLOR_BLACK)
        except curses.error:
            print("Error initializing color pairs. Ensure your terminal supports colors.")
            sys.exit(1)

    def _calculate_maze_and_solution_layout_elements(self):

        # Define the maze layout for curses
        maze_walls = [
            (x, y, self.layout_elements['walls']['char'] if brick else ' ')
            for x, row in enumerate(self.walls)
            for y, brick in enumerate(row)
        ]

        # Start and goal nodes for curses
        maze_start_goal = [self.start_node.state + ('A',), self.goal_node.state + ('B',)]

        # Exploration path for curses
        maze_exploration = []
        for record in self.algorithm_log.get_log()[1:]:
            x, y = record['extracted'].state
            maze_exploration.append((x, y,
                self.layout_elements['exploration']['char']))

        # Solution path for curses
        maze_solution = []
        if self.solution is not None:
            for node in self.solution:
                x, y = node.state
                maze_solution.append((x, y,
                    self.layout_elements['solution']['char']))

        # Layout elements dict
        maze_solution_layout = {
            'walls': maze_walls,
            'start_goal': maze_start_goal,
            'exploration': maze_exploration,
            'solution': maze_solution,
            }

        self.maze_solution_layout = maze_solution_layout

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
        sys.exit("Usage: python3 maze.py <path to utf-8 .txt maze layout file>")
    maze_filename = sys.argv[1]

    maze = Maze(maze_filename)
    maze.solve('BFS')

    if maze.show_solution():
        maze.solve('DFS')
        maze.show_solution()

