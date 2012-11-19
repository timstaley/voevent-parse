import unittest
from unittest import TestCase
from resources import datapaths

from lxml import objectify, etree
#from astropysics.coords.coordsys import FK5Coordinates
from copy import deepcopy

import voeparse as voe

class TestElementCopying(TestCase):
    def setUp(self):
        self.raw_swift_packet = objectify.parse(datapaths.swift_bat_grb_pos_v2)
        self.raw_swift_packet = self.raw_swift_packet.getroot()

class TestValidation(TestCase):
    def setUp(self):
        self.raw_swift_packet = objectify.parse(datapaths.swift_bat_grb_pos_v2)
        self.raw_swift_packet = self.raw_swift_packet.getroot()

    def test_schema_valid_for_test_data(self):
        voe.voevent_v2_0_schema.validate(self.raw_swift_packet)
        self.assertTrue(voe.voevent_v2_0_schema.validate(self.raw_swift_packet))
        #NB dropping the namespace from root element invalidates packet:
        self.raw_swift_packet.tag = 'VOEvent'
        self.assertFalse(voe.voevent_v2_0_schema.validate(self.raw_swift_packet))

    def test_schema_invalid_for_bad_data(self):
        v = self.raw_swift_packet
        Who = v['{}Who']
        Who.BadChild = 42
        self.assertFalse(voe.voevent_v2_0_schema.validate(v))
        del Who.BadChild
        self.assertTrue(voe.voevent_v2_0_schema.validate(v))


class TestBuilders(TestCase):
    def test_builders_on_voe_v2(self):
        vff = voe.build.from_file(datapaths.swift_bat_grb_pos_v2)
        with open(datapaths.swift_bat_grb_pos_v2) as f:
            vfs = voe.build.from_string(f.read())
        self.assertEqual(objectify.dump(vff), objectify.dump(vfs))
        self.assertEqual(vfs.tag, 'VOEvent')
        self.assertEqual(vfs.attrib['ivorn'],
                         'ivo://nasa.gsfc.gcn/SWIFT#BAT_GRB_Pos_532871-729')

class TestOutput(TestCase):
    def setUp(self):
        self.swift_grb_v2_raw = objectify.parse(
                                      datapaths.swift_bat_grb_pos_v2).getroot()
        self.swift_grb_v2_trimmed = voe.build.from_file(
                                        datapaths.swift_bat_grb_pos_v2)

    def test_conversion_to_string(self):
        raw = etree.tostring(self.swift_grb_v2_raw,
                             pretty_print=True,
                             xml_declaration=True,
                             encoding='UTF-8')
        processed = voe.output.to_string(self.swift_grb_v2_trimmed)
#        print
#        print "-------------------------------"
#        print "RAW"
#        print raw[:256]
#        print "-------------------------------"
#        print "Munged"
#        print processed[:256]
#        print "-------------------------------"
#        with open("testout.xml", 'w') as f:
#            f.write(processed)
        self.assertEqual(raw, processed)

#
#class TestAstroCoords(TestCase):
#    def setUp(self):
#        self.swift_grb_v2 = voe.build.from_file(datapaths.swift_bat_grb_pos_v2)
#        self.swift_grb_posn = FK5Coordinates(ra=74.741200, dec= -9.313700,
#                                             raerr=0.05, decerr=0.05)
#    def test_swift_grb_v2(self):
#        p = voe.pull_astro_coords(self.swift_grb_v2)
#        self.assertEqual(p, self.swift_grb_posn)






