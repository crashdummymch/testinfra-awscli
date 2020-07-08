# pylint: disable=line-too-long
"""
conftest for pytest
"""
import os
import pytest
import yaml


@pytest.fixture(scope="module")
def load_defaults(request):
    """
    loads default variables for module
    """
    overrides = {}
    for filename in os.listdir(os.path.join(request.fspath.dirname, "defaults")):
        filename = os.path.join(request.fspath.dirname, "defaults", filename)
        if not filename.endswith(".yml") or filename.endswith(".yaml"):
            continue
        with open(filename, 'r') as file:
            try:
                overrides.update(yaml.load(file, Loader=yaml.FullLoader))
            except TypeError:
                continue
    yield overrides
