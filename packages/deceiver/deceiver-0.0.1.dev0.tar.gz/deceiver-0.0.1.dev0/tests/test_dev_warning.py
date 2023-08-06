import pytest


def test_message():
    with pytest.warns(
        UserWarning, match="This is just a stub for a project undergoing development"
    ):
        import deceiver  # noqa: F401
