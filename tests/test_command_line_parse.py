import unittest
from methods import commandLine_parse

class TestCommandLineParse(unittest.TestCase):
    """Тесты для функции commandLine_parse()"""
    
    def test_empty_string(self):
        """Проверка пустой строки"""
        self.assertEqual(commandLine_parse(""), {})
        
    def test_single_flag(self):
        """Проверка одиночного флага"""
        self.assertEqual(commandLine_parse("-v"), {"v": True})
        
    def test_multiple_flags(self):
        """Проверка нескольких флагов"""
        self.assertEqual(
            commandLine_parse("-a -b --verbose"),
            {"a": True, "b": True, "verbose": True}
        )
        
    def test_key_value_pairs(self):
        """Проверка пар ключ-значение"""
        self.assertEqual(
            commandLine_parse('--file test.txt --name "John Doe"'),
            {"file": "test.txt", "name": "John Doe"}
        )
        
    def test_mixed_format(self):
        """Проверка смешанного формата"""
        self.assertEqual(
            commandLine_parse('-f input.txt --output=result.json --force'),
            {"f": "input.txt", "output": "result.json", "force": True}
        )
        
    def test_quoted_values(self):
        """Проверка значений в кавычках"""
        self.assertEqual(
            commandLine_parse('--message "Hello world" --path "/usr/bin"'),
            {"message": 'Hello world', "path": "/usr/bin"}
        )
        
    def test_equal_sign_format(self):
        """Проверка формата с ="""
        self.assertEqual(
            commandLine_parse('--width=100 --height=200'),
            {"width": "100", "height": "200"}
        )

if __name__ == '__main__':
    unittest.main()