===============================================
How does *maze.py* use *search*
===============================================

-----------------------------------------------
Basic *search* usage in *maze.py* script
-----------------------------------------------

The maze.py script follows the basic usage pattern of the *search* module described in :doc:`../user_guide`:

1. Import interface classes Node and SearchProblem
2. Create its own maze problem specific derived classes: Maze and MazeNode
3. Write/override methods that implement maze specific problem environment
4. Call *search* module interface methods

Lest see each step:


1. Import interface classes Node and SearchProblem
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: python

   from search import Node, SearchProblem

2. Create its own maze problem specific derived classes: Maze and MazeNode
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   class Maze(SearchProblem):
      ...

   class MazeNode(Node):
      ...

Those classes details, as follows:

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Maze class
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: maze.Maze
   :no-index:
   :no-members:

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
MazeNode class
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: maze.MazeNode
   :no-index:
   :no-members:


3. Write/override methods that implement maze specific problem environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following methods are created or overridden to define the maze-specific environment:

.. code-block:: python

   class Maze(SearchProblem):
      def __init__():
         ...

      def show_solution():
         ...

      def save_algorithm_steps_to_file()
         ...


   class MazeNode(Node):
      def actions():
         ...

      def result():
         ...

      def __repr__():
         ...

Lets see each method detail:


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:meth:`maze.Maze.__init__`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automethod:: maze.Maze.__init__
   :no-index:

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:meth:`maze.Maze.show_solution`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automethod:: maze.Maze.show_solution
   :no-index:

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:meth:`maze.Maze.save_algorithm_steps_to_file`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automethod:: maze.Maze.save_algorithm_steps_to_file
   :no-index:

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:meth:`maze.MazeNode.actions`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automethod:: maze.MazeNode.actions
   :no-index:

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:meth:`maze.MazeNode.result`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automethod:: maze.MazeNode.result
   :no-index:

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
:meth:`maze.MazeNode.__repr__`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automethod:: maze.MazeNode.__repr__
   :no-index:



4. Call *search* module interface methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As we saw in :doc:`../user_guide`, the script calls *search* module interface methods:

* :meth:`maze.Maze.solve`
* :meth:`maze.Maze.show_solution`
* :meth:`maze.Maze.save_algorithm_steps_to_file`

These method calls are made within the `main()` function of the script. Two example functions illustrate their usage:

* :func:`maze.search_module_simple_usage_example`
* :func:`maze.dynamic_solution_display_search_usage_example`

