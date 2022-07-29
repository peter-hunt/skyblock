from sys import version_info


__all__ = ['skyblock_main']


def skyblock_main():
    if version_info < (3, 10):
        raise ValueError('at least python 3.10 is required by this project')

    from .install import init
    init()
    from .menu import main
    main()


if __name__ == '__main__':
    skyblock_main()
