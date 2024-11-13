
📌 TO DO:
* AuditTrail parece que debería unirse de alguna forma a la clase Solution,no tiene sentido que estén seaparados.
* Usar ABC !


## *search* module
*search* module provides an interface of two base classes that implement  breadth-first search (BFS) and depth-first search (DFS) algorithms.

To use module, you have to create a derived class from each of those base ones and override some methods, in order to implement your problem specific details, e.g.: solving a maze, a puzzle, ..

## How to use *search* module

Methods to be written by you to override base class ones specification:

#### SearchProblem() derived class methods

* **__init__()**

    * MUST be implemented by you.
    * Initializes values relevant to the specific search problem for these **attributes**:
      - **start_node**
      - **goal_node**
    * MAY define other attributes if needed by **Node** derived class methods:
      - actions()
      - result()
    * MUST call super().__init__(), generally as first method statement.


* **show_solution()**

    * MAY be defined, if *search* module default format for solution print needs modification, otherwise there is no need to override parent class method.

#### Node() derived class methods:

* **__init__()**

    * Needed only in case it is necessary to initialize attributes needed by Node derived class methods:
        - actions()
        - result()
    * if defined, MUST call super().init(), generally as first method statement.


* **actions()**
    * MUST be implemented by you.
    * Defines possible actions from a node that lead to other nodes in the search tree. (Example: possible movements in a maze.)


* **result()**
    * MUST be implemented by you.
    * Returns the node that results from performing an 'action' on self (provided by 'actions()'). Example: new position in a maze after a possible movement provided by 'actions()'.


### 3.- Basic usage example

📌 TO DO: REVISAR parametros de metodos, cambian:
REVISAR el resultado en real!!


Example for maze search problem, where:
  - *SearchProblem* derived user class is named *Maze*
  - *Node* derived user class is named *MazeNode*


```python
from search import Node, SearchProblem

class Maze(SearchProblem):
    def __init__():
        ...
    def show_solution():
        ...

class MazeNode(Node):
    def actions():
        ...
    def result():
        ...

maze = Maze(<maze_file_path>)

try:
    maze.solve('BSF')
except ValueError as e:
    print(e)
else:
    maze.show_solution()
```

To see complete code of maze solving example, please visit [maze](../maze/maze.py)