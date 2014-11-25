import maya.cmds as cmds
from rigFunctions import name
from rigWorkshop.ws_functions.logger import logger

def autoRotoWheel( driver=None, driven = None, dia = None ):
    """ creating auto rotate wheel"""

    #checking
    assert cmds.objExists(driver), (driver + "does not exist!!")
    assert cmds.objExists(driver), (driven + "does not exist!!")

    
    PI = 3.14
    #Get diameter of wheel
    diameterMD = cmds.shadingNode('multiplyDivide', asUtility=True, name= name.getSide(driven)+ "_" + name.getDescription(driven) + 'wheelCirc_MD')
    #diameterMD input
    cmds.setAttr(diameterMD+'.input1.input1X', dia)
    cmds.setAttr(diameterMD+'.input2.input2X', PI)
    
    #Get distance traveled for each degree of rotation
    distanceMD = cmds.shadingNode('multiplyDivide', asUtility=True, name= name.getSide(driven)+ "_" + name.getDescription(driven) + 'wheelDistance_MD')
    # distanceMD input
    cmds.connectAttr(driver+'.tz', distanceMD+'.input1X')
    cmds.setAttr(distanceMD+'.input2X', 360)
    
    #Multiply distance by trans X of C_baggageCartSecondary0_CTL
    rotateSecMD = cmds.shadingNode('multiplyDivide', asUtility=True, name= name.getSide(driven)+ "_" + name.getDescription(driven) + 'wheelRotate_MD')
    cmds.setAttr(rotateSecMD+'.operation', 2)
    # rotateSecMD inputs
    cmds.connectAttr(distanceMD+'.outputX', rotateSecMD+'.input1X')
    cmds.connectAttr(diameterMD+'.outputX', rotateSecMD+'.input2X')
    # rotateSecMD output
    cmds.connectAttr(rotateSecMD+'.outputX', driven+'.rx')


