import pytest
from count_vowels import count_vowels

def test_count_vowels():
    assert count_vowels('hello') == 2
    assert count_vowels('world') == 1
    assert count_vowels('python') == 2
