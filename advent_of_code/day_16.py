"""
Classes for managing Day 16 packet seperating.
"""
from dataclasses import dataclass, InitVar, field
from typing import Optional
from advent_of_code import utils


class InvalidPacketError(Exception):
    """Raised when the input value is invalid for making a packet"""

    def __init__(self, message="Binary data is too small."):
        self.message = message
        super().__init__(self.message)


@dataclass(frozen=True, order=True, eq=True)
class PacketHeader:
    """A dataclass for holding the Packet's standard header"""

    version: int
    type_id: int

    def length(self) -> int:
        return 6


@dataclass(frozen=True, order=True, eq=True)
class OperatorPacketInfo:
    """
    When a packet is an Operator packet there will be some
    extra meta information describing the payload.

        If the length type ID is 0, then the next 15 bits are a
        number that represents the total length in bits of the
        sub-packets contained by this packet.

        If the length type ID is 1, then the next 11 bits are a
        number that represents the number of sub-packets immediately
        contained by this packet.
    """

    length_type_id: int
    data_size_bits: str

    def __post_init__(self):
        if self.length_type_id not in [0, 1]:
            raise InvalidPacketError("Length Type ID is invalid.")

        if (self.length_type_id == 0 and len(self.data_size_bits) != 15) or (
            self.length_type_id == 1 and len(self.data_size_bits) != 11
        ):
            raise InvalidPacketError(
                "The number of bits storing the the length is invalid "
                "for this Length Type ID."
            )

    def length(self) -> int:
        return 1 + len(self.data_size_bits)


class Packet(object):
    """Base Packet class"""

    binary_data: InitVar[str]
    header: PacketHeader
    data_bits: str
    operator_info: Optional[OperatorPacketInfo] = field(default=None)

    def __new__(cls, binary_data: str):
        if utils.bin_to_dec(binary_data[3:6]) == 4:
            return object.__new__(LiteralPacket)
        else:
            return object.__new__(OperatorPacket)

    def __init__(self, binary_data):
        """Creates a very basic packet."""
        if len(binary_data) < 11:
            raise InvalidPacketError("Binary data is too small.")

        # create standard packet.
        self.header = PacketHeader(
            utils.bin_to_dec(binary_data[0:3]),  # version
            utils.bin_to_dec(binary_data[3:6]),  # type_id
        )
        self.data_bits = ""
        self.operator_info = None

    def sum_of_version_numbers(self) -> int:
        """
        Returns the version number. Additionally, if this is an OperatorPacket,
        the sum of children version numbers is added.
        """
        sum_version = self.header.version
        if isinstance(self, OperatorPacket):
            sum_version += sum(
                [sp.sum_of_version_numbers() for sp in self.sub_packets]
            )
        return sum_version

    def length(self) -> int:
        """
        Returns the packet length (header, data, and optional operator
        information)
        """
        return (
            self.header.length()
            + len(self.data_bits)
            + (
                self.operator_info.length()
                if self.operator_info is not None
                else 0
            )
        )
    

class LiteralPacket(Packet):
    """Literal packet class."""

    value: str

    def __init__(self, binary_data: str):
        super(LiteralPacket, self).__init__(binary_data)
        if self.header.type_id != 4:
            raise ValueError(
                "A packet with a type != 4 cannot be a LiteralPacket."
            )

        self.data_bits = binary_data[6:]
        self.value = self.parse()
        # print(f"Found: {self}")

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(version={self.header.version}, "
            f"type_id={self.header.type_id}, value={self.value}, "
            f"bits_len={len(self.data_bits)}, bits={self.data_bits})"
        )

    def parse(self, byte_length=5) -> str:
        """
        Converts binary_data into the value string using this logic:

            Packets with type ID 4 represent a literal value. Literal
            value packets encode a single binary number. To do this,
            the binary number is padded with leading zeroes until its
            length is a multiple of four bits, and then it is broken
            into groups of four bits. Each group is prefixed by a 1
            bit except the last group, which is prefixed by a 0 bit.

        Sets the parsed value binary to string representation of
        value to self.value.
        Returns:None
        """
        bytes: list[str] = [
            self.data_bits[idx:idx+byte_length]
            for idx in range(0, len(self.data_bits), 5)
            if idx + 5 <= len(self.data_bits)
        ]

        actual_bits = ""
        for byte in bytes:
            actual_bits += byte
            if byte[0] == "0":
                break

        # set object properties
        self.data_bits = actual_bits
        return self.compute_value_from_bits()

    def compute_value_from_bits(self, byte_length=5) -> int:
        """Returns the value of the bytes when combined."""
        valid_bits = "".join(
            [x for idx, x in enumerate(self.data_bits) if idx % byte_length]
        )
        return str(int(valid_bits, 2))


class OperatorPacket(Packet):
    """Operator Packet"""

    sub_packets: list[Packet] = field(default_factory=list())

    def __init__(self, binary_data: str):
        super(OperatorPacket, self).__init__(binary_data)

        if self.header.type_id == 4:
            raise InvalidPacketError("Invalid binary for OperatorPacket.")
        else:
            self.operator_info = OperatorPacketInfo(
                int(binary_data[6]),  # op type
                # data length info
                binary_data[7:22]
                if int(binary_data[6]) == 0
                else binary_data[7:18],
            )

        data_bits_idx_start = (
            self.header.length() + self.operator_info.length()
        )
        self.data_bits = binary_data[data_bits_idx_start:]
        self.sub_packets = []

        if self.operator_info.length_type_id == 0:
            if utils.bin_to_dec(binary_data[7:22]) > len(self.data_bits):
                raise InvalidPacketError(
                    "Expected data size: "
                    f"{utils.bin_to_dec(binary_data[7:22])} "
                    f"found {len(self.data_bits)}"
                )
            self.parse_data_typ0()
        elif self.operator_info.length_type_id == 1:
            if utils.bin_to_dec(binary_data[7:18]) * 11 > len(self.data_bits):
                raise InvalidPacketError(
                    "Expected data size > "
                    "{utils.bin_to_dec(binary_data[7:18])*11} "
                    f"found {len(self.data_bits)}"
                )
            self.parse_data_typ1()
        else:
            raise NotImplementedError(
                "No handling for operator type not in [0,1]"
            )
        # print(f"Found: {self}")

    def __repr__(self) -> str:
        pval = (
            f"{self.__class__.__name__}("
            f"version={self.header.version}, "
            f"type_id={self.header.type_id}, "
            f"operator_type={self.operator_info.length_type_id}, "
            f"packet_size={self.length()}, "
            f"bits={self.data_bits})"
        )
        for subp in self.sub_packets:
            pval = pval + f"\n\t -> {subp}"
        return pval

    def parse_data_typ0(self):
        """
        Converts binary_data into the value string using this logic:

            If the length type ID is 0, then the next 15 bits are a
            number that represents the total length in bits of the
            sub-packets contained by this packet.
        """
        # we know the size of packet because it is stored in the header
        packet_data_size = utils.bin_to_dec(self.operator_info.data_size_bits)
        self.data_bits = self.data_bits[:packet_data_size]

        remaining_bits = self.data_bits[:]  # copy it.
        while packet_data_size > 0 and len(remaining_bits) >= 11:
            try:
                sub_packet = Packet(remaining_bits)
            except InvalidPacketError as err:
                print(remaining_bits)
                print(err.message)
                return

            self.sub_packets.append(sub_packet)
            remaining_bits = remaining_bits[sub_packet.length():]
            packet_data_size = packet_data_size - sub_packet.length()

    def parse_data_typ1(self):
        """
        Converts binary_data into the value string using this logic:

            If the length type ID is 1, then the next 11 bits are a
            number that represents the number of sub-packets immediately
            contained by this packet.

        Returns:None
        """

        sub_packet_counter = utils.bin_to_dec(
            self.operator_info.data_size_bits
        )
        remaining_bits = self.data_bits[:]
        valid_bit_counter = 0
        while sub_packet_counter > 0 and len(remaining_bits) >= 11:
            # print(f"sub packet counter: {sub_packet_counter}")
            try:
                sub_packet = Packet(remaining_bits)
            except InvalidPacketError as err:
                print(remaining_bits)
                print(err.message)
                break

            self.sub_packets.append(sub_packet)
            valid_bit_counter = valid_bit_counter + sub_packet.length()
            remaining_bits = remaining_bits[sub_packet.length():]
            sub_packet_counter = sub_packet_counter - 1

        self.data_bits = self.data_bits[:valid_bit_counter]
