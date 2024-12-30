###############################
Key Features of *search* module
###############################

.. Key Features of *search*

Design notes on *search* module.

1. **Object-Oriented Design**

   The module follows OOP principles, encapsulating problem-solving elements into classes such as *SearchProblem*, *Node*, and various internal classes. Each class is responsible for specific functionality, ensuring modularity and reusability.

2. **Abstract Classes**

   - **Abstract Base Classes (ABC)**

     The *SearchProblem* and *Node* classes are defined as abstract using Python’s ABC module. This forces any concrete subclass to implement critical methods, like *actions()*, *result()*, and *\_\_init\_\_()*, maintaining a consistent interface.

   - **Protected Methods and Attributes**

     Methods and attributes prefixed with an underscore (_) are intended for internal use, keeping users focused on essential interfaces and abstracting lower-level details.

   - **Explicit Subclassing Requirements**

     Marking methods such as *actions()* and *result()* as abstract in *Node* and **SearchProblem** ensures subclasses provide the necessary implementations, promoting a controlled interface tailored to each search scenario.

3. **Modularity and Extensibility**

   - **Pluggable Search Algorithms**

     The *solve()* method in *SearchProblem* supports different search strategies (BFS, DFS) by selecting the type of frontier (*_StackFrontier* for BFS, *_QueueFrontier* for DFS). This design simplifies adding or modifying search algorithms without changing the overall structure.

   - **Separate Components for State Tracking**

     Classes like *_Frontier*, *_ExploredNodes*, and *_Solution* manage distinct concerns such as the frontier, explored nodes, and the final solution. This separation of responsibilities makes it easy to modify or extend each component independently.

4. **Audit Trail and Algorithm Steps Log**

   The *AuditTrail* class captures each step of the search process, including frontier and explored-node states. This comprehensive record aids in debugging and provides transparent insight into how the search progresses.

5. **Customizable Output**

   The *show_solution()* method can be used directly or overridden in subclasses to customize the solution's presentation format, allowing for flexible output that meets domain-specific or user-defined requirements.
