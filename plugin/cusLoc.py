#----
#creator	: marc dubrois
#email 		: marc.dubrois@gmail.com
#--
#version 
#--
#1.0			: first release
#----


import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMayaRender as OpenMayaRender
import maya.OpenMayaUI as OpenMayaUI
import maya.cmds as cmds

import sys

nodeType		= "customLocShape"
nodeId			= OpenMaya.MTypeId(0x87012)
glRenderer	= OpenMayaRender.MHardwareRenderer.theRenderer()
glFT				= glRenderer.glFunctionTable()

# default settings
defaultFactor	= 1.0
defaultShape	= 'cross'
defaultLineW	= 'small'

# shape definition
shapeValue	= {\
				'cross':([-0.3,0,-0.5], [-0.3,0,-0.3], [-0.5,0,-0.3],[-0.5,0,0.3], [-0.3,0,0.3], [-0.3,0,0.5], [0.3,0,0.5], [0.3,0,0.3], [0.5,0,0.3], [0.5,0,-0.3], [0.3,0,-0.3], [0.3,0,-0.5], [-0.3,0,-0.5]),\
				'square':([-0.5,0,-0.5], [-0.5,0,0.5], [0.5,0,0.5], [0.5,0,-0.5], [-0.5,0,-0.5]),\
				'squareCross':([[0.0, 0.0, -0.80000000000000004], [0.30000000000000004, 0.0, -0.5], [0.20000000000000001, 0.0, -0.5], [0.20000000000000001, 0.0, -0.20000000000000001], [0.5, 0.0, -0.20000000000000001], [0.5, 0.0, -0.30000000000000004], [0.80000000000000004, 0.0, 0.0], [0.5, 0.0, 0.30000000000000004], [0.5, 0.0, 0.20000000000000001], [0.20000000000000001, 0.0, 0.20000000000000001], [0.20000000000000001, 0.0, 0.5], [0.30000000000000004, 0.0, 0.5], [0.0, 0.0, 0.80000000000000004], [-0.30000000000000004, 0.0, 0.5], [-0.20000000000000001, 0.0, 0.5], [-0.20000000000000001, 0.0, 0.20000000000000001], [-0.5, 0.0, 0.20000000000000001], [-0.5, 0.0, 0.30000000000000004], [-0.80000000000000004, 0.0, 0.0], [-0.5, 0.0, -0.30000000000000004], [-0.5, 0.0, -0.20000000000000001], [-0.20000000000000001, 0.0, -0.20000000000000001], [-0.20000000000000001, 0.0, -0.5], [-0.30000000000000004, 0.0, -0.5], [0.0, 0.0, -0.80000000000000004]]),\
				}

lineWidthVal	= {\
				'small':1.0,\
				'medium':2.0,\
				'large':4.0\
				}

lineWidthList	= ['small', 'medium', 'large']
shapeList		= ['cross', 'square', 'squareCross']

def getLineWId(val):
	for i in range(0,len(lineWidthList)):
		if lineWidthList[i] == val:
			return i
def getLineWName(val):
			return lineWidthList[val]
		
def getShapeId(val):
	for i in range(0,len(shapeList)):
		if shapeList[i] == val:
			return i
	
def getShapeName(val):
	return shapeList[val]

#----
#
class basicLoc:
	factor		= defaultFactor
	shapeType	= getShapeId(defaultShape)
	forme		= shapeValue[defaultShape]
	lineWidth	= lineWidthVal[defaultLineW]


class customLocShape(OpenMayaMPx.MPxLocatorNode):	

	aShapeType = OpenMaya.MObject()
	aColor = OpenMaya.MObject()
	aFactor = OpenMaya.MObject()
	aLineWidth = OpenMaya.MObject()
	
	# init
	def __init__(self):		
		OpenMayaMPx.MPxLocatorNode.__init__(self)
		
		self.__myLoc	= basicLoc()
		
	# compute pour un output	
	def compute(self, plug, datahandle):						
		return OpenMaya.kUnknownParameter
		
	
	# draw l'objet	
	def draw(self, view, path, style, status):
		
		# 
		this_object		= self.thisMObject()
		fnThisNode	= OpenMaya.MFnDependencyNode(this_object)
		locName		= fnThisNode.name()
		
		plug = OpenMaya.MPlug(this_object, self.aFactor)		
		self.__myLoc.factor = plug.asDouble()
		
		plug = OpenMaya.MPlug(this_object, self.aShapeType)		
		self.__myLoc.shapeType = plug.asInt()

		plug = OpenMaya.MPlug(this_object, self.aLineWidth)		
		lineWId = plug.asInt()

		plug = OpenMaya.MPlug(this_object, self.aColor)
		col = plug.asMObject()
		numDataFn = OpenMaya.MFnNumericData(col)

		rParam = OpenMaya.MScriptUtil()
		rParam.createFromDouble(0.0)
		rPtr = rParam.asFloatPtr()

		gParam = OpenMaya.MScriptUtil()
		gParam.createFromDouble(0.0)
		gPtr = gParam.asFloatPtr()

		bParam = OpenMaya.MScriptUtil()
		bParam.createFromDouble(0.0)
		bPtr = bParam.asFloatPtr()

		numDataFn.getData3Float(rPtr, gPtr, bPtr)

		color = OpenMaya.MFloatVector(OpenMaya.MScriptUtil(rPtr).asFloat(), OpenMaya.MScriptUtil(gPtr).asFloat(), OpenMaya.MScriptUtil(bPtr).asFloat())

		self.__myLoc.color = [color[0], color[1], color[2]]
		
		
		shapeName						= getShapeName(self.__myLoc.shapeType)
		self.__myLoc.forme			= shapeValue[shapeName]
		
		#lineWId								= cmds.getAttr(locName+'.lineWidth')
		self.__myLoc.lineWidth		= lineWidthVal[getLineWName(lineWId)]
		
		# start openGL
		view.beginGL()
		if style == OpenMayaUI.M3dView.kFlatShaded or style == OpenMayaUI.M3dView.kGouraudShaded:
			glFT.glPushAttrib(OpenMayaRender.MGL_CURRENT_BIT)
			glFT.glPopAttrib()
		
		#----
		# draw color
		if status == OpenMayaUI.M3dView.kDormant:
			glFT.glColor3f(self.__myLoc.color[0], self.__myLoc.color[1], self.__myLoc.color[2])

		#----
		# draw line
		glFT.glLineWidth(self.__myLoc.lineWidth)
		glFT.glBegin(OpenMayaRender.MGL_LINES)
		
		
		last = len(shapeValue[shapeName]) - 1
		
		for i in range(last):
			
			glFT.glVertex3f( shapeValue[shapeName][i][0]*self.__myLoc.factor, shapeValue[shapeName][i][1]*self.__myLoc.factor, shapeValue[shapeName][i][2]*self.__myLoc.factor )
			glFT.glVertex3f( shapeValue[shapeName][i+1][0]*self.__myLoc.factor, shapeValue[shapeName][i+1][1]*self.__myLoc.factor, shapeValue[shapeName][i+1][2]*self.__myLoc.factor )		
		
		glFT.glEnd()
		
		# reset draw settings
		kLeadColor 					= 18 # green
		kActiveColor					= 15 # white
		kActiveAffectedColor	= 8  # purple
		kDormantColor				= 4  # blue
		kHiliteColor					= 17 # pale blue
		
		glFT.glLineWidth(1.0)
		
		if status == OpenMayaUI.M3dView.kDormant:
			glFT.glColor3f(self.__myLoc.color[0], self.__myLoc.color[1], self.__myLoc.color[2])

		
		if (status == OpenMayaUI.M3dView.kLead):
				view.setDrawColor( kLeadColor, OpenMayaUI.M3dView.kActiveColors )

		elif (status == OpenMayaUI.M3dView.kActive):
				view.setDrawColor( kActiveColor, OpenMayaUI.M3dView.kActiveColors )

		elif (status == OpenMayaUI.M3dView.kActiveAffected):
				view.setDrawColor( kActiveAffectedColor, OpenMayaUI.M3dView.kActiveColors )

		elif (status == OpenMayaUI.M3dView.kDormant):
				view.setDrawColor( kDormantColor, OpenMayaUI.M3dView.kActiveColors )

		elif (status == OpenMayaUI.M3dView.kHilite):
				view.setDrawColor( kHiliteColor, OpenMayaUI.M3dView.kActiveColors )


		# stop openGL
		view.endGL()

	# draw la bouding box
#	def boundingBox(self):
#		thisNode	= self.thisMObject()		
#		corner1		= OpenMaya.MPoint(-0.17, 0.0, -0.7)
#		corner2		= OpenMaya.MPoint(0.17, 0.0, 0.3)
#		bbox			= OpenMaya.MBoundingBox( corner1, corner2 )
#		return bbox
	

# creator
def nodeCreator():
	return OpenMayaMPx.asMPxPtr( customLocShape() )

# initializer
def nodeInitializer():
	# enum attr like optionMenu
	enumAttr 			= OpenMaya.MFnEnumAttribute()	
	customLocShape.aShapeType	= enumAttr.create("shapeType", "st", getShapeId(defaultShape))
	for i in range(0, len(shapeList)):
		enumAttr.addField(shapeList[i], i)
	enumAttr.setHidden(False)
	enumAttr.setKeyable(True)
	customLocShape.addAttribute(customLocShape.aShapeType)

	enumAttr 						= OpenMaya.MFnEnumAttribute()	
	customLocShape.aLineWidth	= enumAttr.create("lineWidth", "lw", getLineWId(defaultLineW))
	for i in range(0, len(lineWidthList)):
		enumAttr.addField(lineWidthList[i], i)
	enumAttr.setHidden(False)
	enumAttr.setKeyable(True)
	customLocShape.addAttribute(customLocShape.aLineWidth)
	
	# numeric attr 
	nAttr						= OpenMaya.MFnNumericAttribute()
	customLocShape.aColor			= nAttr.createColor("shapeColor", "sc")
	nAttr.setDefault(1.0, 0.9, 0.0)
	nAttr.setKeyable(1)
	nAttr.setStorable(1)
	nAttr.setUsedAsColor(1)
	nAttr.setReadable(1)
	nAttr.setWritable(1)
	customLocShape.addAttribute(customLocShape.aColor)

	# numeric attr 
	nAttr						= OpenMaya.MFnNumericAttribute()
	customLocShape.aFactor		= nAttr.create("factor", "f", OpenMaya.MFnNumericData.kDouble, defaultFactor)
	nAttr.setHidden(False)
	nAttr.setKeyable(True)
	customLocShape.addAttribute(customLocShape.aFactor)

	
# initialize the script plug-in
def initializePlugin(mobject):
	mplugin = OpenMayaMPx.MFnPlugin(mobject, "Marc_Dubrois", "1.0", "Any")
	try:
		mplugin.registerNode( nodeType, nodeId, nodeCreator, nodeInitializer, OpenMayaMPx.MPxNode.kLocatorNode )
	except:
		sys.stderr.write( "Failed to register node: %s" % nodeType )
		raise

# uninitialize the script plug-in
def uninitializePlugin(mobject):
	mplugin = OpenMayaMPx.MFnPlugin(mobject)
	try:
		mplugin.deregisterNode( nodeId )
	except:
		sys.stderr.write( "Failed to deregister node: %s" % nodeType )
		raise
	

#cmds.createNode("customLocShape", n="useThisName1Shape")






