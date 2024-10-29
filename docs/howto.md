
📌 TO DO:
* AuditTrail parece que debería unirse de alguna forma a la clase Solution,no tiene sentido que estén seaparados.
* Usar ABC !




## How to use search module

**search** provides two interface classes:

- class **Node**
- class **SearchProblem**

User needs to:

**1.- define derived class from each interface classes**

    class Maze(SearchProblem):
        def __init__():
        ...
        def show_solution():
        ...

    class MazeNode(Node)
        __init__()     (only if specific attributes needed)
        actions()
        result()


**2.- implement specific details of problem context in these methods:**


Example (user own subclass named 'Maze'):








-  &lt;**SearchProblem** derived user class&gt;.__init__()
-  &lt;**SearchProblem** derived user class&gt;.**show_solution()**


-  &lt;**Node** derived user class&gt;.__init__()
-  &lt;**Node** derived user class&gt;.**actions()**
-  &lt;**Node** derived user class&gt;.**result()**





## Overview
**search** provides two base classes: *SearchProblem* and *Node*., that user has to create his/her own derivated classe.
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









## How to use search module

Basically, user instantiates an object from an own SearchProblem class derived class, and then calls solve() (perhaps also show_solution())

User

1) Derive a class from module base classes 'SearchProblem' and 'Node':

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

    SearchProblem.solve()           to solve the problem
    SearchProblem.show_solution()   to show the solution


    show_solution() prints the solution to the problem, if it has been found.
    it can be used as is, or overridden or enhanced in derived classes to
    modify the output format.

