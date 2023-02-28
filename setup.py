from setuptools import setup

setup(
    name='PyScan',
    version='2.0',
    py_modules=['main'],
    install_requires=[
        'PyQt6',
        'pillow',
        'python-sane'
    ],
    entry_points='''
    [console_scripts]
    pyscan=main:run
    '''
)