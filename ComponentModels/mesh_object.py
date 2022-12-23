"""
File for MeshObject class
"""
# pylint: disable=too-many-instance-attributes, too-few-public-methods
class MeshObject():
    """
    Empty mesh object class that contains the essential attributes for time stepping.
    Applies number of cells to pre-size.
    """
    def __init__(self, n_cells):
        self.cell_array = [None] * n_cells
        self.interface_array = [None] * (n_cells + 1)
        self.map_cell_id_to_west_interface_idx = [None] * n_cells
        self.map_cell_id_to_east_interface_idx = [None] * n_cells
        self.map_interface_id_to_west_cell_idx = [None] * (n_cells + 1)
        self.map_interface_id_to_east_cell_idx = [None] * (n_cells + 1)
        self.component_labels = []
        self.cell_idx_to_track = []
        self.interface_idx_to_track = []
