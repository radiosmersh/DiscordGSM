import socket
import time
import struct
import sys
import re
from .helpers import QueryBytes

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
            timestamp = b'\x04\x05\x06\x07'  # timestamp

            query = QueryBytes()
            query.append(b'\xFE\xFD\x09', None)
            query.append(timestamp, None)

            query.append(b'\xFF\x00\x00\x01', None)
            query.set(b'\x00', QueryBytes.BIG_TYPE_BYTE, 1, offset=2)

            self.sock.send(query.buffer)
            response = self.sock.recv(4096)
            response = self.sock.recv(4096)

        except Exception as e:
            print(e)
            return False

        try:
            response = response[16:].decode('unicode_escape').split('\x00\x00\x01player_\x00\x00')
            response = re.sub(r'§.', '', response[0]).replace('\n', ' ') # remove color and next line
            #print(response) # useful output
            kv = response.split('\x00')
            result = {}
            for i in range(0, len(kv), 2):
                result[kv[i]] = kv[i+1]
            return result

        except Exception as e:
            print(e)
            return False

        return False

if __name__ == '__main__':
    query = GamespyV3Query('34.92.81.161', 29903)
    print(query.getInfo())