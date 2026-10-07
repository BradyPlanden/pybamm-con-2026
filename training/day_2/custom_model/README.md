# Custom models, zoo-style

Each folder here is laid out exactly like a
[PyBaMM model zoo](https://github.com/pybamm-team/PyBaMM/tree/main/packages/pybamm-model-zoo)
entry. [`thermal_dfn/`](thermal_dfn) is a worked example: a DFN written from
scratch and coupled to a lumped thermal model.

## Running the checks here

```bash
pytest
```

[`conftest.py`](conftest.py) registers this folder with the zoo as an external
collection. [`test_contract.py`](test_contract.py) then runs the zoo's model
contract on every model in it, alongside each model's own `tests/`.

## Adding a model to the zoo

In a fork of [PyBaMM](https://github.com/pybamm-team/PyBaMM), with the dev
environment installed (`uv sync --extra all --group dev`):

1. Render the template. This creates
   `packages/pybamm-model-zoo/src/pybamm_model_zoo/thermal_dfn/` and adds you to
   `.github/CODEOWNERS`:

   ```bash
   nox -s zoo-new -- --slug thermal_dfn --name ThermalDFN --author "Your Name" --github yourhandle
   ```

2. Copy `model.py`, `README.md`, `CITATION.bib`, `tests/` and `examples/` over
   the rendered files. Carry over the fields of `model.toml` that the template
   left as TODOs.
3. Change the import path from `thermal_dfn` to `pybamm_model_zoo.thermal_dfn`.
   It appears in two places: `class` in `model.toml` and the import in
   `__init__.py`.
4. If the model needs third-party packages, declare them as a `zoo-<slug>` extra.
   See the zoo README.
5. Generate the docs page, then run the full contract and your tests:

   ```bash
   nox -s zoo-docs
   nox -s zoo -- --zoo-model=thermal_dfn
   ```

6. Add a bullet to `packages/pybamm-model-zoo/CHANGELOG.md` (not PyBaMM's own
   changelog) and open a pull request.

New models join the `community` tier. They are tested on every PyBaMM pull
request, but a failure shows up on the model's badge and never blocks a PyBaMM
release.
