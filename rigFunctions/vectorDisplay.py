import maya.cmds as cmds
import maya.OpenMaya as om
import math
from rigWorkshop.ws_user.jun.rigFunctions.rigCommand import rigCommand
from rigFunctions import name, attribute

class VectorDisplay(rigCommand):
    """visualize vector
    
    how to use:
    from rigWorkshop.ws_user.jun.rigFunctions import vectorDisplay
    reload(vectorDisplay)
    b = vectorDisplay.VectorDisplay(moduleName= "vec7", position0=(0,0,0), position1=(2, 4, 2), colorIndex=13)
    """
    def __init__(self, charType = "HUMAN", 
                 moduleName = "vector", 
                 side = "C", 
                 version = 2,
                 position0=None,
                 position1=None,
                 colorIndex=14
                 ):
        """
        @param
        str charType: specify the name of character type
        str mouduleName: specify module name
        int version: specify the version
        tuple position: specify the position
        tuple position: specify the position
        int colorIndex: specify the color index
        """
        super(VectorDisplay, self).__init__(charType = charType, 
                                            moduleName = moduleName, 
                                            side = side, 
                                            version = version)
        rigCommand.create(self)
        
        #arg
        self.moduleName = moduleName
        self.position0  = position0
        self.position1  = position1
        self.colorIndex = colorIndex
        self.side       = side
        
        #vars
        self.cluster    = []
        self.drawLine()
        
    def drawLine(self):
        """
        draw line between two position
        """
        
        if self.position0 == None or self.position1 == None:
            om.MGlobal.displayError("please specify the two position")
            return
        
        #create curve
        CRV = cmds.curve( d=1, p=[self.position0, self.position1], k=[0, 1], n= self.side + "_"+ self.moduleName + "_" + "CRV")
        
        #create cone and move pivot
        cone = cmds.polyCone(ch=False, o=True, r=0.05, h=0.1, cuv=3, n= self.side + "_"+ self.moduleName + "_" + "GEO")
        cmds.move(0, 0.05, 0, cone[0] + ".scalePivot", r=True )
        cmds.move(0, 0.05, 0, cone[0] + ".rotatePivot", r=True )
        
        objs = [CRV, cone]
        for obj in objs:    
            shapeNodes = cmds.listRelatives(obj, shapes=True)
            for shape in shapeNodes:
                try:
                    cmds.setAttr("{0}.overrideEnabled".format(shape), True)
                    cmds.setAttr("{0}.overrideColor".format(shape), self.colorIndex)
                except:
                    om.MGlobal.displayWarning("Failed to override color: {0}".format(shape))    
    
        #create cluster both end
        for i in range(2):
            clusterName = name.uniqueName(self.side + "_"+ self.moduleName + "_" + "CLT")
            clusters = cmds.cluster("%s.cv[%d]" % (CRV,i), n= self.side + "_"+ clusterName + "_" + "CLT" )
            print clusters
            cmds.setAttr("%s.visibility" % clusters[1], 0)
            self.cluster.append(clusters[1])
      
        #create locator
        startLoc = cmds.spaceLocator(p=(0, 0, 0), n= self.side + "_"+ self.moduleName + "_" + "LOC")
        cmds.move(self.position0[0], self.position0[1], self.position0[2], startLoc)
        endLoc = cmds.spaceLocator(p=(0, 0, 0), n= self.side + "_"+ self.moduleName + "_" + "LOC")
        cmds.move(self.position1[0], self.position1[1], self.position1[2], endLoc)
    
        #create annotation
        annotation = cmds.annotate( endLoc, tx='position:%s' % `self.position1`, p=self.position1)
        annotation = cmds.listRelatives(annotation, p=True)
        annotation = cmds.rename(annotation, self.side + "_"+ self.moduleName + "_" + "ANT")
        shape = cmds.listRelatives(annotation, shapes=True)
        cmds.setAttr("{0}.overrideEnabled".format(shape[0]), True)
        cmds.setAttr("{0}.overrideColor".format(shape[0]), self.colorIndex) 
               
        #create point locator
        cmds.pointConstraint(startLoc, self.cluster[0], offset=(0, 0, 0), weight=1, mo=False)
        cmds.pointConstraint(endLoc, self.cluster[1], offset=(0, 0, 0), weight=1, mo=False)
        cmds.pointConstraint(endLoc, annotation, offset=(0, 0, 0), weight=1, mo=False)
       
        cmds.pointConstraint(self.cluster[1], cone, offset=(0, 0, 0), weight=1, mo=False)
        cmds.aimConstraint(self.cluster[0], cone, offset=(0, 0, 0), weight=1, aimVector=(0, -1, 0),  upVector=(0, 1, 0), worldUpType="vector", worldUpVector=(0, 1, 0))
        
        #parenting
        cmds.parent(endLoc, startLoc)
        cmds.parent(annotation, startLoc)
        cmds.parent(self.cluster[0], startLoc)
        cmds.parent(self.cluster[1], startLoc)
        cmds.parent(cone, startLoc)
        cmds.parent(startLoc, self.groupNode)
        cmds.parent(CRV, self.groupNode)
        
        #cleanup
        attribute.lockAndHide(CRV, ['t', 'r', 's', 'v'], False)
        cmds.setAttr("RIG_GRP.overrideDisplayType", 0)
        cmds.setAttr(endLoc[0] + ".visibility", 0)

        return startLoc, endLoc 

    def pntLocator(self):
        """
        create locator at position 0
        """
        if self.position0 == None:
            om.MGlobal.displayError("please specify the two position")
            return
        
        #create locator
        startLoc = cmds.spaceLocator(p=(0, 0, 0), n=self.side + "_"+ self.moduleName + "_" + "LOC")
        cmds.move(self.position0[0], self.position0[1], self.position0[2], startLoc)            
        
        #parenting
        cmds.parent(startLoc, self.groupNode)
        
        return startLoc
                
