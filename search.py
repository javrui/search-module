"""================================================================ JRM 2024.02
Module: search
============================================================================"""

from abc import ABC, abstractmethod

class SearchProblem(ABC):

    @abstractmethod
    def __init__(self):

        self.start_node = None
        self.goal_node = None

        self.frontier = _Frontier()
        self.explored_nodes = _ExploredNodes()

        self.solution = None
        self.nodes_explored = None
        self.audit_trail = None


    def solve(self, search_algorithm='BFS', audit_trail=False):

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
        if search_algorithm == 'BFS':
            self.frontier = _StackFrontier()
        elif search_algorithm == 'DFS':
            self.frontier = _QueueFrontier()
        else:
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
                if not child in self.frontier and \
                   not child in self.explored_nodes:
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


class Node(ABC):

    def __init__(self, state=None, parent=None, action=None):

        self.state = state
        self.parent = parent
        self.action = action

    @abstractmethod
    def actions(self, search_problem: SearchProblem):

        pass

    @abstractmethod
    def result(self, action, search_problem: SearchProblem):

        pass


    def expand(self, search_problem: SearchProblem):

        child_nodes = []
        valid_actions = self.actions(search_problem)
        for action in valid_actions:
            expanded = self.result(action, search_problem)
            child_nodes.append(expanded)

        return child_nodes




class AuditTrail():

    def __init__(self):
        """ Implemented as list (of dictionaries)"""
        self.audit_trail = []


    def add_record(self, frontier, explored, extracted, expanded):

        record = {  'frontier': frontier,
                    'explored': explored,
                    'extracted': extracted,
                    'expanded': expanded}

        self.audit_trail.append(record)


    def show(self):

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

    @abstractmethod
    def add(self, node):

        pass


    def not_empty(self):

        return len(self.frontier) > 0

    @abstractmethod
    def extract(self):

        pass


    def copy(self):

        return self.frontier.copy()


class _StackFrontier(_Frontier):


    def add(self, node):

        self.frontier.append(node)

    def extract(self):

        if self.not_empty():
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node
        else:
            raise RuntimeError("trying to extract node from empty frontier")


class _QueueFrontier(_Frontier):

    def add(self, node):

        self.frontier.append(node)


    def extract(self):

        if self.not_empty():
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node
        else:
            raise RuntimeError("trying to extract node from empty frontier")


class _Solution():

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

        self.solution = self.solution[::-1]
