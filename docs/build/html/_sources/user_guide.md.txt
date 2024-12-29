# User Guide

## Installation

No installation is required. Simply import the following classes from the module:

``` python
from search import Node, SearchProblem
```

## Usage: basic concepts

*search* module provides two interface classes: **SearchProblem** and **Node**.

Both are abstract classes. You **must** subclass each one, i.e., you have to create your own two derived classes where you will write code that implements the
following methods, specific for your problem:

* SearchProblem.**\_\_init\_\_**()
* Node.**actions**()
* Node.**result**()

You **may** also want to override these methods, e.g. to adapt the solution to your specific problem graphic representation, or other needs:

* SearchProblem.**show_solution**()
* SearchProblem.**save_algorithm_steps_to_file**()
* Node.**\_\_init\_\_**()
* Node.**\_\_repr\_\_**()

Once base classes have been implemented, you just call **SearchProblem** interface methods:

* **solve**()
* **show_solution**()
* **save_algorithm_steps_to_file**()

## Usage: basic example

Here is an example of using the module in a script to solve mazes. The structure of the script would look like this:

First, we import interface classes:

``` python
from search import Node, SearchProblem
```

We create our own maze problem specific derived classes. In this example,
*Maze* and *MazeNode*:

```python
class Maze(SearchProblem):
   # ...

class MazeNode(Node):
   # ...
```

Then, we write mentioned methods that implement maze specific problem environment:

```python
class Maze(SearchProblem):
   def __init__():
      # Maze specific implementation here

   def show_solution():
      # Maze specific implementation here

   def save_algorithm_steps_to_file()
      # Maze specific implementation here


class MazeNode(Node):
   def actions():
      # Maze specific implementation here

   def result():
      # Maze specific implementation here

   def __repr__():
      # Maze specific implementation here
```

And finally, our script would call *search* methods:

```python
maze = Maze(<filename>)

# Solve search problem with 'BFS' or 'DFS' algorithm:
maze.solve('BFS')

# Print solution found:
maze.show_solution()

# Save to file a detailed log of algorithm steps
maze.save_algorithm_steps_to_file()
```

The former code skeleton gives an overview of the process to use this module.
To see a complete example of script using *search* for maze solving, please visit [Maze.py script](maze/usage_example_maze.rst).



## Instructions to override methods in subclass

As shown above, you have to override a few methods of interface classes :class:`search.SearchProblem` and :class:`search.Node`. You may also want to override other methods, as well.

Lets see requirements for that overriding, for each method:

### SearchProblem methods

#### :meth:`search.SearchProblem.\_\_init\_\_`

* This method MUST be overridden.

* Redefined method in subclass:
  * MUST call `super().__init__()` (generally as first statement)
  * MUST at least assign 'start_node' and 'goal_node' attributes with appropriate values.
  * MAY define other attributes relevant to the specific search problem, if needed by actions() or result() methods in 'Node' derived class.

#### :meth:`search.SearchProblem.show_solution`

* This method MAY be overridden to customize the output format or content to specific search problem.
* Base class method ("default" method) prints the nodes sequence that form the solution path if one exists,along with the number of nodes explored.

#### :meth:`search.SearchProblem.save_algorithm_steps_to_file`

* This method MAY be overridden to customize the output format or content of solution to search problem.
* Base class method ("default" method) details algorithm name, number of explored and solution nodes, and for each algorithm step, the current state of explored nodes, frontier, extracted nodes, and expanded nodes.

### Node methods

#### :meth:`search.Node.\_\_init\_\_`

* This method MAY be overridden.
* Redefined method in subclass:
  * MUST call `super().__init__()` (generally as first statement)
  * MAY define other attributes relevant to the specific search problem, if needed by actions() or result() methods.

#### :meth:`search.Node.action`

* This method MUST be overridden.
* Redefined method in subclass MUST return a list of the possible actions that can be taken from the current node state in  the context of the search problem.

  Example: If your search problem is path finding in a maze, this method should return all valid moves that can be taken from the current state. E.g.: selecting valid ones among 'up', 'down', 'left', 'right' in a two-dimension maze.

#### :meth:`search.Node.result`

* This method MUST be overridden.
* Redefined method in subclass MUST return the node that results from performing 'action' on (self) node.

  Example in maze path finding: method would return the node representing new position in maze after movement provided by 'action()'
