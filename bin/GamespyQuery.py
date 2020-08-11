import socket
import time
import struct
import sys
import re

class GamespyV1Query(object):

    def __init__(self, addr, port=23000, timeout=5.0):
        self.ip, self.port, self.timeout = socket.gethostbyname(addr), port, timeout
        self.sock = False

    def disconnect(self):
        if self.sock:
            self.sock.close()
            self.sock = False

    def connect(self):
        self.disconnect()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(self.timeout)
        self.sock.connect((self.ip, self.port))

    def getInfo(self):
        self.connect()

        # request  
        try:
            self.sock.send(b'\\info\\')
            response = self.sock.recv(1400)
        except Exception as e:
            print(e)
            return False

        try:
            response = response[1:].decode('ascii').split('\\')
            result = dict(zip(response[::2], response[1::2]))
            return result

        except Exception as e:
            print(e)
            return False

        return False

class GamespyV2Query(object):

    def __init__(self, addr, port=29900, timeout=5.0):
        self.ip, self.port, self.timeout = socket.gethostbyname(addr), port, timeout
        self.sock = False

    def disconnect(self):
        if self.sock:
            self.sock.close()
            self.sock = False

    def connect(self):
        self.disconnect()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(self.timeout)
        self.sock.connect((self.ip, self.port))

    def getInfo(self):
        self.connect()

        # request  
        try:
            self.sock.send(b'\xFE\xFD\x00\x43\x4F\x52\x59\xFF\x00\x00')
            response = self.sock.recv(1400)
        except Exception as e:
            print(e)
            return False

        try:
            response = response[5:].decode('ascii').split('\x00')
            result = dict(zip(response[::2], response[1::2]))
            return result

        except Exception as e:
            print(e)
            return False

        return False

class GamespyV3Query(object):

    def __init__(self, addr, port=29900, timeout=5.0):
        self.ip, self.port, self.timeout = socket.gethostbyname(addr), port, timeout
        self.sock = False

    def disconnect(self):
        if self.sock:
            self.sock.close()
            self.sock = False

    def connect(self):
        self.disconnect()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(self.timeout)
        self.sock.connect((self.ip, self.port))

    def getInfo(self):
        self.connect()

        # request  
        try:
            timestamp = b'\x10\x20\x30\x40'  # timestamp
            query = b'\xFE\xFD\x00' + timestamp + b'\xFF\x00\x00\x00'
            self.sock.send(query)
            response = self.sock.recv(1400)
        except Exception as e:
            print(e)
            return False

        try:
            response = response[5:-2].decode('ascii').split('\x00')
            result = dict(zip(response[::2], response[1::2]))
            return result

        except Exception as e:
            print(e)
            return False

        return False


if __name__ == '__main__':
    query = GamespyV3Query('fh2.cmp-gaming.com', 29900)
    print(query.getInfo())
    query = GamespyV1Query('176.9.19.239', 23000)
    print(query.getInfo())