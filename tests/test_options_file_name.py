import unittest
from methods import options_FileName
import sys

class TestOptionsFileName(unittest.TestCase):
    """Тесты для функции options_FileName()"""
    
    def test_no_arguments(self):
        """Проверка вызова без аргументов"""
        sys.argv = ["drakon_SU.py"]
        self.assertEqual(options_FileName(), "")
        
    def test_file_open_argument(self):
        """Проверка аргумента --file_open"""
        sys.argv = ["drakon_SU.py", "--file_open", "test.drakon"]
        self.assertEqual(options_FileName(), "test.drakon")
        
    def test_file_open_with_equal(self):
        """Проверка аргумента --file_open=value"""
        sys.argv = ["drakon_SU.py", "--file_open=test.drakon"]
        self.assertEqual(options_FileName(), "test.drakon")
        
    def test_multiple_arguments(self):
        """Проверка нескольких аргументов"""
        sys.argv = ["drakon_SU.py", "--file_open", "test.drakon", "--verbose"]
        self.assertEqual(options_FileName(), "test.drakon")

if __name__ == '__main__':
    unittest.main()