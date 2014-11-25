import sys
from os import getenv, path
from rigWorkshop.ws_functions.logger import logger

def importPath(filepath=None, user=None):
    """
    @descripttion: checking the path if there is on the os.path list and add if not
    @author: Jung Hun Kim
    @usage:
            user=getenv("USER")
            filepath = "/corp/projects/eng/" + user + "/workspace/rnkRig/rigWorkshop/ws_functions/"
            importPath(filepath, user) 
    @return: 
            if path exist, print "the path is already on the sys.path"
            if not, add the path to sys.path
            
    @DONE: checking module if there is module on the sys.path.
    
    @param 
        string filepath: specify the path of module
        string user: specify the name of user
    """
    # check if the folder exist to import the module
    assert path.isdir(filepath), logger.info("the path does not exist")
    
    # if the path is not on the os.path list, add it.
    if filepath not in sys.path    :
        sys.path.append(filepath)
        return logger.info("path" + filepath + "has been added")
    return logger.info("the path is already on the sys.path")