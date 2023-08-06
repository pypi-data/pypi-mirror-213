"""Library to parse PUS style packets using an SCOS-2000 instance

The core data classes of this package are:

 - ``PUSPacket``, a PUS packet with accessors
 - ``SCOSTMPacket``, wrapping a PUS packet and providing convenient access to
   the telemetry's parameters and values
 - ``SCOSTCPacket``, wrapping a PUS packet and providing convenient access to
   the telecommand's parameters and values

To get from a ``PUSPacket`` to a ``SCOSTMPacket`` (or the TC), you can simply
call ``PUSPacket.interprete`` and pass the instance of the SCOS-2000 that you
want to use.

To read telemetry or telecommands from archives, the following two types of
archive are supported:

 - ``dds``, a binary format that will prefix each PUS packet with a DDS header
 - Airbus CSV (``airbuscsv``), a plain text semi-colon separated format with
   one packet per line

Both ``dds`` and ``airbuscsv`` provide a respective reader function to iterate
over all packets in the opened archive file.

For example, the DDS reader can be used like this:

    from scospus.dds import DDSReader

    for ddspacket in DDSReader(filepath):
        packet = ddspacket.payload.interprete(scosinstance)

        if packet.is_tm:
            print(f"Received {packet.spid} on {ddspacket.timestamp}")

Similarly the Airbus CSV reader can be used like this:

    from scospus.airbuscsv import AirbusCSVReader

    for csvpacket in AirbusCSVReader(filepath):
        packet = csvpacket.payload.interprete(scosinstance)

        if packet.is_tm:
            print(f"Received {packed.spid} on {csvpacket.local_time}")

"""
from .crc16 import crc16
from .pus import PUSPacket
from .enums import PUSType, PCAT
from .tm import SCOSTMPacket
from .tc import SCOSTCPacket
from .internal import SCOSPUSError
from . import dds
from . import airbuscsv
from .guess import guess_reader
