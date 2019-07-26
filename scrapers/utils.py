from functools import reduce


def get_nested(dictionary: dict, keys: str, default=None):
    """
    Get a value inside a nested dict, or return the default value otherwise.

    source: https://stackoverflow.com/a/46890853
    :param dictionary: the dict with the value inside
    :param keys: a string to the path, nested values are concatenated with a '.'.
    :param default: the default value to return if the keys path is invalid
    :return: the value that is found when the dictionary is reduced with the keys, or the default value otherwise.
    """
    return reduce(lambda d, key: d.get(key, default) if isinstance(d, dict) else default, keys.split("."), dictionary)
