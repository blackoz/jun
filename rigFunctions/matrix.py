# Python code
# matrixutils.py

import maya.cmds as mc
import maya.OpenMaya as om

def listToMMatrix(mList):
    """
    Convert a list of 16 floats into a MMatrix object
    Mainly a helper for getMMatrix()
    """
    if len(mList) != 16:
        raise Exception("Argument 'mList' needs to have 16 float elements")
    m = om.MMatrix()
    om.MScriptUtil.createMatrixFromList(mList, m)
    return m

def mMatrixToList(matrix):
    """
    Convert a MMatrix object into a list of 16 floats.
    Mainly a helper for matrixXform()
    """
    return [matrix(i,j) for i in range(4) for j in range(4)]

def getMMatrix(node, matrixType):
    """
    Get matrix data from a node, and return as MMatrix object.
    """
    good = ["matrix", "inverseMatrix", "worldMatrix", "worldInverseMatrix",
            "parentMatrix", "parentInverseMatrix", "xformMatrix"]
    if matrixType not in good:
        raise Exception("Argument 'matrixType' is an invalid matrix attr type."+
                        "  Please choose from: " + ' '.join(good))
    return listToMMatrix(mc.getAttr(node+"."+matrixType))

def matrixXform(node, matrix, spaceType):
    """
    Transform a Maya DAG (transform, joint) object based on a given matrix value,
    via the mel 'xform' command.

    matrix : either a maya.OpenMaya.MMatrix object, or a list with 16 entries.
    spaceType :  either 'worldSpace' or 'objectSpace'
    """
    mList = None
    if type(matrix) is type(om.MMatrix()):
        mList = mMatrixToList(matrix)
    elif type(matrix) is type(list()) and len(matrix) == 16:
        mList = matrix
    else:
        raise TypeError("Arg 'matrix' either needs to be a maya.OpenMaya.MMatrix object, or list with 16 entries")

    if(spaceType == "worldSpace"):
        mc.xform(node, worldSpace=True, matrix=mList)
    elif(spaceType == "objectSpace"):
        mc.xform(node, objectSpace=True, matrix=mList)
    else:
        raise ValueError("spaceType arg is either 'worldSpace' or 'objectSpace', passed value is '%s'"%spaceType)
    
def printMMatrix(matrix):
    """
    print matrix 4*4 format
    """
    matrix = [[matrix(i, j) for j in range(int(4))] for i in range(int(4))]
    for i in range(4):
        print matrix[i]
        
def matchPosition(source, target):
    """how to use:
        matchPosition("pSphere1", "locator1")"""
    #creating Mpoint and MMatrix object
    p0 = om.MPoint()
    p1 = om.MPoint()
    mat = om.MMatrix()
    
    #get source matrix
    mat = matrix.getMMatrix(source, "matrix")
    #get tartget position
    targetPos = cmds.xform(target, q=True, t=True)
    #put it Mpoint
    p0 = om.MPoint(targetPos[0], targetPos[1], targetPos[2])

    #get position
    p1 = p0*mat
    #moving targeting to source position
    cmds.xform(target, t=[p1.x, p1.y, p1.z], ws=True)
    
def matchPosMatrix(source, target):
    """copy the matrix from source to target
    
    @param
    str source: specify source object
    str target: specify target object
    
    how to use:
    from rigWorkshop.ws_user.jun.utils import matrix
    matrix.matchPosMatrix("pCylinder1", "pCylinder2")
    """
    sourceObj = pm.PyNode(source)
    targetObj = pm.PyNode(target)
    pos = sourceObj.getMatrix()
    targetObj.setMatrix(pos)
    
def addPosMatrix(source, target):
    """copy the matrix from source to target
    
    @param
    str source: specify source object
    str target: specify target object

    how to use:
    from rigWorkshop.ws_user.jun.utils import matrix
    matrix.addPosMatrix("pCylinder1", "pCylinder2")    
    """
    sourceObj = pm.PyNode(source)
    targetObj = pm.PyNode(target)
    sourcePos = sourceObj.getMatrix()
    targetPos =  targetObj.getMatrix()
    newPos = sourcePos*targetPos
    targetObj.setMatrix(newPos)

