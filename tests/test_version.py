import nincore
from nincore.version import is_newer_ver, is_older_ver, is_same_ver, parse_module_ver


def test_parse_version() -> None:
    parsed = parse_module_ver(nincore)
    assert nincore.__version__ == str(parsed)


class TestVersion:
    def test_version_newer(self) -> None:
        assert not is_newer_ver(nincore, '9999.99.99')

    def test_version_older(self) -> None:
        assert not is_older_ver(nincore, '0.0.0')

    def test_version_equal(self) -> None:
        assert is_same_ver(nincore, nincore.__version__)
