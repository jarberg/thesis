from setuptools import setup
from setuptools import find_packages
from setuptools import find_namespace_packages
from setuptools import setup, find_packages

setup(
    name='your_project_name',
    version='0.1',
    description='A description.',
    packages=find_packages(exclude=['ez_setup', 'tests', 'tests.*']),
    package_data={'': ['box.png','charlie.txt', r"PyOpenGL-3.1.5-py38-none-win_amd64.whl"]},
    include_package_data=True,
    entry_points = {'console_scripts': ['Package = src.__main__:main'],},
    install_requires=[],
)