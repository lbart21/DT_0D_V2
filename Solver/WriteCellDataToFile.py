import os
def WriteCellDataToFile(cell, time, flow_property_variables):
    cwd = os.getcwd()
    cell_ID = cell.cell_ID
    filename = "DataAtCellID" + str(cell_ID) + ".txt"
    if not os.path.exists(cwd + "/data/" + filename):
        with open(cwd + "/data/" + filename, "w") as file:
            cellFlowData = {}
            if "vel_x" in flow_property_variables:
                cellFlowData["vel_x"] = cell.fs.vel_x
            if "p" in flow_property_variables:
                cellFlowData["p"] = cell.fs.fluid_state.p
            if "rho" in flow_property_variables:
                cellFlowData["rho"] = cell.fs.fluid_state.rho
            if "T" in flow_property_variables:
                cellFlowData["T"] = cell.fs.fluid_state.T
            if "u" in flow_property_variables:
                cellFlowData["u"] = cell.fs.fluid_state.u
            if "h" in flow_property_variables:
                cellFlowData["h"] = cell.fs.fluid_state.enthalpy
            if "A_c" in flow_property_variables:
                cellFlowData["A_c"] = cell.GEO["A_c"]

            #cellFlowData = {var : getattr(cell.fs.fluid_state, var) for var in flow_property_variables if var != "vel_x"}
            #if "vel_x" in flow_property_variables:
                #cellFlowData["vel_x"] = getattr(cell.fs, "vel_x")

            variableNames = list(cellFlowData.keys()) #Does not include time
            file.write("ID: " + str(cell_ID) + "\n")
            file.write("Variables: " + str(len(variableNames) + 1) + "\n")
            file.write("time " + " ".join(variableNames) + "\n")
            file.write(str(format(time, ".9f")) + " ")
            for name in variableNames:
                file.write(str(format(cellFlowData[name], ".9f")) + " ")
            file.write("\n")
    else:
        with open(cwd + "/data/" + filename, "a") as file:
            cellFlowData = {}
            if "vel_x" in flow_property_variables:
                cellFlowData["vel_x"] = cell.fs.vel_x
            if "p" in flow_property_variables:
                cellFlowData["p"] = cell.fs.fluid_state.p
            if "rho" in flow_property_variables:
                cellFlowData["rho"] = cell.fs.fluid_state.rho
            if "T" in flow_property_variables:
                cellFlowData["T"] = cell.fs.fluid_state.T
            if "u" in flow_property_variables:
                cellFlowData["u"] = cell.fs.fluid_state.u
            if "h" in flow_property_variables:
                cellFlowData["h"] = cell.fs.fluid_state.enthalpy
            if "A_c" in flow_property_variables:
                cellFlowData["A_c"] = cell.GEO["A_c"]

            variableNames = list(cellFlowData.keys()) #Does not include time
            file.write(str(format(time, ".9f")) + " ")
            for name in variableNames:
                file.write(str(format(cellFlowData[name], ".9f")) + " ")
            file.write("\n")
    file.close()