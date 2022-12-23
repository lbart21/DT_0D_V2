class Integrate():
    def __init__(self, mesh, dt_flag, tCurrent) -> None:
        """
        dt_flag = ["Fixed", float] or ["FromSim"]
        """
        self.mesh = mesh
        self.dtTotal = 0.0
        if dt_flag[0] == "Fixed":
            self.dtTotal = dt_flag[1]
        for interface in self.mesh.interfaceArray:
            interface.completeInterfaceMethods(cellArray = self.mesh.cellArray, interfaceArray = self.mesh.interfaceArray, \
                                                mapCellIDToWestInterfaceIdx = self.mesh.mapCellIDToWestInterfaceIdx, \
                                                mapCellIDToEastInterfaceIdx = self.mesh.mapCellIDToEastInterfaceIdx, \
                                                mapInterfaceIDToWestCellIdx = self.mesh.mapInterfaceIDToWestCellIdx, \
                                                mapInterfaceIDToEastCellIdx = self.mesh.mapInterfaceIDToEastCellIdx, dt_inv = self.dtTotal)
        for cell in self.mesh.cellArray:
            cell.updatePrimativeProperties()
        for cell in self.mesh.cellArray:
            cell.completeCellMethods(dt_inv = self.dtTotal)
        for cell in self.mesh.cellArray:
            cell.updatePrimativeProperties()
        