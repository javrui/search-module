# "search" module documentation


# Introduction to search problem

<details> <summary><h2>Search problem and AI</h2></summary>

A search problem refers to a class of problems in the field of Artificial Intelligence (AI) and computer science where the objective is to find a sequence of **actions** or steps that lead from an **initial state** to a **goal state**  within a problem space. The problem space consists of various states, transitions (actions), and constraints that define the problem environment.

</details>

## Generic uninformed search algorithm
A generic uninformed search algorithm is a strategy for exploring a problem space without prior knowledge of the goal's location. Instead of relying on domain-specific information, uninformed search uses only the structure of the problem to navigate through the state space.

Algorithms like Breadth-First Search (BFS) and Depth-First Search (DFS) are classic examples fo uninformed searching algorithms. **search** module implements both of them.


## Key concepts

Search module implements these key concepts of uninformed search algorithm:

* **State**: Represents a specific configuration or condition within the problem space. For example, in a maze, each position within the maze could be considered a unique state.

* **Node**: A data structure representing a state in the search process, including additional information such as its parent node (where it came from) and the path cost to reach it.

* **Initial State**: The starting point or beginning configuration of the search. The algorithm starts exploring from this state to find a path to the goal state.

* **Goal State**: The desired target state that satisfies the conditions of the problem. The search algorithm stops when it reaches this state.

* **Actions** (from Node): These are the possible moves or steps that can be taken from a given node to transition into neighboring states. For example, in a grid, actions might be moving up, down, left, or right.

* **Expand** (node): The process of exploring a node's neighboring states by generating its successors based on possible actions. Expanding a node involves creating new nodes for each resulting state from an action.

* **Frontier**: A collection of all nodes available to be explored. It contains the nodes that have been generated but not yet expanded. The frontier controls the order in which nodes are expanded and determines the search strategy, such as Breadth-First Search (BFS) or Depth-First Search (DFS).

* **Explored Set**: A set of nodes that have already been expanded. It helps prevent redundant exploration by keeping track of visited nodes to avoid loops and repeated states.


## Algorithm steps
Search algorithm in **search** module follows this pseudocode:

- Start with a 'frontier' that contains the initial state.
- Start with an empty 'explored set'.

- Repeat:
    - If the frontier is empty, then no solution.
    - If node contains goal state, return the solution.
    - Remove a node from the frontier.
    - Add the node to the explored set.
    - Expand node. For each expanded node:
        - If node is not already in the frontier or the explored set:
            Add node to frontier


# search module

## How search module

**search** provides two interface classes:

- class Node
- class SearchProblem

User needs to define a derived class from each one, to implement specific details of problem context.  Precisely, needs to override these abstract methods to define an actual search problem:


- SearchProblem.__init__()
- SearchProblem.**show_solution()**

and

- Node.__init__()
- Node.**actions()**
- Node.**result()**
















“raise NotImplementedError()” is a way to specify that this is an abstract method that needs to be overridden to define an actual search problem


## Overview
**search** provides two classes: *SearchProblem* and *Node*, that user has to create his/her own derivated classe.
The following methods have to be implemented by user to define specific search problem details:

    class Maze(SearchProblem):
        __init__()
        show_solution()

    class MazeNode(Node)
        __init__()     (only if specific attributes needed)
        actions()
        result()



    __init__() in SearchProblem() derived class:

        * Method TO BE IMPLEMENTED with specific initialization code
        * Must call super().__init__()
        * Has to define, according to specific search problem:
            start_node
            goal_node
        * May need to define other relevant attributes specific to problem


    show_solution() in SearchProblem() derived class:

        * CAN be USED AS SI, or OVERRIDDEN to modify output format.
        Shows the solution to the problem.


    __init__() in Node() derived class:
        * MAY need to be implemented to define attributes necessary for
        actions() and results() methods.


    actions() in Node() derived class:
        * TO BE implemented to define possible actions from a node that lead
        to other nodes in the search tree. Example: possible movements in a maze.


    result() in Node() derived class:
        * TO BE IMPLEMENTED to return the node that results from performing
        an 'action' on self (provided by 'actions()'). Example: new position
        in a maze after a possible movement provided by 'actions()'.


User defines his/her problem specific classes, derived from *search* classes. Implements some of its methods (to define problem specific details). Uses some methods to solve the search problem.





## TODO:
AuditTrail parece que debería unirse de alguna forma a la clase Solution,
no tiene sentido que estén seaparados.





## How this module implement search algorithms

Search algorithms implemented is an iterative approach
The search process algorithm implemented involves the following steps (where
'frontier' and 'explored set' are containers of nodes considered in each
algorithm iteration):

    - Start with a 'frontier' that contains the initial state.
    - Start with an empty 'explored set'.
    - Repeat:
        - If the frontier is empty, then no solution.
        - If node contains goal state, return the solution.
        - Remove a node from the frontier.
    - Add the node to the explored set.
    - Expand node. For each expanded node:
        - If node is not already in the frontier or the explored set:
            Add node to frontier

This code implements two uninformed search algorithms (BSF and DSF).The kind of
data structures used as frontier, defines the search algorithm:

    stack for Breadth-First Search (BSF)
    queue for Depth-First Search (DSF).


------------------------------------------------------------------------------
Using the search module
------------------------------------------------------------------------------

To use this module to solve a search problem, the user needs to follow these
steps:

1) Derive a class from module base classes 'SearchProblem' and 'Node':
------------------------------------------------------------------------------

User has to define a subclass specific to search problem, derived from each of
these module base classes:

    SearchProblem()
    Node()

Example of derived classes for a maze problem:

    class Maze(SearchProblem):
        ...

    class MazeNode(Node):
        ...

2) Implement methods in derived classes:
------------------------------------------------------------------------------

    __init__() in SearchProblem() derived class:

        * Method TO BE IMPLEMENTED with specific initialization code
        * Must call super().__init__()
        * Has to define, according to specific search problem:
            start_node
            goal_node
        * May need to define other relevant attributes specific to problem


    show_solution() in SearchProblem() derived class:

        * CAN be USED AS SI, or OVERRIDDEN to modify output format.
        Shows the solution to the problem.


    __init__() in Node() derived class:
        * MAY need to be implemented to define attributes necessary for
        actions() and results() methods.


    actions() in Node() derived class:
        * TO BE implemented to define possible actions from a node that lead
        to other nodes in the search tree. Example: possible movements in a maze.


    result() in Node() derived class:
        * TO BE IMPLEMENTED to return the node that results from performing
        an 'action' on self (provided by 'actions()'). Example: new position
        in a maze after a possible movement provided by 'actions()'.


3) Use this methods
------------------------------------------------------------------------------

    SearchProblem.solve()           to solve the problem
    SearchProblem.show_solution()   to show the solution


    show_solution() prints the solution to the problem, if it has been found.
    it can be used as is, or overridden or enhanced in derived classes to
    modify the output format.

