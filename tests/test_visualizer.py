import unittest
import visualizer
import os

class TestVisualizer(unittest.TestCase):
    def test_visualize_drakon(self):
        # Проверяем, что функция не выбрасывает исключений на валидном файле
        visualizer.visualize_drakon('sample.json')
        self.assertTrue(os.path.exists('sample.json'))

if __name__ == '__main__':
    unittest.main()