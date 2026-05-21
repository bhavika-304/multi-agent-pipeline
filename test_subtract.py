import pytest
from subtract import subtract

def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(-5, 3) == -8
    assert subtract(-5, -3) == -2
    assert subtract(0, 0) == 0