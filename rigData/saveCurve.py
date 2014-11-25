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


#import module
from os import getenv, path
from rigData import curveData
import maya.cmds as cmds


class CurveInfo(object):
    """
    set curve information onto SVN and get the information into shot.
    """
    def __init__(self, 
                 user       = None,
                 asset      = None,
                 rigClass   = None,
                 name       = None,
                 close      = True 
                 ):
        """
        :param string user:
            gets user name
        :param string asset:
            gets asset name
        :param string rigClass:
            gets rig types
        :param string name:
            the name of curve
        """
        #--- args
        self.user       = user
        self.asset      = asset
        self.rigClass   = rigClass
        self.name       = name
        
        #--- vars
        self.path = ("/corp/projects/eng/" + self.user  + 
                     "/workspace/rnkRig/rigBuilds/barbie15/" + 
                     self.rigClass + "/" + self.asset + "/body_hi/data/misc/" + 
                     self.name + ".json")
    #END def __init__ 
    
    def setCurve(self):
        """save curve info"""
        if not path.isfile(self.path):
            obj = cmds.ls(sl=True)
            assert obj, "select at least one curve"
            cmds.delete(ch=True)
            shapes = cmds.listRelatives(obj[0], s=True)
            if cmds.objectType(shapes[0]) == "nurbsCurve":
                if obj[0] != self.name: 
                    cmds.rename(obj, self.name)
                    # saving the curve info
                curve = curveData.store(self.path, self.name)
            #END if
            else:
                print "you need to select a nurbsCurve to save curve information"
            #END else
        #END if
    #END def setCurve()  
    
    def getCurve(self):
        """
        get Curve
        """
        assert path.isfile(self.path), "no curve info exists!!, create it first!!"
        # load the curve info
        curve = curveData.apply(self.path)
    #END def getCurve


#make the instance of the class
crvInfo = CurveInfo(user = getenv("USER"),
                 asset = "cmPopAssistant",
                 rigClass = "characters",
                 name = "C_beltStrapGuide_CRV")

#setCurve
crvInfo.setCurve()

#getCurve
#crvInfo.getCurve()


