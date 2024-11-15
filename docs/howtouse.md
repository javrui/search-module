

# How to use *search* module

📌 TO DO: AuditTrail parece que debería unirse de alguna forma a la clase Solution,no tiene sentido que estén seaparados.

*search* module interface consists of two base classes:
- **SearchProblem**
- **Node**

Both have:
- abstract methods that you have to create in derived class
- methods that you may want to override in derived class

So, you have to derive a class from each base, to:
- **write abstract methods** to implement your problem specific details
- **optionally override some methods** to achieve specific behavior beyond default implementation.


### *SearchProblem* class interface methods:

* **\_\_init\_\_()**

    * MUST be written by you in derived class (is abstract)
    * MUST initialize values (relevant to the specific search problem) for these **attributes**:
      - **start_node**
      - **goal_node**
    * MAY define other attributes if needed by **Node** abstract  methods:
      - actions()
      - result()
    * MUST call super().\_\_init\_\_(), generally as first method statement.


* **show_solution()**

    * MAY be written by you, if *search* module default format for solution print needs modification. Otherwise there is no need to override parent class method.

### *Node* class interface methods:

* **\_\_init\_\_()**

    * MAY be written by you, if problem specific attributes need to be initialized to be used by *Node* abstract methods:
        - actions()
        - result()
    * if defined, MUST call super().\_\_init\_\_(), generally as first statement in this method.


* **actions()**
    * This method MUST be written by you.
    * returns the list of valid actions that can be performed on a given node.
    * Example: movements available in a maze from a given node.


* **result()**
    * This method MUST be written by you.
    * Returns the node that results from performing 'action' on (self) node.
    * Example: new position in a maze after a movement provided by 'actions()'.



To see complete code of maze solving example, please visit [maze](../maze/maze.py)