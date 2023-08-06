"""TM packet definitions for use of PUS packets with SCOS"""
import struct

from pyscos2000 import Parameter

from .internal import SCOSPacketProxyBase, uint_types, SCOSPUSError


class UnknownPIDError(SCOSPUSError):
    """Raised when the PID of a packet is not known

    Will only be raised after identification of the packet has been attempted.
    """


class SCOSTMPacket(SCOSPacketProxyBase):
    """A PUS interpreted as telemetry using SCOS"""
    def __init__(self, packet, scos):
        super().__init__(packet, scos)
        self._pic = None
        self._pid = None
        self._pi1 = None
        self._pi2 = None
        self._plfs = []
        self._vpds = []
        self.parameters = []
        self._parsed = False
        # (byte offset, bit offset) 1 bit after the end of the last parameter
        # use '.unmapped' to access the bytes
        self.last_parameter_end = (0, 0)

    @property
    def pustype(self):
        """The (type,subtype) tuple"""
        return self.pus.datafieldheader.servicetype

    @property
    def type(self):
        return self.pus.datafieldheader.servicetype[0]

    @property
    def subtype(self):
        return self.pus.datafieldheader.servicetype[1]

    def should_check_crc(self):
        """Whether or not the database requests a CRC check of this packet"""
        self.identify()
        if self.pid is None:
            raise UnknownPIDError()
        return self.pid['PID_CHECK'].value

    def identify(self):
        """Identify the packet"""
        if self._pi1 is not None:
            # this should only be entered once and _pi1 and _pi2 are the
            # gatekeepers
            assert self._pi2 is not None
            return self._pic

        type_, subtype = self.pus.datafieldheader.servicetype
        self._pi1 = 0
        self._pi2 = 0
        self._pic = None

        apid = self.apid
        none_apid = self.scos.pic.definition.NONE_APID
        none_pics = [pic for pic in self.scos.pic.find((type_, subtype))
                     if pic['PIC_APID'].value == none_apid]
        self._pic = self.scos.pic.get((type_, subtype, apid))

        if self._pic is None and len(none_pics) > 0:
            # there may be older PIC definitions around that don't
            # define the APID
            self._pic = none_pics[0]

        if self._pic is not None:
            # PI1
            offset = self._pic['PIC_PI1_OFF'].value
            if offset != -1:
                bitwidth = self._pic['PIC_PI1_WID'].value
                blob = self.pus.get(bitwidth, offset)
                self._pi1 = uint_types[bitwidth].unpack(blob)
            # PI2
            offset = self._pic['PIC_PI2_OFF'].value
            if offset != -1:
                bitwidth = self._pic['PIC_PI2_WID'].value
                blob = self.pus.get(bitwidth, offset)
                self._pi2 = uint_types[bitwidth].unpack(blob)
        return self._pic

    @property
    def spid(self):
        """Convenience accessor to the packet's SPID"""
        if self.pid is None:
            return None
        return self.pid['PID_SPID'].value

    @property
    def pid(self):
        """Packet identification information"""
        if self._pid is None:
            self.identify()
            type_, subtype = self.pus.datafieldheader.servicetype
            search = (type_, subtype, self.pus.apid, self._pi1, self._pi2)
            pids = list(self.scos.pid.find(search))

            if len(pids) == 0:
                return None

            # it's a problem when there are multiple...; TODO?
            self._pid = pids[0]
        return self._pid

    @property
    def description(self):
        """The description of the packet"""
        return self.pid['PID_DESCR'].value

    def parse_parameters(self):
        """Load the parameters according to the definition from the packet blob"""
        if self.pid is None:
            return

        if self._parsed:
            return

        if len(self._plfs) == 0:
            # find all PLF entries for this PID
            search = {'PLF_SPID': self.pid['PID_SPID'].value}
            self._plfs = list(self.scos.plf.find(search))
            for plf in sorted(self._plfs):
                pcf = self.scos.pcf.get(plf['PLF_NAME'])
                assert pcf is not None
                try:
                    self.parameters.append(TMFixedParameter(self, pcf, plf))
                except SCOSPUSError as exc:
                    self.parameters.append(TMInvalidParameter(self, pcf, exc))

        if len(self._vpds) == 0:
            # find all VPD entries for this TPSD
            search = {'VPD_TPSD': self.pid['PID_TPSD'].value}
            self._vpds = list(sorted(self.scos.vpd.find(search)))
            if len(self._vpds) > 0 and len(self._plfs) > 0:
                raise RuntimeError(f"TM with SPID {self.spid} has both fixed "
                                   "(PLF) and variable (VPD) parameter definitions.")

            # collapse the expanded list of parameters into VPDs and TMParameterGroups
            groupstack = []
            params = []
            for vpd in self._vpds:
                pcf = self.scos.pcf.get(vpd['VPD_NAME'])
                param = TMVariableParameter(self, pcf, vpd)

                if len(groupstack) > 0:
                    groupstack[-1].parameters.append(param)
                else:
                    params.append(param)

                if param.is_group_header:
                    groupstack.append(param)

                while len(groupstack) > 0 and len(groupstack[-1]) == groupstack[-1].group_size:
                    groupstack.pop(-1)

            assert len(groupstack) == 0

            # now expand the parameters in a non-recursive manner
            # we use params as a queue for that purpose:
            # parameters are popped from the head
            bitposition = self.pid['PID_DFHSIZE'].value * 8
            while len(params) > 0:
                param = params.pop(0)
                assert param.vpd['VPD_FIXREP'].rawvalue == '0'
                bitposition += param.vpd['VPD_OFFSET'].value
                fixed = param.as_fixed(bitposition)
                bitposition += param.paramtype.bitwidth

                if param.is_group_header:
                    # the group's parameters are inserted at the position in
                    # the queue where the group parameter used to be (i.e. at
                    # the head)
                    # TODO - vpd['VPD_FIXREP'] should be used if set
                    params = param.parameters*fixed.raw + params
                self.parameters.append(fixed)

        self.parameters.sort()
        self._parsed = True

    @property
    def unmapped(self):
        """Bytes at the end of the packet that have not been mapped to any parameters

        This does *not* include the last 2 bytes of the CRC
        """
        self.parse_parameters()
        last_param = self.parameters[-1]
        next_bit = last_param.byte_offset*8 \
                 + last_param.bit_offset \
                 + last_param.paramtype.bitwidth \
                 + 1
        next_byte = next_bit // 8
        next_bit = next_bit % 8

        if next_byte + 2 >= len(self.pus.raw):
            # this is where the CRC starts, so there's nothing unmapped here
            return bytes()

        blob = self.pus.raw[next_byte:-2]

        if next_bit > 0:
            blob = struct.pack('=b', (blob[0] & (2**(8-next_bit)-1))) + blob[1:]

        return blob

    def __len__(self):
        self.parse_parameters()
        return len(self.parameters)

    def has(self, item):
        """Whether or not ``item`` is part of this packet.

        ``item`` can either be of type ``int`` and refer to an absolute
        position inside the packet or it can be of type ``str`` and refer
        to the identifier of a parameter.

        For example: ``packet.has('CY12345')``
        """
        self.parse_parameters()
        if isinstance(item, int):
            return 0 <= item < len(self.parameters)
        return len([p for p in self.parameters if p.name == item]) > 0

    def get(self, item):
        """Get the parameter ``item`` from the packet.

        ``item`` can either be of type ``int`` and refer to an absolute
        position inside the packet or it can be of type ``str`` and refer
        to the identifier of a parameter.

        For example: ``packet.get('CY12345')``
        """
        self.parse_parameters()
        if isinstance(item, int):
            return self.parameters[item]
        matching = [p for p in self.parameters if p.name == item]
        if len(matching) == 0:
            raise RuntimeError(f"No such parameter '{item}'")
        return matching[0]

    def get_all(self, name):
        """Returns a list of all parameters that match ``name``"""
        self.parse_parameters()
        return [p for p in self.parameters if p.name == name]

    def set(self, item, rawvalue):
        """Set the parameter ``item`` to ``rawvalue``"""
        raise RuntimeError("Not supported for TMs")

    def iter(self):
        """Iterate through all parameters"""
        self.parse_parameters()

        for param in self.parameters:
            yield param

    def synthetics(self):
        """Iterate through all applicable synthetic parameters"""
        for synthname in sorted(self.scos.synthetics_in_spid.get(self.spid, [])):
            yield self.scos.synthetics[synthname].evaluate(self)


class TMParameter(Parameter):
    """An SCOS PUS TM parameter

    ``pcf`` is the ``TableRow`` instance applicable to this TMParameter.
    """
    def __init__(self, tmpacket, pcf):
        super().__init__(tmpacket, pcf)
        self.blob = b''

    def get_data(self, byte_offset, bit_offset):
        """Get this parameter's data from the packet at the byte and bit offset

        Sets ``self.blob`` and also returns it
        """
        self.blob = self.packet.pus.get(self.paramtype.bitwidth,
                                        byte_offset,
                                        bit_offset)
        return self.blob

    def get_raw(self):
        """Implements Parameter.get_raw"""
        return self.paramtype.unpack(self.blob)

    def get_hex(self):
        """Implements Parameter.get_hex"""
        return self.blob.hex()

    def sorting(self):
        """Used for sorting"""
        return (9999, 9)

    def __lt__(self, other):
        return self.sorting() < other.sorting()


class TMInvalidParameter(TMParameter):
    """A parameter that was expected to be in this packet but could not be unpacked"""
    def __init__(self, tmpacket, pcf, exc):
        super().__init__(tmpacket, pcf)
        self.exc = exc
        """The exception that was raised while attempting to unpack the parameter"""


class TMFixedParameter(TMParameter):
    """A TM parameter in a fixed structure (plf)

    ``plf`` can be either a row from the PLF table or a tuple with
    ``byte_offset`` and ``bit_offset``.
    """
    def __init__(self, tmpacket, pcf, plf):
        super().__init__(tmpacket, pcf)
        if isinstance(plf, (tuple, list)):
            byte_offset, bit_offset = plf
        else:
            byte_offset = plf['PLF_OFFBY'].value
            bit_offset = plf['PLF_OFFBI'].value
        self.byte_offset = byte_offset
        self.bit_offset = bit_offset
        self.get_data(byte_offset, bit_offset)

    def sorting(self):
        """The tuple used for sorting"""
        return (self.byte_offset, self.bit_offset)


class TMVariableParameter(TMParameter):
    """A TM parameter in a variable packet structure (vpd)"""
    def __init__(self, tmpacket, pcf, vpd):
        super().__init__(tmpacket, pcf)
        self.vpd = vpd
        self.parsed = False
        self.repeat_counter = 0
        self.parameters = []

    def as_fixed(self, bitposition):
        """Return a fixed parameter, given this bit position in the packet"""
        return TMFixedParameter(self.packet, self.pcf, (bitposition//8, bitposition%8))

    @property
    def group_size(self):
        """How many parameters are part of this group"""
        return self.vpd['VPD_GRPSIZE'].value

    @property
    def is_group_header(self):
        """Whether or not this parameter is indicating the start of a group"""
        return self.group_size > 0

    def __len__(self):
        """Count the number of parameters that are in this group"""
        if not self.is_group_header:
            return 0
        return sum(1 + len(p) for p in self.parameters)
