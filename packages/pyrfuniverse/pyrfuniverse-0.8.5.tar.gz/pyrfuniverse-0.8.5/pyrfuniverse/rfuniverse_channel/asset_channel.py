import warnings

import numpy as np

from pyrfuniverse.side_channel.side_channel import (
    IncomingMessage,
    OutgoingMessage,
)
from pyrfuniverse.rfuniverse_channel import RFUniverseChannel
import pyrfuniverse.utils.rfuniverse_utility as utility

class AssetChannel(RFUniverseChannel):

    def __init__(self, env, channel_id: str) -> None:
        super().__init__(channel_id)
        self.env = env
        self.data = {}
        self.messages = {}

    def _parse_message(self, msg: IncomingMessage):
        msg_type = msg.read_string()
        if msg_type in self.messages:
            for i in self.messages[msg_type]:
                i(msg)
        elif msg_type == 'LoadDone':
            self.data['load_done'] = True
        elif msg_type == 'PendDone':
            self.data['pend_done'] = True
        elif msg_type == 'RFMoveColliders':
            collider = []
            object_count = msg.read_int32()
            for i in range(object_count):
                one = {}
                object_id = msg.read_int32()
                one['object_id'] = object_id
                collider_count = msg.read_int32()
                one['collider'] = []
                for j in range(collider_count):
                    collider_data = {}
                    collider_data['type'] = msg.read_string()
                    collider_data['position'] = []
                    collider_data['position'].append(msg.read_float32())
                    collider_data['position'].append(msg.read_float32())
                    collider_data['position'].append(msg.read_float32())
                    if collider_data['type'] == 'box':
                        collider_data['rotation'] = []
                        collider_data['rotation'].append(msg.read_float32())
                        collider_data['rotation'].append(msg.read_float32())
                        collider_data['rotation'].append(msg.read_float32())
                        collider_data['rotation'].append(msg.read_float32())
                        collider_data['size'] = []
                        collider_data['size'].append(msg.read_float32())
                        collider_data['size'].append(msg.read_float32())
                        collider_data['size'].append(msg.read_float32())
                    elif collider_data['type'] == 'sphere':
                        collider_data['radius'] = msg.read_float32()
                    elif collider_data['type'] == 'capsule':
                        collider_data['rotation'] = []
                        collider_data['rotation'].append(msg.read_float32())
                        collider_data['rotation'].append(msg.read_float32())
                        collider_data['rotation'].append(msg.read_float32())
                        collider_data['rotation'].append(msg.read_float32())
                        collider_data['direction'] = msg.read_int32()
                        collider_data['radius'] = msg.read_float32()
                        collider_data['height'] = msg.read_float32()
                    one['collider'].append(collider_data)
                collider.append(one)
            self.data['colliders'] = collider
        elif msg_type == 'CurrentCollisionPairs':
            collision_pairs = []
            pair_count = msg.read_int32()
            for i in range(pair_count):
                data = [msg.read_int32(), msg.read_int32()]
                collision_pairs.append(data)
            self.data['collision_pairs'] = collision_pairs
        else:
            ext_data = self.env.ext.parse_message(msg, msg_type)
            self.data.update(ext_data)
        self.env.data.update(self.data)

    def set_action(self, action: str, **kwargs) -> None:
        warnings.warn("set_action is deprecated, It will be removed in version 1.0", DeprecationWarning)
        """Set action and pass corresponding parameters
        Args:
            action: The action name.
            kwargs: keyword argument for action. The parameter list for each action is shown in each function.
        """
        try:
            if hasattr(self, action):
                eval('self.' + action)(kwargs)
            else:
                msg = eval('ext.' + action)(kwargs)
                self.send_message(msg)
        except AttributeError:
            print('There is no action called \'%s\' or this function has bug, please fix it.' % action)
            exit(-1)

    def PreLoadAssetsAsync(self, names: list) -> None:
        msg = OutgoingMessage()
        msg.write_string('PreLoadAssetsAsync')

        count = len(names)
        msg.write_int32(count)
        for i in range(count):
            msg.write_string(names[i])

        self.send_message(msg)

    def LoadSceneAsync(self, file: str) -> None:
        msg = OutgoingMessage()

        msg.write_string('LoadSceneAsync')
        msg.write_string(file)

        self.send_message(msg)

    def SendMessage(self, message: str, *args) -> None:
        msg = OutgoingMessage()

        msg.write_string('SendMessage')
        msg.write_string(message)
        for i in args:
            if type(i) == str:
                msg.write_string(i)
            elif type(i) == bool:
                msg.write_bool(i)
            elif type(i) == int:
                msg.write_int32(i)
            elif type(i) == float or type(i) == np.float32 or type(i) == np.float64:
                msg.write_float32(float(i))
            elif type(i) == list and type(i[0]) == float:
                msg.write_float32_list(i)
            else:
                print(f'dont support this data type:{type(i)}')

        self.send_message(msg)

    def AddListener(self, message: str, fun):
        if message in self.messages:
            if fun in self.messages[message]:
                self.messages[message].append(fun)
        else:
            self.messages[message] = [fun]

    def RemoveListener(self, message: str, fun):
        if message in self.messages:
            if fun in self.messages[message]:
                self.messages[message].remove(fun)
            if len(self.messages[message]) == 0:
                self.messages[message].pop(message)


    def InstanceObject(self, kwargs: dict) -> None:
        compulsory_params = ['name', 'id']
        optional_params = []
        utility.CheckKwargs(kwargs, compulsory_params)
        msg = OutgoingMessage()
        msg.write_string('InstanceObject')
        msg.write_string(kwargs['name'])
        msg.write_int32(kwargs['id'])
        self.send_message(msg)

    def LoadURDF(self, kwargs: dict) -> None:
        compulsory_params = ['id', 'path', 'native_ik']
        optional_params = []
        utility.CheckKwargs(kwargs, compulsory_params)
        msg = OutgoingMessage()
        msg.write_string('LoadURDF')
        msg.write_int32(kwargs['id'])
        msg.write_string(kwargs['path'])
        msg.write_bool(kwargs['native_ik'])
        self.send_message(msg)

    def LoadMesh(self, kwargs: dict) -> None:
        compulsory_params = ['id', 'path']
        optional_params = []
        utility.CheckKwargs(kwargs, compulsory_params)
        msg = OutgoingMessage()
        msg.write_string('LoadMesh')
        msg.write_int32(kwargs['id'])
        msg.write_string(kwargs['path'])
        self.send_message(msg)

    def IgnoreLayerCollision(self, kwargs: dict) -> None:
        compulsory_params = ['layer1', 'layer2', 'ignore']
        optional_params = []
        utility.CheckKwargs(kwargs, compulsory_params)
        msg = OutgoingMessage()
        msg.write_string('IgnoreLayerCollision')
        msg.write_int32(kwargs['layer1'])
        msg.write_int32(kwargs['layer2'])
        msg.write_bool(kwargs['ignore'])
        self.send_message(msg)

    def GetCurrentCollisionPairs(self, kwargs: dict) -> None:
        msg = OutgoingMessage()
        msg.write_string('GetCurrentCollisionPairs')
        self.send_message(msg)

    def GetRFMoveColliders(self, kwargs: dict) -> None:
        msg = OutgoingMessage()
        msg.write_string('GetRFMoveColliders')
        self.send_message(msg)

    def SetGravity(self, kwargs: dict) -> None:
        compulsory_params = ['x', 'y', 'z']
        optional_params = []
        utility.CheckKwargs(kwargs, compulsory_params)
        msg = OutgoingMessage()
        msg.write_string('SetGravity')
        msg.write_float32(kwargs['x'])
        msg.write_float32(kwargs['y'])
        msg.write_float32(kwargs['z'])
        self.send_message(msg)

    def SetGroundPhysicMaterial(self, kwargs: dict) -> None:
        compulsory_params = ['bounciness', 'dynamic_friction', 'static_friction', 'friction_combine', 'bounce_combine']
        optional_params = []
        utility.CheckKwargs(kwargs, compulsory_params)
        msg = OutgoingMessage()
        msg.write_string('SetGroundPhysicMaterial')
        msg.write_float32(kwargs['bounciness'])
        msg.write_float32(kwargs['dynamic_friction'])
        msg.write_float32(kwargs['static_friction'])
        msg.write_int32(kwargs['friction_combine'])
        msg.write_int32(kwargs['bounce_combine'])
        self.send_message(msg)

    def SetTimeStep(self, kwargs: dict) -> None:
        compulsory_params = ['delta_time']
        optional_params = []
        utility.CheckKwargs(kwargs, compulsory_params)
        msg = OutgoingMessage()
        msg.write_string('SetTimeStep')
        msg.write_float32(kwargs['delta_time'])
        self.send_message(msg)

    def SetTimeScale(self, kwargs: dict) -> None:
        compulsory_params = ['time_scale']
        optional_params = []
        utility.CheckKwargs(kwargs, compulsory_params)
        msg = OutgoingMessage()
        msg.write_string('SetTimeScale')
        msg.write_float32(kwargs['time_scale'])
        self.send_message(msg)

    def SetResolution(self, kwargs: dict) -> None:
        compulsory_params = ['resolution_x', 'resolution_y']
        optional_params = []
        utility.CheckKwargs(kwargs, compulsory_params)
        msg = OutgoingMessage()
        msg.write_string('SetResolution')
        msg.write_int32(kwargs['resolution_x'])
        msg.write_int32(kwargs['resolution_y'])
        self.send_message(msg)
