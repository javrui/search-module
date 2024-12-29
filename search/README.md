# search

This module solves search (path finding) problems using uninformed search algorithms Breadth-First Search (BFS) and Depth-First Search (DFS). Shows algorithm execution step by step for didactic  purposes.

![Python](https://img.shields.io/badge/python-3.6%2B-blue)
![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-yellow.svg)
[![Documentation Status](https://readthedocs.org/projects/mymodule/badge/?version=latest)](https://mymodule.readthedocs.io/en/latest/?badge=latest)


## ✨Overview

The search.py module is a Python framework designed to help solve search problems using classic search algorithms like Breadth-First Search (BFS) and Depth-First Search (DFS). The module provides two main abstract classes: SearchProblem and Node, which users can extend to create their own search implementations.

This module is particularly useful for anyone working with problem-solving techniques involving state-space search, such as pathfinding, game solving, or any domain that requires intelligent exploration of states.


## Key Features

- Abstract Classes for Custom Problems: SearchProblem and Node provide a structured way to define custom search problems by overriding their abstract methods.

- Built-In Support for BFS and DFS: The solve() method supports both BFS and DFS, with flexible components like QueueFrontier and StackFrontier for implementing different search strategies.

- Detailed Logging: The module logs the search progress, showing the state of the frontier, the explored nodes, and expanded nodes at each step, enabling users to analyze the search behavior thoroughly.



## 📥 Installation
No installation required; simply add *search.py* to your project folder and import:

```python
from search import SearchProblem, Node
```

## 🚀 Basic usage

Create your own problem specific classes derived from *search* abstract base classes **SearchProblem** and **Node**.

In this example, your own classes are: *Maze* and *MazeNode*

```python
class Maze(SearchProblem):
   # ...

class MazeNode(Node):
   # ...
```

Define base abstract methods in your classes, to implement specific problem environment (detailed explanations in documentation)

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

Instantiate an object:

```python
maze = Maze()
```

Solve search problem with 'BFS' or 'DFS' algorithm:

```python
maze.solve('BFS')
```

Print solution found:

```python
maze.show_solution('BFS')
```

Get a detailed log of algorithm steps:

```python
maze.save_algorithm_steps_to_file()
```



## 📚 Documentation
📌 TO DO: readthedocs link

[Read The Docs documentation](docs/search_docs.md)


## 🧪 Testing

Instructions for running the test

    pytest tests/


##  🙏 Credits:

This project is a based on code from [HarvardX:CS50’s Introduction to Artificial Intelligence with Python course](https://pll.harvard.edu/course/cs50s-introduction-artificial-intelligence-python) refactored to use object-oriented design and abstract base clases.


## ⚖️ License

Mentioned Harvard course code is published under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) [license](LICENSE.md)

