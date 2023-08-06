"""Test DDS parsing"""

import datetime
import unittest

from scospus.dds import DDSPacket, GROUNDSTATIONS, TimeQuality


class TestBasicParsing(unittest.TestCase):
    def test_parsing(self):
        blob = b':O\xc8\x80\x00\x00\x00\x00\x00\x00\x00\x05\x00' \
               b'\x15\x01\x30\xf0\x01'
        packet = DDSPacket(blob)
        packet.payload = b'xxxxx'

        self.assertEqual(packet.timestamp,
                         datetime.datetime(2001, 1, 1, tzinfo=datetime.timezone.utc))
        self.assertEqual(len(packet), 23)
        self.assertEqual(packet.length, 5)
        self.assertEqual(packet.groundstation, GROUNDSTATIONS[0x15])
        self.assertEqual(packet.SLE, 0xf0)
        self.assertEqual(packet.time_quality, TimeQuality.INACCURATE)
        self.assertEqual(packet.virtual_channel, 0x130)

    def test_sorting(self):
        dds1 = DDSPacket(b':O\xc8\x80\x00\x00\x00\x00\x00\x00\x00\x05\x00\x15\x01\x30\xf0\x01')
        dds2 = DDSPacket(b':O\xc8\x82\x00\x00\x00\x00\x00\x05\x00\x00\x00\x15\x01\x30\xf0\x01')

        self.assertLess(dds1, dds2)

    def test_wrap(self):
        dds1 = DDSPacket(b':O\xc8\x80\x00\x00\x00\x00\x00\x00\x00\x05\x00\x15\x01\x30\xf0\x01')

        dds2 = DDSPacket.wrap(b'xxxxx',
                              timestamp=dds1.timestamp,
                              groundstation=dds1.groundstation,
                              virtual_channel=dds1.virtual_channel,
                              SLE=dds1.SLE,
                              time_quality=dds1.time_quality)

        self.assertEqual(dds1.coarse_time, dds2.coarse_time)
        self.assertEqual(dds1.fine_time, dds2.fine_time)
        self.assertEqual(dds1.length, dds2.length)
        self.assertEqual(dds1.groundstation, dds2.groundstation)
        self.assertEqual(dds1.SLE, dds2.SLE)
        self.assertEqual(dds1.virtual_channel, dds2.virtual_channel)
        self.assertEqual(dds1.time_quality, dds2.time_quality)
