###############################
Key Features of *search* module
###############################

.. Key Features of *search*

Design notes on *search* module.


1. **Object-Oriented Design**

   The module is structured around object-oriented principles, encapsulating problem-solving elements into classes such as *SearchProblem* and *Node*, as well as several internal classes. Each class is designed with a specific responsibility within the search framework, promoting modularity and reusability.

2. **Abstract Classes**

   - **Abstract Base Classes (ABC)**

    The *SearchProblem* and *Node* classes are defined as abstract using Python’s ABC module. This ensures that critical methods such as **actions()**, **result()**, and **init()** must be implemented by any concrete subclass, maintaining a consistent interface across implementations.

   - **Protected Methods and Attributes**

    Methods and attributes prefixed with an underscore (_) are intended for internal use and not part of the public API. This design choice ensures users focus on relevant interfaces while abstracting internal details.

   - **Explicit Subclassing Requirements**

    Marking specific methods (**actions()**, **result()**) as abstract in *Node* and *SearchProblem* enforces that subclasses provide appropriate implementations, thereby creating a controlled interface tailored to each search problem.

3. **Modularity and Extensibility**

   - **Pluggable Search Algorithms**

    The **solve()** method in *SearchProblem* supports different search strategies (BFS, DFS) by managing the type of frontier used (*_StackFrontier* for BFS and *_QueueFrontier* for DFS). This design allows easy addition or modification of search algorithms without altering the broader code structure.

   - **Separate Components for State Tracking**

    Classes like *_Frontier*, *_ExploredNodes*, and *_Solution* encapsulate specific responsibilities for managing states, frontiers, and solutions, making it easier to modify or extend these functionalities independently.


4. **Audit Trail and Algorithm Steps Log**

   - The *AuditTrail* class records every step of the search process, including the states of the frontier and explored nodes. This feature facilitates debugging and offers transparency, enabling users to track and analyze the search process comprehensively.

5. **Customizable Output**

   - The **show_solution()** method can be used as-is or overridden in subclasses to customize the solution output format. This provides flexibility for displaying results in a manner suitable for specific problem domains or user requirements
