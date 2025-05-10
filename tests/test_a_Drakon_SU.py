import unittest
import a_Drakon_SU

class TestADrakonSU(unittest.TestCase):
    def test_b_YAML_2_Graph(self):
        # Пока функция-заглушка, просто проверяем, что она вызывается
        self.assertIsNone(a_Drakon_SU.b_YAML_2_Graph(""))

if __name__ == '__main__':
    unittest.main()