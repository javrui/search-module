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

import unittest
from unittest.mock import Mock
from maze.search import SearchProblem, Node

class MockNode(Node):
    def actions(self, search_problem):
        return self._actions

    def result(self, action, search_problem):
        return Node(state=action)

class TestNodeExpand(unittest.TestCase):
    def setUp(self):
        self.search_problem = Mock(spec=SearchProblem)

    def test_expand_no_actions(self):
        # Arrange
        node = MockNode(state="test")
        node._actions = []

        # Act
        result = node.expand(self.search_problem)

        # Assert
        self.assertEqual(len(result), 0)

    def test_expand_single_action(self):
        # Arrange
        node = MockNode(state="test")
        node._actions = ["action1"]

        # Act
        result = node.expand(self.search_problem)

        # Assert
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].state, "action1")

    def test_expand_multiple_actions(self):
        # Arrange
        node = MockNode(state="test")
        node._actions = ["action1", "action2", "action3"]

        # Act
        result = node.expand(self.search_problem)

        # Assert
        self.assertEqual(len(result), 3)
        self.assertEqual([node.state for node in result],
                        ["action1", "action2", "action3"])

if __name__ == '__main__':
    unittest.main()