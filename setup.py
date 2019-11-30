from setuptools import setup, find_packages


setup(
    name='maze_generator',
    version='1.0.0',
    install_requires=[
        'pillow',
        'numpy'
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            ''
        ]
    }
)
