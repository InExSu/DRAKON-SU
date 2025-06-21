import argparse
import os


def file_create(filename):
    try:
        with open(filename, 'w') as f:
            pass  # Открытие в режиме 'w' само по себе создаёт файл
        # записать в файл код силуэта
        return True
    except Exception as e:
        print(f"Ошибка при создании файла: {e}")
        return False


def file_open(filename):
    try:
        with open(filename, 'r') as f:
            print(f.read())
            return True
        return True
    except Exception as e:
        print(f"Ошибка при создании файла: {e}")
        return False


def command_line_arguments():
    parser = argparse.ArgumentParser(
        description="Утилита для работы с файлами")
    parser.add_argument('--file_create', type=str, help='Файл создать')
    parser.add_argument('--file_open', type=str, help='Файл открыть')

    args = parser.parse_args()

    if args.file_create:
        result = file_create(args.file_create)
    elif args.file_open:
        result = file_open(args.file_open)
        pass
    else:
        pass
