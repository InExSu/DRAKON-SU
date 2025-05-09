from setuptools import setup

APP = ['drakon_SU.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': False,
    'includes': [
        'PyQt5.QtCore', 
        'PyQt5.QtWidgets', 
        'PyQt5.QtGui',
        'jaraco.text'
    ],
    'excludes': ['Carbon'],
    'packages': ['PyQt5'],
    'plist': {
        'CFBundleName': "DRAKON_SU",
        'CFBundleDisplayName': "DRAKON_SU",
        'CFBundleIdentifier': "com.yourcompany.drakon-su",
    }
}

setup_requires = ['py2app']

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=setup_requires,
)