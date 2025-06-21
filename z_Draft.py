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


def file_Open_Check(filename):
    try:
        with open(filename, 'r') as f:
            return True
    except Exception as e:
        return False

def file_2_Variable(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return data

