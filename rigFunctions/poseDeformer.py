###############################################################################
#
# Copyright (c) 2011 Rainmaker Entertainment
# All Rights Reserved.
#
# This file contains unpublished confidential and proprietary
# information of Rainmaker Entertainment.  The contents of this file
# may not be copied or duplicated, in whole or in part, by any
# means, electronic or hardcopy, without the express prior
# written permission of Rainmaker Entertainment.
#
#    $HeadURL: /corp/projects/eng/jkim/workspace/rnkRig/rigWorkshop/ws_functions/saveCurve.py
#    $Revision: 001 $
#    $Author: Jung Hun Kim $
#    $Date: 2014-09-29 
#
###############################################################################

from rigFunctions import asset, attribute, name, check, geo, xform
from rigFunctions.error import RigError
from rigData import poseReaderData
import maya.cmds as cmds
import maya.mel as mel
import json, re
import logging
import os


class mirrorPoseD(object):
    """
    mirror poseDeformer base on Nick's posedeformer tool with wrap deformer
    """
    def __init__(self,
                 description = None, 
                 mesh       = None,
                 control    = None, 
                 axis       = None, 
                 angle      = None,
                 joint     = None):
        """
        @param 
            string description:
                gets description(middle name, ex)"name" in C_name_JNT)

            string mesh:
                specify target Mesh that you want to mirror from 

            string control:
                specify the name of controller where you want to mirror

            string axis:
                specify axis that poseDeformer is triggered
            
            float angle:
                specify angle that you want to mirror.
                
            string joint:
                specify joint that poseDeformer is triggered.
        """

        #arg
        self.description = description 
        self.mesh       = mesh
        self.control    = control 
        self.axis       = axis 
        self.angle      = angle 
        self.joint     = joint 

        #vars
        self.dups       = []
        self.rootName   = "R_GRP"
        self.DupsName   = "Dups"
        self.TransName  = "TRN"
        self.corrGrp    = "CORRECTIVE_SHAPES"
        self.corr       = "CORRECTIVESHAPE"
        self.bsp        = "BSP"
        self.sculptsGrp = "SCULPTS_GRP"
        self.shapesGrp  = "SHAPES_GRP"
        self.drivenMesh = []
        self.eachPose   = None 
        
        #--- methods
        self.__create()       
    
    def wrapDeformer(self, driven, driver):
        """ creating wrapdeformer """
        cmds.select(driven, r=True)
        cmds.select(driver, add=True)
        mel.eval("CreateWrap")
    #END def wrapDeformer()

        
    def __check(self):
        """ check """
        if not cmds.objExists(self.rootName):
            # create group
            self.root = cmds.group(n=self.rootName, em=True)
            self.Dups = cmds.group(n=self.DupsName, em=True)
            self.Trans = cmds.group(n=self.TransName, em=True)
            cmds.parent(self.Trans, self.root)
            cmds.parent(self.Dups, self.root)
            cmds.setAttr(self.Dups + ".scaleX", -1)
            cmds.setAttr(self.Trans + ".scaleX", 1)
    #END def __check(self)
            
    def setDefaultPose(self):
        """ set Default Poses """
        #fk controlelr
        cmds.setAttr("L_legAttrs_CTL.fkIkPin",  0)
        cmds.setAttr("R_legAttrs_CTL.fkIkPin",  0)
        
        cmds.setAttr("L_armShoulderFk_CTL.rotateZ", 0)
        cmds.setAttr("L_legHipFk_CTL.rotateY", 0)
        cmds.setAttr("L_legKneeFk_CTL.rotateY", 0)
        cmds.setAttr("L_armElbowFk_CTL.rotateY", 0)

        cmds.setAttr("R_armShoulderFk_CTL.rotateZ", 0)
        cmds.setAttr("R_legHipFk_CTL.rotateY", 0)
        cmds.setAttr("R_legKneeFk_CTL.rotateY", 0)
        cmds.setAttr("R_armElbowFk_CTL.rotateY", 0)
    #END setDefaultPose()
                
    def prepare(self):
        """ preparing mirror corretiveShape """
        # default pose
        self.setDefaultPose()
        meshName = (name.getSide(self.mesh)+ "_" + name.getDescription(self.mesh) + "DUP" + "_" + name.getType(self.mesh))
        #make hierachy
        if not cmds.objExists(meshName): 
            dup = cmds.duplicate(self.mesh, rr=True, n=meshName)
            attribute.lockAll(dup[0], True)
            cmds.setAttr(dup[0] + ".visibility", 0)
            cmds.parent(dup, self.DupsName)
            self.wrapDeformer(dup, self.mesh)
            xform.zeroOut(dup[0], t = 1, r = 1, s = 1)
            self.dups.append(dup)
        #END if
        else:
            dup = meshName
            print "%s already exists!!!" % meshName
        #END else

        #pose copy
        eachPoseName = (name.getSide(self.mesh)+ "_" + name.getDescription(self.mesh) + self.description + "_" + name.getType(self.mesh))
        cmds.setAttr(self.control + ".rotate" + self.axis, self.angle)
        self.eachPose = cmds.duplicate(dup, rr=True, n=eachPoseName)
        cmds.parent(self.eachPose, self.TransName)
        xform.zeroOut(self.eachPose[0], t = 1, r = 1, s = 1)

        #neutral pose.        
        self.setDefaultPose()
    #END prepare()
    
    def correctiveShape(self):
        """ correctiveShape module from Nick """
        assert self.mesh, "--\ncorrectiveData.createCorrectiveUI.__create: no mesh specified"
        assert self.joint, "--\ncorrectiveData.createCorrectiveUI.__create: no joint specified"
        #make sure we're only working on one corrective at a time
        corrs = cmds.ls(type = "correctiveShape")
        if corrs:
            raise Exception("--\ncorrectiveData.createCorrectiveUI.__selectMesh: existing correctiveShapes found:" + " ".join(corrs))
        #END if
        #read the ui
        description = self.description
        if not description:
            description = "corrective"
        #END if
        try:
            side = name.getSide(self.joint)
        #END try
        except:
            pass
        #END except
        uniqueDescription = name.uniqueName(side + "_" + name.getDescription(self.mesh) + name.getDescription(self.joint).capitalize() + description.capitalize() + "_TRN")
        
        #create the poseReader
        prdTrans = cmds.createNode("transform", n = side + "_" + uniqueDescription + "_TRN")
        prd = cmds.createNode("poseReader", n = side + "_" + uniqueDescription + "_PRD", parent = prdTrans)

        #set prd attrs
        cmds.setAttr(prd + ".readAxis", 0)
        cmds.setAttr(prd + ".maxAngle", 60)
        cmds.setAttr(prd + ".drawCone", 1)
        cmds.setAttr(prd + ".drawText", 1)
        
        m = cmds.xform(self.joint, q = 1, ws = 1, matrix = 1)
        cmds.xform(prdTrans, ws = 1, matrix = m)
        parent = cmds.listRelatives(self.joint, parent = 1)
        
        cmds.connectAttr(self.joint + ".wm", prd + ".worldMatrixLiveIn")
        cmds.connectAttr(prdTrans + ".wm", prd + ".worldMatrixPoseIn")
        
        if side == "R":
            cmds.setAttr(prd + ".drawReverse", 1)
        #END if
        if parent:
            cmds.parent(prdTrans, parent[0])
        #END if
        
        #corrective
        cmds.select(self.mesh)
        csp = cmds.correctiveShapeCmd()
        sculpt = cmds.listConnections(csp + ".inputMesh")
        assert sculpt, "--\ncorrectiveData.createCorrectiveUI.__create: cannot query the sculpt mesh"
        sculpt = cmds.rename(sculpt[0], side + "_" + uniqueDescription + "Sculpt_TRN")
        
        shape = cmds.listConnections(csp + ".og[0]")
        assert shape, "--\ncorrectiveData.createCorrectiveUI.__create: cannot query the blendShapeMesh mesh"
        shape = cmds.rename(shape[0], side + "_" + uniqueDescription + "Corrective_TRN")
        
        if not cmds.objExists(self.corrGrp):
            corrGrp = cmds.createNode("transform", n = self.corrGrp)
            attribute.lockAll(corrGrp)
            
            sculptsGrp = cmds.createNode("transform", n = self.sculptsGrp, parent = corrGrp)
            attribute.lockAll(sculptsGrp)
            
            shapesGrp = cmds.createNode("transform", n = self.shapesGrp, parent = corrGrp)
            attribute.lockAll(shapesGrp)
        #END if
        cmds.parent(sculpt, self.sculptsGrp)
        cmds.parent(shape, self.shapesGrp)
        
            
        #bsp
        desc = None
        side = None
        try:
            desc = name.getDescription(self.mesh)
            side = name.getSide(self.mesh)
        except:
            pass
        
        if desc:
            bsp = side + "_" + name.getDescription(self.mesh) + "Correctives_BSP"
        #END if
        if not cmds.objExists(bsp):
            bsp = cmds.blendShape(shape, self.mesh, foc = 1, weight = [0, 1.0], n = bsp)
            assert self.bsp, "--\ncorrectiveData.createCorrectiveUI.__create: cannot apply blendShape to " + self.mesh
            bsp = self.bsp[0]
            cmds.connectAttr(prd + ".outWeight", bsp + ".weight[0]")
            attribute.addTag(bsp, "CORRECTIVE")
        #END if
        else:
            index = cmds.blendShape(bsp, q = 1, weightCount = 1)
            cmds.blendShape(bsp, e = 1, t = [self.mesh, index, shape, 1.0])
            cmds.connectAttr(prd + ".outWeight", bsp + ".weight[" + `index` + "]")
        #END else
        #cleanup
        cmds.setAttr(shape + ".v", 0)
        self.drivenMesh.append(sculpt)
    
    def finalize(self):
        """ corrective shape finalize """
        mesh = self.mesh
        if not mesh:
            sels = cmds.ls(sl = 1)
            if sels:
                mesh = sels[0]
            #END if
        #END if
        assert mesh, "--\ncorrectiveData.createCorrectiveUI.__finalize: no mesh specified"
        corrs = cmds.ls(type = "correctiveShape")
        if not corrs:
            print "No corrective shapes found in " + mesh + "'s history"
            return
        #END if
        csp = corrs[0]
        sculpt = cmds.listConnections(csp + ".inputMesh")
        shape = cmds.listConnections(csp + ".og[0]")
        if sculpt:
            sculptShapes = cmds.listRelatives(sculpt[0], s=True, ad=True)
            sculpt.insert(0, sculptShapes[0])
        #END if
        cmds.delete(sculpt)
        cmds.select(shape[0])
        cmds.DeleteHistory()  
    #END def finalize():

    def oppositeDirection(self):
        """gets the side of oppositeDirection"""
        if name.getSide(self.control) == "L":
            control = "R_" + name.getDescription(self.control)+ "_" + name.getType(self.control)
        elif name.getSide(self.control == "R"):
            control = "L_" + name.getDescription(self.control)+ "_" + name.getType(self.control)
        cmds.setAttr(control + ".rotate" + self.axis, self.angle)
    #END def oppositeDirection()
        
    def cleanup(self):
        """ cleanup """
        self.setDefaultPose()
    #END def cleanup()
        
    def bShapes(self, drv, drvn):
        """ blendShape """
        cmds.blendShape(drv, drvn, w=[0, 1])
    #END def bShapes()

    def __create(self):
        """ create """
        self.__check()
        
        self.prepare()
        
        self.oppositeDirection()
        
        self.correctiveShape()
        
        self.bShapes(drv = self.eachPose[0], drvn = self.drivenMesh[0])
        
        self.finalize()
        
        self.cleanup()
    #END def __create()
        
#shirtelbow = mirrorPoseD(description = "bend90", mesh = "C_shirt_HI", control = "L_armElbowFk_CTL", axis = "Y", angle = -90, joint = "R_armElbow_JNT")
#shirtUp60 = mirrorPoseD(description = "up60", mesh = "C_shirt_HI", control = "L_armShoulderFk_CTL", axis = "Z", angle = 60, joint = "R_armShoulder_JNT")
#shirtHipfront90 = mirrorPoseD(description = "front90", mesh = "C_shirt_HI", control = "L_legHipFk_CTL", axis = "Y", angle = -90, joint = "R_legHip_JNT")

pantsKnee = mirrorPoseD(description = "bend90", mesh = "C_pants_HI", control = "L_legKneeFk_CTL", axis = "Y", angle = 90, joint = "R_legKnee_JNT")
#pantsback60 = mirrorPoseD(description = "back60", mesh = "C_pants_HI", control = "L_legHipFk_CTL", axis = "Y", angle = 60, joint = "R_legHip_JNT")
#pantsfront15 = mirrorPoseD(description = "front15", mesh = "C_pants_HI", control = "L_legHipFk_CTL", axis = "Y", angle = -15, joint = "R_legHip_JNT")


#jacketelbow = mirrorPoseD(description = "bend90", mesh = "C_jacket_HI", control = "L_armElbowFk_CTL", axis = "Y", angle = -90, joint = "R_armElbow_JNT")
#jacketUp65 = mirrorPoseD(description = "up65", mesh = "C_sweater_HI", control = "L_armShoulderFk_CTL", axis = "Z", angle = 65, joint = "R_armShoulder_JNT")

#bodyelbow = mirrorPoseD(description = "bend90", mesh = "C_body_HI", control = "L_armElbowFk_CTL", axis = "Y", angle = -90, joint = "R_armElbow_JNT")

        