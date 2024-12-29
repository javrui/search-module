===============================================
maze.py script explained
===============================================

-----------------------------------------------
maze.py overview
-----------------------------------------------

The maze layout is defined in a text file, which must be provided as an argument to the script. To run the script:

.. code-block:: console

   $ python3 maze.py path/to/maze_layout.txt

Note: python invocation may vary depending on os

The script solves the maze (if possible) using both depth-first search (DFS) and breadth-first search (BFS) algorithms.

During execution, it:

* Outputs a static representation of the maze, including the solution path and exploration attempts.

* Dynamically displays the explored and solution nodes on the maze representation at each algorithm step, providing a clear visualization of the algorithm's behavior.

* Saves the exploration data to a file in text format, detailing the current state of explored nodes, the frontier, extracted nodes, and expanded nodes for each algorithm iteration.

* Saves the solution path to a file in text format, including the path from the start to the goal node.