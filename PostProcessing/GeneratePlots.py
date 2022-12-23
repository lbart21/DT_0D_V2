from Algorithms.DesignToolAlgorithmV1_0D.PostProcessing.CellDataFileToObject import FormCellDataFromFile
from Algorithms.DesignToolAlgorithmV1_0D.PostProcessing.InterfaceDataFileToObject import FormInterfaceDataFromFile
from Algorithms.DesignToolAlgorithmV1_0D.PostProcessing.SIUnitsDictionary import SIUnits
from Algorithms.DesignToolAlgorithmV1_0D.PostProcessing.Symbols import symbols

import matplotlib.pyplot as plt

import os

class GenerateThrustPlot():
    def __init__(self, interfaceFileName) -> None:
        interfaceData = FormInterfaceDataFromFile(dataFileName = interfaceFileName)

        m_dot = interfaceData.interfaceData["mass_flux"]
        p_exit = interfaceData.interfaceData["p"]
        vel_x_exit = interfaceData.interfaceData["vel_x"]

        A_e = interfaceData.interfaceData["A"]

        interfaceData.interfaceData["Thrust"] = m_dot * vel_x_exit * A_e + p_exit * A_e

        fig = plt.figure(figsize=(15, 5))
        plt.title("Transient Thrust Profile")
        plt.ylabel("Thrust (N)", rotation = "horizontal", ha = "right")
        plt.xlabel("Time (ms)")
        plt.scatter(interfaceData.interfaceData["time"] * 1e3, interfaceData.interfaceData["Thrust"], marker = '.')
        filename = "ThrustProfile.jpg"
        plt.grid()
        mng = plt.get_current_fig_manager()
        mng.full_screen_toggle()
        currentDir = os.getcwd()
        plt.savefig(currentDir + "/plots/" + filename, bbox_inches="tight")
        plt.close()
        pass

class GenerateTransientInterfacePropertyPlots():
    def __init__(self, interfaceFileName, plotVars) -> None:
        interfaceData = FormInterfaceDataFromFile(dataFileName = interfaceFileName)

        for var in plotVars:
            fig = plt.figure(figsize=(15, 5))
            if var == "mass_flux":
                interfaceData.interfaceData["mass_flux"] *= interfaceData.interfaceData["A"]
            if var == "energy_flux":
                interfaceData.interfaceData["energy_flux"] *= interfaceData.interfaceData["A"]
            plt.title("Transient Development of " + symbols[var] + " at Interface " + str(interfaceData.interface_ID))
            plt.ylabel(symbols[var] + " (" + SIUnits[var] +")", \
                        rotation = "horizontal", ha = "right")
            plt.xlabel("Time (ms)")
            plt.scatter(interfaceData.interfaceData["time"] * 1e3, interfaceData.interfaceData[var], marker = '.')
            filename = "Transient Development of " + var + " at Interface " + str(interfaceData.interface_ID) + ".jpg"
            plt.grid()
            mng = plt.get_current_fig_manager()
            mng.full_screen_toggle()
            currentDir = os.getcwd()
            plt.savefig(currentDir + "/plots/" + filename, bbox_inches="tight")
            plt.close()
        pass

class GenerateTransientCellPropertyPlots():
    def __init__(self, cellFileName, plotVars) -> None:
        cellData = FormCellDataFromFile(dataFileName = cellFileName)

        for var in plotVars:
            fig = plt.figure(figsize=(15, 5))
            plt.title("Transient Development of " + symbols[var] + " at Cell " + str(cellData.cell_ID))
            plt.ylabel(symbols[var] + " (" + SIUnits[var] +")", \
                        rotation = "horizontal", ha = "right")
            plt.xlabel("Time (ms)")
            plt.scatter(cellData.cellData["time"] * 1e3, cellData.cellData[var], marker = '.')
            filename = "Transient Development of " + var  + " at Cell " + str(cellData.cell_ID) + ".jpg"
            plt.grid()
            mng = plt.get_current_fig_manager()
            mng.full_screen_toggle()
            currentDir = os.getcwd()
            plt.savefig(currentDir + "/plots/" + filename, bbox_inches="tight")
            plt.close()
        pass

class GenerateMultiFigureCellDataPlot():
    def __init__(self, plotVars, cellFileName) -> None:
        cellData = FormCellDataFromFile(dataFileName = cellFileName)
        nVars = len(plotVars)
        fig, axs = plt.subplots(nrows = nVars, ncols = 1)
        fig.suptitle("Transient Development of Various Properties at Cell " + str(cellData.cell_ID))
        for ind, var in enumerate(plotVars):
            axs[ind].scatter(cellData.cellData["time"] * 1e3, cellData.cellData[var], marker = '.')
            axs[ind].grid()
            axs[ind].set_xlabel("Time (ms)")
            axs[ind].set_ylabel(symbols[var] + " (" + SIUnits[var] +")", \
                                rotation = "horizontal", ha = "right")
        varNamesJoined = "".join(plotVars)
        filename = "Multi-Figure Plot of " + varNamesJoined + " for Cell ID" + str(cellData.cell_ID) + ".jpg"
        mng = plt.get_current_fig_manager()
        mng.full_screen_toggle()
        currentDir = os.getcwd()
        plt.savefig(currentDir + "/plots/" + filename, bbox_inches="tight")
        plt.close()

class GenerateMultiFigureInterfaceDataPlot():
    def __init__(self, plotVars, interfaceFileName) -> None:
        interfaceData = FormInterfaceDataFromFile(dataFileName = interfaceFileName)
        nVars = len(plotVars)
        fig, axs = plt.subplots(nrows = nVars, ncols = 1)
        fig.suptitle("Transient Development of Various Properties at Interface " + str(interfaceData.interface_ID))
        for ind, var in enumerate(plotVars):
            axs[ind].scatter(interfaceData.interfaceData["time"] * 1e3, interfaceData.interfaceData[var], marker = '.')
            axs[ind].grid()
            axs[ind].set_xlabel("Time (ms)")
            axs[ind].set_ylabel(symbols[var] + " (" + SIUnits[var] +")", \
                                rotation = "horizontal", ha = "right")
        varNamesJoined = "".join(plotVars)
        filename = "Multi-Figure Plot of " + varNamesJoined + " for Interface ID" + str(interfaceData.interface_ID) + ".jpg"
        mng = plt.get_current_fig_manager()
        mng.full_screen_toggle()
        currentDir = os.getcwd()
        plt.savefig(currentDir + "/plots/" + filename, bbox_inches="tight")
        plt.close()
        pass

class CheckConvergenceThroughFluxes():
    def __init__(self, interface1FileName, interface2FileName, plotsVars) -> None:
        interface1Data = FormInterfaceDataFromFile(dataFileName = interface1FileName)
        interface2Data = FormInterfaceDataFromFile(dataFileName = interface2FileName)
        for var in plotsVars:
            fig = plt.figure(figsize=(15, 5))
            if var == "mass_flux":
                interface1Data.interfaceData["mass_flux"] *= interface1Data.interfaceData["A"]
                interface2Data.interfaceData["mass_flux"] *= interface2Data.interfaceData["A"]
            if var == "energy_flux":
                interface1Data.interfaceData["energy_flux"] *= interface1Data.interfaceData["A"]
                interface2Data.interfaceData["energy_flux"] *= interface2Data.interfaceData["A"]
            plt.title("Comparison of Interface Values of " + symbols[var] + " at Interfaces " + str(interface1Data.interface_ID) + \
                " and "+ str(interface2Data.interface_ID))
            plt.ylabel(symbols[var] + " (" + SIUnits[var] +")", \
                        rotation = "horizontal", ha = "right")
            plt.xlabel("Time (ms)")
            plt.scatter(interface1Data.interfaceData["time"] * 1e3, interface1Data.interfaceData[var], marker = '.', label = "Interface " + str(interface1Data.interface_ID))
            plt.scatter(interface2Data.interfaceData["time"] * 1e3, interface2Data.interfaceData[var], marker = '.', label = "Interface " + str(interface2Data.interface_ID))
            filename = "Comparison of Interface Values of " + var + " at Interfaces " + str(interface1Data.interface_ID) + \
                " and "+ str(interface2Data.interface_ID) + ".jpg"
            plt.grid()
            plt.legend()
            mng = plt.get_current_fig_manager()
            mng.full_screen_toggle()
            currentDir = os.getcwd()
            plt.savefig(currentDir + "/plots/" + filename, bbox_inches="tight")
            plt.close()

            fig = plt.figure(figsize=(15, 5))
            plt.title("Difference in Interface Values of " + symbols[var] + " at Interfaces " + str(interface1Data.interface_ID) + \
                " and "+ str(interface2Data.interface_ID))
            plt.ylabel(symbols[var] + " (" + SIUnits[var] +")", \
                        rotation = "horizontal", ha = "right")
            plt.xlabel("Time (ms)")
            plt.scatter(interface1Data.interfaceData["time"] * 1e3, abs(interface1Data.interfaceData[var] - interface2Data.interfaceData[var]), marker = '.')
            filename = "Difference in Interface Values of " + var + " at Interfaces " + str(interface1Data.interface_ID) + \
                " and "+ str(interface2Data.interface_ID) + ".jpg"
            plt.grid()
            plt.savefig(currentDir + "/plots/" + filename, bbox_inches="tight")
            plt.close()