===============================================
maze.py script explained
===============================================

-----------------------------------------------
maze.py overview
-----------------------------------------------

The maze.py script is a Python implementation of a maze solver using depth-first search (DFS) and breadth-first search (BFS) algorithms. The script provides a visual representation of the maze, including the solution path and exploration attempts, and saves the exploration data to a file in text format.


The maze layout to be solved, must be defined in a text file, to be provided as argument to the script.

To run the script:

.. code-block:: console

   $ python3 maze.py path/to/maze_layout.txt

Note: python invocation may vary depending on os

During execution, it:

* Outputs a static representation of the maze, including the solution path and exploration attempts.

* Dynamically displays the explored and solution nodes on the maze representation at each algorithm step, providing a clear visualization of the algorithm's behavior.

* Saves the exploration data to a file in text format, detailing the current state of explored nodes, the frontier, extracted nodes, and expanded nodes for each algorithm iteration.

* Saves the solution path to a file in text format, including the path from the start to the goal node.


-----------------------------------------------
maze.py dependencies: curses
-----------------------------------------------

The Maze.py script dynamically displays the explored and solution nodes on the maze representation, based on curses standard Python library.


**Curses availability**

* Linux/Unix/macOS: The curses module is included in the standard Python distribution and works out of the box.

* Windows: The curses module is not natively available on Windows. However, you can install a Windows-compatible implementation, such as:
   * UniCurses
   * windows-curses

To install windows-curses:

.. code-block:: console

   pip install windows-curses
