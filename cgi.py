import re

_boundary_re = re.compile(rb'^[0-9A-Za-z\'()+_,-./:=?]+$')


def parse_header(line):
    if isinstance(line, bytes):
        line = line.decode('ascii', 'strict')

    parts = line.split(';')
    key = parts[0].strip().lower()
    params = {}

    for item in parts[1:]:
        if not item:
            continue
        item = item.strip()
        if '=' in item:
            name, value = item.split('=', 1)
            name = name.strip().lower()
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] == '"':
                value = value[1:-1]
            params[name] = value
        else:
            params[item.lower()] = ''

    return key, params


def valid_boundary(boundary):
    if isinstance(boundary, str):
        try:
            boundary = boundary.encode('ascii')
        except UnicodeEncodeError:
            return False

    if not boundary or len(boundary) > 70:
        return False

    return bool(_boundary_re.match(boundary))
