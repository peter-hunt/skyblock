from sys import version_info

from .install import install
from .menu import main


if version_info < (3, 8):
    raise ValueError('at least python 3.8 is required to run this project')

if __name__ == '__main__':
    install()
    main()
