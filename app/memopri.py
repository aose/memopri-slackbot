#!/usr/bin/python3

# https://gist.github.com/marcan/6ea02bc0daf8dcb4acc74024a4df21b8
# install
# python3 -m pip install Pillow
# use
# python3 memopri.py 20241230_testimg.png

import os
import sys, socket, struct
import PIL, PIL.Image, PIL.ImageOps
from dotenv import load_dotenv

DENSITY_MIN = 0
DENSITY_LIGHT = 1
DENSITY_NORMAL = 2
DENSITY_HEAVY = 3
DENSITY_MAX = 4

WHITESPACE_NONE = 0
WHITESPACE_BEFORE = 1
WHITESPACE_AFTER = 2

load_dotenv()
MEMOPRI_IP_ADDRESS = os.getenv("MEMOPRI_IP_ADDRESS")

class MemoPri(object):
    def __init__(self, host, port=16402):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))

    @classmethod
    def find(cls):
        # stx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # srx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # srx.bind(("0.0.0.0", 49168))
        # stx.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # srx.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # stx.connect(("255.255.255.255", 49167))
        # stx.send(b"MEP r2", 0)
        # data, (ip, port) = srx.recvfrom(128)
        # name = data.split(b"\0")[0].decode("utf-8")
        ip = MEMOPRI_IP_ADDRESS
        name = "MEP-F10"
        print("Found printer %s at %s" % (name, ip))
        return cls(ip)

    def cmd(self, cmd, replylen=1):
        self.s.sendall(bytes(cmd))
        v = self.s.recv(replylen)
        print ("< %r" % v)
        return v
    
    def print(self, img, whitespace=WHITESPACE_NONE, density=DENSITY_NORMAL):
        self.cmd([0x1b, 0x5a])
        self.cmd([0x05], 6)
        self.cmd([0x06])
        self.cmd([0x1b, 0x49])
        self.cmd([0x05], 8)
        self.cmd([0x06])
        self.cmd([0x1b, 0x46])
        self.cmd([0x05], 8)
        self.cmd([0x06])
        self.cmd([0x1b, 0x50])
        rows, data = self.format_data(img)
        length = rows * 16
        self.cmd(
            bytes([0x02, 0x80, 0x0c, 0x00, 0x00, 0x00, whitespace, density,
             0x80, 0x00]) + struct.pack("<HHxx", rows, length)
        )
        self.cmd([0x1b, 0x56])
        print("Sending data...")
        for i in range(0, len(data), 0x200):
            self.cmd(data[i:i+0x200])
        print("Printing...")
        self.cmd([0x1b, 0x42])

    def format_data(self, img, dither=True):
        img = img.transpose(PIL.Image.TRANSPOSE)
        img = img.convert("L")
        img = PIL.ImageOps.invert(img)
        img = img.convert("1", dither=(PIL.Image.FLOYDSTEINBERG if dither else PIL.Image.NONE))
        rows = img.height
        assert img.width <= 96
        canvas = PIL.Image.new("1", (128, rows))
        canvas.paste(img, ((128 - img.width)//2, 0))
        data = canvas.tobytes()
        assert len(data) % 0x10 == 0
        if len(data) & 0x1ff:
            data += b'\x00' * (0x200 - (len(data) & 0x1ff))
        assert len(data) % 0x200 == 0
        return rows, data

if __name__ == "__main__":
    m = MemoPri.find()
    m.print(PIL.Image.open(sys.argv[1]))
    print("Done!")
