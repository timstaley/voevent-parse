import datetime
from copy import copy
from unittest import TestCase

import voeventparse as vp
from voeventparse.tests.resources import datapaths


class TestConvenienceRoutines(TestCase):
    def setUp(self):
        with open(datapaths.swift_bat_grb_pos_v2, 'rb') as f:
            self.swift_grb_v2_packet = vp.load(f)
        with open(datapaths.moa_lensing_event_path, 'rb') as f:
            self.moa_packet = vp.load(f)
        with open(datapaths.gaia_alert_16aac_direct, 'rb') as f:
            self.noname_param_packet = vp.load(f)
        self.blank = vp.Voevent(stream='voevent.soton.ac.uk/TEST',
                                 stream_id='100',
                                 role='test')

    def test_pull_astro_coords(self):
        known_swift_grb_posn = vp.Position2D(ra=74.741200, dec=-9.313700,
                                              err=0.05,
                                              units='deg',
                                              system='UTC-FK5-GEO')
        p = vp.pull_astro_coords(self.swift_grb_v2_packet)
        self.assertEqual(p, known_swift_grb_posn)
        self.assertIsInstance(p.ra, float)

    def test_pull_params(self):
        swift_params = vp.pull_params(self.swift_grb_v2_packet)

        #General example, check basic functionality
        self.assertEqual(swift_params[None]['Packet_Type']['value'], '61')
        self.assertEqual(swift_params['Misc_Flags']['Values_Out_of_Range']['value'],
                         'false')

        #Check ordering is preserved
        self.assertEqual(list(swift_params[None].keys())[:3],
                         ['Packet_Type', 'Pkt_Ser_Num', 'TrigID'])

        #Test empty What section
        params = vp.pull_params(self.blank)
        self.assertEqual(params, {})

        #Test known (generated) example
        single_par = copy(self.blank)
        single_par.What.append(vp.Param(name="test_param", value=123))
        params = vp.pull_params(single_par)
        self.assertEqual(len(params), 1)
        self.assertEqual(list(params[None].keys()), ['test_param'])

        #Test case where a What Group is present, but empty:
        params = vp.pull_params(self.moa_packet)
        self.assertEqual(params['Misc_Flags'], {})

        #Test case where a Param is present with no name:
        params = vp.pull_params(self.noname_param_packet)


    def test_pull_isotime(self):
        isotime = vp.pull_isotime(self.swift_grb_v2_packet)
        self.assertIsInstance(isotime, datetime.datetime)

        null_result = vp.pull_isotime(self.blank)
        self.assertIsNone(null_result)


class TestPrettyStr(TestCase):
    def setUp(self):
        with open(datapaths.swift_bat_grb_pos_v2, 'rb') as f:
            self.swift_grb_v2_packet = vp.load(f)
    def test_for_packet_mangling(self):
        """
        Check that applying prettystr to a packet does not change it.
        """
        self.assertTrue(vp.valid_as_v2_0(self.swift_grb_v2_packet))
        before = vp.dumps(self.swift_grb_v2_packet)
        vp.prettystr(self.swift_grb_v2_packet)
        self.assertTrue(vp.valid_as_v2_0(self.swift_grb_v2_packet))
        after = vp.dumps(self.swift_grb_v2_packet)
        self.assertEqual(before,after)