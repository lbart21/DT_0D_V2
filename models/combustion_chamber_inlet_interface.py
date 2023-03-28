"""
File containing the class for the inlet interface to the combustion chamber.
"""
from gdtk.gas import GasModel, GasState

from Algorithms.DesignToolAlgorithmV2_0D.FluidModel.FlowState import FlowState
from Algorithms.DesignToolAlgorithmV2_0D.BoundaryConditions.FromStagnationInflowBC import GenerateStagnationFluxInterface
class CombustionChamberInletInterface():
    """
    interface_ID = int
    fluidPair = GasState object
    inletBC = list
    """
    def __init__(self, interface_id, fluid_pair, inlet_bc) -> None:
        self.interface_id = interface_id
        g_m = GasModel(fluid_pair["fluid"])
        g_s = GasState(g_m)
        self.interface_state = FlowState(model = g_m, state = g_s)
        self.interface_fluxes = {}
        self.inlet_bc = inlet_bc
        self.geo = None

    def fill_geometry(self, geometry):
        """
        Sets GEO attribute
        """
        self.geo = geometry

    def complete_interface_methods(self, mesh, dt_inv):
        """
        Find interior cell, calculate fluxes and update conserved quantities of cell.
        """
        inside_cell_idx = mesh.map_interface_id_To_east_cell_idx[self.interface_id]
        inside_cell_state = mesh.cell_array[inside_cell_idx]
        self.interface_state.fluid_state.p = inside_cell_state.fs.fluid_state.p
        self.interface_state.fluid_state.T = inside_cell_state.fs.fluid_state.T

        self.interface_state.fluid_state.update_thermo_from_pT()

        if self.inlet_bc[0] == "FromStag":
            fluxes, mach_in = GenerateStagnationFluxInterface(Interface = self, stag_conditions = self.inlet_bc, InternalCell = inside_cell_state)
            self.interface_fluxes = fluxes
            self.interface_state.Ma = mach_in

        inside_cell_state.conserved_properties["mass"] += self.geo["A"] * self.interface_fluxes["mass"] * dt_inv / inside_cell_state.geo["dV"]
        inside_cell_state.conserved_properties["energy"] += self.geo["A"] * self.interface_fluxes["energy"] * dt_inv / inside_cell_state.geo["dV"]
        