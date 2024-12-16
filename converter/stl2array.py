import numpy as np
from stl import mesh

def stl2array(obj_name : str) -> np.ndarray :
    obj_mesh = mesh.Mesh.from_file("./converter/imgs/" + obj_name + ".stl")
    obj_x = np.array([np.array(obj_mesh.x).flatten()])
    obj_y = np.array([np.array(obj_mesh.y).flatten()])
    obj_z = np.array([np.array(obj_mesh.z).flatten()])
    ones_vec = np.array([np.ones(np.size(obj_x))])
    
    obj_arr = np.vstack((obj_x,obj_y,obj_z,ones_vec))

    return obj_arr


