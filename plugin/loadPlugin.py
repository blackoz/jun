"""
@author:      Jung Hun Kim
@data:        Oct 22 2014
@mail:        jkim@rainmaker.com
@brief:       load plulgin
"""

import maya.cmds as cmds
from rigWorkshop.ws_user.jun.logging.logger import logger


class loadPlugin(object):
    """
    @description:   this loads and unload plugin
    @author:        Jung Hun Kim
    @requires:      the path of plugin file
    @usage:         from rigWorkshop.ws_user.jun import loadPlugin
                    reload(loadPlugin)
                    
                    plugin = loadPlugin.loadPlugin(plugin = "/corp/home/jkim/Jun/MayaProgramming/Plugins/PythonApi/slerp.py")
                    
                    #load plugin
                    plugin.loadPlugin()
                    
                    #unload plugin
                    plugin.unloadPlugin()
    @return         nothing
    """

    def __init__(self, plugin=None):
        """
        @param
            stirng plugin: specifies the path of plugin
        """
        #arg
        self.plugin = plugin
        
        #calling method        
        self.check()
    #END def __init__
    
    def check(self):
        assert self.plugin, logger.warning("there is no plugin file.")
    #END def check
    
    def loadPlugin(self):
        """load plugin"""
        if not cmds.pluginInfo(self.plugin,q=True,l=True):
            try:
                cmds.loadPlugin(self.plugin)#compiled, no extension
            except:
                try:
                    cmds.loadPlugin(self.plugin + ".py")#scripted, py extension
                    logger.info(self.plugin + " is loaded")
                except:
                    raise RigError(plugin + " could not be loaded!")
    #END def loadPlugin
    
    def unloadPlugin(self):
        "unload plugin"
        fileName = self.plugin.split("/")[-1]    
        if cmds.pluginInfo(fileName, q=True, l=True):
            cmds.file(f=True, new=True)
            cmds.unloadPlugin(fileName)
            logger.info(fileName + " is unloaded")
    #END def unloadPlugin
        
