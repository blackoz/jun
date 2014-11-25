from rigWorkshop.ws_user.jun.rigFunctions import vectorDisplay, pntLocator
reload(vectorDisplay)


start = (1, 0, 2) 
end = (4.5, 0, 0.5)
pnt = (2, 0, 0.5)

line_vec = vector.vector(start, end)
pnt_vec = vector.vector(start, pnt)
line_unitvec = vector.unit(line_vec)
dot = vector.dotproduct(pnt_vec, line_unitvec)
perpendicular = vector.scale(line_unitvec, dot)


b = (pnt_vec[0] -perpendicular[0], pnt_vec[1] -perpendicular[1] ,pnt_vec[2] -perpendicular[2])
line_vec = vectorDisplay.VectorDisplay(moduleName="perpenline", position0=(0, 0, 0), position1=b, colorIndex=15)
line_Loc = line_vec.drawLine()

# draw line
line_vec = vectorDisplay.VectorDisplay(moduleName="linevector", position0=start, position1=end, colorIndex=15)
line_Loc = line_vec.drawLine()


print perpendicular[0], perpendicular[1], perpendicular[2] 
#put locator on the point
pntpos = vectorDisplay.VectorDisplay(moduleName="pnt", position0=pnt)
pntpos.pntLocator()

perpen[0]# draw line between start line and point
pnt_vec = vectorDisplay.VectorDisplay(moduleName="pntvector", position0=start, position1=pnt, colorIndex=15)
pnt_vec_line = pnt_vec.drawLine()

perpendicular = vectorDisplay.VectorDisplay(moduleName="perpen", position0=perpendicular)
perpen = perpendicular.pntLocator()

#go to origin because vector does not have position
cmds.setAttr(pnt_vec_line[0][0] + ".translateX", 0)
cmds.setAttr(pnt_vec_line[0][0] + ".translateY", 0)
cmds.setAttr(pnt_vec_line[0][0] + ".translateZ", 0)
cmds.setAttr(line_Loc[0][0] + ".translateX", 0)
cmds.setAttr(line_Loc[0][0] + ".translateY", 0)
cmds.setAttr(line_Loc[0][0] + ".translateZ", 0)

objs = [pnt_vec_line[0], perpen[0]]
pos = []
for obj in objs:
    eachpos = cmds.xform(obj, q=True, t=True, ws=True)
    pos.append(eachpos)

perpenLine = vectorDisplay.VectorDisplay(moduleName="perpenLine", position0=pos[0], position1=pos[1], colorIndex=15)
perpenLine.drawLine()


#go back the position where it was
cmds.setAttr(pnt_vec_line[0][0] + ".translateX", start[0])
cmds.setAttr(pnt_vec_line[0][0] + ".translateY", start[1])
cmds.setAttr(pnt_vec_line[0][0] + ".translateZ", start[2])
cmds.setAttr(line_Loc[0][0] + ".translateX", start[0])
cmds.setAttr(line_Loc[0][0] + ".translateY", start[1])
cmds.setAttr(line_Loc[0][0] + ".translateZ", start[2])






