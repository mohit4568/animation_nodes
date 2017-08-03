from bpy.props import *
from . base import SocketTemplate
from ... utils.attributes import getattrRecursive
from ... sockets.info import toIdName as toSocketIdName

class DataTypeSelectorSocket(SocketTemplate):
    def __init__(self, name, identifier, propertyName):
        self.name = name
        self.identifier = identifier
        self.propertyName = propertyName

    @classmethod
    def newProperty(cls, default = "Float"):
        # TODO: Check if default is a valid type
        return StringProperty(default = default)

    def create(self, node, sockets):
        dataType = getattrRecursive(node, self.propertyName)
        socketIdName = toSocketIdName(dataType)
        return sockets.new(socketIdName, self.name, self.identifier)

    def getSocketIdentifiers(self):
        return {self.identifier}

    def getRelatedPropertyNames(self):
        return {self.propertyName}

    def apply(self, node, socket):
        currentType = socket.dataType
        linkedDataTypes = tuple(sorted(socket.linkedDataTypes))
        if len(linkedDataTypes) == 0:
            return {self.propertyName : currentType}, set()
        else:
            linkedType = linkedDataTypes[0]
            return {self.propertyName : linkedType}, {self.propertyName}
