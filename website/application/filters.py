from jinja2 import Undefined

def _slice(iterable, pattern):
    """
    slice method
    :param iterable: str
    :param pattern: str
    :return: str
    """
    if iterable is None or isinstance(iterable,Undefined):
        return iterable

    # convert to list
    items = str(iterable)
    start = None
    end = None
    stride = None
    # split pattern into slice components
    if pattern:
        tokens = pattern.split(':')
        print(tokens)
        if len(tokens)>1:
            start = int(tokens[0])
        if len(tokens)>2:
            end = int(tokens[1])
        if len(tokens)>3:
            stride = int(tokens[2])
    print(items)
    return items[start:end:stride]