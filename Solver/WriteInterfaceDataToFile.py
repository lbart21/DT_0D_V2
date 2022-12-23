import os
def WriteInterfaceDataToFile(interface, time, flow_property_variables):
    cwd = os.getcwd()
    interface_ID = interface.interface_ID
    filename = "DataAtInterfaceID" + str(interface_ID) + ".txt"
    if not os.path.exists(cwd + "/data/" + filename):
        with open(cwd + "/data/" + filename, "w") as file:
            interfaceData = {}
            if "A" in flow_property_variables:
                interfaceData["A"] = interface.GEO["A"]
            if "mass_flux" in flow_property_variables:
                interfaceData["mass_flux"] = interface.interfaceFluxes["mass"]
            if "energy_flux" in flow_property_variables:
                interfaceData["energy_flux"] = interface.interfaceFluxes["energy"]
            if "p" in flow_property_variables:
                interfaceData["p"] = interface.interfaceState.fluid_state.p
            if "Ma" in flow_property_variables:
                interfaceData["Ma"] = interface.interfaceState.Ma
            if "vel_x" in flow_property_variables:
                interfaceData["vel_x"] = interface.interfaceState.vel_x
            if "p_t" in flow_property_variables:
                p = interface.interfaceState.fluid_state.p
                gamma = interface.interfaceState.fluid_state.gamma
                Ma = interface.interfaceState.Ma
                interfaceData["p_t"] = p * (1.0 + 0.5 * (gamma - 1.0) * Ma ** 2.0) ** (gamma / (gamma - 1.0))
            if "T_t" in flow_property_variables:
                T = interface.interfaceState.fluid_state.T
                gamma = interface.interfaceState.fluid_state.gamma
                Ma = interface.interfaceState.Ma
                interfaceData["T_t"] = T * (1.0 + 0.5 * (gamma - 1.0) * Ma ** 2.0)
            
            variableNames = list(interfaceData.keys()) #Does not include time
            file.write("ID: " + str(interface_ID) + "\n")
            file.write("Variables: " + str(len(variableNames) + 1) + "\n")
            file.write("time " + " ".join(variableNames) + "\n")
            file.write(str(format(time, ".9f")) + " ")
            for name in variableNames:
                file.write(str(format(interfaceData[name], ".9f")) + " ")
            file.write("\n")
            #file.write(str(format(time, ".9f")) + " " + str(format(interface.GEO["A"], ".9f")) + "\n")
            
    else:
        with open(cwd + "/data/" + filename, "a") as file:
            interfaceData = {}
            if "A" in flow_property_variables:
                interfaceData["A"] = interface.GEO["A"]
            if "mass_flux" in flow_property_variables:
                interfaceData["mass_flux"] = interface.interfaceFluxes["mass"]
            if "energy_flux" in flow_property_variables:
                interfaceData["energy_flux"] = interface.interfaceFluxes["energy"]
            if "p" in flow_property_variables:
                interfaceData["p"] = interface.interfaceState.fluid_state.p
            if "Ma" in flow_property_variables:
                interfaceData["Ma"] = interface.interfaceState.Ma
            if "vel_x" in flow_property_variables:
                interfaceData["vel_x"] = interface.interfaceState.vel_x
            if "p_t" in flow_property_variables:
                p = interface.interfaceState.fluid_state.p
                gamma = interface.interfaceState.fluid_state.gamma
                Ma = interface.interfaceState.Ma
                interfaceData["p_t"] = p * (1.0 + 0.5 * (gamma - 1.0) * Ma ** 2.0) ** (gamma / (gamma - 1.0))
            if "T_t" in flow_property_variables:
                T = interface.interfaceState.fluid_state.T
                gamma = interface.interfaceState.fluid_state.gamma
                Ma = interface.interfaceState.Ma
                interfaceData["T_t"] = T * (1.0 + 0.5 * (gamma - 1.0) * Ma ** 2.0)
                
            variableNames = list(interfaceData.keys()) #Does not include time

            file.write(str(format(time, ".9f")) + " ")
            for name in variableNames:
                file.write(str(format(interfaceData[name], ".9f")) + " ")
            file.write("\n")
            #file.write(str(format(time, ".9f")) + " " + str(format(interface.GEO["A"], ".9f")) + "\n")
    file.close()