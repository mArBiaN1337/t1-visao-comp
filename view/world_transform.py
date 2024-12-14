from dataclasses import dataclass
import numpy as np 

@dataclass
class WorldTransform:
    x_shift : int | float
    x_rot   : int | float
    y_shift : int | float
    y_rot   : int | float
    z_shift : int | float
    z_rot   : int | float

    order : list[str] = ['']
    transf_matrix : np.ndarray