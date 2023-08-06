"""Various dependency-free enums"""
import enum


class PCAT(enum.Enum):
    """PCAT field of PUS packets"""
    TIME = 0
    ACKNOWLEDGE = 1
    RESERVED1 = 2
    TABLE = 3
    HK = 4
    FUNCTIONAL_CYCLIC = 5
    FUNCTIONAL_NON_CYCLIC = 6
    EVENT = 7
    DIAGNOSTIC = 8
    DUMP = 9
    FILE_TRANSFER = 10
    CONTEXT = 11
    PRIVATE_SCIENCE = 12
    RESERVED2 = 13
    EGSE = 14
    IDLE = 15


class PUSType(enum.Enum):
    """What type a PUS packet is"""
    UNKNOWN = -1
    TELEMETRY = 0
    TELECOMMAND = 1
