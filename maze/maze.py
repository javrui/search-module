"""================================================================ JRM 2024.02
Python script that finds maze exit using 'search' module and shows path.

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
        self.start_char = start_char # start_char = start point character in file
        self.goal_char = goal_char  # goal_char = end point character in file
        self.path_char = path_char # path_char = open path character in file

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

        # For dynamic solutions, if the first solution has been shown
        self.first_dynamic_solution_shown = False

        # Solution and exploration layout elements:
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
                    elif contents[i][j] == self.path_char:
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)

            self.walls.append(row)

    def show_solution(self, dynamic=False):
        """Prints the maze and its solution.
        dynamic = True if you want to see the solution step by step.
        Returns: True if solution was shown, False otherwise.
        """
        if dynamic:
            self._calculate_maze_and_solution_layout_elements()

            offset = self._check_terminal_size()
            if offset is (0, 0):
                return False
            try:
                curses.wrapper(lambda stdscr:
                    self._show_dynamic_solution(stdscr, offset))
                return True
            except curses.error:
                print("Error showing dynamic solution.\n")
                return False
        else:
            for line in self._solution_summary_str():
                print(line)
            #print(self._solution_summary_str())
            print(self._solution_layout_str())
            return True

    def _check_terminal_size(self):
        """ Checks terminal space size needed to fit space for maze solution display.

        Display of two maze solutions (BFS and DFS) can be: "side to side" or "one below the other".
        Returns:
            (horizontal_offset, vertical_offset), where:
                horizontal_offset: minimum terminal width needed to display the two maze solutions.
                vertical_offset: minimum terminal height needed to display the two maze solutions.
            if terminal size is not enough, prints a message and returns (0, 0).

        """
        (term_width, term_height) = os.get_terminal_size()

        display_width = 2 + 2* max(self.width + 6, 29, 12 + len(self.filename))
        display_height = 1 + 2 * (9 + self.height)

        # Side to side layout if possible, otherwise one below the other
        if display_width < term_width:
            return (2 + max(self.width + 6, 29, 12 + len(self.filename)), 1)
        elif display_height < term_height:
            return (0, 1 + 9 * self.height)
        else:
            print(f"Terminal width ({term_width}) < display width needed ({display_width}) and" f"Terminal height ({term_height}) < display height needed ({display_height}).")
            print("Please, resize terminal, or try static solution instead.\n")
            return (0, 0)

    def _show_dynamic_solution(self, stdscr, offset):
        """ This method shows the maze solution step by step.
        Will be called twice (for BFS and DFS solutions). Second will be shown at right or below first, so that we need to know if the first solution has been shown (= this method has been called). Offset tells how much we need to move the second solution to the right or below the first one in terminal screen.
        """

        self._set_curses_settings(stdscr)

        # Offset in terminal display of solution to be printed

        if self.first_dynamic_solution_shown is False:
            offset = (0, 0)

        h_offs, v_offs = offset

        # To clarify expressions in .addch() and .addstr()
        # where blank lines are added
        BLANK_LINE = 1

        # Print Summary:
        start = 3 if self.first_dynamic_solution_shown else 2
        for line_count, line in enumerate(self._solution_summary_str()[start:], BLANK_LINE):
            stdscr.addstr(line_count + v_offs, 2 + h_offs, line)

        # Elements to show in layout:
        show_elements = ['walls', 'start_goal', 'exploration', 'start_goal']
        if self.solution is not None:
            show_elements += ['solution', 'start_goal']

        # Print layout:
        for element_name in show_elements:
            for (y, x, char) in self.maze_solution_layout[element_name]:

                time.sleep(self.layout_elements[element_name]['wait'])

                color = curses.color_pair(self.layout_elements[element_name]['color'])

                stdscr.addch(y + line_count + 2*BLANK_LINE + v_offs,
                                x + 6 + h_offs, char, color)
                stdscr.refresh()


        # Print "press key"
        if self.first_dynamic_solution_shown is True:
            line_count +=1

        stdscr.addstr(3*BLANK_LINE + line_count + self.height, 2 + h_offs, "Press any key.")
        stdscr.refresh()

        # Wait for a key press to exit
        stdscr.getch()
        # Delete "press key"
        stdscr.addstr(3*BLANK_LINE + line_count + self.height, 2 + h_offs, "              ")
        stdscr.refresh()

        self.first_dynamic_solution_shown = True

    def _set_curses_settings(self, stdscr):
        # Disable cursor and enable instant character echoing
        curses.curs_set(0)
        # Blocking mode. getch() waits indefinitely for a key press.
        stdscr.timeout(-1)
        # Set the color pairs
        self._set_colors()
        #stdscr.clear()

    def _set_colors(self):
        if not curses.has_colors():
            raise RuntimeError("Your terminal does not support colors.")

        try:
            curses.start_color()
            for _, components in self.layout_elements.items():
                curses.init_pair(components['color'], components['color'], curses.COLOR_BLACK)
        except curses.error:
            raise RuntimeError("Error initializing color pairs. Ensure your terminal supports colors.")

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

    def _solution_summary_str(self):
        """ Generates and returns a summary of solution data as string"""

        sol = " No Solution found!" if self.solution is None else ""

        lines=[
            "",
            f"{30*'-'}",
            f"- Solving: {self.filename}",
            f"- Algorithm: {self.algorithm}",
            f"- Explored nodes ({self.layout_elements['exploration']['char']}, {self.layout_elements['solution']['char']}): {len(self.explored_nodes)}",
            f"- Solution nodes ({self.layout_elements['solution']['char']}): {len(self.solution) if self.solution else '-'}",
            f"- Solution: {sol}"
            ]

        return lines

    def _solution_layout_str(self):
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
                    string += self.layout_elements['solution']['char']
                elif self.solution and position in self.explored_nodes:
                    string += self.layout_elements['exploration']['char']
                else:
                    string += self.path_char
            string += '\n'

        return string

    def save_algorithm_steps_to_file(self):
        """Saves algorithm steps to file."""
        log_filename=f"{self.filename}_{self.algorithm}_steps.txt"

        with open(log_filename, 'w', encoding="utf-8") as file:

            file.writelines(line + "\n" for line in self._solution_summary_str())
            #file.write(self._solution_summary_str())
            file.write(self._solution_layout_str())

        self.algorithm_log.save_log(log_filename)
        print(f"Algorithm steps saved to file: {log_filename}\n")


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


def search_module_simple_usage_example(filename):
    """ Simple Usage example of 'search' module (shows maze static solution)"""
    maze = Maze(filename)

    maze.solve('BFS')
    maze.show_solution(dynamic=False)
    maze.save_algorithm_steps_to_file()

    maze.solve('DFS')
    maze.show_solution(dynamic=False)
    maze.save_algorithm_steps_to_file()


def dynamic_solution_display_search_usage_example(filename):
    """
    Search module usage example.
    With 'curses' Python module, a dynamic display of both BFS and DFS solutions is shown together (if terminal size allows it)).
    """
    maze = Maze(filename)
    maze.solve('BFS')
    success = maze.show_solution(dynamic=True)

    # To avoid repeating error:
    if success:
        maze.solve('DFS')
        maze.show_solution(dynamic=True)


if __name__ == '__main__':
    # Test for maze.py

    if len(sys.argv) != 2:
        sys.exit("Usage: python maze.py <path to utf-8 .txt maze layout file>")
    maze_filename = sys.argv[1]

    search_module_simple_usage_example(maze_filename)

    dynamic_solution_display_search_usage_example(maze_filename)

