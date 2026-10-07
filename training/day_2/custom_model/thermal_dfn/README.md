# ThermalDFN

## Summary

The Doyle-Fuller-Newman (DFN) model written out equation by equation, coupled to
a single lumped cell temperature:

```
C dT/dt = I (U_eq - V) - h A (T - T_amb)
```

`C` is the new parameter `"Cell heat capacity [J.K-1]"`. The heat-transfer
coefficient, cooling area and ambient temperature come from the parameter set.
The heat source is the irreversible heat only: `U_eq` is the open-circuit voltage
at the electrode-averaged stoichiometries. Every kinetic and transport property
is evaluated at `T`, so the electrochemistry and the temperature are fully
coupled.

This is a teaching model. For real thermal studies use
`pybamm.lithium_ion.DFN({"thermal": "lumped"})`, which also includes reversible
heat and derives the heat capacity from the cell's layers.

## Usage

```python
import pybamm
import pybamm_model_zoo as zoo

model = zoo.load("ThermalDFN")()
solution = pybamm.Simulation(model).solve([0, 3600])
print(solution["Temperature [C]"](3600))
```

`examples/run_thermal_dfn.py` prints the peak temperature of a full discharge at
three C-rates.

## Validation

* With a very large heat capacity the temperature stays fixed and the voltage
  matches `pybamm.lithium_ion.BasicDFN` to within 0.1 mV.
* With no cooling, the heat stored, `C (T_end - T_0)`, equals the time integral
  of `"Heat source [W]"` to `rtol=1e-3`.
* At zero current the cell stays at the ambient temperature.
* All of these run in `tests/test_thermal_dfn.py`.

## Citation

See `CITATION.bib`. Cite `Doyle1993` for the DFN model and
`PyBaMMConference2026` for this implementation. Both are registered when the
model is created, so `pybamm.print_citations()` lists them.

## Maintainer

The PyBaMM Team (@pybamm-team/maintainers) — tier: community
