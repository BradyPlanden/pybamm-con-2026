"""Run the zoo's portable contract checks and example scripts for every model here."""

import runpy

import pytest

import pybamm_model_zoo as zoo
from pybamm_model_zoo.testing.contract import MODEL, checks_in_scope

LOCAL = [entry for entry in zoo.all_entries() if entry.external]
EXAMPLES = [path for entry in LOCAL for path in sorted(entry.path.glob("examples/*.py"))]


@pytest.mark.parametrize("check", checks_in_scope(MODEL), ids=lambda check: check.name)
@pytest.mark.parametrize("entry", LOCAL, ids=lambda entry: entry.slug)
def test_contract(entry, check):
    check.run(entry)


@pytest.mark.parametrize("path", EXAMPLES, ids=lambda path: path.name)
def test_example(path):
    runpy.run_path(str(path), run_name="__main__")
