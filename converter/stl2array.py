import numpy as np
from stl import mesh

def stl2array(obj_name : str) -> np.ndarray :
    try:
        obj_mesh = mesh.Mesh.from_file("./converter/imgs/" + obj_name + ".stl")
    except:
        obj_mesh = mesh.Mesh.from_file("./converter/imgs/tomcat.stl")

    obj_x = np.array([np.array(obj_mesh.x).flatten()])
    obj_y = np.array([np.array(obj_mesh.y).flatten()])
    obj_z = np.array([np.array(obj_mesh.z).flatten()])

    x_mean = np.mean(obj_x)
    y_mean = np.mean(obj_y)
    z_mean = np.mean(obj_z)

    obj_x = obj_x - x_mean
    obj_y = obj_y - y_mean
    obj_z = obj_z - z_mean

    ones_vec = np.array([np.ones(np.size(obj_x))])
    
    obj_arr = np.vstack((obj_x,obj_y,obj_z,ones_vec))

    return obj_arr


