"""=================================================================== JRM 2024
Module: search

This module provides two abstract classes (SearchProblem and Node) to help you solve search problems using algorithms like Breadth-First Search (BFS) and Depth-First Search (DFS).

You can extend these classes to create your own search problem by overriding the abstract methods with custom logic.

Key Features:

- SearchProblem and Node define the structure and methods for search problems.

- Built-in support for BFS and DFS, with the option to add custom algorithms.

- Detailed logging to show the frontier, explored nodes, and expanded nodes at each step, helping you understand how the search algorithm works.

Usage:
Override the abstract methods in your derived classes to define the initial state, goal state, valid actions, and transition model for your problem.

"Read the docs" for details.
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

        self._initialize_search_components()

    def _initialize_search_components(self):
        """ This initializations are necessary not only in __init__(), but also in solve()."""

        self.algorithm = None
        self.frontier = _Frontier()
        self.explored_nodes = _ExploredNodes()
        self.solution = _Solution()
        self.algorithm_log = _LogHandler()

    def solve(self, search_algorithm='BFS'):
        """
        Solve the search problem using BFS or DFS algorithms.

        This method initializes the search components (frontier, explored
        nodes, solution) And executes either Breadth-First Search (BFS) or
        Depth-First Search (DFS) to find a path from the initial state to
        the goal state.

        Maintains detailed algorithm execution log including frontier state,
        explored nodes, and node expansion sequence BEFORE each node expansion.

        Args:
            search_algorithm (str, optional): The search strategy to use.
                Must be either 'BFS' or 'DFS'. Defaults to 'BFS'.

        Returns:
            bool: True if a solution is found, False otherwise.

        Raises:
            ValueError: If search_algorithm is not 'BFS' or 'DFS'.

        """
        # New solution needs initialization:

        self._initialize_search_components()
        self.algorithm = search_algorithm

        self.algorithm_log = _LogHandler()

        # Initialize the frontier based on the search algorithm type
        if search_algorithm == 'BFS':
            self.frontier = _QueueFrontier()
        elif search_algorithm == 'DFS':
            self.frontier = _StackFrontier()
        else:
            raise ValueError(f"Unknown search algorithm: {search_algorithm}")

        # Add the start node to the frontier
        self.frontier.add_node(self.start_node)

        # Keep searching until solution is found or frontier is empty
        while self.frontier.not_empty():

            self.algorithm_log.add_to_record(
                frontier=self.frontier.copy(),
                explored=self.explored_nodes.copy()
            )

            # Extract node from frontier
            extracted_node = self.frontier.extract()
            self.algorithm_log.add_to_record(
                extracted=extracted_node)

            # Finished?
            if extracted_node.state == self.goal_node.state:
                self.solution.build(extracted_node)
                self.algorithm_log.save_record()
                return True

            # Mark the node as explored
            self.explored_nodes.add_node(extracted_node)

            # Expand node and add children to the frontier
            # if not already in frontier or explored set
            child_nodes = extracted_node.expand(self)
            self.algorithm_log.add_to_record(
                expanded=child_nodes)
            for child in child_nodes:
                if child not in self.frontier and child not in self.explored_nodes:
                    self.frontier.add_node(child)

            self.algorithm_log.save_record()

        # If no solution found
        self.solution = None
        return False

    def show_solution(self):
        """
        Basic print of solution, if one exists, along with the number of nodes explored.
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
        """
        Initialize a Node object in the search tree.

        Args:
            state: The state represented by this node. Default is None.
            parent (Node, optional): The parent node from which this node
            was generated. Default is None.
            action: The action that was taken to reach this node from its parent. Default is None.

        Returns:
            None
        """
        self.state = state
        self.parent = parent
        self.action = action

    @abstractmethod
    def actions(self, search_problem: SearchProblem):
        """
        Return a list of valid actions for this node.

        This method should be implemented by subclasses to define the possible
        actions that can be taken from the current node state in the context
        of the given search problem.
        Args:
            search_problem (SearchProblem): The problem being solved, which
                provides the context and constraints for determining valid actions.

        Returns:
            list: A list of actions available from this node. The specific type
                of the actions depends on the problem domain and should be
                consistent with the action representation used in the search problem.

        Raises:
            NotImplementedError: If the method is not implemented by a subclass.
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

    def node_action(self):
        return self.action

    def node_state(self):
        return self.state

    def expand(self, search_problem: SearchProblem):
        """
        Expands the current node by generating all possible child nodes based on valid actions.

        Args:
            search_problem (SearchProblem): The search problem instance providing the context
                                        for expanding this node.

        Returns:
            list[Node]: A list of child Node objects resulting from applying all valid
                    actions to the current node.

        Note:
            This method uses the node's actions() method to get valid actions and
            result() method to generate child nodes for each action.
        """
        child_nodes = []
        valid_actions = self.actions(search_problem)
        for action in valid_actions:
            expanded = self.result(action, search_problem)
            child_nodes.append(expanded)
        return child_nodes

    def __eq__(self, other):
        if not isinstance(other, Node):
            return NotImplemented
        return self.state == other.state

    def __hash__(self):
        return hash(self.state)


class _NodeContainer(ABC):

    def __init__(self, node=None):
        self.nodes = node

    def __contains__(self, element):
        if isinstance(element, Node):
            return element in self.nodes
        elif isinstance(element, tuple):
            return any(element == nd.state for nd in self.nodes)
        else:
            raise ValueError("Element must be a Node or a tuple (state)")

    def __iter__(self):
        return iter(self.nodes)

    def __repr__(self) -> str:
        return f"{[node.state for node in self.nodes]}"

    def __len__(self):
        return len(self.nodes)

    def not_empty(self):
        return len(self.nodes) > 0

    def copy(self):
        copied = self.__class__()  # Create a new instance of the same class
        copied.nodes = self.nodes.copy()  # Copy the nodes
        return copied


class _ExploredNodes(_NodeContainer):
    """
    Represents the set of explored nodes in the search.
    """

    def __init__(self):
        super().__init__(set())

    def add_node(self, node):
        self.nodes.add(node)


class _Frontier(_NodeContainer):
    """
    Represents the frontier in a search, i.e., nodes yet to be explored.
    """

    def __init__(self):
        super().__init__(list())

    def add_node(self, node):
        self.nodes.append(node)

    def extract(self):
        raise NotImplementedError


class _StackFrontier(_Frontier):
    """
    Implements a stack-based frontier (LIFO) for depth-first search (DFS).
    """
    def extract(self):
        if self.not_empty():
            return self.nodes.pop()
        else:
            raise RuntimeError("Trying to extract node from an empty frontier")


class _QueueFrontier(_Frontier):
    """
    Implements a queue-based frontier (FIFO) for breadth-first search (BFS).
    """

    def extract(self):
        if self.not_empty():
            return self.nodes.pop(0)
        else:
            raise RuntimeError("Trying to extract node from an empty frontier")


class _Solution (_NodeContainer):
    """
    List of nodes that form the solution path.
    """

    def __init__(self):
        super().__init__(list())

    def build (self, goal_node):
        """Builds the solution path from the goal node back to the start node.
        Args:
            goal_node (_type_): _description_
        """
        node = goal_node
        while node is not None:
            self.nodes.append(node)
            node = node.parent
        self.nodes.pop()
        self.nodes.reverse()


class _LogHandler():

    def __init__(self):
        # Initialize an empty log and a temporary record for staging entries
        self.log = []
        self.current_record = {}

    def add_to_record(self, frontier=None, explored=None, extracted=None, expanded=None):

        # Define a dictionary mapping parameter names to expected types
        params = {
            'frontier': (frontier, _Frontier),
            'explored': (explored, _ExploredNodes),
            'extracted': (extracted, Node),
            'expanded': (expanded, list)
        }

        # Iterate over each parameter to validate and update the record
        for key, (value, expected_type) in params.items():
            if value is not None:
                if isinstance(value, expected_type):
                    self.current_record[key] = value
                else:
                    raise ValueError(f"Invalid {key}: {value}. "
                        f"Must be an instance of {expected_type.__name__}.")

    def save_record(self):

        # Add a copy of the current record to the log
        self.log.append(self.current_record.copy())

        # Clear the current record for the next set of entries
        self.current_record.clear()

    def get_log(self):
        # Optional: Provide a method to access the entire log
        return self.log

    def save_log(self, log_filename):
        with open(log_filename, 'a', encoding='utf-8') as file:
            file.write("- Algorithm steps:\n")

            for step_nr, record in enumerate(self.log, start=1):
                file.write(f"[{step_nr}]\n")

                # Writes explored set:
                file.write("  > Explored nodes:\n")
                if record.get('explored'):
                    for nd in record['explored']:
                        file.write(f"      {nd.node_state()}\n")
                # Writes frontier:
                file.write("  > Frontier:\n")
                for nd in record.get('frontier', []):
                    file.write(f"      {nd.node_state()}\n")

                # Writes extracted node:
                if record.get('extracted'):
                    file.write(f"  > Extracted node:\n      {record['extracted'].node_state()}\n")

                # Writes nodes expanded from extracted node:
                file.write("  > Node expands to:\n")
                for nd in record.get('expanded', []):
                    file.write(f"      {nd.node_state()}\n")