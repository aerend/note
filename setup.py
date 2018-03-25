from setuptools import setup

setup(
    name='note',
    packages=['note'],
    entry_points = {
        'console_scripts': ['note = note.__main__:main']
    }
)
