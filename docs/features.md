## Key Features of 'search'

📌 TO DO: REVISAR BIEN!!!, incluso quizás rehacer con chat GPT


1. **Object-Oriented Design**:
   - The module is structured around object-oriented principles, encapsulating problem-solving elements into classes such as `SearchProblem`, `Node`, and `_Frontier`. Each class has a specific responsibility within the search problem framework, promoting modularity and reusability.

2. **Abstract Classes**:
   - **Abstract Base Classes (ABC)**: `SearchProblem` and `Node` are defined as abstract classes using Python’s `ABC` module. This design enforces that certain methods (`actions`, `result`, and `__init__` in subclasses) must be implemented by any concrete subclass, ensuring consistent interfaces across different search problem implementations.

3. **Interface Methods and Encapsulation**:
   - **Protected Methods and Attributes**: Many methods and attributes are prefixed with an underscore (`_`), indicating they are meant for internal use and not intended to be part of the public API. This encapsulation helps users focus on relevant interfaces while hiding internal details.
   - **Explicit Subclassing Requirements**: By marking specific methods (`actions()`, `result()`) as abstract in `Node` and `SearchProblem`, the design enforces that subclasses provide specific implementations, effectively creating a controlled interface for each search problem.

4. **Modularity and Extensibility**:
   - **Pluggable Search Algorithms**: The `solve()` method in `SearchProblem` allows different search strategies (BFS, DFS) by controlling the type of frontier used (`_StackFrontier` for BFS and `_QueueFrontier` for DFS). This design makes it easy to add or modify search algorithms without changing the overall code structure.
   - **Separate Components for State Tracking**: Classes like `_Frontier`, `_ExploredNodes`, and `_Solution` encapsulate specific responsibilities for managing states, frontiers, and solutions, making it easier to modify or extend these functionalities independently.

5. **Audit Trail for Debugging and Analysis**:
   - The `AuditTrail` class records every step of the search process, including the states of the frontier and explored nodes at each step. This feature is useful for debugging and provides transparency, allowing users to track and analyze the search process if desired.

6. **Customizable Output with `show_solution()`**:
   - The `show_solution()` method can be used as-is or overridden in subclasses to customize the format of the solution output. This provides flexibility for displaying results in a way that suits specific problem domains or user preferences.

This list should capture the technical and design-oriented aspects of your module for the `README.md`. Let me know if you need further detail on any of these points!