from rigWorkshop.ws_user.jun.utils import pyMel
#mel to pymel convertor.
pyMel.mel2pyDialog()


import pymel.core as pm

jnt = pm.joint(n="madeWithpymel")

see(jnt)

# list of transform in order
pm.selected()

pm.selected(flatten=True)
pm.selected(os=True, flatten=True)

#select some joints but it 
pm.selectedNodes() #vs
[n.longName() for n in pm.selected()]

pm.selected(assemblies=True)
pm.ls(assemblies=True)

# 3 cast with pm.PyNode("anything")
geom = pm.PyNode("body")
geomShape = geom.getShape()
see(geomShape)

# 3a you can't pynode an time that doesn't exist.
fightClub = pm.PyNode("fightClub")

#sometimes you will get a list of itmes you need
#to pynode them all and perform operatinos on them.
#like operating on a list of items from some legacy code.
items = map( pm.PyNode, pm.selectedNodes() )

#pyNode always check if the node exists.
badItems = pm.selectedNodes() + ["bob"]
items = map(pm.PyNode, badItems)

#if node exists, put in the list.
fightClubMembers = []
for item in badItems:
    try:
        bob = pm.PyNode(item)
        fightClubMembers.append(bob)
    except:
        print ("Rule one.. we don't talk about %s. Because doesn't exist" % item)


import pymel.core as pm

edges = pm.selected(flatten=True)

edgeA = edges[0]
see(edgesA)
edgeA.connectedVertices()

# list comprehension
verts = [list(e.connectedVertices()) for e in edges ], []

clus = pm.cluster(verts)


bob = ["cindy"] + ["kat", "simon"]

####################
# node type
####################

#joint node
jnt = pm.createNode("joint", n="L_toe_JNT")
jnt = pm.PyNode("L_toe_JNT")

#mult divide node
multDiv = pm.createNode("multiplyDivide")

#typeing checking a mode for comparision
jnt.type() # not used anymore -- collided with some other type method

#recommanded
jnt.nodeType() # use nodeType for comparison
jnt.__class__.__name__.lower()
jnt.nodeType() == "joint"
multDiv.nodeType() == "multiplyDivide"

# so so
type(jnt)
type(multDiv)

help(type(jnt))

#############################
# pymel.core.general.PyNode
#############################

# OpenMaya.MObjectHandle
print jnt.__apihandle__()

# OpenMaya.MObject
print jnt.__apimobject__()

# Openmaya.MDagPath
print jnt.__apimdagpath__()

# OpenMaya.MPlug only an attributes
print jnt.rotate.__apimplug__()

# OpenMayaAnim.MFnIkJoint
print jnt.__apimfn__()

###################################
# PyMel searches for the shape automatically, if there is not method pymel is looking for 
###################################
#generate a cube
cubeTRN, cubeSHP = pm.polyCube(n="cube")
cubeTRN.vtx[1]
cubeTRN.getShape().vtx[1] == cubeTRN.vtx[1]

###################################
# manage Attribute
###################################
import pymel.core as pm

# create the objects
objectA = pm.PyNode("objectA")

# check out the .translateX attr
objectA.translateX

# check out .tx attr same s the translateX
objectA.tx

# compare the long and short names
objectA.tx == objectA.translateX
see(objectA.tx)

#get the value of an attr
rotX = objectA.rotateX.get()
rot = objectA.rotate.get()
pos = objectA.translate.get()

#transforms have -getMatrix() method
#!! more on using Matrices in the next modules on aligning joints !!
a = objectA.getMatrix() # returns a normalize Matrix
print a.formated()
objectA.matrix.get()
help(objectA.getMatrix())

#set the value of an attr
objectA.tx.set(5)
objectA.rotateX.set(45)
objectA.template.set(True)
objectA.template.set(False)

#colors
objectA.overrideEnabled.set(True)
objectA.overrideColor.set(13) #red
objectA.overrideColor.set(17) #yellow
objectA.overrideColor.set(6) #blue
objectA.overrideEnabled.set(False)

#put value as List or tuple
objectA.translate.set([1, 2, 3])
objectA.translate.set((1, 4, 3))
#vector or Point
objectA.rotate.set(pm.dt.Vector(180, -90, 10))
# even if you forget to classify it and give it 3 args
objectA.rotate.set(0, 0, 0)

theAttr = 't'
objectA.attr('%sx' % theAttr).get()

for vec in ['t', 'r']:
    for ch in ['x', 'y', 'z']:
        #objectA.attr("%s%s" % (vec, ch)).set(20)
        objectA.attr("%s%s" % (vec, ch)).unlock()

# eval the last value has long name not short name!!!
objectA.translateX.longName()
#get short name
objectA.translateX.shortName()


#.get() always returns the proper type
#.set() is flexible about input types
theTuple = (90, -90, 180)
objectA.rotate.set(theTuple)
objARot = objectA.rotate.get()

#objARot is vector. theTuple is list. to match those value.
theTuple == objARot

#make list
list(theTuple) == list(objARot)

#checking for attrs
#approved python way
hasattr(node, attrname)

#checking for an attr on a pynode
objectA.hasAttr("matrix")
objectA.hasAttr("bob")
objectA.getShape().hasAttr("template")

#useful attr method
objectA.translateX.isKeyable()
objectA.rotateX.isLocked()
objectA.scale.lock()
objectA.scale.unlock()

#connect
objectA.translate.connect(objectB.translate)
#will error if a connectino is already present
objectC.translate.connect(objectB.translate)
#use the force flag
objectC.translate.connect(objectB.translate, f=True)

#what if the attribute has animation values
#!!!! key the rotate of objectB
objectA.rotate.connect(objectB.rotate)

#no error but not working. why?
#the nature of comfound attribute
objectA.translate.isCompound()
objectA.translate.getChildren()
objectA.tx.parent()
objectA.tx.getAllParents()
objectA.tx.siblings() 

objectA.inputs()
objectA.inputs(type="animCurve")

from see import see

objectB.inputs()
objectB.inputs(plugs=True)

#better to use
objectB.inputs(connections=True, plugs=True)
object.translate.disconnect()

#it does not recommand because it's hard to read for the beginner.
ojbectB.translate // objectB.translate
objectB.translate >> objectB.translate
 
objectA.outputs()

#loop through and disconnect.
[con.disconnect() for con in objectB.inputs(plugs=True)]

if not objectA.hasAttr("bob"):
    objectA.addAttr("bob", at="float", k=True)
    
if not objectA.hasAttr("sam"):
    objectA.addAttr("sam", at="float", minValue=0.0, maxValue=1.0, hasMaxValue=True, hasMinValue=True)

#modify attribute behavior after it has been made
objectA.sam.setkeyable(True)
objectA.sam.setMin(-1.0)

#delete attr
objectA.sam.delete() 


################################################
# blendshape node
################################################
head = pm.PyNode("face_with_Blendshapes")

#get the shape node
headShape = head.getShape()

#get the blendshape node input
blendShapeNode = pm.PyNode("blendShape1")
see(blendShapeNode)
blendShapeNode.listAliases()

# same but a little different for weights on constraints
parCon = pm.PyNode("nameOfConstraint")
see (parCon)
parCon.getWeightAliasList() 




###################################
# math
###################################

import pymel.core as pm

vec = pm.dt.Vector(4,3,5)

see(vec)
vec.length()

vec.x

vec2 = pm.dt.Vector.xAxis
vec3 = pm.dt.Vector.xNegAxis

vec = pm.dt.Vector((4,3,5))
vec.length()
see(vec)
vecNorm = vec.normal()
loc = pm.spaceLocator(n='locNorm')
loc.translate.set(vecNorm)

#normalize vector inline, it doesn't return value. it recommand .normal()
vec.normalize()

###################################
#matrix
###################################
import pymel.core as pm
theCone = pm.PyNode("theCone")

xVec = pm.dt.Vector([1, 2, 3])
yVec = pm.dt.Vector([1, 2, 3])
zVec = pm.dt.Vector([1, 2, 3])
trans = pm.dt.Vector([1, 2, 3])

coneM = pm.dt.Matrix(xVec, yVec, zVec, trans)

see(coneM)

theCone.setMatrix(coneM)

cub = pm.PyNode("Cube")

theCone.setMatrix(cub.getMatrix())

####################################
# cross product
####################################

#cross product has problem with 0 and 180 degree.
xVec = pm.dt.Vector([1, 2, 3,])
xVec = pm.dt.Vector([1, 3, 3,])

xVec.length()
oppVec.length()

xVec.normalize()
oppVec.normalize()

yVec = oppVec.cross(xVec).normal()
yVecNeg = xVec.cross(oppVec).normal()

yVec.length()

#to get cross vector of z

zVec = xVec.cross(yVec).normal()

#create cube
theCube.pm.selected()[0]
trans = pm.dt.Vector([1, 2, 3])
cubeM = pm.dt.Matrix(xVec, yVec, trans)
theCube.setMatrix(cubeM)


