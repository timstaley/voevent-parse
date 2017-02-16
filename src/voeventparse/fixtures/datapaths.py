import os
from voeventparse.fixtures import __path__ as data_dir

data_dir = data_dir[0]
swift_bat_grb_pos_v2 = os.path.join(data_dir,
                                    'SWIFT_bat_position_v2.0_example.xml')
swift_xrt_pos_v1 = os.path.join(data_dir,
                                'SWIFT_xrt_position_v1.1_example.xml')
no_namespace_test_packet = os.path.join(data_dir, 'no_namespace_packet.xml')

moa_lensing_event_path = os.path.join(data_dir,
                                      'MOA_Lensing_Event_2015-07-10T14:50:54.00.xml')

gaia_alert_16aac_direct = os.path.join(data_dir, 'Gaia16aac.xml')

asassn_scraped_example = os.path.join(
    data_dir, 'ASASSN#2016-09-25.47_2016fvf_PTSS-16nqb_PS16ejf.xml')
