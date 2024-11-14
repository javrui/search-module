# Introduction to search problem


## Search problem and AI
A search problem refers to a class of problems in the field of Artificial Intelligence (AI) and computer science where the objective is to find a sequence of **actions** or steps that lead from an **initial state** to a **goal state**  within a problem space. The problem space consists of various states, transitions (actions), and constraints that define the problem environment.


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

* **Result** (node): The node resulting from an action on a given node.

* **Expand** (node): The process of exploring a node's neighboring states by generating its successors based on possible actions. Expanding a node involves creating all possible new 'Result' nodes.

* **Frontier**: A collection of all nodes available to be explored. It contains the nodes that have been generated but not yet expanded. The frontier controls the order in which nodes are expanded and determines the search strategy, such as Breadth-First Search (BFS) or Depth-First Search (DFS).

* **Explored Set**: A set of nodes that have already been expanded. It helps prevent redundant exploration by keeping track of visited nodes to avoid loops and repeated states.


## Algorithm steps
Search algorithm in **search** module follows this steps:

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


## Methods in *search* module related to key concepts

User of *search* module has to write these 2 methods, related to **Actions** and **Result** concepts explained above, to adapt them to the specific search problem to be solved.

- **actions()**:
Method that returns the list of valid actions that can be performed on a given node.


- **result()**: Returns the node that results from performing 'action' on (self) node.

See  [how to use search module](howto.md) for details.