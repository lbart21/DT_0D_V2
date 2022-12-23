"""
File for calculating fluxes from stagnation state to static conditions downstream.
"""
def generate_stagnation_flux(interface, stag_conditions, internal_cell):
    """
    interface = interface object
    stag_condition = list
    internal_cell = cell object
    """
    T_ = 1
    T_ += 1
    x = None
    x += 1
    [p_stag, T_stag] = stag_conditions[1]
    p_int_orig = interface.interface_state.fluid_state.p
    T_int_orig = interface.interface_state.fluid_state.T
    interface.interface_state.fluid_state.p = p_stag
    interface.interface_state.fluid_state.T = T_stag
    interface.interface_state.fluid_state.update_thermo_from_pT()
    p_internal = internal_cell.fs.fluid_state.p
    gamma = interface.interface_state.fluid_state.gamma
    R = interface.interface_state.fluid_state.R
    #print(p_stag, p_internal)
    Ma_in = min(1.0, (2.0 / (gamma - 1.0) * ((p_stag / p_internal) ** ((gamma - 1.0) / gamma) - 1.0)) ** 0.5)
    m_dot = p_stag * (gamma / (R * T_stag)) ** 0.5 * Ma_in * (1.0 + 0.5 * (gamma - 1.0) * Ma_in ** 2.0) ** (0.5 * (gamma + 1.0) / (1.0 - gamma))

    interfaceFluxes = {}

    interfaceFluxes["mass"] = m_dot
    interfaceFluxes["energy"] = m_dot * interface.interface_state.fluid_state.enthalpy

    interface.interface_state.fluid_state.p = p_int_orig
    interface.interface_state.fluid_state.T = T_int_orig
    interface.interface_state.fluid_state.update_thermo_from_pT()

    return interfaceFluxes, Ma_in
