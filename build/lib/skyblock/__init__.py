from sys import version_info


if version_info < (3, 10):
    raise ValueError('at least python 3.10 is required to run this project')
