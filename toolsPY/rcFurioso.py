"""
Author: Rob Coakley (robcoakley@gmail.com)
Copyright (C) 2014 Robert Coakley
http://robocolabo.com/blog/
Version: 0.6
Function:
	This script takes the renderlayers and passes in Maya and imports them into After Effects 

	To install it you need to copy the script : "rcMaya2AEA.py" into a python system path or
		into your  maya user scripts directory:
		 Windows example "c:/Users/_your user name_/Documents/maya/2014/scripts/"
	If you dont know your python paths:
		In the python tab of the script editor type:
			import sys
			for each in sys.path: print each 
		The last item is usually your scripts folder 
Button Script:
	 Add this python script to a button:
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
	mc.setAttr(sel+'.FuriosoFlag','transform',type='string')	
	
def UI():
	mc.columnLayout('furiosoObjectConform')
	mc.separator(h=15,style='in')
	#mc.checkBox('Objects',l='Objects:',v=int(aePrefs.get('Objects')),cc=partial(runMethod,'aePrefs.checkBox',"('Objects')"))
	#mc.checkBox('chkImportRCam',l='Import render Cameras:',vis=0,v=0,en=0)
	
	mc.rowLayout(w=ui.rowWidth,numberOfColumns=3)
	mc.button(w=ui.rowWidth/3,h=ui.btn_large,al='left',l=' + ',c=partial(runMethod,'btnPlus','(mc.ls(sl=1))')) 
	mc.button(h=ui.btn_large,w=ui.rowWidth/3,al='center',l=' - ',c=partial(runMethod,'btnNuke','("sel")')) 
	mc.button(h=ui.btn_large,w=ui.rowWidth/3,al='right',l='NUKE',c=partial(runMethod,'btnNuke','("all")'))
	mc.setParent('..')
	
	mc.iconTextScrollList('FuriosoObjScroll',w=ui.rowWidth,h=500)
	mc.setParent('furiosoObjectConform')
	########
	mc.checkBox('chkAbsFrames',l='Use Timeline Frame Numbers',vis=0,v=1)
	mc.checkBox('chkOverrideTime',l='Override Timeline',vis=0,v=0,en=0)
	mc.button(l='EXPORT',w=ui.rowWidth,bgc=[.586,.473,.725],align='center',h=ui.btn_large,c=partial(runMethod,'btnExport','()'))
	mc.setParent('..')
	
	buildUILists()
	#mc.scriptJob('import rcMaya2AE',event=SceneOpened)
def applyrlmAttrs(): 
	mc.setAttr('renderLayerManager.shotName',mc.textField('objAnchor',q=1,text=1),type='string')
	buildUILists()
	
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
		fileColor=[index+1,.7,0.0,0.0]
		if mc.objExists(each+'.FuriosoFlag'):
			index=index+1
			mc.iconTextScrollList('FuriosoObjScroll',e=1,a=each,itc=fileColor,sc=tagListCallBack)
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
		[sel.append(each) for each in mc.iconTextScrollList('FuriosoObjScroll',q=1,si=1) if mc.iconTextScrollList('FuriosoObjScroll',q=1,si=1) ]
	except:
		pass
	mc.select(sel)
###	

def btnPlus(sel):
	for each in sel: 
		tagFuriosoFlag(each)
	buildUILists()
def btnNuke(opt): #deletes all sets and locators
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
def getTaggedObjData():#WIP
	objList=[]
	cameras=[]
	lights=[]
	positions=[]
	objList=[obj for obj in mc.ls() if mc.objExists(obj+'.FuriosoFlag')]
	for obj in objList:
		objType=mc.getAttr(obj+'.FuriosoFlag')
		if objType=='camera': cameras.append(obj)
		elif objType=='light' : lights.append(obj)
		elif objType=='transform': positions.append(obj)
	
	renderLayers=[]
	
	exportList = { 'layers':renderLayers, 'cameras': cameras, 'lights' : lights, 'positions' : positions }
	return(exportList)
def getOutputFlags():#WIP
	outputFlags={}
	outputFlags['layers']=mc.checkBox('Layers',q=1,v=1)
	outputFlags['objects']='0'#mc.checkBox('chkImportObj',q=1,v=1)
	outputFlags['Force1080']=aePrefs.get('Force1080')
	outputFlags['UseTimeline']=aePrefs.get('UseTimeline')
	outputFlags['Behavior']=aePrefs.get('Behavior')
	outputFlags['ImageSource']=aePrefs.get('ImageSource')
	outputFlags['ImageLabel']=aePrefs.get('ImageLabel')
	return(outputFlags)

###############
def sendImage():
	pass
	
#################
if __name__== 'rcMaya2AE' :
	ui.win()
	UI()
