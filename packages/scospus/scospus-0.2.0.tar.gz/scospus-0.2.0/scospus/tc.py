"""Classes for TC handling using SCOS"""
from .internal import SCOSPacketProxyBase


class SCOSTCPacket(SCOSPacketProxyBase):
    """A PUS interpreted as a telecommand using SCOS"""
