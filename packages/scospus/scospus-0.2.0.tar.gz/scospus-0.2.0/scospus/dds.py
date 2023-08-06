"""DDS parsing and handling

You usually just want to use a ``DDSReader`` instance like this::

    for ddspacket in DDSReader('thatfile.dds'):
        print("Packet's timestamp:", ddspacket.timestamp)
        # extract a usable PUS packet using your SCOS instance:
        packet = ddspacket.payload.interprete(my_scos)

DDS packets are represented by ``DDSPacket``. The PUS packet wrapped
by the DDS packet are accessible by the ``payload`` member.

To wrap a PUS packet in an DDS packet, use the ``DDSBuilder``.

"""
import datetime
import struct
import enum
import io
from collections import namedtuple
from pathlib import Path

from .internal import SCOSPUSError
from .pus import PUSPacket


GroundStation = namedtuple('GroundStation', ('id', 'organisation', 'name'))
"""A ground station

DDS headers contain ground stations by ID."""


GROUNDSTATIONS = {gs[0]: GroundStation(*gs)
                  for gs in [
                      (0, '', ''),
                      (0x0d, 'ESA', 'Villafranca2'),
                      (0x15, 'ESA', 'Kourou'),
                      (0x16, '', 'NDIU Lite'),
                      (0x17, 'ESA', 'New Norcia'),
                      (0x18, 'ESA', 'Cebreros'),
                      (0x22, 'NASA', 'Goldstone (old)'),
                      (0x67, 'NASA', 'Goldstone (new)'),
                      (0x23, 'NASA', 'Canberra (old)'),
                      (0x70, 'NASA', 'Canberra (new)'),
                      (0x24, 'NASA', 'Madrid (old)'),
                      (0x6c, 'NASA', 'Madrid (new)'),
                      (0x7f, 'ESA/ESOC', 'Test Station'),
                      (0x82, '', 'NDIU Classic'),
                  ]}
"""The ground stations as defined in RO-MEX-VEX-ESC-IF-5003_DDID_C4"""


class PrematureEndOfFileError(SCOSPUSError):
    """Raised when trying a file is too short to hold the entire DDS packet"""


class TimeQuality(enum.Enum):
    """DDS packet time quality"""
    GOOD = 0
    INACCURATE = 1
    BAD = 2
    UNKNOWN = -1


class DDSPacket:
    """A DDS header with payload"""

    FORMAT = ">IIIHHBB"

    def __init__(self, header):
        self.dds = header
        self.payload = b''
        self.offset = -1
        """Byte offset position of this DDS packet in the source data stream"""

        self.coarse_time = 0
        self.fine_time = 0
        self.timestamp = datetime.datetime(1, 1, 1, 0, 0, 0,
                                           tzinfo=datetime.timezone.utc)
        self.groundstation = GROUNDSTATIONS[0]
        self.virtual_channel = 0
        self.SLE = 0
        self.time_quality = TimeQuality.BAD
        self.length = 0

        if len(self.dds) > 0:
            self.do_parse()

    def __len__(self):
        len_ = len(self.dds)
        if self.payload is not None:
            len_ += len(self.payload)
        return len_

    def __lt__(self, other):
        return self.sorting() < other.sorting()

    def sorting(self):
        """Return the list used for sorting"""
        if hasattr(self.payload, 'sorting'):
            return [self.timestamp] + self.payload.sorting()
        return [self.timestamp]

    def __bytes__(self):
        return self.dds + bytes(self.payload)

    @classmethod
    def wrap(cls, packet,
             timestamp=None,
             groundstation=None,
             virtual_channel=None,
             SLE=None,
             time_quality=None):
        """Create a new DDS packet that wraps the given packet"""
        dds = cls(b'')

        if timestamp is None:
            timestamp = datetime.datetime.now(datetime.timezone.utc)

        assert isinstance(timestamp, datetime.datetime)
        assert timestamp.tzinfo is not None

        coarse_time = int(timestamp.timestamp())
        fine_time = int((timestamp.timestamp() - coarse_time)*1000000)

        if groundstation is None:
            groundstation = GROUNDSTATIONS[0]

        if isinstance(groundstation, GroundStation):
            groundstation = groundstation.id

        if virtual_channel is None:
            virtual_channel = 0

        if SLE is None:
            SLE = 0

        if time_quality is None:
            time_quality = TimeQuality.INACCURATE

        if isinstance(time_quality, TimeQuality):
            time_quality = time_quality.value

        length = len(bytes(packet))

        dds.dds = struct.pack(cls.FORMAT,
                              coarse_time, fine_time,
                              length,
                              groundstation,
                              virtual_channel,
                              SLE,
                              time_quality)
        dds.do_parse()
        dds.payload = packet
        return dds

    @classmethod
    def parse(cls, stream):
        """Parse a DDS packet from the ``stream``

        This will read out only the DDS header. It's up to you to read the
        remaining packet using ``DDSPacket.length`` as an indicator how long
        the following packet is.
        """
        offset = stream.tell()
        blob = stream.read(18)
        if len(blob) < 18:
            raise EOFError()
        packet = DDSPacket(blob)
        packet.offset = offset
        return packet

    def do_parse(self):
        """Parse the usable values from the internal binary representation of the DDS header"""
        values = struct.unpack(self.FORMAT, self.dds)
        self.coarse_time = values[0]
        self.fine_time = values[1]
        self.length = values[2]
        self.timestamp = datetime.datetime.fromtimestamp(self.coarse_time,
                                                         tz=datetime.timezone.utc) + \
                         datetime.timedelta(microseconds=self.fine_time)
        gsid = values[3]
        self.groundstation = GROUNDSTATIONS.get(gsid,
                                                GroundStation(gsid, '', 'Unknown'))
        self.virtual_channel = values[4]
        self.SLE = values[5]
        try:
            self.time_quality = TimeQuality(values[6])
        except ValueError:
            self.time_quality = TimeQuality.UNKNOWN

    def __str__(self):
        return f"<DDS {self.timestamp} payload: {len(self.payload)} bytes>"


class DDSReader:
    """State-aware reader for DDS files

    Must be given a path to a DDS file.

    Can also be used as a context like this::

        with DDSReader('thatfile.dds') as reader:
            packet = reader.read_next()
            # equivalent:
            packet = next(reader)

    If ``next`` or ``read_next`` fail (and raise an exception), you can query
    ``DDSReader.position`` to get the byte offset in the stream where the DDS
    packet started that caused the failure.
    """

    def __init__(self, filepath):
        if isinstance(filepath, str):
            filepath = Path(filepath).expanduser()
        self.filepath = filepath
        self.stream = None
        self.position = -1
        self.raise_errors = True

    def seek(self, position):
        """Jump to this position in the stream"""
        assert self.stream is not None
        self.position = self.stream.seek(position)

    def open(self):
        """Open the source file for reading

        Will open the stream only once"""
        if self.stream is None:
            self.stream = open(self.filepath, 'rb')
            self.position = 0

    def close(self):
        """Close the source file"""
        if self.stream is not None:
            self.stream.close()
        self.stream = None
        self.position = -1

    def __enter__(self):
        if self.stream is None:
            self.open()
        return self

    def __exit__(self, *args, **kwargs):
        self.close()

    def read_next(self):
        """Read the next packet from the stream

        Will skip over initial stretches of ``0`` bytes.

        Will return ``None`` when the end of the stream is reached.
        """
        assert self.stream is not None
        # skip over lengths of zeroes
        while True:
            try:
                peeked = self.stream.peek(1)
            except EOFError:
                break
            zeroes = 0
            for char in peeked:
                if char != 0:
                    break
                zeroes += 1
            if zeroes == 0:
                break
            self.stream.read(zeroes)
            self.position = self.stream.tell()

        try:
            self.position = self.stream.tell()
            ddspacket = DDSPacket.parse(self.stream)
        except EOFError:
            return None
        try:
            self.position = self.stream.tell()
            blob = self.stream.read(ddspacket.length)
        except EOFError:
            return None

        if len(blob) < ddspacket.length:
            raise PrematureEndOfFileError()

        try:
            ddspacket.payload = PUSPacket.parse(io.BytesIO(blob))
        except (ValueError,) as exc:
            if self.raise_errors:
                raise RuntimeError(f"Failed to parse at {self.position}: {exc}") from exc
            ddspacket = None

        return ddspacket

    def __next__(self):
        if self.stream is None:
            self.open()
        packet = self.read_next()
        if packet is None:
            raise StopIteration()
        return packet

    def __iter__(self):
        if self.stream is None:
            self.open()
        return self


def read_from_dds(filepath):
    """Read all interpreted DDS packets from the given dds file

    A DDS packet is the DDS packet header and the PUS packet.

    ``filepath`` is the location of a ``.dds`` file,
    """
    with DDSReader(filepath) as reader:
        yield from reader
