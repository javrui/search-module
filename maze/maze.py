"""
Python script that finds and prints 2 dimension's maze solution.

It is an usage example of 'search' module, which provides classes and functions
for solving search problems.

Usage:
    python3 maze.py <maze layout .txt utf-8 file path>

Dependencies:
    Python 3.6 or higher
    search module
    curses library ('pip install windows-curses' for Windows)

Author:
    JRM 2024.02

Credits:
    Based on code from HarvardX:CS50’s Introduction to Artificial Intelligence
    with Python course.

License:
    Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
    (CC BY-NC-SA 4.0)

"""
import sys
import os
import time
import curses
from typing import List, Tuple
from search import Node, SearchProblem # pylint: disable=C0413


class Maze(SearchProblem):
    """ Defines a maze object to be solved with 'search' module.

    Subclasses SearchProblem class, to:
        Implement __init__() with attributes that define maze layout

        Override show_solution() to print static maze layout with solution
        and dynamic maze path forming

        Override save_algorithm_steps_to_file() to add static maze print
        to file.

    Attributes:
        filename (str): Name of the UTF-8 text file defining the maze.
        start_char (str): Character representing the start point in maze file.
        goal_char (str): Character representing the goal point in maze file.
        path_char (str): Character representing the open path in maze file.
        walls (list of list of bool): Boolean grid representing walls (True)
            and open paths (False) in maze.
        height (int): Number of rows in the maze.
        width (int): Number of columns in the maze.
        offset (dict): Directional offsets (horizontal, vertical) for movement.
        first_dynamic_solution_shown (bool): Tracks if a dynamic solution was
            displayed.
        layout_elements (dict): Styling for maze components during visualization.
        maze_solution_layout (dict): Stores elements for dynamic maze display.
        start_node (MazeNode): Node object for the maze start position.
        goal_node (MazeNode): Node object for the maze goal position.

    Notes on maze layout definition file:
        Maze layout is defined in an utf-8 encoded text file. Each character in
        file represents a cell in maze grid. Cells can be:

            * starting cell (default character is ‘A’)
            * goal cell (default character is ‘B’)
            * path (default character is ‘ ‘)
            * wall (any other character)

        Maze layout file content example:
            '███████████'
            '█         █'
            '████ ████ █'
            '█B   █    █'
            '█ ████ ████'
            '█         █'
            '█A█████████'

        """


    def __init__(self, filename: str, start_char: str = 'A',
                 goal_char: str = 'B', path_char: str = ' ') -> None:
        """Reads maze layout from 'filename' to initialize a maze object.

        Args:
            filename (str): name of utf-8 text file .txt defining maze layout.
            start_char (str, optional): The character representing the start
                position in the maze. Defaults to 'A'.
            goal_char (str, optional): The character representing the goal
                position in the maze. Defaults to 'B'.
            path_char (str, optional): The character representing the path in
                the maze. Defaults to ' '.

        """
        super().__init__()
        self.filename = filename
        self.start_char = start_char
        self.goal_char = goal_char
        self.path_char = path_char
        self.height = None
        self.width = None
        self.offset = {"up": (-1, 0), "right": (0, 1), "down": (1, 0), "left": (0, -1)}
        self.first_dynamic_solution_shown = False
        self.layout_elements = {
        #    'walls': {'char': '█', 'color': 243, 'wait': 0},
            'walls': {'char': '█', 'color': 108, 'wait': 0},
        #    'exploration': {'char': '·', 'color': 208, 'wait': 0.01}, #, gray
        #    'exploration': {'char': '·', 'color': 198, 'wait': 0.01}, # Quick
        #    'solution': {'char': '¤', 'color': 118, 'wait': 0.05}, # Quick
             'exploration': {'char': '·', 'color': 198, 'wait': 0.15}, # Slow
             'solution': {'char': '¤', 'color': 118, 'wait': 0.1}, # Slow

            'start_goal': {'char': '_', 'color': 7, 'wait': 0.1},
        }
        self.maze_solution_layout = None
        self._load_maze_from_file()


    def _load_maze_from_file(self) -> None:
        """Loads the maze configuration from a file.

        This method reads the maze configuration from a file specified by `self.filename`.
        It ensures that the file contains exactly one start point and one goal point.
        It also initializes the maze's dimensions and wall configuration.

        Raises:
            SystemExit: If the file is not found, permission is denied, or an
                I/O error occurs.
            ValueError: If the maze does not contain exactly one start point or
                one goal point.

        """
        # Read file and check start and goal points exist
        try:
            with open(self.filename, encoding="utf-8") as f:
                contents = f.read()
        except FileNotFoundError:
            sys.exit(f"Error: File '{self.filename}' not found.")
        except PermissionError:
            sys.exit(f"Error: Permission denied for accessing file '{self.filename}'.")
        except IOError as e:
            sys.exit(f"Error: Unable to read file '{self.filename}'. Details: {str(e)}")

        # Ensure start and goal points are present
        if contents.count(self.start_char) != 1:
            raise ValueError("maze must have exactly one start point")
        if contents.count(self.goal_char) != 1:
            raise ValueError("maze must have exactly one goal")

        # Define height and width of maze (ignores empty lines)
        contents = [line for line in contents.splitlines() if line.strip()]
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        # Creates wall values
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
                except IndexError:
                    row.append(False)
            self.walls.append(row)


    def show_solution(self, dynamic: bool = False) -> bool:
        """Prints the maze and its solution.

        Args:
            dynamic (bool): If True, shows the solution step by step dynamically.

        Returns:
            bool: True if the solution was shown successfully, False otherwise.

        Raises:
            curses.error: If there is an error showing the dynamic solution.

        """

        if dynamic:
            self._calculate_maze_and_solution_layout_elements()

            offset = self._calculate_display_offsets()
            if offset == (0, 0):
                return False
            try:
                curses.wrapper(lambda stdscr:
                    self._show_dynamic_solution(stdscr, offset))
                return True
            except curses.error:
                print("Error showing dynamic solution. Check terminal size.\n")
                return False
        else:
            for line in self._solution_summary_str():
                print(line)
            #print(self._solution_summary_str())
            print(self._solution_layout_str())
            return True


    def _calculate_maze_and_solution_layout_elements(self) -> None:
        """Calculates and sets the layout elements for the maze and its solution.

        This method prepares the layout elements required for displaying the
        maze, including walls, start and goal nodes, exploration path, and
        solution path. The layout elements are stored in the
        `self.maze_solution_layout` attribute.

        """
        # Define the maze layout for curses
        maze_walls = [
            (x, y, self.layout_elements['walls']['char'] if brick else ' ')
            for x, row in enumerate(self.walls)
            for y, brick in enumerate(row)
        ]

        # Define start and goal nodes for curses
        maze_start_goal = [self.start_node.state + ('A',), self.goal_node.state + ('B',)]

        # Define exploration path for curses
        maze_exploration = []
        for record in self.algorithm_log.get_log()[1:]:
            x, y = record['extracted'].state
            maze_exploration.append((x, y,
                self.layout_elements['exploration']['char']))

        # Define solution path for curses
        maze_solution = []
        if self.solution is not None:
            for node in self.solution:
                x, y = node.state
                maze_solution.append((x, y,
                    self.layout_elements['solution']['char']))

        # Create layout elements dictionary
        self.maze_solution_layout = {
            'walls': maze_walls,
            'start_goal': maze_start_goal,
            'exploration': maze_exploration,
            'solution': maze_solution,
            }


    def _calculate_display_offsets(self) -> Tuple[int, int]:
        """ Calculates dynamic display elements offsets and checks terminal
        size needed to fit space for maze solution display.

        Display of two maze solutions (BFS and DFS) can be: "side to side" or
        "one below the other". Offsets will be aimed at side to side layout
        (vertical_offset = 1). If not possible, tries vertical layout
        (horizontal_offset will be 0).
        If terminal size is not enough, prints a warning message and
        returns (0, 0).

        Returns:
            tuple: (horizontal_offset, vertical_offset), where curses library
                will print the second solution.

        """
        (term_width, term_height) = os.get_terminal_size()

        h_title_indent = 2
        v_title_indent = 1
        title_width = 29
        h_layout_indent = 6
        v_layout_indent = 6
        v_press_key_lines = 2


        element_width_needed = max(h_title_indent + title_width,
                                    h_layout_indent + self.width)
        element_heigh_needed = (v_title_indent + v_layout_indent +
                               self.height + v_press_key_lines)

        # Side to side layout if possible, otherwise one below the other
        if 2 * element_width_needed <= term_width and element_heigh_needed <= term_height:
            return (element_width_needed, 1)
        elif 2 * element_heigh_needed <= term_height and element_width_needed <= term_width:
            return (0, element_heigh_needed)
        else:
            print(
                f"\nError trying to show dynamic solution:\n"
                f"\nTerminal width = {term_width}.\n"
                f"Display width needed = {2*element_width_needed}.\n"
                f"\nTerminal height = {term_height}.\n"
                f"Display height needed = {2*element_heigh_needed}.\n"
                "\nPlease, resize terminal to fit maze layout display size.\n"
                )
            input("Press Key to continue...")
            return (0, 0)


    def _show_dynamic_solution(self, stdscr: curses.window,
                               offset: Tuple[int, int]) -> None:
        """Shows the maze solution step by step dynamically.

        This method displays the maze solution step by step using the curses
        library.
        It is called twice (for BFS and DFS solutions). The second solution is
        shown either to the right or below the first one, so the offset
        parameter indicates where 'curses' has to locate second solution.

        Display of two maze solutions (BFS and DFS) can be: "side to side" or
        "one below the other". Offsets will be aimed at side to side layout
        vertical_offset = 1 if "side to side" display is to be shown.
        horizontal_offset = 0 if "one below the other" display is to be shown.

        Args:
            stdscr (curses.window): The curses window object.
            offset (tuple): A tuple (horizontal_offset, vertical_offset)
                indicating the offset for displaying the second solution.

        Raises:
            curses.error: If there is an error displaying the solution
                dynamically.

        """
        self._set_curses_settings(stdscr)
        #time.sleep(1)

        # Offset in terminal display of solution to be printed
        if self.first_dynamic_solution_shown is False:
            offset = (0, 0)

        h_offs, v_offs = offset

        blank_line = 1  # To clarify expressions in curses.addch() and curses.addstr()

        # Print Summary:s
        start = 3 if self.first_dynamic_solution_shown else 2
        for line_count, line in enumerate(self._solution_summary_str()[start:], blank_line):
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

                stdscr.addch(y + line_count + 2 * blank_line + v_offs,
                                x + 6 + h_offs, char, color)
                stdscr.refresh()

        # Print "press key"
        if self.first_dynamic_solution_shown is True:
            line_count +=1
            factor = 2 if h_offs == 0 else 1
            press_key_v_offset = factor* (3 * blank_line + line_count + self.height)
        else:
            press_key_v_offset = 3 * blank_line + line_count + self.height
        stdscr.addstr(press_key_v_offset, 2, "Press any key.")
        stdscr.refresh()
        # Wait for a key press to exit
        stdscr.getch()
        # Delete "press key"
        stdscr.addstr(press_key_v_offset, 2 + h_offs, "              ")
        stdscr.refresh()

        self.first_dynamic_solution_shown = True


    def _set_curses_settings(self, stdscr: curses.window) -> None:
        """Sets the curses settings for displaying the maze.

        This method configures the curses library settings, such as disabling the
        cursor, enabling instant character echoing, setting blocking mode for
        key presses, and initializing color pairs.

        Args:
            stdscr (curses.window): The curses window object.

        """
        # Disable cursor and enable instant character echoing
        curses.curs_set(0)
        # Blocking mode. getch() waits indefinitely for a key press.
        stdscr.timeout(-1)
        # Set the color pairs
        self._set_colors()
        #stdscr.clear()


    def _set_colors(self) -> None:
        """Initializes color pairs for the maze display using the curses library.

        This method checks if the terminal supports colors and initializes the
        color pairs for different maze components. If the terminal does not support
        colors or there is an error initializing color pairs, it raises a RuntimeError.

        Raises:
            RuntimeError: If the terminal does not support colors or if there is an
                        error initializing color pairs.

        """
        if not curses.has_colors():
            raise RuntimeError("Your terminal does not support colors.")
        try:
            curses.start_color()
            for _, components in self.layout_elements.items():
                curses.init_pair(components['color'], components['color'], curses.COLOR_BLACK)
        except curses.error as exc:
            raise RuntimeError("Error initializing color pairs."
                              "Ensure your terminal supports colors.") from exc


    def _solution_summary_str(self) -> List[str]:
        """
        Generates and returns a summary of explored nodes and, if solution
        exists, solution path nodes.

        This method creates a summary string that includes information about
        the maze being solved, the algorithm used, the number of explored
        nodes, and the solution path nodes if a solution exists.

        Returns:
            list: A list of strings representing the summary of the maze solution.

        """
        expl_char = self.layout_elements['exploration']['char']
        sol_char = self.layout_elements['solution']['char']
        expl_len = len(self.explored_nodes)
        sol_len = len(self.solution) if self.solution else '-'
        sol = " No Solution found!" if self.solution is None else ""

        lines=[
            "",
            f"{28*'-'}",
            f"- Solving: {self.filename}",
            f"- Algorithm: {self.algorithm}",
            f"- Explored nodes ({expl_char}, {sol_char}): {expl_len}",
            f"- Solution nodes ({sol_char}): {sol_len}",
            f"- Solution: {sol}",
            ]
        return lines


    def _solution_layout_str(self) -> str:
        """
        Generates and returns the maze layout as a string, including the
        solution path if it exists.

        This method creates a string representation of the maze layout,
        marking walls, start and goal nodes, the solution path, and explored
        nodes.

        Returns:
            str: A string representing the maze layout with the solution path
            if it exists.

        """
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


    def save_algorithm_steps_to_file(self) -> None:
        """Saves algorithm steps to a file.

        Overrides base method to save maze graphic solution. The file name
        saved is the same as the layout filename read, ending in
        _<algorithm name>_steps.txt.

        The file contains a summary of the solution and the maze layout with
        the solution path.

        """
        log_filename=f"{self.filename}_{self.algorithm}_steps.txt"

        with open(log_filename, 'w', encoding="utf-8") as file:
            file.writelines(line + "\n" for line in self._solution_summary_str())
            file.write(self._solution_layout_str())

        self.algorithm_log.save_log(log_filename)
        print(f"Algorithm steps saved to file:\n {log_filename}")


class MazeNode(Node):
    """Represents a node in the maze.

    A MazeNode is mainly the position in the maze. It also includes the
    previous position and the direction taken to get there, although these are
    used sparsely.

    Subclasses Node class, to implement actions() and result() methods
    according to a maze layout. It also overrides __repr__ to be used in Maze
    methods printing nodes.

    Attributes:
        state (tuple): The current position in the maze as a tuple (row, column).
        parent (MazeNode): The parent node from which this node was reached.
        action (str): The action taken to reach this node from the parent node.

    """

    def actions(self, search_problem: SearchProblem) -> List[str]:
        """List of valid movements (actions) to occupy contiguous cells.

        This method determines the valid actions that can be performed from the
        current position in the maze, considering the maze boundaries and walls.

        Args:
            search_problem (SearchProblem): The search problem instance
                containing the maze layout, including the offset information,
                dimensions, and wall positions.

        Returns:
            list: A list of valid actions (str) that can be performed from the
            current position.

        """

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


    def result (self, action: str, search_problem: SearchProblem) -> 'MazeNode':
        """Returns the node that results from performing 'action' on self.

        Calculates the new position in the maze based on the given action and
        the search problem's offset.

        Args:
            action (str): The action to be performed.
            search_problem (SearchProblem): The search problem instance
                containing the offset information.

        Returns:
            MazeNode: A new MazeNode instance representing the new position
            in the maze.

        Raises:
            ValueError: If the action is not valid.

        """
        initial_row, initial_col = self.state

        if action not in search_problem.offset:
            raise ValueError(f"Invalid action: {action}")

        new_position = (initial_row + search_problem.offset[action][0],# row
                        initial_col + search_problem.offset[action][1])# column

        return MazeNode(state=new_position, parent=self, action=action)


    def __repr__(self) -> str:
        """Returns a string representation of the object.

        This method provides a simple view of the object, omitting details.

        Returns:
            str: A string representation of the object, including its state and
            action.

        """
        return f"{self.state}'{self.action}'"


def search_module_simple_usage_example(filename: str) -> None:
    """Simple usage example of the 'search' module (shows maze static solution).

    This function demonstrates the usage of the 'search' module by solving the
    maze using both BFS and DFS algorithms and displaying the static solutions.
    It also saves the steps of each algorithm to a file.

    Args:
        filename (str): The path to the maze layout file.

    Returns:
        None

    Raises:
        None

    """

    maze = Maze(filename)

    maze.solve('BFS')
    maze.show_solution(dynamic=False)
    maze.save_algorithm_steps_to_file()

    maze.solve('DFS')
    maze.show_solution(dynamic=False)
    maze.save_algorithm_steps_to_file()


def dynamic_solution_display_search_usage_example(filename: str) -> None:
    """Displays a dynamic solution of the maze using BFS and DFS algorithms.

    This function uses the 'curses' Python module to dynamically display both
    BFS and DFS solutions of the maze, if the terminal size allows it. It first
    solves the maze using BFS and displays the solution. If successful,
    it then solves the maze using DFS and displays the solution.

    Args:
        filename (str): The path to the maze layout file.

    Returns:
        None

    Raises:
        None

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
        sys.exit(f"Usage: python {os.path.basename(__file__)}"
                 " <path to utf-8 .txt maze layout file>")

    maze_filename = sys.argv[1]

    search_module_simple_usage_example(maze_filename)

    input("\nPress Enter to see dynamic steps...")

    dynamic_solution_display_search_usage_example(maze_filename)
