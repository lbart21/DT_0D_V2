from gdtk.gas import GasModel, GasState
from Algorithms.DesignToolAlgorithmV1_0D.FluidModel.FlowState import FlowState
class NozzleOutletInterfaceChokedFlow():
    def __init__(self, interface_ID, fluidPair) -> None:
        self.interface_ID = interface_ID
        gm = GasModel(fluidPair["fluid"])
        gs = GasState(gm)
        self.interfaceState = FlowState(model = gm, state = gs)
        self.interfaceFluxes = {
            "mass"      :   0.0,
            "energy"    :   0.0,
            }

    def fillGeometry(self, Geometry):
        self.GEO = Geometry
    
    def completeInterfaceMethods(self, cellArray, interfaceArray, mapCellIDToWestInterfaceIdx, \
                                        mapCellIDToEastInterfaceIdx, mapInterfaceIDToWestCellIdx, \
                                        mapInterfaceIDToEastCellIdx, dt_inv):
        WestCellState = cellArray[mapInterfaceIDToWestCellIdx[self.interface_ID]]
        self.interfaceState.Ma = 1.0
                          
        p_w = WestCellState.fs.fluid_state.p
        T_w = WestCellState.fs.fluid_state.T
        vel_x_w = WestCellState.fs.vel_x
        gamma_w = WestCellState.fs.fluid_state.gamma
        M_w = WestCellState.fs.Ma
        #print("Internal Mach number: ", M_w)
        
        gamma = self.interfaceState.fluid_state.gamma
        R = self.interfaceState.fluid_state.R

        P_t = p_w * (1.0 + 0.5 * (gamma_w - 1.0) * M_w ** 2.0) ** (gamma_w / (gamma_w - 1.0))
        T_t = T_w * (1.0 + 0.5 * (gamma_w - 1.0) * M_w ** 2.0)
        h_t = WestCellState.fs.fluid_state.enthalpy + 0.5 * vel_x_w ** 2.0
        
        M_int = self.interfaceState.Ma

        T_int = T_t * (1.0 + 0.5 * (gamma - 1.0) * M_int ** 2.0) ** (-1.0)
        p_int = P_t * (1.0 + 0.5 * (gamma_w - 1.0) * M_int ** 2.0) ** (-1.0 * gamma_w / (gamma_w - 1.0))
        self.interfaceState.fluid_state.T = T_int
        self.interfaceState.fluid_state.p = p_int
        self.interfaceState.fluid_state.update_thermo_from_pT()
        self.interfaceState.vel_x = M_int * self.interfaceState.fluid_state.a
        
        m_dot = P_t * (gamma / (R * T_t)) ** 0.5 * M_int * (1.0 + 0.5 * (gamma - 1.0) * M_int ** 2.0) ** (0.5 * (gamma + 1.0) / (1.0 - gamma))
        
        self.interfaceFluxes["mass"] = m_dot
        self.interfaceFluxes["energy"] = m_dot * h_t
        
        WestCellState.conservedProperties["mass"] -= self.GEO["A"] * self.interfaceFluxes["mass"] * dt_inv / WestCellState.GEO["dV"]
        WestCellState.conservedProperties["energy"] -= self.GEO["A"] * self.interfaceFluxes["energy"] * dt_inv / WestCellState.GEO["dV"]