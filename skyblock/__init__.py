from sys import version_info

if version_info < (3, 8):
    raise ValueError('at least python 3.8 is required to run this project')
