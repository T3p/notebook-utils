from setuptools import setup, find_packages
import sys

if sys.version_info.major != 3:
    print("This Python is only compatible with Python 3, but you are running "
          "Python {}. The installation will likely fail.".format(sys.version_info.major))


setup(name='nu',
      packages=[package for package in find_packages()
                if package.startswith('nu')],
      install_requires=[
              'numpy',
              'scipy',
              'matplotlib',
              'jupyter',
              'pandas'],
      description="RL notebook utils",
      author="Matteo Papini",
      url='https://github.com/T3p/notebook-utils',
      author_email="matteo.papini@polimi.it",
      version="0.1.1")
