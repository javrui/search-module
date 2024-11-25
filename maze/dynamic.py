"""================================================================ JRM 2024.02
Python script to show 'search' module usage for solving a maze problem.

Usage:
    python3 maze.py <maze .txt file path>

Dependencies:
    search module

===============================================================================
Maze layout must be utf-8 text file (.txt) to be supplied as argument, where:
    - space characters mean open paths
    - 'start_char' is the start point and 'goal_char' is the goal point
    -  walls are any character except 'start_char' or 'goal_char'
============================================================================"""

import curses
import time
import sys
from maze import Maze


# '¤'
LAYOUT_ELEMENTS = {
    'walls':{'char':'█', 'color':243, 'wait':0},
    'exploration':{'char':'·', 'color':208, 'wait':0.1},
    'solution':{'char':'¤', 'color':118, 'wait':0.1},
    'start_goal':{'char':'_', 'color':7, 'wait':0.1},
    }

def set_curses_settings(stdscr):
    # Disable cursor and enable instant character echoing
    curses.curs_set(0)
    # Blocking mode. getch() waits indefinitely for a key press.
    stdscr.timeout(-1)
    # Set the color pairs
    set_colors()
    stdscr.clear()


def set_colors():
    if not curses.has_colors():
        raise RuntimeError("Your terminal does not support colors.")

    curses.start_color()

    try:
        for _, components in LAYOUT_ELEMENTS.items():
            curses.init_pair(components['color'], components['color'], curses.COLOR_BLACK)
    except curses.error:
        print("Error initializing color pairs. Ensure your terminal supports colors.")
        sys.exit(1)


def calculate_maze_and_solution_layout_elements(maze):

    # Define the maze layout
    maze_walls = [
        (x, y, LAYOUT_ELEMENTS['walls']['char'] if brick else ' ')
        for x, row in enumerate(maze.walls)
        for y, brick in enumerate(row)
    ]

    # Start node
    maze_start_goal = [maze.start_node.state + ('A',), maze.goal_node.state + ('B',)]

    # Exploration path
    maze_exploration = []
    for record in maze.algorithm_log.get_log()[1:]:
        x, y = record['extracted'].state
        maze_exploration.append((x, y,
            LAYOUT_ELEMENTS['exploration']['char']))

    # Solution path
    maze_solution = []
    if maze.solution is not None:
        for node in maze.solution:
            x, y = node.state
            maze_solution.append((x, y,
                LAYOUT_ELEMENTS['solution']['char']))

    # Elements in a dict
    maze_solution_layout_elements = {
        'walls': maze_walls,
        'start_goal': maze_start_goal,
        'exploration': maze_exploration,
        'solution': maze_solution,
        }

    return maze_solution_layout_elements


def show_maze_and_solution_layout_elements(stdscr, maze, maze_solution_layout_elements):

    set_curses_settings(stdscr)

    try:
        end_message_vertical_offset = maze.height
        # Print the tittle
        stdscr.addstr(0, 2, str(f"Solution to {sys.argv[1]}:"))

        if maze.solution is None:
            show_elements = ['walls', 'start_goal', 'exploration', 'start_goal']
            stdscr.addstr(1, 2, str("No solution found!"))
        else:
            show_elements = ['walls', 'start_goal', 'exploration', 'start_goal','solution', 'start_goal']
            stdscr.addstr(1, 2, str("Solution:"))

        # Print layout:
        for element_name in ['walls', 'start_goal', 'exploration', 'start_goal','solution', 'start_goal']:
            for (x, y, char) in maze_solution_layout_elements[element_name]:
                time.sleep(LAYOUT_ELEMENTS[element_name]['wait'])
                color = curses.color_pair(LAYOUT_ELEMENTS[element_name]['color'])
                stdscr.addch(2+x, 5+y, char, color)
                stdscr.refresh()

        # Print the end message
        stdscr.addstr(3+end_message_vertical_offset, 2, str("Press any key to exit"))
        stdscr.refresh()
        # Wait for a key press to exit
        stdscr.getch()

    except KeyboardInterrupt:
        pass  # Handle Ctrl+C gracefully


def main(stdscr):

    if len(sys.argv) != 2:
        sys.exit("Usage: python3 maze.py <path to utf-8 .txt maze layout file>")

    # Create a maze object and solve it
    maze = Maze(sys.argv[1])
    maze.solve('BFS', keep_algorithm_log=True)

    # Calculate the maze layout
    maze_solution_layout_elements = calculate_maze_and_solution_layout_elements(maze)
    show_maze_and_solution_layout_elements(stdscr, maze, maze_solution_layout_elements)

if __name__ == '__main__':
    # Start the curses application
    curses.wrapper(main)
