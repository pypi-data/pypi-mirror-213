"""
"""
import pytest

from builder import Builder


def test_builder_initialization():
    """"""
    builder = Builder("sass", "sass.json")
    assert builder.project == "sass"


@pytest.mark.skip()
def test_paths_method_creates_a_list_of_paths():
    """"""
    pass


@pytest.mark.skip()
def test_build_method_creates_project_from_template():
    """"""
    pass
