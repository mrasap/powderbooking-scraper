import pytest
from scrapers.utils import get_nested


@pytest.mark.parametrize('input, path, expected, explanation', [
    ({'a': 42}, 'a', 42, 'single should work'),
    ({'a': 42}, 'b', 0, 'single should default'),
    ({'a': {'b': {'c': 42}}}, 'a.b.c', 42, 'triple nested should work'),
    ({'a': {'b': {'c': 42}}}, 'c', 0, 'single nested should default'),
    ({'a': {'b': {'c': 42}}}, 'a.c', 0, 'double nested should default'),
    (['a', 42], 'a', 0, 'array input should default'),
    (None, 'a', 0, 'None should default'),
])
def test_get_nested(input, path, expected, explanation):
    assert expected == get_nested(dictionary=input, keys=path, default=0)
