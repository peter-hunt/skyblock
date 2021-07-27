try:
    from readline import add_history
except (ImportError, ModuleNotFoundError):
    def add_history(line: str):
        pass


def _open(path: str, mode: str = 'r', /, *, encoding: str = 'utf-8'):
    return open(path, mode=mode, encoding=encoding)
