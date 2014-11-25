import maya.cmds as cmds
import maya.OpenMaya as om
def pntLocator(p0=None, colorIndex=14):
    """
    draw line between two position
    """
    if p0 == None:
        om.MGlobal.displayError("please specify the two position")
        return
    
    #create locator
    startLoc = cmds.spaceLocator(p=(0, 0, 0))
    cmds.move(p0[0], p0[1], p0[2], startLoc)

