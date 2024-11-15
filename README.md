# search
Python module for search problems solving

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-yellow.svg)
![Dependencies](https://img.shields.io/librariesio/github/username/repo-name)
![GitHub issues](https://img.shields.io/github/issues/username/repo-name)

📌 TO DO: links in badges

## ✨Overview
📌 TO DO: esto no me gusta como queda:

This module provides two abstract base classes to be used for search problems solving, using Breadth-First or Depth-First Search algorithms.

Users of this module are expected to subclass those base classes to write its abstract methods according to the search problem specific logic.




## 🚀 Basic usage
Example of maze problem solving. User writes abstract methods of derived classes (Maze and MazeNode), and solves maze just calling **solve()**:

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


    maze = Maze(<maze_file_path>)
    maze.solve(search_algorithm='DSF')
    maze.show_solution()


## features
Object-Oriented Design, Interface Methods and Encapsulation, Abstract Base Classes (ABC), Modularity and Extensibility to add search algorithms (e.g.: informed search algorithms), debug mode to trace solving steps.
[enhanced in documentation](docs/features.md)


## 📚 Documentation
📌 TO DO: readthedocs link

[Read The Docs documentation](docs/search_docs.md)



## 💼 Usage complete examples

The following example scripts use **search** to solve these problems:

📌 TO DO: below links to GitHub directory, that shoul have a readme ¿refering to readthedocs or just explaining in README.md?

- [maze](https://github.com/javrui/search-maze-puzzle/blob/main/maze.md): Maze solver.


- [puzzle](https://github.com/javrui/search-maze-puzzle/blob/main/puzzle.md): puzzle solver.

## dependencies
none


## 📥 Installation
Step-by-step guide to install your module.

```bash
# Clone the repo
git clone https://github.com/yourusername/my_module.git
cd my_module

# Install dependencies
pip install -r requirements.txt

# Install the module
pip install .
```


## 🧪 Testing

Instructions for running the test

    pytest tests/


## ⚖️ License

Mentioned Harvard course code is published under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) [license](LICENSE.md)



##  🙏 Credits:

This project is a based on code from [HarvardX:CS50’s Introduction to Artificial Intelligence with Python course](https://pll.harvard.edu/course/cs50s-introduction-artificial-intelligence-python) refactored to use object-oriented design and abstract base clases.
