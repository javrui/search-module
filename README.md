# search
Python module to be used in pathfinding and other problem-solving contexts.

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-yellow.svg)
![Dependencies](https://img.shields.io/librariesio/github/username/repo-name)
![GitHub issues](https://img.shields.io/github/issues/username/repo-name)

📌 TO DO: links in badges

## ✨Overview
**search** implements Breadth-First Search and Depth-First Search algorithms as a solve() method of base classes

two interface classes implementing Breadth-First Search and Depth-First Search algorithms.

User just needs to override some abstract methods in her/his derived classes, to implement specific problem context details

See [📚 Documentation](#-documentation) for details.


## 🚀 Basic usage
Example of maze solving: user creates 2 derived classes from 2 **search** module base classes, overrides 5 methods, and solves maze just calling **solve()**:

    from search import Node, SearchProblem

    # Create derived classes and override base class abstract methods

    class Maze(SearchProblem):
        def __init__():
        ...

        def show_solution():
        ...

    class MazeNode(Node)
        def __init__():
        ...

        def actions():
        ...

        def result():
        ...

    # create problem instance, solve it and show solution:

    maze = Maze(<maze_file_path>)
    maze.solve(search_algorithm='DSF')
    maze.show_solution()


## 📚 Documentation
📌 TO DO: readthedocs link

[search documentation](docs/search_docs.md)



## 💼 Usage complete examples

The following example scripts use **search** to solve these problems:

📌 TO DO: below links to GitHub directory, that shoul have a readme ¿refering to readthedocs or just explaining in README.md?

- [maze](https://github.com/javrui/search-maze-puzzle/blob/main/maze.md): Maze solver.


- [puzzle](https://github.com/javrui/search-maze-puzzle/blob/main/puzzle.md): puzzle solver.


## 🧪 Testing

Instructions for running the test

    pytest tests/


##  🙏 Credits:

This project is a based on code from [HarvardX:CS50’s Introduction to Artificial Intelligence with Python course](https://pll.harvard.edu/course/cs50s-introduction-artificial-intelligence-python) refactored to use object-oriented design.


## ⚖️ License

Mentioned Harvard course code is published under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) [license](LICENSE.md)


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
