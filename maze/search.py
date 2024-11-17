"""================================================================ JRM 2024.02
Module: search
============================================================================"""

from typing import Optional
from abc import ABC, abstractmethod

class SearchProblem(ABC):
    """
    Represents an abstract search problem.
    It defines the common methods and properties needed for implementing search algorithms.

    Note:
        Derived classes will likely need to override the `__init__()` method
        to include problem-specific attributes.
        When overriding `__init__()`, it is important to call
        `super().__init__()` to ensure that the base class
        attributes are properly initialized.
    """

    def __init__(self):
        self.start_node: Optional[Node] = None
        self.goal_node: Optional[Node] = None

        self.algorithm = None
        self.frontier = _Frontier()
        self.explored_nodes = _ExploredNodes()
        self.solution = _Solution()
        self.algorithm_steps_record = None


    def solve(self, search_algorithm='BFS', record_algorithm_steps=False):
        """
        Solve the search problem using the specified search algorithm.


        'algorithm_steps_record' attribute records the state of the frontier
        and explored nodes BEFORE extracting node to be expanded.

        Args:
            search_algorithm (str): The search algorithm to use ('BFS' or 'DFS').
            record_algorithm_steps (bool): Whether to keep an audit trail of the search process.

        Returns:
            bool: True if a solution is found, False otherwise.

        """
        # A new solution needs initialization:
        self.frontier = _Frontier()
        self.explored_nodes = _ExploredNodes()
        self.solution = _Solution()
        self.algorithm = search_algorithm
        self.algorithm_steps_record = _AlgorithmLog()

        if record_algorithm_steps is True:
            audit_trail_frontier = None
            audit_trail_explored = None
            audit_trail_extracted = None
            audit_trail_expanded = None

        # Initialize the frontier based on the search algorithm type
        if search_algorithm == 'BFS':
            self.frontier = _QueueFrontier()
        elif search_algorithm == 'DFS':
            self.frontier = _StackFrontier()
        else:
            raise ValueError(f"Unknown search algorithm: {search_algorithm}")

        # Add the start node to the frontier
        self.frontier.add(self.start_node)

        # Keep searching until solution is found or frontier is empty
        while self.frontier.not_empty():

            if record_algorithm_steps is True:
                # records values BEFORE node extraction
                audit_trail_frontier = self.frontier.copy()
                audit_trail_explored = self.explored_nodes.copy()

            # Extract node from frontier
            node_extracted = self.frontier.extract()
            if record_algorithm_steps is True:
                audit_trail_extracted = node_extracted

            # If the node is the goal, trace back the solution
            if node_extracted.state == self.goal_node.state:
                node = node_extracted
                while node.parent is not None:
                    self.solution.add(node)
                    node = node.parent
                self.solution.reverse()
                return True

            # Mark the node as explored
            self.explored_nodes.add(node_extracted)

            # Expand node and add children to the frontier
            # if not already in frontier or explored set
            child_nodes = node_extracted.expand(self)
            if record_algorithm_steps is True:
                audit_trail_expanded = child_nodes
            for child in child_nodes:
                if child not in self.frontier and child not in self.explored_nodes:
                    self.frontier.add(child)

            if record_algorithm_steps is True:
                self.algorithm_steps_record.add_record(
                    audit_trail_frontier, audit_trail_explored,
                    audit_trail_extracted, audit_trail_expanded
                )

        # If no solution found
        self.solution = None
        return False

    def show_solution(self):
        """
        Print the solution, if one exists, along with the number of nodes explored.
        """
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


class Node(ABC):
    """
    Represents a node in the search tree.
    """

    def __init__(self, state=None, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.action = action

    @abstractmethod
    def actions(self, search_problem: SearchProblem):
        """
        Return a list of valid actions for this node.

        Args:
            search_problem (SearchProblem): The problem being solved.

        Returns:
            list: A list of actions available from this node.
        """

    @abstractmethod
    def result(self, action, search_problem: SearchProblem):
        """
        Return the resulting node from performing the given action.

        Args:
            action: The action to be performed.
            search_problem (SearchProblem): The problem being solved.

        Returns:
            Node: The resulting node after the action.
        """


    def expand(self, search_problem: SearchProblem):
        """
        Expand this node to generate child nodes.

        Args:
            search_problem (SearchProblem): The problem being solved.

        Returns:
            list: A list of child nodes generated from this node.
        """
        child_nodes = []
        valid_actions = self.actions(search_problem)
        for action in valid_actions:
            expanded = self.result(action, search_problem)
            child_nodes.append(expanded)
        return child_nodes


class _ExploredNodes:
    """
    Represents the set of explored nodes in the search.
    """

    def __init__(self):
        self.explored_nodes = set()

    def __contains__(self, element):
        if isinstance(element, Node):
            return any(element.state == nd.state for nd in self.explored_nodes)
        elif isinstance(element, tuple):
            return any(element == nd.state for nd in self.explored_nodes)
        else:
            raise ValueError("Element must be a Node or a tuple (state)")

    def __iter__(self):
        return iter(self.explored_nodes)

    def __repr__(self) -> str:
        return f"{[node.state for node in self.explored_nodes]}"

    def __len__(self):
        return len(self.explored_nodes)

    def add(self, node):
        self.explored_nodes.add(node)

    def copy(self):
        return self.explored_nodes.copy()


class _Frontier():
    """
    Represents the frontier in a search, i.e., nodes yet to be explored.
    """

    def __init__(self):
        self.frontier = []

    def __iter__(self):
        return iter(self.frontier)

    def __contains__(self, element):
        if isinstance(element, Node):
            return any(element.state == nd.state for nd in self.frontier)
        elif isinstance(element, tuple):
            return any(element == nd.state for nd in self.frontier)
        else:
            raise ValueError("Element must be a Node or a tuple (state)")

    def __repr__(self) -> str:
        return f"{[node.state for node in self.frontier]}"

    def add(self, node):
        self.frontier.append(node)

    def not_empty(self):
        return len(self.frontier) > 0

    def extract(self):
        raise NotImplementedError

    def copy(self):
        return self.frontier.copy()


class _StackFrontier(_Frontier):
    """
    Implements a stack-based frontier (LIFO) for depth-first search (DFS).
    """
    def extract(self):
        if self.not_empty():
            return self.frontier.pop()
        else:
            raise RuntimeError("Trying to extract node from an empty frontier")


class _QueueFrontier(_Frontier):
    """
    Implements a queue-based frontier (FIFO) for breadth-first search (BFS).
    """

    def extract(self):
        if self.not_empty():
            return self.frontier.pop(0)
        else:
            raise RuntimeError("Trying to extract node from an empty frontier")


class _Solution:
    """
    Represents the solution found by the search algorithm.
    """

    def __init__(self):
        self.solution = []

    def __contains__(self, state):
        return any(state == nd.state for nd in self.solution)

    def __repr__(self) -> str:
        return f"{[node.state for node in self.solution]}"

    def __iter__(self):
        return iter(self.solution)

    def __len__(self):
        return len(self.solution)

    def add(self, node):
        self.solution.append(node)

    def reverse(self):
        self.solution.reverse()



class _AlgorithmLog:
    """
    Keeps a record of frontier, explored set, node extracted and nodes
    generated when expanded in algorithm solving, for didactic purposes.

    Generated every time solve() method is called with record_algorithm_steps=True.
    """

    def __init__(self):
        self.algorithm_steps = []

    def add_record(self, frontier, explored, extracted, expanded):
        """
        Add a record to the audit trail.

        Args:
            frontier: The state of the frontier.
            explored: The state of the explored nodes.
            extracted: The node extracted from the frontier.
            expanded: The nodes expanded from the extracted node.
        """
        record = {'frontier': frontier, 'explored': explored,
                  'extracted': extracted, 'expanded': expanded}
        self.algorithm_steps.append(record)

    def not_empty(self):
        return len(self.algorithm_steps) > 0

    def show(self):
        """
        Print the audit trail.
        """
        for step, record in enumerate(self.algorithm_steps, start=1):
            print(f"\n[{step}]")
            # Shows frontier:
            print("  > Frontier:")
            for nd in record.get('frontier', []):
                print(f"      {nd}")

            # Shows explored set:
            print("  > Explored nodes:")
            if record.get('explored'):
                for nd in record['explored']:
                    print(f"      {nd}")

            # Shows extracted node:
            if record.get('extracted'):
                print(f"  > Extracted node:\n      {record['extracted']}")

            # Shows nodes expanded from extracted node:
            print("  > Node expands to:")
            for nd in record.get('expanded', []):
                print(f"      {nd}")
