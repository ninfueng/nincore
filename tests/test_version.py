import nincore
from nincore.version import is_equal, is_newer, is_older, parse_module


def test_parse_version() -> None:
    parsed = parse_module(nincore)
    assert nincore.__version__ == str(parsed)


class TestVersion:
    def test_version_newer(self) -> None:
        assert not is_newer(nincore, "9999.99.99")

    def test_version_older(self) -> None:
        assert not is_older(nincore, "0.0.0")

    def test_version_equal(self) -> None:
        assert is_equal(nincore, nincore.__version__)
