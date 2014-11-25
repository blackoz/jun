import maya.OpenMaya as om
def angle(angle=None, returnType="Radians"):
    
    if type == "Degrees":
        angle = om.MAngle(angle, om.MAngle.kRadians)
        return angle.asDegrees()
    if type == "Radians":
        angle = om.MAngle(angle, om.MAngle.kDegrees)
        return angle.asRadians()   
    

#convert angle unit with lambda func
def degToRad(deg):
    M_PI = 3.14
    DEG_TO_RAD = M_PI/180.0
    return deg*DEG_TO_RAD

def radToDeg(rad):
    #this is not accurate as Mangle because of flaot tolerance
    M_PI = 3.14
    RAD_TO_DEG = 180.0/M_PI
    return rad*RAD_TO_DEG
