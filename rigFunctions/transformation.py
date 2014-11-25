import maya.OpenMaya as om
import maya.cmds as cmds
import math

def MQuaternionRotation(obj, rotateOrder=0, space=1):
    """ get euler rotation.
    
        @param
        string obj: specify the name of object
        int rotateRoder:kXYZ=0, kYZX=1, kZXY=2, kXZY=3, kYXZ=4, kZYX=5
        int space:  kInvalid = 0, kTransform = 1, kPreTransform = 2, kPostTransform = 3,
                      kWorld = 4, kObject = kPreTransform, kLast = 5 
          how to use:
          >>>from rigWorkshop.ws_user.jun.rigFunctions import transformation
          >>>transformation.MQuaternionRotation("pSphere1", 0, 1)
    """

    #rotateOrder = om.MEulerRotation.kXYZ
    #space = om.MSpace.kTransform 

    lista = []
    selectionList = om.MSelectionList()
    selectionList.add(obj)
    selectionList.getSelectionStrings(lista)
    print lista
    #node = om.MObject()
    dagPath= om.MDagPath()
    selectionList.getDagPath(0, dagPath)
    
    #print pathName
    print dagPath.fullPathName()
    transformFn = om.MFnTransform(dagPath)
    rotation = om.MQuaternion()
    transformFn.getRotation(rotation, space)

    #creating MScriptUtil
    doubleArray = om.MScriptUtil()
    doubleArray.createFromDouble(rotation.x, rotation.y, rotation.z, rotation.w)
        
    return om.MDoubleArray(doubleArray.asDoublePtr(), 4)

#how to get euler Rotation
def eulerRotation(obj, rotateOrder=0, space=1):
    """ get euler rotation.
    
    @param
    string obj: specify the name of object
    int rotateRoder:kXYZ=0, kYZX=1, kZXY=2, kXZY=3, kYXZ=4, kZYX=5
    int space:  kInvalid = 0, kTransform = 1, kPreTransform = 2, kPostTransform = 3,
    kWorld = 4, kObject = kPreTransform, kLast = 5 
    how to use:
    >>>from rigWorkshop.ws_user.jun.rigFunctions import transformation
    >>>transformation.eulerRotation("pSphere1", 0, 1)
    """
    
    #rotateOrder = om.MEulerRotation.kXYZ
    #space = om.MSpace.kTransform 
    
    lista = []
    selectionList = om.MSelectionList()
    selectionList.add(obj)
    selectionList.getSelectionStrings(lista)
    print lista
    #node = om.MObject()
    dagPath= om.MDagPath()
    selectionList.getDagPath(0, dagPath)
    
    #print pathName
    print dagPath.fullPathName()
    transformFn = om.MFnTransform(dagPath)
    euler = om.MEulerRotation()
    transformFn.getRotation(euler)
    
    #creating MScriptUtil
    doubleArray = om.MScriptUtil()
    doubleArray.createFromDouble(math.degrees(euler.x), math.degrees(euler.y), math.degrees(euler.z))
    
    return om.MDoubleArray(doubleArray.asDoublePtr(), 3)

def getScale(obj):
    """    get scale value from obj
    
    @param
    string obj: specify the name of object
    
    how to use:
    >>>from rigWorkshop.ws_user.jun.rigFunctions import transformation
    >>>transformation.getScale("pSphere1")
    
    """
    lista = []
    selectionList = om.MSelectionList()
    selectionList.add(obj)
    selectionList.getSelectionStrings(lista)
    print lista
    #node = om.MObject()
    dagPath= om.MDagPath()
    selectionList.getDagPath(0, dagPath)
    
    #print pathName
    print dagPath.fullPathName()
    transformFn = om.MFnTransform(dagPath)
    
    #get MScriptUtil to put simple number
    util=om.MScriptUtil()  
    util.createFromDouble(0.0, 0.0, 0.0)
    s=util.asDoublePtr()
    transformFn.getScale( s )
    scale =util.getDouble(s)
    scaleX = util.getDoubleArrayItem(s, 0)
    scaleY = util.getDoubleArrayItem(s, 1)
    scaleZ = util.getDoubleArrayItem(s, 2)
    return scaleX, scaleY, scaleZ

def getShear(obj):
    """    get Shear value from obj
    
    @param
    string obj: specify the name of object
    
    how to use:
    >>>from rigWorkshop.ws_user.jun.rigFunctions import transformation
    >>>transformation.getShear("pSphere1")
    
    """
    lista = []
    selectionList = om.MSelectionList()
    selectionList.add(obj)
    selectionList.getSelectionStrings(lista)
    print lista
    #node = om.MObject()
    dagPath= om.MDagPath()
    selectionList.getDagPath(0, dagPath)
    
    #print pathName
    print dagPath.fullPathName()
    transformFn = om.MFnTransform(dagPath)
    
    #get MScriptUtil to put simple number
    util=om.MScriptUtil()  
    util.createFromDouble(0.0, 0.0, 0.0)
    s=util.asDoublePtr()
    transformFn.getShear( s )
    shear =util.getDouble(s)
    shearX = util.getDoubleArrayItem(s, 0)
    shearY = util.getDoubleArrayItem(s, 1)
    shearZ = util.getDoubleArrayItem(s, 2)
    return shearX, shearY, shearZ 

