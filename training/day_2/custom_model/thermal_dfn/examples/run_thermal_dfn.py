"""Peak cell temperature of a full discharge at several C-rates."""

import pybamm
import pybamm_model_zoo as zoo

model = zoo.load("ThermalDFN")()
print("  C-rate   capacity [A.h]   peak temperature [C]")
for c_rate in (0.5, 1, 2):
    experiment = pybamm.Experiment([f"Discharge at {c_rate}C until 2.5V"])
    solution = pybamm.Simulation(model, experiment=experiment).solve()
    t = solution.t
    print(
        f"{c_rate:8.1f}   {solution['Discharge capacity [A.h]'](t[-1]):14.2f}"
        f"   {max(solution['Temperature [C]'](t)):20.1f}"
    )
