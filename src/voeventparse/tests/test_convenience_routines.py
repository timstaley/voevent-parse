from __future__ import print_function
import datetime
from copy import copy
from unittest import TestCase

import voeventparse as vp
from voeventparse.tests.resources import datapaths
import iso8601


class TestConvenienceRoutines(TestCase):
    def setUp(self):
        with open(datapaths.swift_bat_grb_pos_v2, 'rb') as f:
            self.swift_grb_v2_packet = vp.load(f)
        with open(datapaths.moa_lensing_event_path, 'rb') as f:
            self.moa_packet = vp.load(f)
        with open(datapaths.gaia_alert_16aac_direct, 'rb') as f:
            self.gaia_noname_param_packet = vp.load(f)
        with open(datapaths.asassn_scraped_example, 'rb') as f:
            self.assasn_scraped_packet = vp.load(f)
        self.blank = vp.Voevent(stream='voevent.foo.bar/TEST',
                                stream_id='100',
                                role='test')

    def test_get_event_position(self):
        known_swift_grb_posn = vp.Position2D(ra=74.741200, dec=-9.313700,
                                             err=0.05,
                                             units='deg',
                                             system='UTC-FK5-GEO')
        p = vp.get_event_position(self.swift_grb_v2_packet)
        self.assertEqual(p, known_swift_grb_posn)
        self.assertIsInstance(p.ra, float)

    def test_pull_params(self):
        """
        Basic functionality tested here, but this function is deprecated
        due to some serious flaws. See ``test_get_toplevel_params``.
        """
        swift_params = vp.pull_params(self.swift_grb_v2_packet)

        # General example, check basic functionality
        self.assertEqual(swift_params[None]['Packet_Type']['value'], '61')
        self.assertEqual(
            swift_params['Misc_Flags']['Values_Out_of_Range']['value'],
            'false')

        # Check ordering is preserved
        self.assertEqual(list(swift_params[None].keys())[:3],
                         ['Packet_Type', 'Pkt_Ser_Num', 'TrigID'])

        # Test empty What section
        params = vp.pull_params(self.blank)
        self.assertEqual(params, {})

        # Test known (generated) example
        single_par = copy(self.blank)
        single_par.What.append(vp.Param(name="test_param", value=123))
        params = vp.pull_params(single_par)
        self.assertEqual(len(params), 1)
        self.assertEqual(list(params[None].keys()), ['test_param'])

        # Test case where a What Group is present, but empty:
        params = vp.pull_params(self.moa_packet)
        self.assertEqual(params['Misc_Flags'], {})

        # Test case where a Param is present with no name:
        params = vp.pull_params(self.gaia_noname_param_packet)

    def test_get_toplevel_params(self):
        v = self.blank
        p_foo1 = vp.Param(name='foo',
                          value=42,
                          unit='bars',
                          ac=True
                          )
        p_foo2 = vp.Param(name='foo',
                          value=123,
                          unit='bars',
                          ac=True
                          )
        p_noname = vp.Param(name='delete_me', value=111)
        param_list = [p_foo1, p_foo2, p_noname]
        del p_noname.attrib['name']
        v.What.extend(param_list)

        # Show flaws in old routine:
        old_style_toplevel_param_dict = vp.pull_params(v)[None]
        # print(old_style_toplevel_param_dict)
        vp.assert_valid_as_v2_0(v)
        # The old 'pull_params' routine will simply drop Params with duplicate
        # names:
        assert len(old_style_toplevel_param_dict)==(len(param_list) - 1)
        none_group = vp.Group([],name=None)
        complex_group1 =vp.Group([vp.Param(name='real', value=1.),
                                vp.Param(name='imag', value=0.5)],
                               name='complex')
        complex_group2 =vp.Group([vp.Param(name='real', value=1.5),
                                vp.Param(name='imag', value=2.5)],
                               name='complex')
        group_list = [none_group, complex_group1, complex_group2]
        v.What.extend(group_list)
        vp.assert_valid_as_v2_0(v)
        old_style_toplevel_param_dict_w_group = vp.pull_params(v)[None]
        # An un-named group will also overshadow top-level Params.
        # This is a total fail, even though it's actually in-spec.
        assert len(old_style_toplevel_param_dict_w_group)==0

        toplevel_params = vp.get_toplevel_params(v)
        # .values method behaves like regular dict, one value for each key:
        assert len(toplevel_params.values())==(len(param_list) - 1)
        # Use .allvalues if you want to see duplicates:
        assert len(toplevel_params.allvalues())==len(param_list)

        grouped_params = vp.get_grouped_params(v)
        assert len(grouped_params.values())==len(group_list) - 1
        assert len(grouped_params.allvalues())==len(group_list)



    def test_get_event_time_as_utc(self):
        isotime = vp.get_event_time_as_utc(self.swift_grb_v2_packet)
        # check it works, and returns timezone aware datetime:
        self.assertIsInstance(isotime, datetime.datetime)
        self.assertTrue(isotime.tzinfo is not None)
        self.assertEqual(isotime.utcoffset(), datetime.timedelta(0))

    def test_get_event_time_as_utc_blank(self):
        # Running on an empty VOEvent should return None, not an exception:
        null_result = vp.get_event_time_as_utc(self.blank)
        self.assertIsNone(null_result)

    def test_get_event_time_as_utc_formatted_with_timezone_plus(self):
        # An edge case: ISOFormat can include a timezone suffix,
        # e.g. '2016-09-25T11:16:48+00:00'
        # The VOEvent UTC format means that the suffix is redundant,
        # but *that doesn't necessarily mean it won't get added anyway!*
        asassn_time = vp.get_event_time_as_utc(self.assasn_scraped_packet)
        self.assertIsNotNone(asassn_time)

    def test_get_event_time_as_utc_from_TDB(self):
        converted_isotime = vp.get_event_time_as_utc(
            self.gaia_noname_param_packet)
        # check it works, and returns timezone aware datetime:
        self.assertIsInstance(converted_isotime, datetime.datetime)
        self.assertTrue(converted_isotime.tzinfo is not None)
        self.assertEqual(converted_isotime.utcoffset(), datetime.timedelta(0))
        self.assertEqual(converted_isotime.utcoffset(), datetime.timedelta(0))

        od = self.gaia_noname_param_packet.WhereWhen.ObsDataLocation[0]
        ol = od.ObservationLocation
        coord_sys = ol.AstroCoords.attrib['coord_system_id']
        self.assertEqual(coord_sys, 'TDB-ICRS-BARY')

        raw_iso_string = str(ol.AstroCoords.Time.TimeInstant.ISOTime)
        misinterpreted_as_utc = iso8601.parse_date(raw_iso_string)
        self.assertNotEqual(converted_isotime, misinterpreted_as_utc)


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
        self.assertEqual(before, after)
