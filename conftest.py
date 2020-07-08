import os
import pytest
import yaml


@pytest.fixture(scope="module")
def load_overrides():
    overrides = {}
    for filename in os.listdir("overrides"):
        filename = os.path.join("overrides", filename)
        if not filename.endswith(".yml") or filename.endswith(".yaml"):
            continue
        with open(filename, 'r') as file:
            try:
                overrides.update(yaml.load(file, Loader=yaml.FullLoader))
            except TypeError as error:
                continue
    yield overrides
