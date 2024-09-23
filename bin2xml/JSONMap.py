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

from json import dump

class JSONMap:
    def __init__(self):
        self.staticGeometry = []
        self.collisionGeometry = []
    
    def addProp(self, libraryName, groupName, name, textureName="", position=(0.0,0.0,0.0), rotation=(0.0,0.0,0.0)):
        positionX, positionY, positionZ = position
        rotationX, rotationY, rotationZ = rotation

        prop = {}
        prop["position"] = [positionX, positionY, positionZ]
        prop["rotation"] = [rotationX, rotationY, rotationZ]
        prop["textureName"] = textureName
        prop["libraryName"] = libraryName
        prop["groupName"] = groupName
        prop["name"] = name

        self.staticGeometry.append(prop)

    def addCollisionBox(self, size, position, rotation):
        pass

    def addCollisionPlane(self, width, length, position, rotation):
        pass

    def addCollisionTriangle(self, v0, v1, v2, position, rotation):
        pass

    def exportJSON(self, fileName):
        print("Export JSON")

        mapData = {}
        mapData["staticGeometry"] = self.staticGeometry
        mapData["collisionGeometry"] = self.collisionGeometry
        with open(fileName, "w") as jsonFile:
            dump(mapData, jsonFile)