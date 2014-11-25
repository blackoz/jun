#Points
import maya.OpenMaya as om

def cartesianToHomogeneous(x, y ,z):
    "convert the Cartesian to homogeneous coords"    
    pt = om.MPoint(x, y, z)
    pt.homogenize()
    return pt.x, pt.y, pt.z, pt.w

def homogeneousToCartesian(x, y ,z, w, rationalize=False):
    "convert the Cartesian to homogeneous coords"
    pt = om.MPoint(x, y, z, w)
    
    if not rationalize:
        #pt = (x/w, y/w, z/w, 1)
        pt.cartesianize()
        return pt.x, pt.y, pt.z, pt.w    

    else:
        # put w instead of 1 for 4th element
        #pt = (x/w, y/w, z/w, w)
        pt.rationalize()
        return pt.x, pt.y, pt.z, pt.w

def originPoint():
    "point at (0, 0, 0)"
    #point at (0, 0, 0)
    pt = om.MPoint.origin
    return pt.x, pt.y, pt.z