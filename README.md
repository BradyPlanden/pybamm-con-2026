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

### Day 1: PyBaMM basics and practical simulations — [`training/day_1`](training/day_1)

Slides: [`day_1_slides.pdf`](training/day_1/day_1_slides.pdf)

| Notebook | Topics |
| --- | --- |
| [`01-getting-started`](training/day_1/01-getting-started.ipynb) | Models, parameters, experiments, outputs, and what a model is under the hood |
| [`02-power-vs-energy`](training/day_1/02-power-vs-energy.ipynb) | C-rate sweeps, energy vs power, electrode thickness |
| [`03-simulating-long-experiments`](training/day_1/03-simulating-long-experiments.ipynb) | Hundreds of cycles, summary variables, saving selected cycles |
| [`04-rpt-experiment`](training/day_1/04-rpt-experiment.ipynb) | Ageing cycles with reference performance tests |
| [`05-custom-experiments`](training/day_1/05-custom-experiments.ipynb) | Custom terminations, explicit and implicit control |

### Day 2: the model zoo, custom models and performance — [`training/day_2`](training/day_2)

Slides: [`day_2_slides.pdf`](training/day_2/day_2_slides.pdf)

Day 2 has two tracks. The talk covers both; for the self-guided hour, pick
the **model track** (notebooks 01–02: the model zoo and writing your own model)
or the **performance track** (notebooks 03–04: input parameters and solvers).

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

You need [Python](https://www.python.org/downloads/) 3.10–3.14 and
[Git](https://git-scm.com/downloads) (or download this repository as a ZIP from
the green **Code** button). The install downloads a few hundred MB, so please run
it before the session.

### macOS and Linux

```bash
git clone https://github.com/pybamm-team/pybamm-con-2026
cd pybamm-con-2026
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter lab
```

On Debian or Ubuntu, if `python3 -m venv` fails, install the venv module first
with `sudo apt install python3-venv`.

### Windows (PowerShell)

```powershell
git clone https://github.com/pybamm-team/pybamm-con-2026
cd pybamm-con-2026
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
jupyter lab
```

If PowerShell refuses to run `Activate.ps1`, allow local scripts once with
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, or use Command Prompt and
run `.venv\Scripts\activate.bat` instead.

### Next time

Activate the environment again before starting Jupyter:
`source .venv/bin/activate` on macOS and Linux, `.venv\Scripts\Activate.ps1` on
Windows.

This installs [PyBaMM](https://github.com/pybamm-team/PyBaMM) 26.10.1.0 and the
[PyBaMM model zoo](https://github.com/pybamm-team/PyBaMM/tree/main/packages/pybamm-model-zoo)
0.1.0, the versions the notebooks were tested with.
