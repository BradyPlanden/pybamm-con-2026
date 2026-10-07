"""Register the models in this folder with the zoo, as an external collection.

Not needed once a model is copied into PyBaMM's `packages/pybamm-model-zoo`.
"""

import sys
from pathlib import Path

import pybamm_model_zoo as zoo

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
zoo.refresh(external_paths=[HERE])
