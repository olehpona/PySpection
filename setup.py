from setuptools import setup

setup(
    name='PyScan',
    version='0.2',
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