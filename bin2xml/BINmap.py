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

from .AlternativaProtocol import readPacket, OptionalMask

class BINMap:
    def __init__(self):
        self.atlases = []
        self.batches = []
        self.collisionGeometry = []
        self.collisionGeometryOutsideGamingZone = []
        self.materials = []
        self.spawnPoints = []
        self.staticGeometry = []

    def readAtlases(self, stream, optionalMask):
        print("Reading atlases")

    def readBatches(self, stream, optionalMask):
        print("Reading batches")

    def readCollisionGeometry(self, stream, optionalMask):
        print("Reading collision geometry")

    def readCollisionGeometryOutsideGamingZone(self, stream, optionalMask):
        print("Reading collision geometry outside gaming zone")

    def readMaterials(self, stream, optionalMask):
        print("Reading materials")

    def readSpawnPoints(self, stream, optionalMask):
        print("Reading spawn points")

    def readStaticGeometry(self, stream, optionalMask):
        print("Reading static geometry")

    def read(self, stream):
        print("Reading BIN map")

        # Read packet
        optionalMask = OptionalMask()
        optionalMask.read(stream)
        packet = readPacket(stream)

        # Read data
        if optionalMask.getOptional():
            self.readAtlases(packet, optionalMask)
        if optionalMask.getOptional():
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
            self.readStaticGeometry(packet, optionalMask)