from Algorithms.DT_0D_V2.solver.write_cell_data_to_file import write_cell_data_to_file
from Algorithms.DT_0D_V2.solver.write_interface_data_to_file import write_interface_data_to_file
from Algorithms.DT_0D_V2.integrate.integrate import Integrate

class Solver():
    def __init__(self, mesh_object, dt_flag, t_final, data_save_dt, cell_flow_property_variables_to_write, \
                        interface_flow_property_variables_to_write, rapid_data_save_n_steps) -> None:
        t_current = 0.0
        current_mesh_object = mesh_object
        time_tol = 1e-9
        current_step = 0
        rapid_data_written = False
        
        for cell_id in mesh_object.cell_idx_to_track:
            #print("Writing cell data")
            write_cell_data_to_file(cell = mesh_object.cell_array[cell_id], time = t_current, \
                                flow_property_variables = cell_flow_property_variables_to_write)
        
        while t_current < t_final and abs(t_current - t_final) > time_tol:
            new_data = Integrate(mesh = current_mesh_object, dt_flag = dt_flag, t_current = t_current)
            t_current += new_data.dt_total
            written_data = False
            current_step += 1
            rapid_data_written = False
            current_mesh_object = new_data.mesh
            
            if current_step % rapid_data_save_n_steps == 0:
                print("Writing data, t = ", t_current)
                for cell_id in new_data.mesh.cell_idx_to_track:
                    #print("Writing cell data")
                    write_cell_data_to_file(cell = new_data.mesh.cellArray[cell_id], time = t_current, \
                                        flow_property_variables = cell_flow_property_variables_to_write)
                for interface_id in new_data.mesh.interface_idx_to_track:
                    write_interface_data_to_file(interface = new_data.mesh.interface_array[interface_id], \
                                            time = t_current - new_data.dtTotal, \
                                            flow_property_variables = interface_flow_property_variables_to_write)
                rapid_data_written = True
            
        if not rapid_data_written:
            for cell_id in new_data.mesh.cell_idx_to_track:
                #print("Writing cell data")
                write_cell_data_to_file(cell = new_data.mesh.cell_array[cell_id], time = t_current, \
                                    flow_property_variables = cell_flow_property_variables_to_write)
            for interface_id in new_data.mesh.interface_idx_to_track:
                write_interface_data_to_file(interface = new_data.mesh.interface_array[interface_id], \
                                            time = t_current - new_data.dt_total, \
                                            flow_property_variables = interface_flow_property_variables_to_write)
        