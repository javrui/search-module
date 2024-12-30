"""
    This module provides a framework for solving path finding problems using
    common search algorithms like Breadth-First Search (BFS) and
    Depth-First Search (DFS).

    It presents two interface classes: 'SearchProblem' and 'Node'. Both are
    abstract classes. You must subclass each one. Create your own two derived
    classes where you will write code to implement the following methods,
    specific for your problem:

        SearchProblem.__init__()
        Node.actions()
        Node.result()

    You may also want to override the following methods, if necessary for your problem:

        Node.__init__()
        Node.__repr__()

    To achieve a solution representation adapted to your specific problem, you
    may also want to override this methods:

        SearchProblem.show_solution()
        SearchProblem.save_algorithm_steps_to_file()

    Once base classes have been implemented, you just call SearchProblem
    interface methods:

        solve()
        show_solution()
        save_algorithm_steps_to_file()

    Dependencies:
        - Python 3.6 or higher
"""

from typing import Optional, List, Union
from abc import ABC, abstractmethod

class SearchProblem(ABC):
    """
    Represents an abstract search problem.

    It defines the common methods and properties needed for implementing
    search algorithms.

    Derived classes need to override the `__init__()` method to include
    problem-specific attributes. show_solution() and
    save_algorithm_steps_to_file() methods are usual candidates for override.

    Attributes:
        start_node (Optional[Node]): The initial state of the search problem.
        goal_node (Optional[Node]): The goal state of the search problem.
        algorithm (Optional[str]): The search algorithm to use (e.g., 'BFS',
            'DFS').
        frontier (_Frontier): The frontier used in the search algorithm.
        explored_nodes (_ExploredNodes): The set of nodes that have been
            explored.
        solution (_Solution): The solution path from the start node to the
            goal node.
        algorithm_log (_LogHandler): A handler for recording algorithm
            execution steps.

    """

    def __init__(self) -> None:
        """
        Initializes the SearchProblem object.

        This method sets up the 'start_node' and 'goal_node' attributes,
        both initially assigned as `None`. It also initializes other attributes
        (e.g., frontier, explored nodes, solution) by calling
        `_initialize_search_components()`.

        Note:
            This method MUST be overridden. Redefined method in subclass:

            - MUST assign 'start_node' and 'goal_node' attributes with
              appropriate values.
            - MUST call `super().__init__()` (generally as first statement)
            - MAY define other attributes relevant to the specific search
              problem, if needed by actions() or result() methods in 'Node'
              derived class.

        Returns:
            None

        """
        self.start_node = None
        self.goal_node = None

        self._initialize_search_components()

    def _initialize_search_components(self) -> None:
        """
        Initializes components required for the search.

        This method is responsible for initializing the search attributes,
        such as the algorithm type, frontier, explored nodes, solution, and log
        handler.
        It is called during both initialization of class object, and
        at the start of the solve process, that is why it is apart from __init__() method.

        Returns:
            None
        """
        self.algorithm = None
        self.frontier = _Frontier()
        self.explored_nodes = _ExploredNodes()
        self.solution = _Solution()
        self.algorithm_log = _LogHandler()

    def solve(self, search_algorithm: str = 'BFS') -> bool:
        """
        Solves the search problem using BFS or DFS algorithms.

        This method initializes the search components (frontier, explored
        nodes, solution) and executes either Breadth-First Search (BFS) or
        Depth-First Search (DFS) to find a path from the initial state to
        the goal state.

        Breadth-First Search (BFS) explores nodes level by level, whereas
        Depth-First Search (DFS) explores nodes as far as possible along each
        branch.

        Maintains detailed algorithm execution log including frontier state,
        explored nodes, and node expansion sequence BEFORE each node expansion.

        Args:
            search_algorithm (str): The search strategy to use. Must be either
                'BFS' or 'DFS'.

        Returns:
            bool: True if a solution is found, False otherwise.

        Raises:
            ValueError: If search_algorithm is not 'BFS' or 'DFS'.
        """
        self._initialize_search_components()
        self.algorithm = search_algorithm

        self.algorithm_log = _LogHandler()

        if search_algorithm == 'BFS':
            self.frontier = _QueueFrontier()
        elif search_algorithm == 'DFS':
            self.frontier = _StackFrontier()
        else:
            raise ValueError(f"Unknown search algorithm: {search_algorithm}")

        self.frontier.add_node(self.start_node)

        while self.frontier.not_empty():
            self.algorithm_log.add_to_record(
                frontier=self.frontier.copy(),
                explored=self.explored_nodes.copy()
            )

            extracted_node = self.frontier.extract()
            self.algorithm_log.add_to_record(extracted=extracted_node)

            if extracted_node.state == self.goal_node.state:
                self.solution.build(extracted_node)
                self.algorithm_log.save_record()
                return True

            self.explored_nodes.add_node(extracted_node)

            child_nodes = extracted_node.expand(self)
            self.algorithm_log.add_to_record(expanded=child_nodes)
            for child in child_nodes:
                if child not in self.frontier and child not in self.explored_nodes:
                    self.frontier.add_node(child)

            self.algorithm_log.save_record()

        self.solution = None
        return False

    def show_solution(self) -> None:
        """
        Prints the nodes sequence that form the solution path if one exists,
        along with the number of nodes explored.

        The solution, if found, is printed from the start node,
        showing step-by-step nodes to the goal node, along with the number of
        nodes explored. If no solution exists, prints "No Solution found!".

        Returns:
            None

        Note:
            This method MAY be overridden to customize the output format.
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

    def save_algorithm_steps_to_file(self, log_filename):
        """
        Saves algorithm steps to file.

        Details algorithm name, number of explored and solution nodes, and for
        each algorithm step, the current state of explored nodes, frontier,
        extracted nodes, and expanded nodes.
        If no solution exists, prints "No Solution found!".

        Returns:
            None

        Note:
            This method MAY be overridden to customize the output format or
            include additional information.
        """

        lines=[
            f"- Algorithm: {self.algorithm}",
            f"- Explored nodes: {len(self.explored_nodes)}",
            f"- Solution nodes: {len(self.solution) if self.solution else '-'}",
        ]

        with open(log_filename, 'w', encoding="utf-8") as file:
            file.writelines(line + "\n" for line in lines)

        self.algorithm_log.save_log(log_filename)
        print(f"Algorithm steps saved to file: {log_filename}\n")


class Node(ABC):
    """Represents a node in the search tree.

    Derived classes need to override actions() and result() methods to include
    problem-specific logic. __init__() is likely to be overridden as well.


    Attributes:
        state (Optional[object]): The state represented by this node.
        parent (Optional[Node]): The parent node from which this node was generated.
        action (Optional[object]): The action taken to reach this node from its parent.
    """

    def __init__(self, state: Optional[object] = None,
                 parent: Optional['Node'] = None,
                 action: Optional[object] = None) -> None:
        """
        Initialize a Node object in the search tree.

        Args:
            state (Optional[object]): The state represented by this node.
                Default is None.
            parent (Optional[Node]): The parent node from which this node was
                generated. Default is None.
            action (Optional[object]): The action that was taken to reach
                this node from its parent. Default is None.

        Returns:
            None

        Note:
            This method MAY be overridden. Redefined method in subclass:

            - MUST call `super().__init__()` (generally as first statement)
            - MAY define other attributes relevant to the specific search
              problem, if needed by actions() or result() methods

        """
        self.state = state
        self.parent = parent
        self.action = action

    @abstractmethod
    def actions(self, search_problem: SearchProblem) -> List[object]:
        """
        Return a list of valid actions for this node.

        Note:
            This method MUST be implemented in a subclass.

        Args:
            search_problem (SearchProblem): The problem being solved, which
                provides the context and constraints for determining valid
                actions.

        Returns:
            list: A list of actions available from this node. If no actions are
            available, an empty list should be returned.

            Example: If your search problem is to find a path in a maze,
            this method should return all valid moves (e.g., 'up', 'down',
            'left', 'right') that can be taken from the current state.

        Raises:
            NotImplementedError: If the method is not implemented by a subclass.
        """

        pass

    @abstractmethod
    def result(self, action: object, search_problem: SearchProblem) -> 'Node':
        """
        Return the resulting node from performing the given action.

        Note:
            This method MUST be implemented in a subclass.

        Args:
            action (object): The action to be performed.
            search_problem (SearchProblem): The problem being solved.

        Returns:
            Node: The resulting node after 'action' is performed.

            Example: returns node representing new position in a maze after a
            movement ('action') provided by 'actions()'

        """
        pass

    def node_action(self) -> Optional[object]:
        """
        Returns the action that was taken to reach this node from its parent.

        Returns:
            Optional[object]: The action that was taken to reach this node.
        """
        return self.action

    def node_state(self) -> Optional[object]:
        """
        Returns the state represented by this node.

        Returns:
            Optional[object]: The state represented by this node.
        """
        return self.state

    def expand(self, search_problem: SearchProblem) -> List['Node']:
        """
        Expands the current node by generating all possible child nodes.

        This method uses the node's actions() method to get valid actions
        and result() method to generate child nodes for each action.

        Args:
            search_problem (SearchProblem): The search problem instance
                providing the context for expanding this node.

        Returns:
            list: A list of child Node objects resulting from applying all
                valid actions to the current node.
        """
        child_nodes = []
        valid_actions = self.actions(search_problem)
        for action in valid_actions:
            expanded = self.result(action, search_problem)
            child_nodes.append(expanded)
        return child_nodes

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Node):
            return NotImplemented
        return self.state == other.state

    def __hash__(self) -> int:
        return hash(self.state)


class _NodeContainer(ABC):
    """
    Represents a generic container for storing nodes.

    Attributes:
        nodes (Union[List[Node], set]): The container to store nodes, which can
            be either a list or a set, depending on the container type.
    """
    def __init__(self, node: Optional[Union[List[Node], set]] = None) -> None:
        """
        Initializes the _NodeContainer object.

        Args:
            node (Optional[Union[List[Node], set]]): The initial node or nodes
            to be added to the container. Default is None.
        """
        self.nodes = node if node is not None else []

    def __contains__(self, element: Union[Node, tuple]) -> bool:
        """
        Checks if the container contains the given element.

        Args:
            element (Union[Node, tuple]): The element to check for. Must be a
                Node or a tuple representing a state.

        Returns:
            bool: True if the element is in the container, False otherwise.

        Raises:
            ValueError: If the element is not a Node or a tuple.
        """
        if isinstance(element, Node):
            return element in self.nodes
        elif isinstance(element, tuple):
            return any(element == nd.state for nd in self.nodes)
        else:
            raise ValueError("Element must be a Node or a tuple (state)")

    def __iter__(self):
        """
        Returns an iterator over the nodes in the container.

        Returns:
            Iterator: An iterator over the nodes in the container.
        """
        return iter(self.nodes)

    def __repr__(self) -> str:
        """
        Returns a string representation of the container.

        Returns:
            str: A string representation of the container.
        """
        return f"{[node.state for node in self.nodes]}"

    def __len__(self) -> int:
        """
        Returns the number of nodes in the container.

        Returns:
            int: The number of nodes in the container.
        """
        return len(self.nodes)

    def not_empty(self) -> bool:
        """
        Checks if the container is not empty.

        Returns:
            bool: True if the container is not empty, False otherwise.
        """
        return len(self.nodes) > 0

    def copy(self) -> '_NodeContainer':
        """
        Creates a copy of the container.

        Returns:
            _NodeContainer: A copy of the container.
        """
        copied = self.__class__()  # Create a new instance of the same class
        copied.nodes = self.nodes.copy()  # Copy the nodes
        return copied


class _ExploredNodes(_NodeContainer):
    """
    Represents the set of explored nodes in the search.

    Attributes:
        nodes (set): The set of nodes that have been explored during the
            search.
    """

    def __init__(self) -> None:
        """
        Initializes the _ExploredNodes object as an empty set.
        """
        super().__init__(set())

    def add_node(self, node: Node) -> None:
        """
        Adds a node to the explored nodes set.

        Args:
            node (Node): The node to be added.

        Returns:
            None
        """
        self.nodes.add(node)


class _Frontier(_NodeContainer):
    """
    Represents the frontier in a search, i.e., nodes yet to be explored.

    This is an abstract class and must be subclassed to implement the extract()

    Attributes:
        nodes (list): The list of nodes in the frontier.
    """

    def __init__(self) -> None:
        """
        Initializes the _Frontier object as an empty list.
        """
        super().__init__(list())

    def add_node(self, node: Node) -> None:
        """
        Adds a node to the frontier.

        Args:
            node (Node): The node to be added.

        Returns:
            None
        """
        self.nodes.append(node)

    def extract(self) -> Node:
        """
        Extracts a node from the frontier.

        Returns:
            Node: The extracted node.

        Raises:
            NotImplementedError: If the method is not implemented by a subclass.

        Note:
            Subclasses (_StackFrontier, _QueueFrontier) must implement this method.

        """
        raise NotImplementedError


class _StackFrontier(_Frontier):
    """
    Implements a stack-based frontier (LIFO) for depth-first search (DFS).

    Attributes:
        nodes (list): The list of nodes in the stack-based frontier.
    """

    def extract(self) -> Node:
        """
        Extracts a node from the stack-based frontier, using Last-In-First-Out
        (LIFO) extraction (suitable for depth-first search).

        Returns:
            Node: The extracted node.

        Raises:
            RuntimeError: If trying to extract from an empty frontier.
        """
        if self.not_empty():
            return self.nodes.pop()
        else:
            raise RuntimeError("Trying to extract node from an empty frontier")


class _QueueFrontier(_Frontier):
    """
    Implements a queue-based frontier (FIFO) for breadth-first search (BFS).

    Attributes:
        nodes (list): The list of nodes in the queue-based frontier.
    """

    def extract(self) -> Node:
        """
        Extracts a node from the queue-based frontier, using First-In-First-Out
        (FIFO) extraction (suitable for breadth-first search).

        Returns:
            Node: The extracted node.

        Raises:
            RuntimeError: If trying to extract from an empty frontier.
        """
        if self.not_empty():
            return self.nodes.pop(0)
        else:
            raise RuntimeError("Trying to extract node from an empty frontier")


class _Solution(_NodeContainer):
    """
    Represents the solution path as a list of nodes.

    Attributes:
        nodes (list): The list of nodes that form the solution path.
    """
    def __init__(self) -> None:
        """
        Initializes the _Solution object as an empty list.
        """
        super().__init__(list())

    def build(self, goal_node: Node) -> None:
        """
        Builds the solution path from the goal node back to the start node.

        Args:
            goal_node (Node): The goal node from which to build the solution path.

        Returns:
            None
        """
        node = goal_node
        while node is not None:
            self.nodes.append(node)
            node = node.parent
        self.nodes.pop()
        self.nodes.reverse()


class _LogHandler:
    """
    Handles logging of the search algorithm's execution steps.

    Attributes:
        log (List[dict]): The complete log of all algorithm steps.
        current_record (dict): The current log record being assembled.
    """

    def __init__(self) -> None:
        """
        Initializes the _LogHandler object.

        Returns:
            None
        """
        self.log = []
        self.current_record = {}

    def add_to_record(self, frontier: Optional[_Frontier] = None,
                      explored: Optional[_ExploredNodes] = None,
                      extracted: Optional[Node] = None,
                      expanded: Optional[List[Node]] = None) -> None:
        """
        Adds information to the current log record.

        Parameters are optional depending on which part of the algorithm is
        being logged.

        Args:
            frontier (Optional[_Frontier]): The current state of the frontier.
            explored (Optional[_ExploredNodes]): The current state of the explored nodes.
            extracted (Optional[Node]): The node that was extracted.
            expanded (Optional[List[Node]]): The nodes that were expanded.

        Returns:
            None

        Raises:
            ValueError: If any of the provided values are not of the expected
                types (e.g., _Frontier, _ExploredNodes, Node, List[Node]).

        """
        params = {
            'frontier': (frontier, _Frontier),
            'explored': (explored, _ExploredNodes),
            'extracted': (extracted, Node),
            'expanded': (expanded, list)
        }

        for key, (value, expected_type) in params.items():
            if value is not None:
                if isinstance(value, expected_type):
                    self.current_record[key] = value
                else:
                    raise ValueError(f"Invalid {key}: {value}. "
                                     f"Must be an instance of {expected_type.__name__}.")

    def save_record(self) -> None:
        """
        Saves the current log record.

        Returns:
            None
        """
        self.log.append(self.current_record.copy())
        self.current_record.clear()

    def get_log(self) -> List[dict]:
        """
        Returns the entire log.

        Returns:
            list: The entire log.
        """
        return self.log

    def save_log(self, log_filename: str) -> None:
        """
        Saves the log of algorithm steps to a file.

        Logs are saved in a structured format with each step showing the
        current state of the explored nodes, frontier, extracted nodes, and
        expanded nodes.

        Args:
            log_filename (str): The name of the file to save the log to.

        Returns:
            None
        """
        with open(log_filename, 'a', encoding='utf-8') as file:
            file.write("\n- Algorithm steps:\n")

            for step_nr, record in enumerate(self.log, start=1):
                file.write(f"[{step_nr}]\n")

                file.write("  > Explored nodes:\n")
                if record.get('explored'):
                    for nd in record['explored']:
                        file.write(f"      {nd.node_state()}\n")

                file.write("  > Frontier:\n")
                for nd in record.get('frontier', []):
                    file.write(f"      {nd.node_state()}\n")

                if record.get('extracted'):
                    file.write(f"  > Extracted node:\n      {record['extracted'].node_state()}\n")

                file.write("  > Node expands to:\n")
                for nd in record.get('expanded', []):
                    file.write(f"      {nd.node_state()}\n")
