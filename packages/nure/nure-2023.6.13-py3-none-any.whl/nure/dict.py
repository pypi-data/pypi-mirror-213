import collections.abc


def update(default, modified):
    for k, v in modified.items():
        if isinstance(v, collections.abc.Mapping):
            default[k] = update(default.get(k, {}), v)
        else:
            default[k] = v
    return default


def get(obj, key: str, sep='.', default=None, suppress_error=True):
    l_key = key.split(sep)
    for k in l_key:
        try:
            obj = obj[k]
        except Exception:
            try:
                obj = obj[int(k)]
            except Exception:
                if suppress_error:
                    return default

                raise KeyError(f'{k} is not in {obj}')

    return obj


def set(obj, key, value, sep='.'):
    l_key = key.split(sep)
    for k in l_key[:-1]:
        try:
            obj = obj[k]
        except Exception:
            try:
                obj = obj[int(k)]
            except Exception:
                obj[k] = dict()
                obj = obj[k]

    obj[l_key[-1]] = value


def delete(obj, key, sep='.', suppress_error=False):
    l_key = key.split(sep)
    pre_obj = obj
    for k in l_key:
        if not isinstance(obj, collections.abc.MutableMapping) or k not in obj:
            if suppress_error:
                return None

            raise ValueError(f'{k} is not in {obj}')

        pre_obj = obj
        obj = obj[k]

    value = pre_obj[l_key[-1]]
    del pre_obj[l_key[-1]]
    return value
