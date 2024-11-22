import curses
import time
import sys
from maze import Maze
import locale

WAIT_EXPLORED = 0.03
WAIT_SOLUTION = 0.03

MAZE_LAYOUT_ELEMENTS = {
    'WALLS':{'char':'█', 'color':130},
    'EXPLORATION':{'char':'¤', 'color':184},
    'SOLUTION':{'char':'*', 'color':196},
    'START_END':{'char':'_', 'color':162}
}


WALLS = {'char':'█', 'color':130}
EXPLORATION = {'char':'¤', 'color':184}
SOLUTION = {'char':'*', 'color':196}
START_END = {'char':'_', 'color':162}




def set_curses_settings(stdscr):
    curses.curs_set(0) # Disable cursor and enable instant character echoing
    stdscr.timeout(-1) # Blocking mode. getch() waits indefinitely for a key press.
    set_colors() # Set the color pairs

def set_colors():
    if not curses.has_colors():
        raise RuntimeError("Your terminal does not support colors.")
    curses.start_color()
    try:
        curses.init_pair(WALLS['color'], WALLS['color'], curses.COLOR_BLACK)
        curses.init_pair(EXPLORATION['color'], EXPLORATION['color'], curses.COLOR_BLACK)
        curses.init_pair(SOLUTION['color'], SOLUTION['color'], curses.COLOR_BLACK)
        curses.init_pair(START_END['color'], START_END['color'], curses.COLOR_BLACK)

    except curses.error:
        print("Error initializing color pairs. Ensure your terminal supports colors.")
        sys.exit(1)


def calculate_maze_layout(maze):

    # Define the maze layout
    maze_walls = [
        (x, y, WALLS['char'] if brick else ' ')
        for x, row in enumerate(maze.walls)
        for y, brick in enumerate(row)
    ]
    maze_start_end = [maze.start_node.state + ('A',), maze.goal_node.state + ('B',)]

    # Exploration path
    maze_exploration = []
    for record in maze.algorithm_log.get_log()[1:-1]:
        x, y = record['extracted'].state
        maze_exploration.append((x, y, EXPLORATION['char']))

    # Solution path
    maze_solution = []
    if maze.solution is not None:
        for node in maze.solution:
            x, y = node.state
            maze_solution.append((x, y, SOLUTION['char']))


    return (maze_walls, maze_start_end, maze_exploration, maze_solution)


def main(stdscr):

    set_curses_settings(stdscr)

    # Create a maze object and solve it
    maze = Maze(sys.argv[1])
    maze.solve('DFS', keep_algorithm_log=True)

    # Calculate the maze layout
    maze_walls, maze_start_end, maze_exploration, maze_solution = calculate_maze_layout(maze)

    try:
        stdscr.clear()

        # Print the tittle
        stdscr.addstr(0, 2, str(f"Solution to {sys.argv[1]}"))

        # Print Walls
        for (x, y, brick) in maze_walls:
            stdscr.addch(2+x, 5+y, brick, curses.color_pair(WALLS['color']))

        # Print start/goall
        for (x, y, node) in maze_start_end:
            stdscr.addch(2+x, 5+y, node, curses.color_pair(START_END['color']))

        # print exploration:
        for (x, y, node) in maze_exploration:
            time.sleep(WAIT_EXPLORED)
            stdscr.addch(2+x, 5+y, node, curses.color_pair(EXPLORATION['color']))
            stdscr.refresh()

        # print solution:
        for (x, y, node) in maze_solution:
            time.sleep(WAIT_SOLUTION)
            stdscr.addch(2+x, 5+y, node, curses.color_pair(SOLUTION['color']))
            stdscr.refresh()

        # Restore star/goal nodes:
        x, y = maze.start_node.state
        stdscr.addch(2+x, 5+y, 'A', START_END['color'])
        x, y = maze.goal_node.state
        stdscr.addch(2+x, 5+y, 'B', START_END['color'])
        stdscr.refresh()


        # Print the end message
        stdscr.addstr(3+maze.height, 2, str("Press any key to exit"))
        stdscr.refresh()
        stdscr.getch()

    except KeyboardInterrupt:
        pass  # Handle Ctrl+C gracefully


# Start the curses application
curses.wrapper(main)


