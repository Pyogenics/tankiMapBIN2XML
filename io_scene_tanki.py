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

import bpy
from bpy.props import StringProperty
from bpy_extras.io_utils import ImportHelper

import xml.etree.ElementTree as ET
from pathlib import Path

bl_info = {
    "name": "Tanki map importer",
    "description": "Tool to import Tanki Online maps into blender",
    "author": "Pyogenics https://www.github.com/Pyogenics",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "location": "File > Import",
    "doc_url": "https://github.com/Pyogenics/tankiMapBIN2XML",
    "tracker_url": "https://github.com/Pyogenics/tankiMapBIN2XML",
    "support": "COMMUNITY",
    "category": "Import",
}

'''
File IO
'''
class XMLProp:
    def __init__(self):
        self.libraryName = ""
        self.groupName = ""
        self.name = ""
        self.rotationZ = 0.0
        self.textureName = ""
        self.position = (0.0, 0.0, 0.0)

    def read(self, xmlData):
        self.libraryName = xmlData.attrib["library-name"]
        self.groupName = xmlData.attrib["group-name"]
        self.name = xmlData.attrib["name"]

        rotationData = xmlData.find("rotation")
        self.rotationZ = float(rotationData.find("z").text)
        self.textureName = xmlData.find("texture-name").text
        positionData = xmlData.find("position")
        positionX = float(positionData.find("x").text)
        positionY = float(positionData.find("y").text)
        positionZ = float(positionData.find("z").text)
        self.position = (positionX, positionY, positionZ)

class XMLMap:
    def __init__(self):
        self.staticGeometry = []
        self.collisionGeometry = []

    def parseVersion1(self, xmlData):
        print(f"Parse version 1")

        staticGeometryData = xmlData.find("static-geometry")
        for propData in staticGeometryData:
            prop = XMLProp()
            prop.read(propData)
            self.staticGeometry.append(
                prop
            )

    def read(self, xmlData):
        print("Reading XML map")        

        version = xmlData.attrib["version"] # XXX: Handle maps with no version attrib
        print(xmlData.attrib)
        print(f"Found version {version}")

        if version == "1.0.Light":
            self.parseVersion1(xmlData)
        else:
            raise RuntimeError(f"Unsupported map XML version: {version}")

class XMLLibraryProp:
    def __init__(self):
        self.meshPath = None

    def parse(self, folderPath, xmlData):
        # TODO: some props contain <sprite> instead!
        meshData = xmlData.find("mesh")
        if meshData != None:
            meshFile = meshData.attrib["file"]
            self.meshPath = folderPath / meshFile

        # TODO: parse textures

class XMLLibrary:
    def __init__(self):
        # Contains {"libraryName": {"propGroup": {"propName": prop, "propName": prop}}} 
        self.libraries = {}

    def getProp(self, libraryName, groupName, propName):
        return self.libraries[libraryName][groupName][propName]

    def loadLibrary(self, folderPath, xmlPath):
        xmlData = ET.parse(xmlPath).getroot()
        
        libraryName = xmlData.attrib["name"]
        
        # Read prop groups and their props
        library = {}
        for propGroupData in xmlData:
            propGroupName = propGroupData.attrib["name"]
            library[propGroupName] = {}
            for propData in propGroupData:
                propName = propData.attrib["name"]
                prop = XMLLibraryProp()
                prop.parse(folderPath, propData)
                library[propGroupName][propName] = prop
        self.libraries[libraryName] = library

    # Recursive function
    def loadChildren(self, path):
        # Check for library.xml and load it
        xmlPath = path / "library.xml"
        if xmlPath.exists():
            self.loadLibrary(path, xmlPath)

        # TODO: images.xml

        # Check sub folders
        for subPath in path.iterdir():
            if subPath.is_dir(): self.loadChildren(subPath)

    def load(self, path):
        print(f"Loading library from {path}")
        self.loadChildren(path)
        print(f"Loaded {len(self.libraries)} libraries")


'''
Blender IO
'''
class ImportTanki(bpy.types.Operator, ImportHelper):
    bl_idname = "tankionline.importmap"
    bl_label = "Import map"

    filter_glob: StringProperty(default="*.xml", options={'HIDDEN'})

    def invoke(self, context, event):
        return ImportHelper.invoke(self, context, event)

    def execute(self, context):
        print("Begin map import")

        # Library setup
        print("Setup libraries")
        libraryPath = context.preferences.addons[__name__].preferences.libraryPath
        libraryPath = Path(libraryPath)
        library = XMLLibrary()
        library.load(libraryPath)

        with open(self.filepath, "r") as file:
            mapData = ET.parse(self.filepath).getroot()
            print(mapData)
            tankiMap = XMLMap()
            tankiMap.read(mapData)

            # Begin loading the map into blender
            for mapProp in tankiMap.staticGeometry:
                propData = library.getProp(mapProp.libraryName, mapProp.groupName, mapProp.name)
                if propData.meshPath != None:
                    meshPath = str(propData.meshPath)
                print(meshPath)
                bpy.ops.import_scene.max3ds(filepath=meshPath)

        return {"FINISHED"}

'''
UI
'''
class TankiImporterPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    libraryPath: StringProperty(
        name="Library folder",
        subtype='FILE_PATH',
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="Map importer settings")
        layout.prop(self, "libraryPath")


def menu_func_import(self, context):
    self.layout.operator(ImportTanki.bl_idname, text="Tanki Online map (.xml)")

classes = [
    ImportTanki,
    TankiImporterPreferences
]

def register():
    for c in classes:
        bpy.utils.register_class(c)

    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)

    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)