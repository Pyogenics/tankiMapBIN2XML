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

import xml.etree.ElementTree as ET

class XMLMap:
    def __init__(self):
        self.map = ET.Element("map", version="1.0.Light")
        self.staticGeometry = ET.SubElement(self.map, "static-geometry")
        self.collisionGeometry = ET.SubElement(self.map, "collision-geometry")

    def addProp(self, libraryName, groupName, name, textureName="", position=(0.0,0.0,0.0), rotationZ=0.0):
        positionX, positionY, positionZ = position
        
        prop = ET.SubElement(self.staticGeometry, "prop")
        prop.attrib["library-name"] = libraryName
        prop.attrib["group-name"] = groupName
        prop.attrib["name"] = name

        rotation = ET.SubElement(prop, "rotation")
        ET.SubElement(rotation, "z").text = str(rotationZ)

        ET.SubElement(prop, "texture-name").text = textureName

        position = ET.SubElement(prop, "position")
        ET.SubElement(position, "x").text = str(positionX)
        ET.SubElement(position, "y").text = str(positionY)
        ET.SubElement(position, "z").text = str(positionZ)

    def addCollisionBox(self, size, position, rotation):
        pass

    def addCollisionPlane(self, width, length, position, rotation):
        pass

    def addCollisionTriangle(self, v0, v1, v2, position, rotation):
        pass

    def exportXML(self, fileName):
        print("Export XML data")

        xmlData = ET.ElementTree(self.map)
        xmlData.write(fileName)