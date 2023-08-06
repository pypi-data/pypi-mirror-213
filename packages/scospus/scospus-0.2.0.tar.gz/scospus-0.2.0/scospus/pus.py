"""Data structures describing a PUS packet"""
import datetime
import math
import struct
import enum
from pathlib import Path

from pyscos2000 import unpack_uint_format

from .crc16 import crc16
from .enums import PUSType, PCAT
from .internal import uint_types, SCOSPUSError
from .tm import SCOSTMPacket
from .tc import SCOSTCPacket


EPOCH = datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)


class PrematureEndOfPacketError(SCOSPUSError):
    """Raised when trying to extract more data from a packet than there is"""


class NoDataFieldHeaderError(SCOSPUSError):
    """Raised when attempting to interprete a packet that has no data field header"""


class UnknownPacketTypeError(SCOSPUSError):
    """Raised when encountering a PUS packet that’s neither TM nor TC"""


class AckFlags(enum.Flag):
    """Ack flag of a PUS TC"""
    ACCEPTED = 1
    STARTEXEC = 2
    PROGRESS = 4
    EXECUTED = 8


class Grouping(enum.Enum):
    """Grouping information of a PUS TM"""
    CONTINUATION = 0
    FIRSTPACKET = 1
    LASTPACKET = 2
    STANDALONE = 3


class PUSReader:
    """Read PUS packets from a file"""
    def __init__(self, filepath):
        self.filepath = Path(filepath).expanduser()
        self.stream = None
        self.position = -1

    def open(self):
        """Open the stream for reading"""
        if self.stream is None:
            self.stream = open(self.filepath, 'rb')
            self.position = 0

    def close(self):
        """Close the stream"""
        if self.stream is not None:
            self.stream.close()
        self.stream = None
        self.position = -1

    def seek(self, position):
        """Go to ``position`` in the stream"""
        assert self.stream is not None
        self.position = self.stream.seek(position)

    def read_next(self):
        """Read the next PUS packet from the stream"""
        assert self.stream is not None
        self.position = self.stream.tell()
        try:
            return PUSPacket.parse(self.stream)
        except (EOFError, ValueError):
            return None

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

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, *args, **kwargs):
        self.close()


class PUSTimestamp:
    """A timestamp of a PUS packet"""
    def __init__(self, packet):
        self.packet = packet

    def coarse(self):
        """Return the coarse time field of the packet

        This will NOT include the most significant bit, as it is an indicator
        of the availability of absolute timestamps"""
        return self.packet.datafieldheader.coarse_time & 0x7fffffff

    def fine(self):
        """Return the fine time field of the packet

        For SCET that means the microseconds part of the timestamp
        """
        return self.packet.datafieldheader.fine_time

    def is_absolute(self):
        """Whether or not the timestamp is absolute

        If set, the timestamp really is an absolute timestamp
        """
        return 0 == (self.packet.datafieldheader.coarse_time & 0x80000000)

    def as_datetime(self, offset=None):
        """Turn the PUS timestamp into a datetime

        ``offset`` can be used to set a datetime offset in case the timestamp
        is not absolute."""
        if offset is None:
            offset = EPOCH

        return offset + self.as_interval()

    def as_interval(self):
        """Return the timestamp as an interval

        This function assumes that the timestamp really not absolute"""
        return datetime.timedelta(seconds=self.coarse() + self.fine()/0x10000)

    def strftime(self, pattern, offset=None):
        """Format the time according to `pattern`

        ``offset`` is passed into ``as_datetime``. It defines the offset to be
        used in case the timestamp is not absolute.

        Behaves otherwise exactly like ``datetime.strftime`` would"""
        return self.as_datetime(offset).strftime(pattern)

    def __lt__(self, other):
        if isinstance(other, datetime.datetime):
            return self.as_datetime() < other
        if isinstance(other, datetime.timedelta):
            return self.as_interval() < other
        assert isinstance(other, PUSTimestamp)
        return self.as_datetime() < other.as_datetime()

    def __gt__(self, other):
        if isinstance(other, datetime.datetime):
            return self.as_datetime() > other
        if isinstance(other, datetime.timedelta):
            return self.as_interval() > other
        assert isinstance(other, PUSTimestamp)
        return self.as_datetime() > other.as_datetime()

    def __str__(self):
        return self.strftime('%Y-%m-%d %H:%M:%S')


class PUSPacket:
    """A PUS packet"""
    def __init__(self):
        self.version = 0
        self.type = PUSType.UNKNOWN
        self.apid = 0
        """The APID"""

        self.grouping = Grouping.STANDALONE
        """Grouping information"""

        self.sequence_count = 0
        """The sequence counter value"""

        self.df_len = 0
        """Length of the datafield header"""

        self.datafieldheader = None
        """The data field header"""

        self.raw = bytes()
        self._len = 0

    def __len__(self):
        return self._len

    def hex(self):
        """The hex representation of the packet"""
        return self.raw.hex()

    def __bytes__(self):
        return self.raw

    def __str__(self):
        return f'<PUSPacket {self.apid} seq: {self.sequence_count} ' \
               f'length: {self._len} bytes>'

    def __lt__(self, other):
        assert isinstance(other, PUSPacket)
        return self.sorting() < other.sorting()

    def sorting(self):
        """Returns the list used for sorting"""
        return [self.timestamp, self.sequence_count]

    @property
    def is_tm(self):
        """Whether or not this is a TM packet"""
        return self.type == PUSType.TELEMETRY

    @property
    def is_tc(self):
        """Whether or not this is a TC packet"""
        return self.type == PUSType.TELECOMMAND

    @property
    def has_dfh(self):
        """Whether or not this packet has a ``DataFieldHeader``"""
        return self.datafieldheader is not None

    @property
    def prid(self):
        """The PRID header field"""
        return (self.apid >> 4) & 0x7f

    @property
    def pcat(self):
        """The PCAT header field"""
        return PCAT(self.apid & 0x0f)

    @property
    def payload(self):
        """The payload of the packet"""
        if self.datafieldheader is not None:
            return self.raw[16:-2]
        return self.raw[6:-2]

    @property
    def timestamp(self):
        """The timestamp of the packet"""
        return PUSTimestamp(self)

    def crc_ok(self):
        """Whether or not the CRC of this packet is correct"""
        return crc16(self.raw) == 0

    def get(self, bits, byte_offset=0, bit_offset=0):
        """Get the the amount of ``bits`` at ``bit_offset`` within ``byte_offset``

        ``byte_offset`` starts to count at the start of the packet, i.e. at
        the first byte of the first header.

        Will return ``bytes``, with your requested bits all right-aligned"""
        assert bit_offset < 8
        assert bits > 0
        # get all the bytes that contain the needed bits
        actualbytesize = math.ceil((bit_offset+bits)/8.)
        data = self.raw[byte_offset:-2][:actualbytesize]

        bitwidth = len(data)*8 - bit_offset
        if bitwidth < bits:
            raise PrematureEndOfPacketError(f"Trying to get {bits} bit from {len(data)} bytes")

        unpackbitwidth = bitwidth
        while unpackbitwidth not in uint_types and unpackbitwidth < 32:
            unpackbitwidth += 1

        if unpackbitwidth not in uint_types:
            # TODO - fix this code in case bit_offset != 0 and/or bits % 8 != 0
            # assert bit_offset == 0
            # assert bits % 8 == 0
            return data

        value = uint_types[unpackbitwidth].unpack(data)
        value = (value >> (len(data)*8 - bit_offset - bits)) & (2**bits - 1)

        databytesize = math.ceil(bits/8.)
        exporttypestr, exportbytesize = unpack_uint_format(bits)

        return struct.pack('>'+exporttypestr, value)[exportbytesize-databytesize:]

    def interprete(self, scos):
        """Use the given SCOS-2000 instance ``scos`` to interprete this PUS packet

        Will return a new instance of either SCOSTMPacket or SCOSTCPacket
        """
        if self.type == PUSType.TELEMETRY:
            if not self.has_dfh:
                raise NoDataFieldHeaderError()
            return SCOSTMPacket(self, scos)

        if self.type == PUSType.TELECOMMAND:
            return SCOSTCPacket(self, scos)

        raise UnknownPacketTypeError()

    def copy_from(self, other):
        """Copy the content from ``other``

        Returns ``self``"""
        self.version = other.version
        self.type = PUSType(other.type)
        self.apid = other.apid
        self.grouping = Grouping(other.grouping)
        self.sequence_count = other.sequence_count
        self.df_len = other.df_len
        self.raw = other.raw[:]
        self._len = len(self.raw)
        self.datafieldheader = other.datafieldheader.copy()

        return self

    @classmethod
    def parse(cls, stream):
        """Parse a PUS packet from the byte stream ``stream``"""
        assert hasattr(stream, 'read')
        raw = stream.read(6)

        if len(raw) < 6:
            raise EOFError()

        pus = PUSPacket()
        pus.version = (raw[0] & 0xe0) >> 5
        pus.type = PUSType((raw[0] & 0x10) >> 4)
        has_dfh = ((raw[0] & 8) >> 3) == 1
        pus.apid = struct.unpack_from('>H', raw)[0] & 0x07ff

        pus.grouping = Grouping((raw[2] & 0xc0) >> 6)
        pus.sequence_count = struct.unpack_from('>H', raw[2:4])[0] & 0x3f
        pus.df_len = struct.unpack_from('>H', raw[4:6])[0] + 1

        payload = stream.read(pus.df_len)
        pus.raw = raw + payload
        pus._len = len(pus.raw)

        if has_dfh:
            if pus.type == PUSType.TELEMETRY:
                pus.datafieldheader = PUSTMDataFieldHeader()
            elif pus.type == PUSType.TELECOMMAND:
                pus.datafieldheader = PUSTCDataFieldHeader()
            else:
                raise UnknownPacketTypeError()
            pus.datafieldheader.parse(payload)

        return pus


class PUSDataFieldHeader:
    """Generic PUS data field header"""
    def __init__(self):
        self.pus_version = 0
        """What version this PUS packet is"""
        self.servicetype = (0, 0)
        """The (type, subtype) of this packet"""
        self.raw = b''

    def parse(self, data):
        """Extract PUS version and type/subtype from the header"""
        if len(data) < 3:
            raise ValueError(f"Not enough data to parse a datafieldheader {len(data)}")
        self.raw = data[:]
        self.pus_version = (self.raw[0] >> 4) & 7
        self.servicetype = (self.raw[1], self.raw[2])

    def copy(self):
        """Create a deep copy of ``self``"""
        other = type(self)()
        other.raw = self.raw[:]
        other.pus_version = self.pus_version
        other.servicetype = self.servicetype
        return other


class PUSTMDataFieldHeader(PUSDataFieldHeader):
    """The Data Field Header of a PUS TM packet"""
    def __init__(self):
        super().__init__()
        self.destination = 0
        """Destination field"""
        self.coarse_time = 0
        """Coarse time field"""
        self.fine_time = 0
        """Fine time field"""

    def parse(self, data):
        super().parse(data)
        if len(self.raw) < 10:
            raise ValueError(f"PUS TM header is too short: {len(self.raw)} bytes")
        self.destination = self.raw[3]
        self.coarse_time, self.fine_time = struct.unpack_from('>IH', self.raw[4:10])

    def copy(self):
        other = super().copy()
        other.destination = self.destination
        other.coarse_time = self.coarse_time
        other.fine_time = self.fine_time
        return other


class PUSTCDataFieldHeader(PUSDataFieldHeader):
    """The Data Field Header of a PUS TC packet"""
    def __init__(self):
        super().__init__()
        self.header_flag = 0
        self.ack_flags = AckFlags(0)

    def parse(self, data):
        super().parse(data)
        self.header_flag = (self.raw[0] >> 7) & 1
        self.ack_flags = AckFlags(self.raw[0] & 0xf)

    def copy(self):
        other = super().copy()
        other.header_flag = self.header_flag
        other.ack_flags = self.ack_flags
        return other