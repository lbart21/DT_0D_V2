import os

from Algorithms.DT_0D_V2.post_processing.cell_data_file_to_object import FormCellDataFromFile
from Algorithms.DT_0D_V2.post_processing.interface_data_file_to_object import FormInterfaceDataFromFile
from Algorithms.DT_0D_V2.post_processing.SI_units_dictionary import SI_UNITS
from Algorithms.DT_0D_V2.post_processing.symbols import SYMBOLS

import matplotlib.pyplot as plt

class GenerateThrustPlot():
    def __init__(self, interface_file_name) -> None:
        interface_data = FormInterfaceDataFromFile(data_file_name = interface_file_name)

        m_dot = interface_data.interface_data["mass_flux"]
        p_exit = interface_data.interface_data["p"]
        vel_x_exit = interface_data.interface_data["vel_x"]

        A_e = interface_data.interface_data["A"]

        interface_data.interface_data["Thrust"] = m_dot * vel_x_exit * A_e + p_exit * A_e

        fig = plt.figure(figsize=(15, 5))
        plt.title("Transient Thrust Profile")
        plt.ylabel("Thrust (N)", rotation = "horizontal", ha = "right")
        plt.xlabel("Time (ms)")
        plt.scatter(interface_data.interface_data["time"] * 1e3, interface_data.interface_data["Thrust"], marker = '.')
        filename = "ThrustProfile.jpg"
        plt.grid()
        mng = plt.get_current_fig_manager()
        mng.full_screen_toggle()
        currentDir = os.getcwd()
        plt.savefig(currentDir + "/plots/" + filename, bbox_inches="tight")
        plt.close()

class GenerateTransientInterfacePropertyPlots():
    def __init__(self, interface_file_name, plot_vars) -> None:
        interface_data = FormInterfaceDataFromFile(data_file_name = interface_file_name)

        for var in plot_vars:
            fig = plt.figure(figsize=(15, 5))
            if var == "mass_flux":
                interface_data.interface_data["mass_flux"] *= interface_data.interface_data["A"]
            if var == "energy_flux":
                interface_data.interface_data["energy_flux"] *= interface_data.interface_data["A"]
            plt.title("Transient Development of " + SYMBOLS[var] + " at Interface " + str(interface_data.interface_id))
            plt.ylabel(SYMBOLS[var] + " (" + SI_UNITS[var] +")", \
                        rotation = "horizontal", ha = "right")
            plt.xlabel("Time (ms)")
            plt.scatter(interface_data.interface_data["time"] * 1e3, interface_data.interface_data[var], marker = '.')
            filename = "Transient Development of " + var + " at Interface " + str(interface_data.interface_id) + ".jpg"
            plt.grid()
            mng = plt.get_current_fig_manager()
            mng.full_screen_toggle()
            currentDir = os.getcwd()
            plt.savefig(currentDir + "/plots/" + filename, bbox_inches="tight")
            plt.close()

class GenerateTransientCellPropertyPlots():
    def __init__(self, cell_file_name, plot_vars) -> None:
        cell_data = FormCellDataFromFile(data_file_name = cell_file_name)
        for var in plot_vars:
            fig = plt.figure(figsize=(15, 5))
            plt.title("Transient Development of " + SYMBOLS[var] + " at Cell " + str(cell_data.cell_id))
            plt.ylabel(SYMBOLS[var] + " (" + SI_UNITS[var] +")", \
                        rotation = "horizontal", ha = "right")
            plt.xlabel("Time (ms)")
            plt.scatter(cell_data.cell_data["time"] * 1e3, cell_data.cell_data[var], marker = '.')
            filename = "Transient Development of " + var  + " at Cell " + str(cell_data.cell_id) + ".jpg"
            plt.grid()
            mng = plt.get_current_fig_manager()
            mng.full_screen_toggle()
            currentDir = os.getcwd()
            plt.savefig(currentDir + "/plots/" + filename, bbox_inches="tight")
            plt.close()

class GenerateMultiFigureCellDataPlot():
    def __init__(self, plot_vars, cell_file_name) -> None:
        cell_data = FormCellDataFromFile(data_file_name = cell_file_name)
        nVars = len(plot_vars)
        fig, axs = plt.subplots(nrows = nVars, ncols = 1)
        fig.suptitle("Transient Development of Various Properties at Cell " + str(cell_data.cell_id))
        for ind, var in enumerate(plot_vars):
            axs[ind].scatter(cell_data.cell_data["time"] * 1e3, cell_data.cell_data[var], marker = '.')
            axs[ind].grid()
            axs[ind].set_xlabel("Time (ms)")
            axs[ind].set_ylabel(SYMBOLS[var] + " (" + SI_UNITS[var] +")", \
                                rotation = "horizontal", ha = "right")
        varNamesJoined = "".join(plot_vars)
        filename = "Multi-Figure Plot of " + varNamesJoined + " for Cell ID" + str(cell_data.cell_id) + ".jpg"
        mng = plt.get_current_fig_manager()
        mng.full_screen_toggle()
        currentDir = os.getcwd()
        plt.savefig(currentDir + "/plots/" + filename, bbox_inches="tight")
        plt.close()

class GenerateMultiFigureInterfaceDataPlot():
    def __init__(self, plot_vars, interface_file_name) -> None:
        interface_data = FormInterfaceDataFromFile(dataFileName = interface_file_name)
        nVars = len(plot_vars)
        fig, axs = plt.subplots(nrows = nVars, ncols = 1)
        fig.suptitle("Transient Development of Various Properties at Interface " + str(interface_data.interface_id))
        for ind, var in enumerate(plot_vars):
            axs[ind].scatter(interface_data.interface_data["time"] * 1e3, interface_data.interface_data[var], marker = '.')
            axs[ind].grid()
            axs[ind].set_xlabel("Time (ms)")
            axs[ind].set_ylabel(SYMBOLS[var] + " (" + SI_UNITS[var] +")", \
                                rotation = "horizontal", ha = "right")
        varNamesJoined = "".join(plot_vars)
        filename = "Multi-Figure Plot of " + varNamesJoined + " for Interface ID" + str(interface_data.interface_id) + ".jpg"
        mng = plt.get_current_fig_manager()
        mng.full_screen_toggle()
        current_dir = os.getcwd()
        plt.savefig(current_dir + "/plots/" + filename, bbox_inches="tight")
        plt.close()

class CheckConvergenceThroughFluxes():
    def __init__(self, interface1_file_name, interface2_file_name, plots_vars) -> None:
        interface1_data = FormInterfaceDataFromFile(dataFileName = interface1_file_name)
        interface2_data = FormInterfaceDataFromFile(dataFileName = interface2_file_name)
        for var in plots_vars:
            fig = plt.figure(figsize=(15, 5))
            if var == "mass_flux":
                interface1_data.interface_data["mass_flux"] *= interface1_data.interface_data["A"]
                interface2_data.interface_data["mass_flux"] *= interface2_data.interface_data["A"]
            if var == "energy_flux":
                interface1_data.interface_data["energy_flux"] *= interface1_data.interface_data["A"]
                interface2_data.interface_data["energy_flux"] *= interface2_data.interface_data["A"]
            plt.title("Comparison of Interface Values of " + SYMBOLS[var] + " at Interfaces " + str(interface1_data.interface_id) + \
                " and "+ str(interface2_data.interface_id))
            plt.ylabel(SYMBOLS[var] + " (" + SI_UNITS[var] +")", \
                        rotation = "horizontal", ha = "right")
            plt.xlabel("Time (ms)")
            plt.scatter(interface1_data.interface_data["time"] * 1e3, interface1_data.interface_data[var], marker = '.', label = "Interface " + str(interface1_data.interface_id))
            plt.scatter(interface2_data.interface_data["time"] * 1e3, interface2_data.interface_data[var], marker = '.', label = "Interface " + str(interface2_data.interface_id))
            filename = "Comparison of Interface Values of " + var + " at Interfaces " + str(interface1_data.interface_id) + \
                " and "+ str(interface2_data.interface_id) + ".jpg"
            plt.grid()
            plt.legend()
            mng = plt.get_current_fig_manager()
            mng.full_screen_toggle()
            current_dir = os.getcwd()
            plt.savefig(current_dir + "/plots/" + filename, bbox_inches="tight")
            plt.close()

            fig = plt.figure(figsize=(15, 5))
            plt.title("Difference in Interface Values of " + SYMBOLS[var] + " at Interfaces " + str(interface1_data.interface_id) + \
                " and "+ str(interface2_data.interface_id))
            plt.ylabel(SYMBOLS[var] + " (" + SI_UNITS[var] +")", \
                        rotation = "horizontal", ha = "right")
            plt.xlabel("Time (ms)")
            plt.scatter(interface1_data.interface_data["time"] * 1e3, abs(interface1_data.interface_data[var] - interface2_data.interface_data[var]), marker = '.')
            filename = "Difference in Interface Values of " + var + " at Interfaces " + str(interface1_data.interface_id) + \
                " and "+ str(interface2_data.interface_id) + ".jpg"
            plt.grid()
            plt.savefig(current_dir + "/plots/" + filename, bbox_inches="tight")
            plt.close()