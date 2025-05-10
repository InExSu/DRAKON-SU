import sys
import unittest
from PyQt5.QtWidgets import QApplication
from a_YAML_2_Graph import code_2_Graph

# Глобальный объект приложения для всех тестов
app = QApplication(sys.argv)

class TestCode2Graph(unittest.TestCase):
    def test_empty_yaml(self):
        scene = code_2_Graph("")
        self.assertIsNotNone(scene)

    def test_invalid_yaml(self):
        scene = code_2_Graph("not: [a, valid, yaml")
        self.assertIsNotNone(scene)

    def test_simple_function(self):
        yaml_code = '''
functions:
  testfunc:
    parameters: ""
    returns: ""
    nodes:
      - id: 1
        type: "start"
        text: "start"
        connections: [2]
      - id: 2
        type: "end"
        text: "end"
        connections: []
'''
        scene = code_2_Graph(yaml_code)
        self.assertIsNotNone(scene)

if __name__ == '__main__':
    unittest.main()