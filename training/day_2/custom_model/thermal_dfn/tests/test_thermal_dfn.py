"""Physics tests for ThermalDFN.

The zoo's contract suite already checks that the model imports, is well posed,
builds, and solves, so these pin *physical* results instead.
"""

import numpy as np

import pybamm
import pybamm_model_zoo as zoo


def solve(updates, t_end):
    model = zoo.load("ThermalDFN")()
    parameter_values = model.default_parameter_values
    parameter_values.update(updates)
    simulation = pybamm.Simulation(model, parameter_values=parameter_values)
    return parameter_values, simulation.solve([0, t_end])


class TestThermalDFN:
    def test_isothermal_limit_matches_core_dfn(self):
        """With a huge heat capacity the temperature cannot move, so this is a DFN."""
        _, solution = solve({"Cell heat capacity [J.K-1]": 1e12}, 3000)
        reference = pybamm.Simulation(
            pybamm.lithium_ion.BasicDFN(),
            parameter_values=pybamm.ParameterValues("Chen2020"),
        ).solve([0, 3000])
        times = np.linspace(0, 3000, 50)
        np.testing.assert_allclose(
            solution["Voltage [V]"](times), reference["Voltage [V]"](times), atol=1e-4
        )

    def test_adiabatic_energy_balance(self):
        """With no cooling, every joule of heat generated warms the cell."""
        parameter_values, solution = solve(
            {"Total heat transfer coefficient [W.m-2.K-1]": 0}, 3000
        )
        times = np.linspace(0, 3000, 3001)
        stored = parameter_values["Cell heat capacity [J.K-1]"] * (
            solution["Temperature [K]"](3000) - solution["Temperature [K]"](0)
        )
        generated = np.trapezoid(solution["Heat source [W]"](times), times)
        np.testing.assert_allclose(stored, generated, rtol=1e-3)

    def test_rest_stays_at_ambient(self):
        """No current means no heat, so the cell stays at the ambient temperature."""
        _, solution = solve({"Current function [A]": 0}, 600)
        np.testing.assert_allclose(
            solution["Temperature [K]"](np.linspace(0, 600, 10)), 298.15, rtol=1e-8
        )
