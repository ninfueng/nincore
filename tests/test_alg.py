from nincore.alg import is_incremental, split_n


def test_split_n() -> None:
    x = [1, 2, 3, 4, 5]
    n = 2
    r = split_n(x, n)
    assert r == [[1, 2], [3, 4], [5]]


def test_is_incremental1() -> None:
    assert is_incremental([1, 2, 3, 4])


def test_is_incremental2() -> None:
    assert not is_incremental([1, 2, 1, 4])
