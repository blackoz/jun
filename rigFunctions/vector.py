import maya.OpenMaya as om
import math

#Vector
def vectorAxis(axis = "x"):
    """ return axis as cartesian
        @arg
        string axis
    """
    if axis == "x":
        vec = om.MVector.xAxis
        return vec.x, vec.y, vec.z
    elif axis == "y":
        vec = om.MVector.yAxis
        return vec.x, vec.y, vec.z
    elif axis == "z":
        vec = om.MVector.zAxis
        return vec.x, vec.y, vec.z
    elif axis == "-x":
        vec = om.MVector.xNegAxis
        return vec.x, vec.y, vec.z
    elif axis == "-y":
        vec = om.MVector.yNegAxis
        return vec.x, vec.y, vec.z
    elif axis == "-z":
        vec = om.MVector.zNegAxis
        return vec.x, vec.y, vec.z

def dotproduct(v, w):
    x, y, z = v
    X, Y, Z = w
    return x*X + y*Y + z*Z

def length(v):
    x, y, z = v
    return math.sqrt(x*x + y*y + z*z)
    
def unit(v):
    x, y, z = v
    mag = math.sqrt(x*x + y*y + z*z)
    return (x/mag, y/mag, z/mag)

def distance(p0, p1):
    return length(sub(p0, p1))
    
def scale(v, sc):
    x, y, z = v
    return (x*sc, y*sc, z*sc)
    
def add(v, w):
    x, y, z = v
    X, Y, Z = w
    return (x+X, y+Y, z+Z)

def sub(v, w):
    x, y, z = v
    X, Y, Z = w
    return (x-X, y-Y, z-Z) 

def vector(p0, p1):
    x, y, z = p0
    X, Y, Z = p1
    return (X-x, Y-y, Z-z)

# Dot product
def angle(vec1, vec2, returnAs="radians"):
    """ return angle between two vectors
    
        @arg
        vector vec1
        vector vec2
        string returnAs: radians or degrees
        
        usage:
        v0 = om.MVector( 1.0, 0.0, 0.0 );
        v1 = om.MVector( 0.0, 1.0, 0.0 );
        angle(v0, v1, "degrees")
    """
    angle = math.acos(dotproduct(vec1, vec2) / (length(vec1) * length(vec2)))
    if returnAs == "radians":
        return math.radians(angle)
        
    elif returnAs == "degrees":
        return math.degrees(angle)

def crossProduct(vec1, vec2):
    vec3 = [vec1[1]*vec2[2] - vec1[2]*vec2[1],
         vec1[2]*vec2[0] - vec1[0]*vec2[2],
         vec1[0]*vec2[1] - vec1[1]*vec2[0]]

    return vec3    
    
    