from pyrfuniverse.envs.base_env import RFUniverseBaseEnv
import pyrfuniverse.attributes as attr
from pyrfuniverse.side_channel.side_channel import (
    IncomingMessage,
    OutgoingMessage,
)

env = RFUniverseBaseEnv(
    assets=['CustomAttr']
)

# asset_channel custom message
env.ext.CustomMessage(message='this is asset channel custom message')
env.step()
print(env.data['custom_message'])

# instance_channel custom message
custom = env.InstanceObject(name='CustomAttr', id=123456, attr_type=attr.CustomAttr)
custom.CustomMessage(message='this is instance channel custom message')
env.step()
print(custom.data['custom_message'])

# dynamic message
def dynamic_function(msg: IncomingMessage):
    print(msg.read_string())
    print(msg.read_int32())
    print(msg.read_float32())
    print(msg.read_bool())
    print(msg.read_float32_list())


env.AddListener('DynamicMessage', dynamic_function)
env.SendMessage(
    'DynamicMessage',
    123456,
    'this is dynamic message',
    True,
    4849.6564,
    [616445.085, 9489984.0, 65419596.0, 9849849.0]
)
env.step()

env.Pend()
env.close()


