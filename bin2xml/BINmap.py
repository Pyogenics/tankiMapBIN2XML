'''
Copyright (c) 2024 Pyogenics

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

from .IOTools import unpackStream
from . import AlternativaProtocol

'''
Objects
'''
class AtlasRect:
    def __init__(self):
        self.height = 0
        self.libraryName = ""
        self.name = ""
        self.width = 0
        self.x = 0
        self.y = 0

    def read(self, stream, optionalMask):
        print("Read AtlasRect")
        self.height, = unpackStream(">I", stream)
        self.libraryName = AlternativaProtocol.readString(stream)
        self.name = AlternativaProtocol.readString(stream)
        self.width, self.x, self.y = unpackStream(">3I", stream)

'''
Main objects
'''
class Atlas:
    def __init__(self):
        self.height = 0
        self.name = ""
        self.padding = 0
        self.rects = []
        self.width = 0

    def read(self, stream, optionalMask):
        print(f"Read Atlas {stream.tell()}")
        self.height, unpackStream(">i", stream)
        self.name = AlternativaProtocol.readString(stream)
        self.padding = unpackStream(">I", stream)
        self.rects = AlternativaProtocol.readObjectArray(stream, AtlasRect, optionalMask)
        self.width, = unpackStream(">I", stream)

class BINMap:
    def __init__(self):
        self.atlases = []
        self.batches = []
        self.collisionGeometry = []
        self.collisionGeometryOutsideGamingZone = []
        self.materials = []
        self.spawnPoints = []
        self.staticGeometry = []

    def read(self, stream):
        print("Reading BIN map")

        # Read packet
        packet = AlternativaProtocol.readPacket(stream)
        with open("packet.bin", "wb") as packetFile:
            packetFile.write(
                packet.read()
            )
            packet.seek(0)
        optionalMask = AlternativaProtocol.OptionalMask()
        optionalMask.read(packet)

        # Read data
        if optionalMask.getOptional():
            self.atlases = AlternativaProtocol.readObjectArray(packet, Atlas, optionalMask)

'''        if optionalMask.getOptional():
            self.readBatches(packet, optionalMask)
        if optionalMask.getOptional():
            self.readCollisionGeometry(packet, optionalMask)
        if optionalMask.getOptional():
            self.readCollisionGeometryOutsideGamingZone(packet, optionalMask)
        if optionalMask.getOptional():
            self.readMaterials(packet, optionalMask)
        if optionalMask.getOptional():
            self.readSpawnPoints(packet, optionalMask)
        if optionalMask.getOptional():
            self.readStaticGeometry(packet, optionalMask)'''