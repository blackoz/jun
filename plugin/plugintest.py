import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx



from rigWorkshop.ws_user.jun.plugin import loadPlugin
reload(loadPlugin)
import maya.mel as mel


#slerp test
plugin = loadPlugin.loadPlugin(plugin = "/corp/home/jkim/Jun/MayaProgramming/Plugins/PythonApi/slerp.py")
#unload plugin
plugin.unloadPlugin()
#load plugin
plugin.loadPlugin()
#creating curve
command = 'curve -d 1 -p -8.434661 0 8.109949 -p -8.955208 0 1.457643 -p 7.021501 0 -1.227189 -p 10.108754 0 5.259066 -k 0 -k 1 -k 2 -k 3'
mel.eval(command)
cmds.createNode("SlerpNode", n="foo")
cmds.connectAttr("curveShape1.local", "foo.inCurve", f=True)
getAttr("foo.outTranslate")


##rivet controller test
#plugin = loadPlugin.loadPlugin(plugin = "/corp/home/jkim/Jun/MayaProgramming/Plugins/PythonApi/rivetNode.py")
##unload plugin
#plugin.unloadPlugin()
##load plugin
#plugin.loadPlugin()
#cmds.createNode("rivetNode", n="foo")
#cmds.polySphere(ch=True, o=True, r=6.818565)
#
#cmds.connectAttr("pSphereShape1.outMesh", "foo.targetMesh", f=True)
#cmds.setAttr("foo.targetVertex", 277)
#a = cmds.spaceLocator(p=(0, 0, 0), n="test")
#cmds.connectAttr("pSphereShape1.outMesh", "test.translate", f=True)


    