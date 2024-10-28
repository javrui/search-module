# search
Python module that implements Breadth-First Search and Depth-First Search algorithms to be used in pathfinding and many problem-solving contexts.

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-yellow.svg)
![Dependencies](https://img.shields.io/librariesio/github/username/repo-name)
![GitHub issues](https://img.shields.io/github/issues/username/repo-name)

📌 TO DO: links in badges

## ✨Overview
**search** provides two interface classes:

- class Node
- class SearchProblem

User needs to define a derived class from each one, to implement specific details of problem context.  Precisely, needs to write these methods:

- SearchProblem.__init__()
- SearchProblem.show_solution()

and

- Node.__init__()
- Node.actions()
- Node.result()

Specific instructions are available in documentation.


## 🚀 Basic usage

    from search import Node, SearchProblem

    # Create derived classes/methods
    class Maze(SearchProblem):
        __init__()
        ...

        show_solution()
        ...

    class MazeNode(Node)
        __init__()
        ...

        actions()
        ...

        result()
        ...


    maze = Maze(<maze_file_path>)         # create problem instance
    maze.solve(search_algorithm='DSF')    # solve it
    maze.show_solution()                  # print solution


## 📚 Documentation
(readthedocs link)



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
