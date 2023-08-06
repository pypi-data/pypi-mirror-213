import base64
import cv2
import numpy as np
import pyrfuniverse.attributes as attr
import pyrfuniverse.utils.active_depth_generate as active_depth
from pyrfuniverse.side_channel.side_channel import (
    IncomingMessage,
    OutgoingMessage,
)


class ActiveLightSensorAttr(attr.CameraAttr):
    """
    Class of IR-based depth sensor, which can simulate the noise of 
    real-world depth camera and produce depth image in similar pattern.
    """
    def __init__(self, env, id: int, data=None):
        super().__init__(env, id, data)
        self.main_intrinsic_matrix = np.eye(4)
        self.ir_intrinsic_matrix = np.eye(4)

    def parse_message(self, msg: IncomingMessage) -> dict:
        """
        Parse messages. This function is called by internal function.

        Returns:
            Dict: A dict containing useful information of this class.\n
            self.data['active_depth']: IR-based depth, shape = (w,h)
        """
        super().parse_message(msg)
        if msg.read_bool() is True:
            self.data['ir_left'] = base64.b64decode(msg.read_string())
            self.data['ir_right'] = base64.b64decode(msg.read_string())

            image_left = np.frombuffer(self.data['ir_left'], dtype=np.uint8)
            image_left = cv2.imdecode(image_left, cv2.IMREAD_COLOR)[..., 2]
            image_right = np.frombuffer(self.data['ir_right'], dtype=np.uint8)
            image_right = cv2.imdecode(image_right, cv2.IMREAD_COLOR)[..., 2]
            left_extrinsic_matrix = np.array(
                [[0., -1., 0., -0.0175], [0., 0., -1., 0.], [1., 0., 0., 0.], [0., 0., 0., 1.]])
            right_extrinsic_matrix = np.array(
                [[0., -1., 0., -0.072], [0., 0., -1., 0.], [1., 0., 0., 0.], [0., 0., 0., 1.]])
            main_extrinsic_matrix = np.array([[0., -1., 0., 0.], [0., 0., -1., 0.], [1., 0., 0., 0.], [0., 0., 0., 1.]])
            self.data['active_depth'] = active_depth.calc_main_depth_from_left_right_ir(image_left, image_right,
                                                                                        left_extrinsic_matrix,
                                                                                        right_extrinsic_matrix,
                                                                                        main_extrinsic_matrix,
                                                                                        self.ir_intrinsic_matrix,
                                                                                        self.ir_intrinsic_matrix,
                                                                                        self.main_intrinsic_matrix,
                                                                                        lr_consistency=False,
                                                                                        main_cam_size=(
                                                                                            self.main_intrinsic_matrix[
                                                                                                0, 2] * 2,
                                                                                            self.main_intrinsic_matrix[
                                                                                                1, 2] * 2),
                                                                                        ndisp=128,
                                                                                        use_census=True,
                                                                                        register_depth=True,
                                                                                        census_wsize=7,
                                                                                        use_noise=False)
            self.data['active_depth'][self.data['active_depth'] > 8.] = 0
            self.data['active_depth'][self.data['active_depth'] < 0.1] = 0
        return self.data

    def GetActiveDepth(self, main_intrinsic_matrix_local: list, ir_intrinsic_matrix_local: list):
        """
        Get IR-based depth image.

        Args:
            main_intrinsic_matrix_local: List[float] The intrinsic matrix of main camera.
            ir_intrinsic_matrix_local: List[float] The intrinsic matrix of IR-based camera.
        """
        msg = OutgoingMessage()

        msg.write_int32(self.id)
        msg.write_string('GetActiveDepth')
        self.main_intrinsic_matrix = np.reshape(main_intrinsic_matrix_local, [3, 3]).T
        self.ir_intrinsic_matrix = np.reshape(ir_intrinsic_matrix_local, [3, 3]).T
        msg.write_float32_list(self.ir_intrinsic_matrix.T.reshape([-1]).tolist())

        self.env.instance_channel.send_message(msg)
