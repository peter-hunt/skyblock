from sys import version_info
from subprocess import run


__all__ = ['skyblock_main']


def skyblock_main():
    if version_info < (3, 8):
        raise ValueError('at least python 3.8 is required by this project')

    from .install import init
    init()
    from .menu import main
    main()


if __name__ == '__main__':
    run(['clear'])
    print('% python -m skyblock')
    skyblock_main()
