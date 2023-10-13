from nincore.alg import split_n


def test_split_n() -> None:
    x = [1, 2, 3, 4, 5]
    n = 2
    r = split_n(x, n)
    assert r == [[1, 2], [3, 4], [5]]
