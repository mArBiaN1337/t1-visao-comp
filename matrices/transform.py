import numpy as np
import collections.abc as c


def translate(ref_point : c.Iterable) -> np.ndarray:

    if np.size(ref_point) != 3:
        raise ValueError("Expected a 3 element Point")

    matrix = matrix = [[1,0,0,ref_point[0]],
                        [0,1,0,ref_point[1]],
                        [0,0,1,ref_point[2]],
                        [0,0,0,1]]
    
    matrix = np.array(matrix)

    return matrix

def vec_norm(vec:c.Iterable):
    return np.sqrt(np.sum(np.array(vec)**2))

def rot_u(u : c.Iterable, ang : float, unit = 'deg') -> np.ndarray:
    if unit == 'deg':
        ang = np.deg2rad(ang)

    if np.size(u) != 3:
        raise ValueError("Expected a 3 element Vector")
    
    if vec_norm(u) != 1.0:
        u = u / vec_norm(u)
    
    cos = np.cos(ang)
    sin = np.sin(ang)

    ux = u[0]
    uy = u[1]
    uz = u[2]

    matrix =    [[(ux**2)*(1-cos)+cos,ux*uy*(1-cos)-uz*sin,ux*uz*(1-cos)+uy*sin,0],
                [(ux*uy)*(1-cos)+uz*sin,(uy**2)*(1-cos)+cos,uy*uz*(1-cos)-ux*sin,0],
                [(ux*uz)*(1-cos)-uy*sin,(uy*uz)*(1-cos)+ux*sin,(uz**2)*(1-cos)+cos,0],
                [0,0,0,1]]
    
    matrix = np.array(matrix)

    return matrix

def rot_x(ang : float, unit = 'deg') -> np.ndarray:
    rot_u([1,0,0],ang,unit)

def rot_y(ang : float, unit = 'deg') -> np.ndarray:
    rot_u([0,1,0],ang,unit)

def rot_z(ang : float, unit = 'deg') -> np.ndarray:
    rot_u([0,0,1],ang,unit)

def inv_transf(matrix : c.Iterable) -> np.ndarray:
    return np.linalg.inv(np.array(matrix))


"""
    ex: [T1, T2, T3, T4]
    return T4 @ T3 @ T2 @ T1
"""
def accum_transf(transf_list : c.Iterable) -> np.ndarray:
    result = np.eye(4)

    for transf in transf_list:
        acc = transf @ result

    acc = np.array(acc)

    return acc

    

