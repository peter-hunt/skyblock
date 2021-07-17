try:
    from readline import add_history
except (ImportError, ModuleNotFoundError):
    def add_history(line: str):
        pass
