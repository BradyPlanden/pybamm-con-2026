# PyBaMM Conference 2026

Training material for the [PyBaMM Battery Modelling Conference 2026](https://eeg.engin.umich.edu/pybamm_conf/),
15–16 October 2026, Rogel Ballroom, Michigan Union, Ann Arbor, Michigan, USA.

The conference combines two science-focused days of invited plenaries and
student and early-career talks. Its themes are:

- Physics-based models, including novel chemistries and degradation mechanisms
- Numerical methods, solver improvements, differentiable programming and software advances
- Data-driven models, machine learning, state estimation and parameter estimation
- System-level models (such as pack models) and techno-economic analysis
- Agentic workflows and integration with other workflow automation tools

Organised by Venkat Viswanathan (University of Michigan), Valentin Sulzer
(Ionworks), Anoushka Bhutani and Amal S Sebastian (University of Michigan).

## Training

There is a 1.5 hour training session on each day: a ~30 minute talk, followed
by ~1 hour of self-guided work through the notebooks, with members of the
PyBaMM team on hand to help. You are welcome to bring your own problems.

### Day 1: PyBaMM basics and real-world simulations — [`training/day_1`](training/day_1)

Slides: [`day_1_slides.pdf`](training/day_1/day_1_slides.pdf)

| Notebook | Topics |
| --- | --- |
| [`01-getting-started`](training/day_1/01-getting-started.ipynb) | Models, parameters, experiments, outputs, and what a model is under the hood |
| [`02-power-vs-energy`](training/day_1/02-power-vs-energy.ipynb) | C-rate sweeps, energy vs power, electrode thickness |
| [`03-simulating-long-experiments`](training/day_1/03-simulating-long-experiments.ipynb) | Hundreds of cycles, summary variables, saving selected cycles |
| [`04-rpt-experiment`](training/day_1/04-rpt-experiment.ipynb) | Ageing cycles with reference performance tests |
| [`05-custom-experiments`](training/day_1/05-custom-experiments.ipynb) | Custom terminations, explicit and implicit control |

### Day 2: the model zoo, custom models, input parameters and solvers — [`training/day_2`](training/day_2)

Slides: [`day_2_slides.pdf`](training/day_2/day_2_slides.pdf)

| Notebook | Topics |
| --- | --- |
| [`01-model-zoo`](training/day_2/01-model-zoo.ipynb) | Finding, loading and testing models from the PyBaMM model zoo |
| [`02-custom-zoo-model`](training/day_2/02-custom-zoo-model.ipynb) | Writing a standalone model (a thermal DFN) in the zoo format, validating it, and contributing it |
| [`03-input-parameters`](training/day_2/03-input-parameters.ipynb) | Re-running simulations efficiently with input parameters |
| [`04-pybamm-solvers`](training/day_2/04-pybamm-solvers.ipynb) | The IDAKLU solver: time stepping, tolerances, output variables, parallel solves, sensitivities |

The custom model lives in [`training/day_2/custom_model/thermal_dfn`](training/day_2/custom_model/thermal_dfn),
laid out exactly like a [model zoo](https://github.com/pybamm-team/PyBaMM/tree/main/packages/pybamm-model-zoo)
entry. Run its contract checks and physics tests with:

```bash
cd training/day_2/custom_model
pytest
```

## Installation

You need Python 3.10–3.14. We recommend a fresh virtual environment:

```bash
git clone https://github.com/pybamm-team/pybamm-con-2026
cd pybamm-con-2026
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter lab
```

`requirements.txt` pins PyBaMM and the model zoo to the versions the notebooks
were tested with.
