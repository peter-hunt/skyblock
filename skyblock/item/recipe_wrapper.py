__all__ = ['recipe_type']


def recipe_type(cls: type, /) -> type:
    anno = getattr(cls, '__annotations__', {})
    default = {}
    for name in anno:
        if hasattr(cls, name):
            default[name] = getattr(cls, name)

    init_str = 'lambda self'
    for key in anno:
        if key in default:
            init_str += f', {key}={default[key]!r}'
        else:
            init_str += f', {key}'

    init_str += ': ('
    for key in anno:
        init_str += f'setattr(self, {key!r}, {key}), '
    init_str += 'None,)[-1]'

    cls.__init__ = eval(init_str)

    return cls
