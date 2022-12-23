from Algorithms.DesignToolAlgorithmV1_0D.ComponentModels.meshObject import meshObject
from Algorithms.DesignToolAlgorithmV1_0D.ComponentModels.CombAndNozzleCellWithHeat import CombAndNozzleCellWithHeat
from Algorithms.DesignToolAlgorithmV1_0D.ComponentModels.NozzleOutletInterfaceFixedP import NozzleOutletInterfaceFixedP
from Algorithms.DesignToolAlgorithmV1_0D.ComponentModels.CombustionChamberInletInterface import CombustionChamberInletInterface

import math as m

class JoinedCombAndNozzleFixedP():
    def __init__(self, TotalGeometry, prop1, prop2, vel_x, \
                        backPressure, propsGiven, Eilmer_fluid_file, CombHeatFlux, \
                        componentLabel, inletBC) -> None:
        """
        TotalGeometry = [D_in, D_out, L_comb, L_noz]
        """
        self.meshObject = meshObject(nCells=1)
        fluidPairs = {}
        fluidPairs["fluid"] = Eilmer_fluid_file  #Dictionary of strings of .lua file names to generate Eilmer GasModels and hence GasStates
        self.meshObject.componentLabels = [componentLabel]

        self.initialiseCell(Geometry = TotalGeometry, prop1 = prop1, \
                                prop2 = prop2, propsGiven = propsGiven, \
                                vel_x = vel_x, componentLabel = componentLabel, \
                                fluidPairs = fluidPairs, heatFlux = CombHeatFlux)

        self.initialiseInterfaces(Geometry = TotalGeometry, fluidPairs = fluidPairs, backPressure = backPressure, inletBC = inletBC)

        ### Form connections
        self.connectCellsToInterfaces()
    
    def initialiseCell(self, Geometry, prop1, prop2, propsGiven, vel_x, componentLabel, fluidPairs, heatFlux):
        [D_in, D_out, L_comb, L_noz] = Geometry
        dV_C = m.pi * D_in ** 2.0 * L_comb
        dV_N = m.pi * (D_in ** 2.0 + D_in * D_out + D_out ** 2.0) * L_noz / 12.0

        A_s_C = m.pi * D_in * L_comb
        A_s_N = 0.5 * m.pi * (D_in + D_out) * L_noz * (1.0 + (0.5 * (D_out - D_in) / L_noz) ** 2.0) ** 0.5
        GEO = {
            "dV_C"  : dV_C,
            "dV_N"  : dV_N, 
            "dV"    : dV_N + dV_C,
            "dx_C"  : L_comb,
            "dx_N"  : L_noz,
            "dx"    : L_comb + L_noz,
            "A_s_C" : A_s_C,
            "A_s_N" : A_s_N,
            "A_s"   : A_s_C + A_s_N
        }
        cell = CombAndNozzleCellWithHeat(TotalGeometry = GEO, heatFlux = heatFlux, fluidPair = fluidPairs, cell_ID = 0, label = componentLabel)
        cell.fillProps(prop1 = prop1, prop2 = prop2, propsGiven = propsGiven, vel_x = vel_x)
        self.meshObject.cellArray = [cell]
        

    def initialiseInterfaces(self, Geometry, fluidPairs, backPressure, inletBC):
        [D_in, D_out, L_comb, L_noz] = Geometry
        A_in = 0.25 * m.pi * D_in ** 2.0
        A_out = 0.25 * m.pi * D_out ** 2.0
        InInterface_GEO = {"A"  : A_in}
        OutInterface_GEO = {"A"  : A_out}

        InInterface = CombustionChamberInletInterface(interface_ID = 0, fluidPair = fluidPairs, inletBC = inletBC)
        InInterface.fillGeometry(Geometry = InInterface_GEO)

        OutInterface = NozzleOutletInterfaceFixedP(interface_ID = 1, fluidPair = fluidPairs, backPressure = backPressure)
        OutInterface.fillGeometry(Geometry = OutInterface_GEO)
        self.meshObject.interfaceArray = [InInterface, OutInterface]
        

    def connectCellsToInterfaces(self):
        self.meshObject.mapCellIDToWestInterfaceIdx = [0] 
        self.meshObject.mapCellIDToEastInterfaceIdx = [1] 
        self.meshObject.mapInterfaceIDToWestCellIdx = [None, 0] 
        self.meshObject.mapInterfaceIDToEastCellIdx = [0, None] 
