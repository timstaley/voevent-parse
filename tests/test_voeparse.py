import unittest
from unittest import TestCase
from resources import datapaths

from lxml import objectify, etree
#from astropysics.coords.coordsys import FK5Coordinates
from copy import copy

import voeparse as voe

class TestValidation(TestCase):
    def test_schema_valid_for_test_data(self):
        """
        test_schema_valid_for_test_data:
        First, let's check everything is in order with the test data
        and the schema.

        Here we directly access the lxml validate routine.
        """
        v = objectify.parse(datapaths.swift_bat_grb_pos_v2).getroot()
        self.assertTrue(voe.voevent_v2_0_schema.validate(v))
        Who = v['{}Who']
        Who.BadChild = 42
        self.assertFalse(voe.voevent_v2_0_schema.validate(v))
        del Who.BadChild
        self.assertTrue(voe.voevent_v2_0_schema.validate(v))

        #NB dropping the namespace from root element invalidates packet:
        # This is why we must re-insert it before output.
        v.tag = 'VOEvent'
        self.assertFalse(voe.voevent_v2_0_schema.validate(v))

    def test_validation_routine(self):
        """test_validation_routine

        Now we perform the same validation tests, but applied via the
        convenience functions.
        """
        v = voe.load(datapaths.swift_bat_grb_pos_v2)
        self.assertTrue(voe.validate_as_v2_0(v))
        v.Who.BadChild = 42
        self.assertFalse(voe.validate_as_v2_0(v))
        del v.Who.BadChild
        self.assertTrue(voe.validate_as_v2_0(v))


class TestIO(TestCase):
    def test_load_of_voe_v2(self):
        vff = voe.load(datapaths.swift_bat_grb_pos_v2)
        with open(datapaths.swift_bat_grb_pos_v2) as f:
            vfs = voe.loads(f.read())
        self.assertEqual(objectify.dump(vff), objectify.dump(vfs))
        self.assertEqual(vfs.tag, 'VOEvent')
        self.assertEqual(vfs.attrib['ivorn'],
                         'ivo://nasa.gsfc.gcn/SWIFT#BAT_GRB_Pos_532871-729')

    def test_dumps(self):
        """
        test_dumps:

        Note, the processed output does not match the raw input -
        because I have added the UTF-8 encoding declaration.
        So we match the convenience routines against an
        etree.tostring processed version of the original.
        """
        swift_grb_v2_raw = objectify.parse(
                                  datapaths.swift_bat_grb_pos_v2).getroot()
        swift_grb_v2_voeparsed = voe.load(datapaths.swift_bat_grb_pos_v2)
        raw = etree.tostring(swift_grb_v2_raw,
                             pretty_print=True,
                             xml_declaration=True,
                             encoding='UTF-8')
        processed = voe.dumps(swift_grb_v2_voeparsed)
        self.assertEqual(raw, processed)


#class TestAstroCoords(TestCase):
#    def setUp(self):
#        self.swift_grb_v2 = voe.build.load(datapaths.swift_bat_grb_pos_v2)
#        self.swift_grb_posn = FK5Coordinates(ra=74.741200, dec= -9.313700,
#                                             raerr=0.05, decerr=0.05)
#    def test_swift_grb_v2(self):
#        p = voe.pull_astro_coords(self.swift_grb_v2)
#        self.assertEqual(p, self.swift_grb_posn)






