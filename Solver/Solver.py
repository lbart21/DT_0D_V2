from Algorithms.DesignToolAlgorithmV1_0D.Solver.WriteCellDataToFile import WriteCellDataToFile
from Algorithms.DesignToolAlgorithmV1_0D.Solver.WriteInterfaceDataToFile import WriteInterfaceDataToFile
from Algorithms.DesignToolAlgorithmV1_0D.Integrate.Integrate import Integrate

class Solver():
    def __init__(self, meshObject, dt_flag, tFinal, dataSaveDt, cell_flow_property_variables_to_write, \
                        interface_flow_property_variables_to_write, rapidDataSavenSteps) -> None:
        tCurrent = 0.0
        currentMeshObject = meshObject
        time_tol = 1e-9
        currentStep = 0
        rapidDataWritten = False
        
        for cellID in meshObject.cellIdxToTrack:
            #print("Writing cell data")
            WriteCellDataToFile(cell = meshObject.cellArray[cellID], time = tCurrent, \
                                flow_property_variables = cell_flow_property_variables_to_write)
        
        while tCurrent < tFinal and abs(tCurrent - tFinal) > time_tol:
            newData = Integrate(mesh = currentMeshObject, dt_flag = dt_flag, tCurrent = tCurrent)
            tCurrent += newData.dtTotal
            writtenData = False
            currentStep += 1
            rapidDataWritten = False
            currentMeshObject = newData.mesh
            
            if currentStep % rapidDataSavenSteps == 0:
                print("Writing data, t = ", tCurrent)
                for cellID in newData.mesh.cellIdxToTrack:
                    #print("Writing cell data")
                    WriteCellDataToFile(cell = newData.mesh.cellArray[cellID], time = tCurrent, \
                                        flow_property_variables = cell_flow_property_variables_to_write)
                for interfaceID in newData.mesh.interfaceIdxToTrack:
                    WriteInterfaceDataToFile(interface = newData.mesh.interfaceArray[interfaceID], \
                                            time = tCurrent - newData.dtTotal, \
                                            flow_property_variables = interface_flow_property_variables_to_write)
                rapidDataWritten = True
            
        if not rapidDataWritten:
            for cellID in newData.mesh.cellIdxToTrack:
                #print("Writing cell data")
                WriteCellDataToFile(cell = newData.mesh.cellArray[cellID], time = tCurrent, \
                                    flow_property_variables = cell_flow_property_variables_to_write)
            for interfaceID in newData.mesh.interfaceIdxToTrack:
                WriteInterfaceDataToFile(interface = newData.mesh.interfaceArray[interfaceID], \
                                            time = tCurrent - newData.dtTotal, \
                                            flow_property_variables = interface_flow_property_variables_to_write)
        