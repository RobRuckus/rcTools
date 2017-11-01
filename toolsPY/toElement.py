import maya.cmds as mc 
import random

def renameSG():#renames SG by selecting material
		sel=mc.ls(sl=1)
		for each in sel:
			material=each
			SG=mc.listConnections(each,destination=True,source=False,plugs=False,type="shadingEngine")
			MAT=mc.rename(each,each+'_MAT')
			mc.rename(SG,each)

def seperate():#Attaches New Random Shader Per Selection
	import random
	sel=mc.ls(sl=1)
	for each in sel:
		SHADER=each+'_mat'
		SG=each
		MESH=mc.rename(each,each+'_MESH')
		#create shader with name 
		SN=mc.shadingNode('lambert',n=SHADER,asShader=1)
		SG=mc.sets(renderable=True,noSurfaceShader=True,empty=1,name=SG)
		mc.connectAttr(SN+'.outColor', SG+'.surfaceShader',f=1)
		mc.setAttr( SN+'.color', random.uniform(0,1),random.uniform(0,1),random.uniform(0,1),type='double3')
		#assign shader with name 
		mc.select(MESH)
		mc.hyperShade(assign=SN)
