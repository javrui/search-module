# search

This module solves search (path finding) problems using uninformed search algorithms Breadth-First Search (BFS) and Depth-First Search (DFS). Shows algorithm execution step by step for didactic  purposes.

![Python](https://img.shields.io/badge/python-3.6%2B-blue)
![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-yellow.svg)
![Dependencies](https://img.shields.io/librariesio/github/username/repo-name)
![GitHub issues](https://img.shields.io/github/issues/username/repo-name)

📌 TO DO: links in badges

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
git clone https://github.com/jjavrui/search-module.git
cd my_module
```

Or add search.py to your project folder and import it.
```bash
from search import SearchProblem, Node
```


## 🚀 Basic usage
Example of using 'searc' for maze solving script:

Once abstract methods of derived classes (Maze and MazeNode) are defined, maze solving is just calling **solve()** on MazeNode object.
Show result with **show_solution()** method, and get a detailed log of algorithm steps for that maze calling **save_algorithm_steps_to_file()**.

    from search import Node, SearchProblem

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


    maze = Maze(<filename>)
    maze.solve('BFS')
    maze.show_solution(dynamic=False)
    maze.save_algorithm_steps_to_file()





## features
- Object-Oriented Design
- Interface Methods and Encapsulation
- Abstract Base Classes (ABC)
- Modularity and Extensibility to add search algorithms (e.g.: informed search algorithms)
- Type hints and documentation
- Container implementations



[enhanced in documentation](docs/features.md)


## 📚 Documentation
📌 TO DO: readthedocs link

[Read The Docs documentation](docs/search_docs.md)



## 💼 Usage complete examples

The following example scripts use **search** to solve these problems:

📌 TO DO: below links to GitHub directory, that shoul have a readme ¿refering to readthedocs or just explaining in README.md?

- [maze](https://github.com/javrui/search-maze-puzzle/blob/main/maze.md): Maze solver.


- [puzzle](https://github.com/javrui/search-maze-puzzle/blob/main/puzzle.md): Puzzle solver.

## dependencies
none





## 🧪 Testing

Instructions for running the test

    pytest tests/


## ⚖️ License

Mentioned Harvard course code is published under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) [license](LICENSE.md)



##  🙏 Credits:

This project is a based on code from [HarvardX:CS50’s Introduction to Artificial Intelligence with Python course](https://pll.harvard.edu/course/cs50s-introduction-artificial-intelligence-python) refactored to use object-oriented design and abstract base clases.
