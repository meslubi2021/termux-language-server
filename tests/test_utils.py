r"""Test utils."""
from termux_language_server.utils import get_schema


class Test:
    r"""Test."""

    @staticmethod
    def test_get_document() -> None:
        r"""Test get document.

        :rtype: None
        """
        assert len(
            get_schema("build.sh")
            .get("properties", {})
            .get("TERMUX_PKG_VERSION", {})
            .get("description", "")
            .splitlines()
        )
