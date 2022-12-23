from gdtk.gas import GasModel, GasState
from Algorithms.DesignToolAlgorithmV1_0D.FluidModel.FlowState import FlowState
from Algorithms.DesignToolAlgorithmV1_0D.BoundaryConditions.FromStagnationInflowBC import GenerateStagnationFluxInterface
class CombustionChamberInletInterface():
    def __init__(self, interface_ID, fluidPair, inletBC) -> None:
        self.interface_ID = interface_ID
        gm = GasModel(fluidPair["fluid"])
        gs = GasState(gm)
        self.interfaceState = FlowState(model = gm, state = gs)
        self.interfaceFluxes = {}
        self.inletBC = inletBC
    
    def fillGeometry(self, Geometry):
        self.GEO = Geometry
    
    def completeInterfaceMethods(self, cellArray, interfaceArray, mapCellIDToWestInterfaceIdx, \
                                        mapCellIDToEastInterfaceIdx, mapInterfaceIDToWestCellIdx, \
                                        mapInterfaceIDToEastCellIdx, dt_inv):
        InsideCellState = cellArray[mapInterfaceIDToEastCellIdx[self.interface_ID]]
        self.interfaceState.fluid_state.p = InsideCellState.fs.fluid_state.p
        self.interfaceState.fluid_state.T = InsideCellState.fs.fluid_state.T
        
        self.interfaceState.fluid_state.update_thermo_from_pT()
        
        if self.inletBC[0] == "FromStag":
            fluxes, Ma_in = GenerateStagnationFluxInterface(Interface = self, stag_conditions = self.inletBC, InternalCell = InsideCellState)
            self.interfaceFluxes = fluxes
            self.interfaceState.Ma = Ma_in

        InsideCellState.conservedProperties["mass"] += self.GEO["A"] * self.interfaceFluxes["mass"] * dt_inv / InsideCellState.GEO["dV"]
        InsideCellState.conservedProperties["energy"] += self.GEO["A"] * self.interfaceFluxes["energy"] * dt_inv / InsideCellState.GEO["dV"]
        