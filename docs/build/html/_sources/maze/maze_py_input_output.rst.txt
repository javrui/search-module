-----------------------------------------------
maze.py input: maze layout file
-----------------------------------------------

A maze layout to be solved is defined in a UTF-8 encoded text file.

The maze layout is a rectangular grid, where each character in the file represents a grid cell. The cells are defined as follows:

- **starting cell** (default character is 'A')
- **goal cell** (default character is 'B')
- **path** (default character is ' ')
- **wall** (any other character)

Maze layout file example:

.. literalinclude:: maze_layout.txt
   :caption: example of maze layout text file content


-----------------------------------------------
maze.py output: static representation
-----------------------------------------------

Below is an example of the static representation of the maze, showing the solution path and exploration attempts:

.. image:: maze_static_solution.png
   :alt: (Example Image not loaded!)
   :align: left


-----------------------------------------------
maze.py output: dynamic representation
-----------------------------------------------
A dynamic representation of the maze solution is provided in the following video:

.. video:: maze_dynamic_solution.mp4
   :alt: (Example Video not loaded!)

-----------------------------------------------
maze.py output: algorithm steps data files
-----------------------------------------------

Two text files are generated for each algorithm, named after the maze layout filename with the algorithm name and _steps suffix appended (e.g., maze_layout.txt_DFS_steps.txt, maze_layout.txt_BFS_steps.txt).

Examples of algorithm steps log files:

.. `DFS steps log  <../../../source/maze/maze_layout.txt_DFS_steps.txt>`_

.. literalinclude:: maze_layout.txt_DFS_steps.txt
   :caption: example of DFS algorithm steps log file content


.. literalinclude:: maze_layout.txt_BFS_steps.txt
   :caption: example of BFS algorithm steps log file content

