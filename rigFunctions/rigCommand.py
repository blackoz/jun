from rigFunctions import node, attribute
from rigFunctions.error import RigError
from maya import cmds


#========================================================================================
#CLASS:         rigCommand
#DESCRIPTION:   The base rigCommand. Gathers/created the baseNodes, sets up the nodeCreatorClass 
#               and checks the characterType
#USAGE:         This class should be subclassed rigCommand.__init__(characterType = "HUMAN")
#RETURN:        baseNodes
#REQUIRES:      RigError, check
#AUTHOR:        Catalin Niculescu
#DATE:          06.07.10
#Version        1.0.0
#======================================================================================== 
class rigCommand(object):
    '''
    CLASS:         rigCommand
    DESCRIPTION:   The base rigCommand. Gathers/created the baseNodes, sets up the 
                   nodeCreatorClass and checks the characterType
    USAGE:         This class should be subclassed:
                   rigCommand.__init__(characterType = "HUMAN")
    RETURN:        self.baseNodes
    REQUIRES:      RigError, check
    AUTHOR:        Catalin Niculescu
    DATE:          06.07.10
    Version        1.0.0
    '''
    def __init__(self, charType = None, moduleName = None, side = "C", moduleAttrs = None, color = 4, checkMainCtl = False, version = 1):
        
        self.charType           = charType
        self.moduleName         = moduleName
        self.baseNodes          = None
        self.nodeCreator        = node.node()
        self.groupNode          = None
        self.targetsOffsets     = None
        self.side               = side.upper()
        self.createdControls    = {}
        self.moduleAttrs        = moduleAttrs
        self.inHooks            = {}
        self.outHooks           = {}
        self.targets            = {}
        self.targetDestinations = []
        self.color              = color
        self.sideMlt            = 1.0
        self.checkMainCtl       = checkMainCtl
        self.rnkSide            = "left"
        self.version            = version
        self.rnkTags            = {"rigSection": "", "rigClass": "", "rigGroup": "", "nodeType" : "", 
                                   "mirrorRule": "", "defaultMatrix": "", "rigFunction": "", "rigType": "", 
                                   "part": "", "switchAttributeConnections": "", "ctrlFunction": "", "side": ""}
        
        #check
        self.__check()
        self.__getSideAttrs()
        
    def __check(self):
        if not self.charType:
            raise RigError("No charType specified!")
        if not self.moduleName:
            raise RigError("No moduleName specified!")
        
        #create the baseNodes
        bn = node.baseNodes(charType = self.charType, checkMainCtl = self.checkMainCtl)
        bn.create()
        self.baseNodes = bn.nodes
        
        if self.checkMainCtl:
            self.targetDestinations.append(self.baseNodes["secondaryControlGimbal"])
        
        if not self.baseNodes:
            raise RigError("The baseNodes could not be found!")
    
    def nodeCreatorCleanUp(self):
        self.nodeCreator.setIsHistoricallyInteresting()
        self.nodeCreator.lockAndHide()
        
        for i in self.createdControls:
            if type(self.createdControls[i]).__name__ == "str" or type(self.createdControls[i]).__name__ == "unicode":
                #attribute.lockAndHide(self.createdControls[i], ["t", "r", "s", "v"])
                continue
            else:
                attribute.lockAndHide(self.createdControls[i].control["group"], ["t", "r", "s", "v"])
    
    def setDefaults(self):
        for control in self.createdControls:
            if type(self.createdControls[control]).__name__ == "str" or type(self.createdControls[control]).__name__ == "unicode":
                attribute.setDefaults([self.createdControls[control]])
            else:
                attribute.setDefaults([self.createdControls[control].control["transform"]])
                try:
                    attribute.setDefaults([self.createdControls[control].gimbalControl["transform"]])
                except:
                    pass
                
    def __getSideAttrs(self):
        if self.side == "L":
            self.color = 13
            self.sideMlt = 1.0
            self.rnkSide = "left"
        elif self.side == "R":
            self.color = 6
            self.sideMlt = -1.0
            self.rnkSide = "right"
        else:
            self.color = 22   
            self.sideMlt = 1.0 
            self.rnkSide = "center"
            
    def create(self):
        nc = node.node()
        nodeName = self.side + "_" + self.moduleName + "_M"
        if not cmds.objExists(nodeName):
            self.groupNode = nc.create(node = "module", 
                                       side = self.side, description = self.moduleName, 
                                       skipSelect = 1, parent = self.baseNodes["rig"])
            cmds.setAttr(self.groupNode + ".inheritsTransform", 0)
            
            #targets group
            self.targetsOffsets = nc.create(node = "transform", 
                                       side = self.side, description = self.moduleName + "Targets", 
                                       skipSelect = 1, parent = self.groupNode)
            cmds.setAttr(self.targetsOffsets + ".inheritsTransform", 0)
            
            #module attrs
            attribute.addAttr(node = self.groupNode, attrName = "showJoints", attrType = "short", default = 0, min = 0, max = 1, lock = 0, keyable = 0, channelBox = 1)
            attribute.addAttr(node = self.groupNode, attrName = "jointsDisplayType", attrType = "short", default = 0, min = 0, max = 2, lock = 0, keyable = 0, channelBox = 1)
            attribute.addAttr(node = self.groupNode, attrName = "showRigJoints", attrType = "short", default = 0, min = 0, max = 1, lock = 0, keyable = 0, channelBox = 1)
            attribute.addAttr(node = self.groupNode, attrName = "showLocators", attrType = "short", default = 0, min = 0, max = 1, lock = 0, keyable = 0, channelBox = 1)
            attribute.addAttr(node = self.groupNode, attrName = "showClusters", attrType = "short", default = 0, min = 0, max = 1, lock = 0, keyable = 0, channelBox = 1)
            attribute.addAttr(node = self.groupNode, attrName = "showStuff", attrType = "short", default = 0, min = 0, max = 1, lock = 0, keyable = 0, channelBox = 1)
            attribute.addAttr(node = self.groupNode, attrName = "showMainControls", attrType = "short", default = 0, min = 0, max = 1, lock = 0, keyable = 0, channelBox = 1)
            attribute.addAttr(node = self.groupNode, attrName = "showSecControls", attrType = "short", default = 0, min = 0, max = 1, lock = 0, keyable = 0, channelBox = 1)
            attribute.addAttr(node = self.groupNode, attrName = "version", attrType = "short", default = self.version, lock = 0, keyable = 0, channelBox = 1)
            
            cmds.connectAttr(self.baseNodes["rig"] + ".showSecondaryCtls", self.groupNode + ".showSecControls")
            attribute.lockAndHide(self.groupNode, ["showSecControls"])
            #add custom attrs if needed
            if self.moduleAttrs:
                for attr in self.moduleAttrs:
                    attribute.addAttr(node = self.groupNode, attrName = attr, attrType = "short", default = 0, min = 0, max = 1, lock = 0, keyable = 0, channelBox = 1)
            
            nc.setIsHistoricallyInteresting()
            nc.lockAndHide()
            
            #tag it as a module
            attribute.addTag(self.groupNode, "MODULE", self.side + "_" + self.moduleName)
   
        else:
            self.groupNode = nodeName
            print self.groupNode, " exists already. Using the existing one!"
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
