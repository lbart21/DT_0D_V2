from gdtk.gas import GasModel, GasState
from Algorithms.DesignToolAlgorithmV1_0D.FluidModel.FlowState import FlowState
class CombAndNozzleCellWithHeat():
    def __init__(self, TotalGeometry, heatFlux, fluidPair, cell_ID, label) -> None:

        eilmer_fluid_name = fluidPair["fluid"]
        gm = GasModel(eilmer_fluid_name)
        gs = GasState(gm)
        self.fs = FlowState(model = gm, state = gs) #fs = flow state, not fluid state 
        self.conservedProperties = {
            "mass"      : 0.0,
            "energy"    : 0.0
        }
        self.heatFlux = heatFlux
        self.GEO = TotalGeometry
        self.cell_ID = cell_ID
        self.label = label
    
    def updatePrimativeProperties(self):
        self.fs.fluid_state.rho = self.conservedProperties["mass"]
        self.fs.fluid_state.u = self.conservedProperties["energy"] / self.conservedProperties["mass"] - 0.5 * self.fs.vel_x ** 2
        self.fs.fluid_state.update_thermo_from_rhou()
        self.fs.Ma = self.fs.vel_x / self.fs.fluid_state.a

    def fillProps(self, prop1, prop2, propsGiven, vel_x):
        if propsGiven == "pT":
            self.fs.fluid_state.p = prop1
            self.fs.fluid_state.T = prop2
            self.fs.vel_x = vel_x
            self.fs.fluid_state.update_thermo_from_pT() 
            self.fs.Ma = self.fs.vel_x / self.fs.fluid_state.a
            
        if propsGiven == "rhoP":
            self.fs.fluid_state.p = prop1
            self.fs.fluid_state.rho = prop2
            self.fs.vel_x = vel_x
            self.fs.fluid_state.update_thermo_from_rhop()
            self.fs.Ma = self.fs.vel_x / self.fs.fluid_state.a
            
        self.initialiseConservedProperties()
    
    def initialiseConservedProperties(self):
        self.conservedProperties["mass"] = self.fs.fluid_state.rho
        self.conservedProperties["energy"] = self.fs.fluid_state.rho * (self.fs.fluid_state.u + 0.5 * self.fs.vel_x ** 2)

    def completeCellMethods(self, dt_inv):
        self.conservedProperties["energy"] += self.heatFlux * self.GEO["A_s_C"] * dt_inv / self.GEO["dV"]
        