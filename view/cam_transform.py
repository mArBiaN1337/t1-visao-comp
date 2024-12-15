from dataclasses import dataclass
from matrices.transform import Transform
import numpy as np

@dataclass
class CamTransform(Transform):

    def build_cam(self, curr_cam : np.ndarray) -> np.ndarray:
        shift_matrix = self.translate([self.x_shift_value,self.y_shift_value,self.z_shift_value])

        x_rot_matrix = self.rot_x(self.x_rot_value)
        y_rot_matrix = self.rot_y(self.y_rot_value)
        z_rot_matrix = self.rot_z(self.z_rot_value)

        default_cam = np.eye(4)

        rotation_matrix = z_rot_matrix @ y_rot_matrix @ x_rot_matrix
        operation  = shift_matrix @ rotation_matrix

        cam = curr_cam @ operation @ default_cam

        return cam