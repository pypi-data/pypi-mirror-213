"""
"""

import pytest

from builder import Template


def test_template_initialization():
    """"""
    template = Template("sass.json")
    assert template.name == "sass.json"


@pytest.mark.skip()
def test_load_method_reads_a_json_file():
    """"""
    # TODO - mock open json file
    pass


@pytest.mark.skip()
def test_traverse_method_returns_a_generator():
    """"""
    pass


@pytest.mark.skip()
def test_structure_method_returns_a_list_of_lists():
    """"""
    pass


@pytest.mark.skip()
def test_tails_method_returns_list_of_tails():
    """"""
    pass
