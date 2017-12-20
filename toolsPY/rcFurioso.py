"""
Author: Rob Coakley (robcoakley@gmail.com)
Copyright (C) 2017 Robert Coakley
http://robocolabo.com/blog/
Version: 0.1
Function:
try:
	reload(rcMaya2AE)
except:
	import rcMaya2AE
"""
###########
import subprocess
import os
import maya.cmds as mc
import rcTools.rcMaya as rc
from rcTools.main import *
###########
from functools import partial
def runMethod(method,string,*args): exec(method+string) #Button Delay Function
###########
#UI VARIABLES FROM MAIN
ui=rc.ui('Furioso')

def tagFuriosoFlag(sel):#AE COMP FLAG
	if not mc.objExists(sel+'.FuriosoFlag') : mc.addAttr(sel,ln='FuriosoFlag',dt='string')		
	mc.setAttr(sel+'.FuriosoFlag',sel.rstrip('_mesh'),type='string')
def UI():
	mc.columnLayout('furiosoObjectConform')
	#mc.rowColumnLayout(numberOfColumns=2,columnWidth=[(1, 120),(2, 215)])
	#mc.checkBox('objRenameChk',l='Object Rename:',vis=1,v=0)
	#mc.textField('compAnchor',font='tinyBoldLabelFont',h=20,text='',cc=partial(runMethod,'applyrlmAttrs','()'))#,en=mc.getAttr('renderLayerManager.EnableRenderFolder')
	#mc.setParent('..')

	#mc.separator(h=15,style='in')
	#mc.checkBox('chkImportRCam',l='Import render Cameras:',vis=0,v=0,en=0)
	
	mc.rowLayout(w=ui.rowWidth,numberOfColumns=3)
	mc.button(w=ui.rowWidth/3,h=ui.btn_large,al='left',l=' + ',c=partial(runMethod,'btnPlus','(mc.ls(sl=1))'))  #
	mc.button(h=ui.btn_large,w=ui.rowWidth/3,al='center',l=' - ',c=partial(runMethod,'btnDel','("sel")')) 
	mc.button(h=ui.btn_large,w=ui.rowWidth/3,al='right',en=0,l='NUKE',c=partial(runMethod,'btnDel','("all")'))
	mc.setParent('..')
	mc.iconTextScrollList('FuriosoObjScroll',w=ui.rowWidth,h=500)
	mc.setParent('furiosoObjectConform')
	########
	mc.checkBox('chkAbsFrames',l='Use Timeline Frame Numbers',vis=0,v=1)
	mc.checkBox('chkOverrideTime',l='Override Timeline',vis=0,v=0,en=0)
	#mc.button(l='EXPORT',w=ui.rowWidth,bgc=[.586,.473,.725],align='center',h=ui.btn_large,c=partial(runMethod,'btnExport','()'))
	mc.setParent('..')
	
	buildUILists()
	#mc.scriptJob('import rcMaya2AE',event=SceneOpened)

def updateMenu():#UPDATE
	
	mc.menu('Path',e=True,dai=True)
	mc.menuItem(d=True,dl='Maya Render Images')
	for each in sceneData.outputImages():
		mc.menuItem(each,l=each,itl=True,c=partial(runMethod,'spawnBrowser','("%s")'%os.path.dirname(each)))
	mc.menuItem(l='Set Path Presets',c=partial(runMethod,'rc.set.globals','()'))
	mc.menuItem(d=True,dl='After Effects')
	
	mc.menuItem('Image Output',l=aePrefs.get('AELoc'),itl=True,en=0)
	
	mc.menuItem(l='Set Path',c=partial(runMethod,'aePrefs.path','()'))
	mc.setParent('..')
	
def buildUILists():
	mc.iconTextScrollList('FuriosoObjScroll',e=1,ams=1,ra=1)
	index=0
	for each in mc.ls():
		fileColor=[index+1,0,1,0]#		fileColor=[index+1,.7,0.0,0.0]

		if mc.objExists(each+'.FuriosoFlag'):
			index=index+1
			mc.iconTextScrollList('FuriosoObjScroll',e=1,a=each.rsplit('_mesh')[0],itc=fileColor,sc=tagListCallBack)
	#for i, each in enumerate(sceneData.outputLayers()):
		#fileColor=[i+1,.7,0,0]
		#print 
		#if os.path.exists(sceneData.outputImages()[i]):
		#	fileColor=[i+1,0,.7,0]
		#location=os.path.dirname(sceneData.outputImages()[i])
		#if imageLabel=='Label2': 
		#	mc.iconTextScrollList('OBJConformedScroll',e=1,itc=fileColor,a='%s.%s'%(rlm.get('shotName'),each))
		#if imageLabel=='Label3':
		#	mc.iconTextScrollList('OBJConformedScroll',e=1,itc=fileColor,dcc=partial(runMethod,'spawnBrowser','("%s")'%location),a='%s'%each)
	#updateMenu()
def tagListCallBack():
	sel=[]
	try:
		[sel.append(each+'_mesh') for each in mc.iconTextScrollList('FuriosoObjScroll',q=1,si=1) if mc.iconTextScrollList('FuriosoObjScroll',q=1,si=1) ]
	except:
		pass
	if sel: 
	    if sel=='_mesh':
	        pass
	    else:
	        mc.select(sel)
###	

def btnPlus(sel):
	for each in sel:
	    #mc.select(each)
		conform(each)
		tagFuriosoFlag(each)
	buildUILists()
def btnDel(opt): #deletes all sets and locators
	if opt=='all':
		for each in mc.ls():
			if mc.objExists(each+'.FuriosoFlag'): mc.deleteAttr(each+'.FuriosoFlag')
			if mc.objExists(each.replace('|','_')+'_pos'):mc.delete(each.replace('|','_')+'_pos')
	if opt=='sel':
		for each in mc.ls(sl=1):
			if mc.objExists(each+'.FuriosoFlag'): mc.deleteAttr(each+'.FuriosoFlag')
			if mc.objExists(each+'_pos'):mc.delete(each+'_pos')
	buildUILists()
################
def conform(sel):#Furioso obj naming : *_mesh on mesh, *_material on material, auto link file nodes *_color and *_spec
    mc.select(sel)
    #sel=mc.ls(sl=True)
    prompt=mc.promptDialog(t="Conform",m="Name:                                     ",tx=sel.rsplit('_mesh')[0],button="Go")
    if prompt=='dismiss':
        sys.exit()
    objName= mc.promptDialog(q=1,t=1)
    mesh= mc.rename(sel,objName+'_mesh')
    material=(objName+'_material')
    if not mesh==objName+'_mesh':
        mc.rename(objName+'_mesh',objName+'_mesh'+'_old')
        #print 'sel= ' +sel
        mc.rename(mesh,objName+'_mesh')
        mc.confirmDialog(b='Ok',m='Existing Objects Renamed '+objName+'_old')      
    matNode(objName)
    mc.select(objName+'_mesh')
    mc.hyperShade(assign=material)

def fileNode(name,outAttr):
    if outAttr == 'spec' : connectedAttr = 'specularColor'
    else: connectedAttr = outAttr
    obj=name+'_file_' + outAttr   
    if not mc.objExists(obj):
        print 'obj doesnt exist'
        image=mc.shadingNode('file',asTexture=True,name=obj)
        mc.setAttr(image+'.fileTextureName','sourceimages/'+name+'_'+outAttr+'.png',type='string')
        mc.connectAttr(image+'.outColor',name+'_material.'+connectedAttr)
        return image
    else:
        pass
        #mc.confirmDialog(b='Ok',m=obj+' Already Exists')
        try:
            mc.connectAttr(obj+'.outColor',name+'_material.'+connectedAttr)
        except:#catch already connected error
            textureFile=mc.getAttr(obj+'.fileTextureName')
            if not textureFile=='sourceimages/'+name+'_'+outAttr+'.png':#check for conformity 
                mc.confirmDialog(b='Ok',m = 'Texture File Mismatch: '+ textureFile)      
            else: print textureFile + ' Already Connected'
       
def matNode(name):
        material= name+'_material'
        if not mc.objExists(material): 
            mc.shadingNode('blinn',name=material,asShader=1)
            fileNode(name,'color')
            fileNode(name,'spec')
        else:
            return 'exists'
            #print material + ' already exists'
            #mc.confirmDialog(b='Ok',m= material + ' Already Exists')
                
  


#################
if __name__== 'rcFurioso' :
	ui.win()
	UI()
