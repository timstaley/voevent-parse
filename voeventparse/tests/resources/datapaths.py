import os
from voeventparse.tests.resources import __path__ as data_dir

data_dir = data_dir[0]
swift_bat_grb_pos_v2 = os.path.join(data_dir,
                                    'SWIFT_bat_position_v2.0_example.xml')
swift_xrt_pos_v1 = os.path.join(data_dir,
                                    'SWIFT_xrt_position_v1.1_example.xml')
no_namespace_test_packet = os.path.join(data_dir, 'no_namespace_packet.xml')
