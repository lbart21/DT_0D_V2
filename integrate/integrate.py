class Integrate():
    def __init__(self, mesh, dt_flag, t_current) -> None:
        """
        dt_flag = ["Fixed", float] or ["FromSim"]
        """
        self.mesh = mesh
        self.dt_total = 0.0
        if dt_flag[0] == "Fixed":
            self.dt_total = dt_flag[1]
        for interface in self.mesh.interface_array:
            interface.complete_interface_methods(cellArray = self.mesh.cell_array, interfaceArray = self.mesh.interface_array, \
                                                mapCellIDToWestInterfaceIdx = self.mesh.map_cell_id_to_west_interface_idx, \
                                                mapCellIDToEastInterfaceIdx = self.mesh.map_cell_id_to_east_interface_idx, \
                                                mapInterfaceIDToWestCellIdx = self.mesh.map_interface_id_to_west_cell_idx, \
                                                mapInterfaceIDToEastCellIdx = self.mesh.map_interface_id_to_east_cell_idx, dt_inv = self.dt_total)
        for cell in self.mesh.cell_array:
            cell.decode_to_primative_properties()
        for cell in self.mesh.cell_array:
            cell.complete_cell_methods(dt_inv = self.dt_total)
        for cell in self.mesh.cell_array:
            cell.decode_to_primative_properties()
        