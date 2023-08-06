"""Airbus CSV parsing

You probably just want to use the ``AirbusCSVReader`` class like this::

    for packet in AirbusCSVReader('thatfile.csv'):
        print("Packet's local time:", packet.local_time)
        # use your scos instance to get a usable PUS packet
        packet = packet.payload.interprete(my_scos)

"""
import datetime
import csv
import io
from pathlib import Path

from .pus import PUSPacket


class AirbusCSVDialect(csv.Dialect):
    """CSV dialect for SCOS-style .dat files"""
    delimiter = ';'
    doublequote = False
    escapechar = None
    lineterminator = '\n'
    quoting = csv.QUOTE_NONE
    skipinitialspace = False
    strict = True


class AirbusCSVPacket:
    """One TM or TC packet extracted from Airbus CSV files"""
    def __init__(self, row):
        self.row = row
        self.payload = b''
        """The wrapped packet"""
        self.local_time = None
        """The local time of packet arrival"""
        self.mission_time = None
        """Mission time of packet arrival"""

    def sorting(self):
        if hasattr(self.payload, 'sorting'):
            return [self.local_time] + self.payload.sorting()
        return [self.local_time]

    def __lt__(self, other):
        return self.sorting() < other.sorting()

    def parse(self):
        """Parse the row"""
        blobstr = ''.join(self.row[-3:])
        blob = bytes.fromhex(blobstr)
        puspacket = PUSPacket.parse(io.BytesIO(blob))
        self.payload = puspacket

        timestamp = int(self.row[0])/1000.
        self.local_time = datetime.datetime.fromtimestamp(timestamp) \
                          .replace(tzinfo=datetime.timezone.utc)

        if self.payload.is_tm:
            timestamp = int(self.row[1])/1000.
            self.mission_time = datetime.datetime.fromtimestamp(timestamp) \
                                .replace(tzinfo=datetime.timezone.utc)


class AirbusCSVReader:
    """Stateful reader of Airbus CSV files with TC or TM

    Can be used as a context or directly to iterate a CSV file.
    """
    def __init__(self, target):
        if isinstance(target, str):
            target = Path(target).expanduser()
        if isinstance(target, Path):
            target = open(target, 'rt', newline='', encoding='utf-8')

        self.target = target
        self.reader = None
        self.header = None

    def open(self):
        """Open the stream for reading"""
        self.reader = csv.reader(self.target, dialect=AirbusCSVDialect)
        self.header = None

    def read_next(self):
        """Read the next packet from the CSV file"""
        assert self.reader is not None
        if self.header is None:
            self.header = next(self.reader)

        try:
            row = next(self.reader)
            packet = AirbusCSVPacket(row)
            packet.parse()
            return packet
        except StopIteration:
            return None
        except EOFError:
            return None

    def close(self):
        """Close the stream"""
        if self.reader is not None:
            del self.reader
        self.reader = None
        self.header = None

    def __iter__(self):
        """Read all packets from the given path or file"""
        if self.reader is None and self.header is None:
            self.open()
        while True:
            packet = self.read_next()
            if packet is None:
                break
            yield packet

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, *args, **kwargs):
        self.close()
