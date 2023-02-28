from setuptools import setup

setup(
    name='PyScan',
    version='0.1',
    py_modules=['main'],
    install_requires=[
        'PyQt6',
        'pillow'
    ],
    entry_points='''
    [console_scripts]
    pyscan=main:run
    '''
)