"""Run the zoo's portable contract checks against every model in this folder."""

import pytest

import pybamm_model_zoo as zoo
from pybamm_model_zoo.testing.contract import MODEL, checks_in_scope

LOCAL = [entry for entry in zoo.all_entries() if entry.external]


@pytest.mark.parametrize("check", checks_in_scope(MODEL), ids=lambda check: check.name)
@pytest.mark.parametrize("entry", LOCAL, ids=lambda entry: entry.slug)
def test_contract(entry, check):
    check.run(entry)
