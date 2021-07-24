from sys import version_info


__all__ = ['skyblock_main']


def skyblock_main():
    if version_info < (3, 8):
        raise ValueError('at least python 3.8 is required to run this project')

    from .install import install
    install()
    from .menu import main
    main()


if __name__ == '__main__':
    skyblock_main()
