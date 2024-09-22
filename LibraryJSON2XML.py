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

from sys import argv
from json import loads
import xml.etree.ElementTree as ET

def convertJSON(jsonLibrary):
    print("Convert JSON")
    
    xmlLibrary = ET.Element("library")
    xmlLibrary.attrib["name"] = jsonLibrary["name"]
    
    for group in jsonLibrary["groups"]:
        propGroup = ET.SubElement(xmlLibrary, "prop-group")
        if group["name"] != None:
            propGroup.attrib["name"] = group["name"]
        else:
            propGroup.attrib["name"] = ""
        for prop in group["props"]:
            propElement = ET.SubElement(propGroup, "prop")
            propElement.attrib["name"] = prop["name"]

            propMesh = ET.SubElement(propElement, "mesh")
            propMesh.attrib["file"] = prop["mesh"]["file"]

    return ET.ElementTree(xmlLibrary)

with open(argv[1], "r") as jsonFile:
    jsonData = jsonFile.read()
    jsonData = loads(jsonData)
    xmlData = convertJSON(jsonData)
    xmlData.write(argv[2])