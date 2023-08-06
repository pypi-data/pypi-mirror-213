from setuptools import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='TicTacToeAI',
    version='0.0.4',
    description='Tic Tac Toe with AI.',
    author= 'Ujjwal Reddy K S',
    url = 'https://github.com/ujjwalredd/Tic-Tac-Toe-with-AI',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    keywords=['MinMax', 'Diffcult', 'AI'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=['TicTacToeAI'],
    package_dir={'':'src'},
    install_requires = [
        'numpy'
    ]
)
