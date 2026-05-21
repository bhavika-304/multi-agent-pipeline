def test_check_even_odd():
    from even_odd import check_even_odd
    assert check_even_odd(10) == 'even'
    assert check_even_odd(11) == 'odd'

test_check_even_odd()