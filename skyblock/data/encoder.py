from math import isinf, isnan


NoneType = type(None)


def _dumps(obj, /, *, current_indent=0, current_width=0,
           indent=2, sort_keys=True):
    if obj is None:
        return 'null'
    elif isinstance(obj, bool):
        return 'true' if obj else 'false'
    elif isinstance(obj, (float, int)):
        if isnan(obj):
            return 'NaN'
        elif isinf(obj):
            return 'Infinity' if obj > 0 else '-Infinity'
        else:
            return f'{obj}'
    elif isinstance(obj, str):
        result = ''
        for char in obj:
            if char == '"':
                result += '\\"'
            elif char in {'\b', '\f', '\n', '\r', '\t', '\v', '\\'}:
                result += f'{char!r}'
            else:
                result += char
        return f'"{result}"'
    elif isinstance(obj, tuple):
        return _dumps([*obj], current_indent=current_indent,
                      current_width=current_width, indent=indent,
                      sort_keys=sort_keys)
    elif isinstance(obj, list):
        if len(obj) == 0:
            return '[]'

        for item in obj:
            if not isinstance(item, (bool, float, int, str, NoneType)):
                break
        else:
            compact = ', '.join(_dumps(item) for item in obj)
            if current_width + len(compact) + 2 <= 80:
                return f'[{compact}]'

        result = '['
        for index, item in enumerate(obj):
            if index != 0:
                result += ','
            result += '\n' + ' ' * (current_indent + indent)
            result += _dumps(
                item, current_indent=current_indent + indent,
                current_width=current_indent + indent,
                indent=indent, sort_keys=sort_keys,
            )
        result += '\n' + ' ' * current_indent + ']'
        return result
    elif isinstance(obj, dict):
        if len(obj) == 0:
            return '{}'

        keys = [*obj.keys()]
        if sort_keys:
            keys.sort()

        result = '{'
        for index, key in enumerate(keys):
            if index != 0:
                result += ','
            result += '\n' + ' ' * (current_indent + indent)
            more_indent = _dumps(key) + ': '
            more_len = len(more_indent)
            result += more_indent
            result += _dumps(
                obj[key], current_indent=current_indent + indent,
                current_width=current_indent + indent + more_len,
                indent=indent, sort_keys=sort_keys,
            )
        result += '\n' + ' ' * current_indent + '}'
        return result
    else:
        return f'{obj!r}'


def dumps(obj, /, *, indent=2, sort_keys=False):
    return _dumps(obj, indent=indent, sort_keys=sort_keys)


def dump(obj, file, /, *, indent=2, sort_keys=False):
    content = _dumps(obj, indent=indent, sort_keys=sort_keys)
    file.write(content)
