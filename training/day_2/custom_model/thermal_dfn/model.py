"""Doyle-Fuller-Newman model with a lumped thermal energy balance, written from scratch."""

from __future__ import annotations

import pybamm
import pybamm_model_zoo

SLUG = "thermal_dfn"


class ThermalDFN(pybamm.lithium_ion.BaseModel):
    """DFN model coupled to a lumped (zero-dimensional) cell temperature.

    Every equation is written out explicitly rather than assembled from PyBaMM
    submodels, so the whole model can be read in one file. The cell temperature
    obeys ``C dT/dt = Q - h A (T - T_amb)``, where the heat source ``Q`` is the
    irreversible heat ``I (U_eq - V)`` and ``U_eq`` is the open-circuit voltage
    at the electrode-averaged stoichiometries.

    Parameters
    ----------
    name : str, optional
        The name of the model.
    """

    def __init__(self, name: str = "Thermal DFN") -> None:
        super().__init__(name=name)
        pybamm_model_zoo.register_citation(SLUG, "PyBaMMConference2026", "Doyle1993")
        param = self.param

        ######################
        # Variables
        ######################
        # Variables that depend on time only are created without a domain
        Q = pybamm.Variable("Discharge capacity [A.h]")
        T = pybamm.Variable("Temperature [K]")

        # Variables that vary spatially are created with a domain
        c_e_n = pybamm.Variable(
            "Negative electrolyte concentration [mol.m-3]", domain="negative electrode"
        )
        c_e_s = pybamm.Variable(
            "Separator electrolyte concentration [mol.m-3]", domain="separator"
        )
        c_e_p = pybamm.Variable(
            "Positive electrolyte concentration [mol.m-3]", domain="positive electrode"
        )
        # Concatenations let one equation hold across several domains
        c_e = pybamm.concatenation(c_e_n, c_e_s, c_e_p)

        phi_e_n = pybamm.Variable(
            "Negative electrolyte potential [V]", domain="negative electrode"
        )
        phi_e_s = pybamm.Variable(
            "Separator electrolyte potential [V]", domain="separator"
        )
        phi_e_p = pybamm.Variable(
            "Positive electrolyte potential [V]", domain="positive electrode"
        )
        phi_e = pybamm.concatenation(phi_e_n, phi_e_s, phi_e_p)

        phi_s_n = pybamm.Variable(
            "Negative electrode potential [V]", domain="negative electrode"
        )
        phi_s_p = pybamm.Variable(
            "Positive electrode potential [V]", domain="positive electrode"
        )
        # Particle concentrations also vary through the electrode, so they need a
        # secondary domain
        c_s_n = pybamm.Variable(
            "Negative particle concentration [mol.m-3]",
            domain="negative particle",
            auxiliary_domains={"secondary": "negative electrode"},
        )
        c_s_p = pybamm.Variable(
            "Positive particle concentration [mol.m-3]",
            domain="positive particle",
            auxiliary_domains={"secondary": "positive electrode"},
        )

        ######################
        # Parameters
        ######################
        current = param.current_with_time
        i_cell = param.current_density_with_time
        # A new parameter: it needs a default in `default_parameter_values`
        heat_capacity = pybamm.Parameter("Cell heat capacity [J.K-1]")
        h = pybamm.Parameter("Total heat transfer coefficient [W.m-2.K-1]")
        area = pybamm.Parameter("Cell cooling surface area [m2]")
        T_amb = pybamm.Parameter("Ambient temperature [K]")

        # Primary broadcasts turn a scalar into a vector on a domain
        eps_n = pybamm.PrimaryBroadcast(
            pybamm.Parameter("Negative electrode porosity"), "negative electrode"
        )
        eps_s = pybamm.PrimaryBroadcast(
            pybamm.Parameter("Separator porosity"), "separator"
        )
        eps_p = pybamm.PrimaryBroadcast(
            pybamm.Parameter("Positive electrode porosity"), "positive electrode"
        )
        eps = pybamm.concatenation(eps_n, eps_s, eps_p)
        eps_s_n = pybamm.Parameter("Negative electrode active material volume fraction")
        eps_s_p = pybamm.Parameter("Positive electrode active material volume fraction")
        tor = pybamm.concatenation(
            eps_n**param.n.b_e, eps_s**param.s.b_e, eps_p**param.p.b_e
        )
        a_n = 3 * param.n.prim.epsilon_s_av / param.n.prim.R_typ
        a_p = 3 * param.p.prim.epsilon_s_av / param.p.prim.R_typ

        ######################
        # Butler-Volmer kinetics
        ######################
        # `surf` takes the value at the particle surface (the "right" boundary)
        c_s_surf_n = pybamm.surf(c_s_n)
        sto_surf_n = c_s_surf_n / param.n.prim.c_max
        j0_n = param.n.prim.j0(c_e_n, c_s_surf_n, T)
        eta_n = phi_s_n - phi_e_n - param.n.prim.U(sto_surf_n, T)
        j_n = (
            2
            * j0_n
            * pybamm.sinh(param.n.prim.ne / 2 * param.F * eta_n / (param.R * T))
        )

        c_s_surf_p = pybamm.surf(c_s_p)
        sto_surf_p = c_s_surf_p / param.p.prim.c_max
        j0_p = param.p.prim.j0(c_e_p, c_s_surf_p, T)
        eta_p = phi_s_p - phi_e_p - param.p.prim.U(sto_surf_p, T)
        j_p = (
            2
            * j0_p
            * pybamm.sinh(param.p.prim.ne / 2 * param.F * eta_p / (param.R * T))
        )

        a_j_n = a_n * j_n
        a_j_p = a_p * j_p
        a_j = pybamm.concatenation(
            a_j_n, pybamm.PrimaryBroadcast(0, "separator"), a_j_p
        )

        ######################
        # Discharge capacity
        ######################
        self.rhs[Q] = current / 3600
        self.initial_conditions[Q] = pybamm.Scalar(0)

        ######################
        # Particles
        ######################
        # `div` and `grad` become matrices at the discretisation stage
        N_s_n = -param.n.prim.D(c_s_n, T) * pybamm.grad(c_s_n)
        N_s_p = -param.p.prim.D(c_s_p, T) * pybamm.grad(c_s_p)
        self.rhs[c_s_n] = -pybamm.div(N_s_n)
        self.rhs[c_s_p] = -pybamm.div(N_s_p)
        self.boundary_conditions[c_s_n] = {
            "left": (pybamm.Scalar(0), "Neumann"),
            "right": (
                -j_n / (param.F * pybamm.surf(param.n.prim.D(c_s_n, T))),
                "Neumann",
            ),
        }
        self.boundary_conditions[c_s_p] = {
            "left": (pybamm.Scalar(0), "Neumann"),
            "right": (
                -j_p / (param.F * pybamm.surf(param.p.prim.D(c_s_p, T))),
                "Neumann",
            ),
        }
        self.initial_conditions[c_s_n] = param.n.prim.c_init
        self.initial_conditions[c_s_p] = param.p.prim.c_init

        ######################
        # Current in the solid
        ######################
        sigma_eff_n = param.n.sigma(sto_surf_n, T) * eps_s_n**param.n.b_s
        sigma_eff_p = param.p.sigma(sto_surf_p, T) * eps_s_p**param.p.b_s
        i_s_n = -sigma_eff_n * pybamm.grad(phi_s_n)
        i_s_p = -sigma_eff_p * pybamm.grad(phi_s_p)
        # Algebraic equations are keyed by the variable they determine; the L_x**2
        # factor improves conditioning
        self.algebraic[phi_s_n] = param.L_x**2 * (pybamm.div(i_s_n) + a_j_n)
        self.algebraic[phi_s_p] = param.L_x**2 * (pybamm.div(i_s_p) + a_j_p)
        self.boundary_conditions[phi_s_n] = {
            "left": (pybamm.Scalar(0), "Dirichlet"),
            "right": (pybamm.Scalar(0), "Neumann"),
        }
        self.boundary_conditions[phi_s_p] = {
            "left": (pybamm.Scalar(0), "Neumann"),
            "right": (i_cell / pybamm.boundary_value(-sigma_eff_p, "right"), "Neumann"),
        }
        # For algebraic equations the initial condition is an initial guess
        self.initial_conditions[phi_s_n] = pybamm.Scalar(0)
        self.initial_conditions[phi_s_p] = param.ocv_init

        ######################
        # Electrolyte
        ######################
        i_e = (param.kappa_e(c_e, T) * tor) * (
            param.chiRT_over_Fc(c_e, T) * pybamm.grad(c_e) - pybamm.grad(phi_e)
        )
        self.algebraic[phi_e] = param.L_x**2 * (pybamm.div(i_e) - a_j)
        self.boundary_conditions[phi_e] = {
            "left": (pybamm.Scalar(0), "Neumann"),
            "right": (pybamm.Scalar(0), "Neumann"),
        }
        self.initial_conditions[phi_e] = -param.n.prim.U_init

        N_e = -tor * param.D_e(c_e, T) * pybamm.grad(c_e)
        self.rhs[c_e] = (1 / eps) * (
            -pybamm.div(N_e) + (1 - param.t_plus(c_e, T)) * a_j / param.F
        )
        self.boundary_conditions[c_e] = {
            "left": (pybamm.Scalar(0), "Neumann"),
            "right": (pybamm.Scalar(0), "Neumann"),
        }
        self.initial_conditions[c_e] = param.c_e_init

        ######################
        # Lumped thermal model
        ######################
        voltage = pybamm.boundary_value(phi_s_p, "right")
        sto_n_av = pybamm.x_average(pybamm.r_average(c_s_n)) / param.n.prim.c_max
        sto_p_av = pybamm.x_average(pybamm.r_average(c_s_p)) / param.p.prim.c_max
        ocv = param.p.prim.U(sto_p_av, T) - param.n.prim.U(sto_n_av, T)
        heat_source = current * (ocv - voltage)
        heat_loss = h * area * (T - T_amb)
        self.rhs[T] = (heat_source - heat_loss) / heat_capacity
        self.initial_conditions[T] = param.T_init

        ######################
        # Output variables
        ######################
        num_cells = pybamm.Parameter(
            "Number of cells connected in series to make a battery"
        )
        self.variables = {
            "Time [s]": pybamm.t,
            "Discharge capacity [A.h]": Q,
            "Current [A]": current,
            # needed by pybamm.Experiment
            "Current variable [A]": current,
            "Voltage [V]": voltage,
            "Battery voltage [V]": voltage * num_cells,
            "Bulk open-circuit voltage [V]": ocv,
            "Temperature [K]": T,
            "Temperature [C]": T - 273.15,
            "Heat source [W]": heat_source,
            "Heat loss [W]": heat_loss,
            "Electrolyte concentration [mol.m-3]": c_e,
            "Electrolyte potential [V]": phi_e,
            "Negative electrode potential [V]": phi_s_n,
            "Positive electrode potential [V]": phi_s_p,
            "Negative particle concentration [mol.m-3]": c_s_n,
            "Positive particle concentration [mol.m-3]": c_s_p,
            "Negative particle surface concentration [mol.m-3]": c_s_surf_n,
            "Positive particle surface concentration [mol.m-3]": c_s_surf_p,
        }
        # Events stop the solver, e.g. at the voltage cut-offs
        self.events += [
            pybamm.Event("Minimum voltage [V]", voltage - param.voltage_low_cut),
            pybamm.Event("Maximum voltage [V]", param.voltage_high_cut - voltage),
        ]

    @property
    def default_parameter_values(self) -> pybamm.ParameterValues:
        parameter_values = pybamm.ParameterValues("Chen2020")
        # Roughly a 21700 cell: ~70 g at ~1 J.g-1.K-1
        parameter_values.update(
            {"Cell heat capacity [J.K-1]": 70.0}, check_already_exists=False
        )
        return parameter_values
