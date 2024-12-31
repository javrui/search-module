# search

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
[![Documentation Status](https://readthedocs.org/projects/search-module/badge/?version=latest)](https://search-module.readthedocs.io/en/latest/)
![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-yellow.svg)

## ✨Overview

The *search* module is a Python framework designed to solve search problems using classic algorithms such as Breadth-First Search (BFS) and Depth-First Search (DFS).

It demonstrates step-by-step algorithm execution and logs internal data structures for educational purposes.

This module is especially useful for tasks involving state-space search, such as pathfinding, game solving, or any scenario that requires systematic exploration of states.

## 📥 Installation
No installation is required; simply add *search.py* to your project folder and import the necessary classes:

```python
from search import SearchProblem, Node
```

## 🚀 Basic usage

The module provides two core abstract classes, *SearchProblem* and *Node*, which can be extended to implement custom search solutions.

Create problem-specific classes by inheriting from *SearchProblem* and *Node*. In this example, the classes *Maze* and *MazeNode* handle maze-related logic.

```python
class Maze(SearchProblem):
   # ...

class MazeNode(Node):
   # ...
```

Implement the required abstract methods in your subclasses to define your specific problem environment (refer to the documentation for more details).

```python
class Maze(SearchProblem):
   def __init__():
      # Maze specific implementation here

   def show_solution():
      # Maze specific implementation here

class MazeNode(Node)
   def __init__():
      # Maze specific implementation here

   def actions():
      # Maze specific implementation here

   def result():
      # Maze specific implementation here
```

Instantiate a Maze object:

```python
maze = Maze()
```

Solve the search problem using BFS or DFS:

```python
maze.solve('BFS')
```

Print the discovered solution:

```python
maze.show_solution('BFS')
```

Obtain a detailed log of algorithmic steps:

```python
maze.save_algorithm_steps_to_file()
```

## 📝 Documentation

Full documentation, including the API specification and a working example that solves mazes, is available on [Read The Docs](https://search-module.readthedocs.io/en/latest/)

TOC:

* WELLCOME
*
  * [What is search module?](https://search-module.readthedocs.io/en/latest/wellcome.html)
  * [Watch search in action: maze solving](https://search-module.readthedocs.io/en/latest/wellcome.html#watch-search-in-action-maze-solving)

* INTRODUCTION

  * [Introduction to search problem](https://search-module.readthedocs.io/en/latest/AI_intro.html)

* USER GUIDE

  * [User Guide](https://search-module.readthedocs.io/en/latest/user_guide.html)
  * [API Reference](https://search-module.readthedocs.io/en/latest/search_api_reference.html)

* USAGE EXAMPLE

  * [maze.py script](https://search-module.readthedocs.io/en/latest/maze/usage_example_maze.html)

* ALL THE REST

  * [Key Features of search module](https://search-module.readthedocs.io/en/latest/features.html)
  * [Credits and license](https://search-module.readthedocs.io/en/latest/credits_license.html)
  * [Testing](https://search-module.readthedocs.io/en/latest/testing.html)

## 💡 Key Features

### Object-Oriented Design

The module follows OOP principles, encapsulating problem-solving elements into classes such as *SearchProblem*, *Node*, and various internal classes. Each class is responsible for specific functionality, ensuring modularity and reusability.

### Abstract Classes

**Abstract Base Classes (ABC)**

The *SearchProblem* and *Node* classes are defined as abstract using Python’s ABC module. This forces any concrete subclass to implement critical methods, like *actions()*, *result()*, and *\_\_init\_\_()*, maintaining a consistent interface.


**Protected Methods and Attributes**

Methods and attributes prefixed with an underscore (_) are intended for internal use, keeping users focused on essential interfaces and abstracting lower-level details.

**Explicit Subclassing Requirements**

Marking methods such as *actions()* and *result()* as abstract in *Node* and **SearchProblem** ensures subclasses provide the necessary implementations, promoting a controlled interface tailored to each search scenario.

### Modularity and Extensibility

**Pluggable Search Algorithms**

The *solve()* method in *SearchProblem* supports different search strategies (BFS, DFS) by selecting the type of frontier (*_StackFrontier* for BFS, *_QueueFrontier* for DFS). This design simplifies adding or modifying search algorithms without changing the overall structure.

**Separate Components for State Tracking**

Classes like *_Frontier*, *_ExploredNodes*, and *_Solution* manage distinct concerns such as the frontier, explored nodes, and the final solution. This separation of responsibilities makes it easy to modify or extend each component independently.

### Audit Trail and Algorithm Steps Log

The *AuditTrail* class captures each step of the search process, including frontier and explored-node states. This comprehensive record aids in debugging and provides transparent insight into how the search progresses.

### Customizable Output

The *show_solution()* method can be used directly or overridden in subclasses to customize the solution's presentation format, allowing for flexible output that meets domain-specific or user-defined requirements.

## 🧪 Testing

To run tests, execute:

   pytest tests/

## 🙏 Credits

This project is a based on code from [HarvardX:CS50’s Introduction to Artificial Intelligence with Python course](https://pll.harvard.edu/course/cs50s-introduction-artificial-intelligence-python) refactored to achieve mentioned key features.

## ⚖️ License

The Harvard course code is published under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) [license](LICENSE.md)
