# search
Module that defines classes to be used to solve search problems applying Breadth-First Search and Depth-First Search uninformed algorithms.


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




## Understanding search problems

A 'search problem' in the field of Artificial Intelligence (AI) and computer science, are problems where the objective is to find a sequence of actions or steps  that lead from an initial state to a goal state within a problem space. In a search problem, the problem space consists of various states, transitions  (actions), and constraints that define the problem environment.

Formally, a search problem is defined by:

 - Initial State: The starting configuration or condition of the problem space
   from which the search process begins.

 - Goal State: The desired outcome or target configuration that the search
   algorithm aims to reach. The goal state represents the solution to the
   problem.

 - Actions: Possible moves or transitions that can be taken from one state to
   another in the problem environment. Each action defines a valid path in the
   search space.

 - State Space: The set of all possible states that can be reached from the
   initial state through a sequence of actions. The state space represents the
   entire problem domain that the search algorithm explores.


These concepts are also relevant:

 - Node: represents a specific state within the state space. Each node contains information about the state it represents, as well as other relevant attributes as parent node and action that leads to node from parent.

 - Solution: a sequence of actions or steps that lead from the initial state to the goal state, satisfying the problem's requirements or constraints. It represents the desired outcome or resolution of the problem..



## How this module implement search algorithms

Search algorithms implemented is an iterative approach
The search process algorithm implemented involves the following steps (where
'frontier' and 'explored set' are containers of nodes considered in each
algorithm iteration):

    • Start with a 'frontier' that contains the initial state.
    • Start with an empty 'explored set'.
    • Repeat:
        • If the frontier is empty, then no solution.
        • If node contains goal state, return the solution.
        • Remove a node from the frontier.
    • Add the node to the explored set.
    • Expand node. For each expanded node:
        • If node is not already in the frontier or the explored set:
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


------------------------------------------------------------------------------
Basic usage examples:
------------------------------------------------------------------------------

Basic usage (example with maze problem):

    1.- Import module

            from search import Node, SearchProblem

    2.- Declare 'SearchProblem' and 'Node' subclasses for specific problem, and
        implement methods in those subclasses. For example, for a maze problem:

            class Maze(SearchProblem):
                __init__()
                show_solution()

            class MazeNode(Node)
                __init__()     (only if specific attributes needed)
                actions()
                result()

        See 'SearchProblem' and 'Node' classes docstring for details on methods


    3.- Example of basic code for maze problem:

            maze = Maze(maze_file_path)           # create problem instance
            maze.solve(search_algorithm='DSF')    # solve it
            maze.show_solution()                  # print solution





============================================================================"""
