from setuptools import setup

APP = ['drakon_SUC.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': False,
    'includes': [
        'PyQt5.QtCore', 
        'PyQt5.QtWidgets', 
        'PyQt5.QtGui',
        'jaraco.text'  # Добавляем явное указание модуля
    ],
    'excludes': ['Carbon'],
    'packages': ['PyQt5'],
    'plist': {
        'CFBundleName': "DRAKON_SUC",
        'CFBundleDisplayName': "DRAKON_SUC",
        'CFBundleIdentifier': "com.yourcompany.drakon_suc",
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)