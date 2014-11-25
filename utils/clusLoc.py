import pymel.core as pm
from rigWorkshop.ws_user.jun.utils.logger import logger


def clusLoc():
    """
    create locator at a centroid position in a ring of edges
    
    how to use:
    select edges loop and excute this command
    
    from rigWorkshop.ws_user.jun.utils import clusLoc
    reload(clusLoc)
    clusLoc.clusLoc()
    """
    edges = pm.selected(flatten=True)
    #list comprehension
    verts = list(set(sum([list(e.connectedVertices()) for e in edges], [])))
    
    #cluster
    clusDFM, clusTRN = pm.cluster(verts)
    
    #locator 
    loc = pm.spaceLocator()
    
    #point constraint
    pm.delete(pm.pointConstraint(clusTRN, loc, mo=False))
    pm.delete(clusTRN)

    
def clusLoc2(debugLevel="DEBUG"):
    """create locator or position selected joint at a centroid position in a ring of edges
    
    how to use:
    from rigWorkshop.ws_user.jun.utils import clusLoc
    reload(clusLoc)
    clusLoc.clusLoc2()
    """
    # set debug level
    logger.setLevel(debugLevel)

        
    sel = pm.selected(flatten=True)
    
    verts = []
    edges = []
    TRNs =[]
    
    for s in sel:
        sortMe = s.__class__.__name__
        
        if sortMe == "Joint" or sortMe =="transform":
            TRNs.append(s)
            
        if sortMe == "MeshVertex":
            verts.append(s)
            
        if sortMe == "MeshEdge":
            edges.append(s)
    # convert egdes to vertex        
    if edges:
        edgeVerts = list(set(sum([list(e.connectedVertices()) for e in edges], [])))
        verts = verts + edgeVerts
        
    logger.debug("verts = %s" % verts)
    logger.debug("TRNs = %s" % TRNs)
    
    clusDef, clusTRN = pm.cluster(verts)
    
    if not TRNs:
        loc = pm.spaceLocator()
        TRNs.append(loc)
        logger.debug("Locator %s has been created" % TRNs)    
    
    for TRN in TRNs:
        #hierarchy issues prepped
        parent = TRN.getParent()
        logger.debug("parent is %s " % parent) 
        children = TRN.getChildren(type="transform")
        logger.debug("children is %s " % children) 
        
        if parent:
            TRN.setParent(world=True)
            
        for child in children:
            child.setParent(world=True)
            
        pm.delete(pm.pointConstraint(clusTRN, TRN, mo=False))
        
        for child in children:
            child.setParent(TRN)

        if parent:
            TRN.setParent(parent)
    pm.delete(clusTRN)
    logger.debug("Done!!")    
