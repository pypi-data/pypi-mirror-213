"""Shared internal data structures and types"""
from pyscos2000 import ParameterType, PacketInterface


uint_types = {8: ParameterType.resolve((3, 4)),
              12: ParameterType.resolve((3, 8)),
              16: ParameterType.resolve((3, 12)),
              24: ParameterType.resolve((3, 13)),
              32: ParameterType.resolve((3, 14)),
              }


class SCOSPUSError(RuntimeError):
    """Generic runtime errors from the SCOS PUS system"""


class SCOSPacketProxyBase(PacketInterface):
    """Base class for all PUS packets as interpreted by SCOS"""
    def __init__(self, packet, scos):
        super().__init__()
        self.pus = packet
        self.scos = scos

    def crc_ok(self):
        """Whether or not the CRC16 checks out"""
        return self.pus.crc_ok()

    def hex(self):
        """The hex representation of the packet"""
        return self.pus.hex()

    @property
    def apid(self):
        """This packets APID"""
        return self.pus.apid

    @property
    def prid(self):
        """This packets PRID"""
        return self.pus.prid

    @property
    def pcat(self):
        """This packets PCAT"""
        return self.pus.pcat

    def __bytes__(self):
        return bytes(self.pus)

    def __setitem__(self, item, value):
        return self.set(item, value)

    def set(self, item, rawvalue):
        """Set the parameter ``item`` to ``rawvalue``

        Like for ``get_parameter``, ``item`` can be a number position of the
        parameter or the 8-character string identifying the parameter by name.

        Raises ``KeyError`` if the parameter does not exist.
        May raise ``RuntimeError`` if the parameter is read-only.
        """
        raise NotImplementedError("Must be implemented in a subclass")
