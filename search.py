"""================================================================ JRM 2024.02
Module: search
Module that defines classes to be used for solving search problems.
==============================================================================

***
TODO: AuditTrail parece que debería unirse de alguna forma a la clase Solution,
no tiene sentido que estén seaparados. ¿O Solution no es publica?
***
TODO:
En GitHub, una acprta explicando con markdown este proyecto de Search:
- origen (curso)
- codigo original del curso (copiarlo)
- mi codigo de search
- explicación de codigo search
- ejemplos de uso:
    maze
    puzzle
    ¿sokoban?
***

------------------------------------------------------------------------------
This module
------------------------------------------------------------------------------
This module provides classes to be used as a base for solving search problems
using uninformed search algorithms Breadth-First Search and Depth-First Search.

------------------------------------------------------------------------------
Introduction: search problems
------------------------------------------------------------------------------
A "search problem" refers to a class of problems in the field of Artificial
Intelligence (AI) and computer science where the objective is to find a
sequence of actions or steps that lead from an initial state to a goal state
within a problem space. In a search problem, the problem space consists of
various states, transitions (actions), and constraints that define the problem
environment.

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

 - Solution: a sequence of actions or steps that lead from the initial state to the goal state, satisfying the problem's requirements or constraints. It represents the desired outcome or resolution of the problem being solved.


------------------------------------------------------------------------------
Search implementation details
------------------------------------------------------------------------------
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

        * CAN be USED AS IS, or OVERRIDDEN to modify output format.
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

            maze = Maze(maze_file_path)             # create problem instance
            puzzle.solve(search_algorithm='DSF')    # solve it
            puzzle.show_solution()                  # print solution





============================================================================"""

class SearchProblem():
    """Base class to be used as parent for specific classes representing a
    problem that can be solved by a search algorithm.

    These are the implementations to be done by user in subclasses:

        Method to be IMPLEMENTED in subclass with specific initialization code:
            __init__()

        Method to be USED as is, OR IMPLEMENTED in subclasses with different style:
            show_solution()

        Method to be USED in subclasses (no need of further implementation)
            solve(search_algorithm)

    (See description of each method for details.)
    """

    def __init__(self):
        """ Defines common attributes for search problems.

        * Must be called from __init__() in subclasses (super().__init__(self))
        * Must be implemented in subclasses to define problem, including:
            start_node
            goal_nodE
        """

        self.start_node = None
        self.goal_node = None

        self.frontier = _Frontier()
        self.explored_nodes = _ExploredNodes()

        self.solution = None
        self.nodes_explored = None
        self.audit_trail = None

        if self.__class__ == SearchProblem:
            raise NotImplementedError("SearchProblem() subclasses must implement __init__()")


    def solve(self, search_algorithm='BSF', audit_trail=False):
        """Finds a solution to the problem using the specified search algorithm.

        Args:
            search_algorithm (str): The search algorithm to use.
                                    Defaults to 'BSF'. 'DSF' also available.
            audit_trail (bool): If True, keeps track of state changes steps
        Raises:
            Exception: If an unknown search algorithm is specified.

        Modifies:
            self.solution: list of nodes that form a solution to the problem

        Returns:
            True if a solution was found, False otherwise.
        """

        self.solution = _Solution()
        self.nodes_explored = 1

        if audit_trail:
            self.audit_trail = AuditTrail()
            audit_trail_frontier = None     # Frontier BEFORE extraction
            audit_trail_explored = None     # Explored set BEFORE extraction
            audit_trail_extracted = None
            audit_trail_expanded = None     # Nodes expanded from extracted node

        #----------------------------------------------------------------------
        # defines (empty) frontier according to search_algorithm
        #----------------------------------------------------------------------
        match search_algorithm:
            case 'BSF':
                self.frontier = _StackFrontier()
            case 'DSF':
                self.frontier = _QueueFrontier()
            case _:
                raise ValueError(f"Unknown search algorithm: {search_algorithm}")

        #----------------------------------------------------------------------
        # start node initializes frontier, explored items empty
        #----------------------------------------------------------------------
        self.frontier.add(self.start_node)
        # New set to store explored nodes
        self.explored_nodes = _ExploredNodes()

        #----------------------------------------------------------------------
        # Keep looping until solution found or frontier empty (no solution)
        #----------------------------------------------------------------------
        while self.frontier.not_empty():

            if audit_trail:
                audit_trail_frontier = self.frontier.copy()
                audit_trail_explored = self.explored_nodes.copy()

            #------------------------------------------------------------------
            # choose a node from frontier
            #------------------------------------------------------------------
            node_extracted = self.frontier.extract()

            if audit_trail:
                audit_trail_extracted = node_extracted

            #------------------------------------------------------------------
            # If node is the goal, return solution
            #------------------------------------------------------------------
            if node_extracted.state == self.goal_node.state:
                # Trace back the solution
                node = node_extracted
                while node.parent is not None:
                    self.solution.add(node)
                    node = node.parent
                self.solution.reverse()

                return True

            #------------------------------------------------------------------
            # Mark node as explored (add to explored set)
            #------------------------------------------------------------------
            self.explored_nodes.add(node_extracted)

            if audit_trail:
                audit_trail_extracted = node_extracted

            #------------------------------------------------------------------
            # Expand node (find children nodes)
            #------------------------------------------------------------------
            child_nodes = node_extracted.expand(self)

            if audit_trail:
                audit_trail_expanded = child_nodes

            #------------------------------------------------------------------
            # add each child to frontier if not in frontier nor explored_nodes
            #------------------------------------------------------------------

            for child in child_nodes:
                if not child in self.frontier and not child in self.explored_nodes:
                    self.frontier.add(child)

            #------------------------------------------------------------------
            # Adds audit trail record in case it is being kept:
            #------------------------------------------------------------------
            if audit_trail:
                self.audit_trail.add_record(audit_trail_frontier, audit_trail_explored,
                                audit_trail_extracted, audit_trail_expanded)

            self.nodes_explored += 1

        self.solution = None
        return False


    def show_solution(self):
        """Prints the solution to the problem, if it has been found."""

        print(100*'=')
        print(f"Initial state:\n{self.start_node}")
        print(f"\nGoal state:\n{self.goal_node}")

        if self.solution:
            print(self.start_node)
            for nd in self.solution:
                print(nd)
            print(f"Solution steps: {len(self.solution)} "
                    f"({len(self.explored_nodes)} nodes tried)")
        else:
            print("\nNo Solution found!")


class Node():
    """Base class to be used as parent for specific classes representing a node
    in the search tree.

    These are the implementations to be done by user in subclasses:

        Method that MAY need to be IMPLEMENTED to define attributes specific
        to search problem to be solved:
            __init__()

        Methods to be IMPLEMENTED in subclass to define issues specific to
        search problem to be solved:
            actions()
            result()
    """

    def __init__(self, state=None, parent=None, action=None):
        """Initializes a node in the search tree.

        May need to be subclassed to define attributes specific to search problem.
        """
        self.state = state
        self.parent = parent
        self.action = action


    def expand(self, search_problem: SearchProblem):
        """Return list of expanded (children) nodes of (self) node."""

        # print(f"\n> Expanding:\n{self}") #DBG
        child_nodes = []
        valid_actions = self.actions(search_problem)
        for action in valid_actions:
            expanded = self.result(action, search_problem)
            child_nodes.append(expanded)

        return child_nodes


    def actions(self, search_problem: SearchProblem):
        """Returns the list of valid actions that can be performed from a given node.

        Virtual: needs to be subclassed to define actions in specific search problem.
        """
        raise NotImplementedError


    def result(self, action, search_problem: SearchProblem):
        """Returns the node that results from performing 'action' on (self) node.

        Virtual: needs to be subclassed to define actions in specific search problem.
        """
        raise NotImplementedError


class AuditTrail():
    """ Keeps track of every step taken in in algorithm, so that it can be shown.

        - frontier
        - explored
        - extracted_node
        - expanded_nodes
    """

    def __init__(self):
        """ Implemented as list (of dictionaries)"""
        self.audit_trail = []


    def add_record(self, frontier, explored, extracted, expanded):
        """ Adds a record to the audit trail"""
        record = {  'frontier': frontier,
                    'explored': explored,
                    'extracted': extracted,
                    'expanded': expanded}

        self.audit_trail.append(record)


    def show(self):
        """ Shows list of audit records"""

        #print(f"**** DBG: {self.audit_trail=}")

        for record in self.audit_trail:
            print(50*'-')
            # Shows frontier:
            print ("> Frontier:")
            for nd in record['frontier']:
                print(f"{nd}") #DBG

            # Shows explored set:
            print ("> Explored nodes:")
            if record['explored']:
                for nd in record['explored']:
                    print(f"{nd}") #DBG
            else:
                print("Empty") #DBG

            # Shows extracted node:
            print (f"> Extracted node:\n{record['extracted']}")

            # Shows nodes expanded from extracted node:
            print ("> Node expands to:")
            for nd in record['expanded']:
                print(f"{nd}") #DBG


class _ExploredNodes():
    """Defines a set of nodes that have been explored."""

    def __init__(self):
        """Empty set of explored nodes."""
        self.explored_nodes = set()


    def __contains__(self, element):
        """Check if the explored nodes has node or node with state received"""

        if isinstance(element, Node):
            return any(element.state == nd.state for nd in self.explored_nodes)
        elif isinstance(element, tuple):
            return any(element == nd.state for nd in self.explored_nodes)
        else:
            raise ValueError("Element must be a Node or a tuple (state)")


    def __iter__(self):
        """Return an iterator over the explored nodes."""
        return iter(self.explored_nodes)


    def __repr__(self) -> str:
        """Just nodes state (other attributes omitted)"""
        return f"{[node.state for node in self.explored_nodes]}"


    def __len__(self):
        """ number of explored nodes"""
        return len(self.explored_nodes)


    def add(self, node):
        """ Add a node to the set of explored nodes"""
        self.explored_nodes.add(node)


    def copy(self):
        """Returns a copy of the explored nodes."""
        return self.explored_nodes.copy()


class _Frontier():
    """ Defines a frontier (nodes to be explored) for the search problem."""

    def __init__(self):
        """Frontier is just a list of nodes to be explored."""

        self.frontier = []


    def __iter__(self):
        """Return an iterator over the frontier."""
        return iter(self.frontier)


    def __contains__(self, element):
        """Check if the frontier has node or node with state received"""
        if isinstance(element, Node):
            return any(element.state == nd.state for nd in self.frontier)
        elif isinstance(element, tuple):
            return any(element == nd.state for nd in self.frontier)
        else:
            raise ValueError("Element must be a Node or a tuple (state)")


    def __repr__(self) -> str:
        """Just nodes state (other attributes omitted)"""
        return f"{[node.state for node in self.frontier]}"


    def add(self, node):
        """ Add a node to the frontier"""
        raise NotImplementedError


    def not_empty(self):
        """Returns true if the frontier contains nodes, false otherwise."""

        return len(self.frontier) > 0


    def extract(self):
        """ Abstract method to extract a node from the frontier, returning it.
        To be implemented in subclasses using stack or queue."""

        raise NotImplementedError


    def copy(self):
        """Returns a copy of the frontier."""
        return self.frontier.copy()


class _StackFrontier(_Frontier):
    """Defines a frontier for Breadth-First Search, using a stack (LIFO)"""

    def add(self, node):
        """ Add a node to the frontier, at end (BSF)"""

        self.frontier.append(node)

    def extract(self):
        """ extracts LAST node from the frontier and returns it"""

        if self.not_empty():
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node
        else:
            raise RuntimeError("trying to extract node from empty frontier")


class _QueueFrontier(_Frontier):
    """Defines a frontier for Depth First Search, using a queue (FIFO)"""

    def add(self, node):
        """ insert a node in the (first place of) frontier (DSF)"""

        self.frontier.append(node)


    def extract(self):
        """ Extracts FIRST node from the frontier and returns it"""

        if self.not_empty():
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node
        else:
            raise RuntimeError("trying to extract node from empty frontier")


class _Solution():
    """List of nodes that form a solution to a search problem."""

    def __init__(self):
        """Empty list of nodes that form a solution"""

        self.solution = []


    def __contains__(self, state):
        """Check if the solution already contains a 'node' with state received"""

        return any(state == nd.state for nd in self.solution)


    def __repr__(self) -> str:
        """Just shows list of nodes state"""

        return f"{[node.state for node in self.solution]}"


    def __iter__(self):
        """Return an iterator over the solution."""
        return iter(self.solution)


    def __len__(self):
        """Return number of nodes in the solution. (initial state not counted)"""
        return len(self.solution)


    def add(self, node):
        """ Add a node to the solution"""
        self.solution.append(node)


    def reverse(self):
        """Reverse the order of the nodes in the solution."""

        self.solution = self.solution[::-1]

