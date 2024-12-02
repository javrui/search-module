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
No installation required; simply clone the repository and import search.py into your Python project.


```bash
# Clone the repo
git clone https://github.com/javrui/search-module.git
cd my_module
```

Or add search.py to your project folder and import it.
```bash
from search import SearchProblem, Node
```


## 🚀 Basic usage
Import the search module base clases
```bash
from search import Node, SearchProblem
```

Define abstract methods of derived classes (Maze and MazeNode in this example):
```bash
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
Solve maze just calling **solve()** on MazeNode object.
Show solution with **show_solution()** method.
Get a detailed log of algorithm steps for that maze solution calling **save_algorithm_steps_to_file()**.

```bash

maze = Maze(<filename>)

maze.solve('BFS')
maze.show_solution(dynamic=False)
maze.save_algorithm_steps_to_file()
```

See more advanced usage examples in documentation, with dynamic representation of algorithm steps.



[enhanced in documentation](docs/features.md)


## 📚 Documentation
📌 TO DO: readthedocs link

[Read The Docs documentation](docs/search_docs.md)


## 🧪 Testing

Instructions for running the test

    pytest tests/


## ⚖️ License

Mentioned Harvard course code is published under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) [license](LICENSE.md)



##  🙏 Credits:

This project is a based on code from [HarvardX:CS50’s Introduction to Artificial Intelligence with Python course](https://pll.harvard.edu/course/cs50s-introduction-artificial-intelligence-python) refactored to use object-oriented design and abstract base clases.
