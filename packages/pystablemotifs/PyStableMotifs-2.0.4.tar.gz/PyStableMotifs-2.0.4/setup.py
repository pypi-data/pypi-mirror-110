from setuptools import setup

setup(
    name="PyStableMotifs",
    version='2.0.4',
    author="Jordan Rozum",
    author_email="jcr52@psu.edu",
    description="Python package for analyzing Boolean Netowrk",
    url="https://github.com/jcrozum/PyStableMotifs",
    license='MIT',
    python_requires='>=3.5',
    packages=['PyStableMotifs'],
    install_requires=[
    'PyBoolNet',
    "networkx >= 2.4.0",
    "sympy >= 1.5.1",
    "pandas >= 1.0.0",
    "numpy >= 1.19.2",
    "matplotlib >= 3.2.1"
    ],
    dependency_links=[
    'https://github.com/hklarner/PyBoolNet/tarball/master#egg=PyBoolNet-2.3.0'
    ]
)
