import unittest
import methods

class TestMethods(unittest.TestCase):
    def test_file_Choice(self):
        # Здесь можно протестировать логику выбора файла, например, с пустым списком
        result = methods.file_Choice([])
        self.assertIn(result, ["Exit", "File create", "File open dialog"])

    def test_code_Good(self):
        self.assertTrue(methods.code_Good("любая строка"))

    # Добавьте тесты для других функций

if __name__ == '__main__':
    unittest.main()