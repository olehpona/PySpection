from setuptools import setup

setup(
    name='pyscan',
    version='3.0',
    py_modules=['main'],
    license='GPLv3',
    install_requires=[
        'PyQt6',
        'pillow',
        'python-sane',
        'tomlkit'
    ],
    entry_points='''
    [console_scripts]
    pyscan=main:run
    '''
)