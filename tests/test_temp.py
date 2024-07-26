import unittest


def add(a, b):
    return a + b


def test_add_positive_numbers():
    assert add(2, 3) == 5
    assert add(9, 4) == 13
    assert add(10, 38) == 48


def test_add_negative_numbers():
    assert add(-1, -1) == -2
    assert add(-12, 4) == -8
    assert add(-13, 41) == 28


def test_add_zero():
    assert add(0, 0) == 0
    assert add(3, 0) == 3
    assert add(0, 16) == 16


if __name__ == "__main__":
    unittest.main()
