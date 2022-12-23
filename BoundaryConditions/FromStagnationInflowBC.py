def GenerateStagnationFluxInterface(Interface, stag_conditions, InternalCell):
    [p_stag, T_stag] = stag_conditions[1]
    p_int_orig = Interface.interfaceState.fluid_state.p
    T_int_orig = Interface.interfaceState.fluid_state.T
    Interface.interfaceState.fluid_state.p = p_stag
    Interface.interfaceState.fluid_state.T = T_stag
    Interface.interfaceState.fluid_state.update_thermo_from_pT()
    p_internal = InternalCell.fs.fluid_state.p
    gamma = Interface.interfaceState.fluid_state.gamma
    R = Interface.interfaceState.fluid_state.R
    #print(p_stag, p_internal)
    Ma_in = min(1.0, (2.0 / (gamma - 1.0) * ((p_stag / p_internal) ** ((gamma - 1.0) / gamma) - 1.0)) ** 0.5)
    m_dot = p_stag * (gamma / (R * T_stag)) ** 0.5 * Ma_in * (1.0 + 0.5 * (gamma - 1.0) * Ma_in ** 2.0) ** (0.5 * (gamma + 1.0) / (1.0 - gamma))

    interfaceFluxes = {}

    interfaceFluxes["mass"] = m_dot
    interfaceFluxes["energy"] = m_dot * Interface.interfaceState.fluid_state.enthalpy

    Interface.interfaceState.fluid_state.p = p_int_orig
    Interface.interfaceState.fluid_state.T = T_int_orig
    Interface.interfaceState.fluid_state.update_thermo_from_pT()

    return interfaceFluxes, Ma_in
