#!/usr/bin/env python

from ipaddress import ip_address
import struct

class EndPoint(object):
    def __init__(self, address, udpPort, tcpPort):
        self.address = ip_address(address)
        self.udpPort = udpPort
        self.tcpPort = tcpPort

    def pack(self):
        return [self.address.packed,
                struct.pack(">H", self.udpPort),
                struct.pack(">H", self.tcpPort)]

    def __str__(self):
        return "EP: " + self.address.exploded + " " + str(self.udpPort) + " " + str(self.tcpPort)

    @classmethod
    def unpack(cls, packed):
        # print(str(len(packed)))
        # for e in packed:
        #     print(str(e) + ", " + str(len(e)))
        addr = packed[0]
        udpPort = struct.unpack(">H", packed[1])[0]

        # Not sure why and when this occurs
        if len(packed[2]) != 0:
            tcpPort = struct.unpack(">H", packed[2])[0]
        else:
            tcpPort = 0
        return cls(addr, udpPort, tcpPort)

class PingPacket(object):
    packet_type = b'\x01';
    version = b'\x04';
    def __init__(self, endpoint_from, endpoint_to, timestamp):
        self.endpoint_from = endpoint_from
        self.endpoint_to = endpoint_to
        self.timestamp = timestamp

    def pack(self):
        return [self.version,
                self.endpoint_from.pack(),
                self.endpoint_to.pack(),
                struct.pack(">I", int(self.timestamp))]

    def From(self):
        return self.endpoint_from

    def To(self):
        return self.endpoint_to
    
    def __str__(self):
        return "PingPacket. v" + str(self.version) + ", From: " + str(self.endpoint_from) + ", To: " + str(self.endpoint_to) + ", At: " +  str(self.timestamp)

    @classmethod
    def unpack(cls, packed):
        # TODO: This fails. why?
        # assert(packed[0] == cls.version)
        version = packed[0]
        ep_from = EndPoint.unpack(packed[1])
        ep_to = EndPoint.unpack(packed[2])
        timestamp = struct.unpack(">I", packed[3])[0]
        return cls(ep_from, ep_to, timestamp)

class PongPacket(object):
    packet_type = b'\x02'

    def __init__(self, endpoint_to, echo, timestamp):
        self.endpoint_to = endpoint_to
        self.echo = echo
        self.timestamp = timestamp
        print(str(self.endpoint_to))

    def pack(self):
        return [self.endpoint_to.pack(),
                self.echo,
                struct.pack(">I", int(self.timestamp))]

    def From(self):
        return self.endpoint_to

    def Timestamp(self):
        return self.timestamp

    def __str__(self):
        return "Pong. To: " + str(self.endpoint_to) + ", At: " +  str(self.timestamp)


    @classmethod
    def unpack(cls, packed):
        to = EndPoint.unpack(packed[0])
        echo = packed[1]
        timestamp = struct.unpack(">I", packed[2])[0]
        return cls(to, echo, timestamp)
