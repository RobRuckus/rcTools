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
from rcTools2.main import *
###########
from functools import partial
def runMethod(method,string,*args): exec(method+string) #Delay Function
###########
#UI VARIABLES FROM MAIN
ui=ui()
###########
class aePrefs(iniFile):#aePrefs.ini 
	def __init__(self):
		iniFile.__init__(self,os.path.join(userDirectory(),'rcMaya2AE.ini').replace('\\','/'))
		if not os.path.isfile(self.fileName):
				file=open(self.fileName,'w')
				file.close()
				mc.confirmDialog(m='Set Path to After Effects')
				self.path()
				self.write('Force1080','1')
				self.write('UseTimeline','1')
				self.write('Layers','1')
				self.write('Objects','0')
				self.write('Behavior','Replace')
				self.write('ImageSource', 'images')
				self.write('ImageLabel', 'Label3')
	def path(self):
		self.AEPath=mc.fileDialog2(fm=1,ds=1,okc='Set',cc='Cancel')[0]
		self.write('AELoc',self.AEPath)
		if mc.objExists('Path'): mc.menuItem('Path',e=1,l=self.get('AELoc'))
	def menuItem(self,name):#Used to write values
			self.write(name,int(mc.menuItem(name,q=1,cb=1)))
	def checkBox(self,name):
		self.write(name,int(mc.checkBox(name,q=1,v=1)))
	def set(self,att,value):
    		self.write(att,value)
    		buildUILists()
aePrefs=aePrefs()
##########
rlm=customAttr('renderLayerManager')
rlmAttrs()
########CONSTRAINER
def constrainWS(sel,opt,suffix='_pos'):
	conName=sel.replace("|","_")+suffix
	if not mc.objExists('x_AEPos'): mc.group(em=1,name='x_AEPos',w=1)
	if opt=='con':
		if not mc.objExists(conName): 
			mc.createNode('parentConstraint',name=conName)
			mc.connectAttr(sel+'.translate',conName+'.target[0].targetTranslate',force=1)
			mc.connectAttr(sel+'.parentMatrix',conName+'.target[0].targetParentMatrix',force=1)
			mc.connectAttr(sel+'.scale',conName+'.target[0].targetScale',force=1)
			mc.connectAttr(sel+'.rotateOrder',conName+'.target[0].targetRotateOrder',force=1)
			mc.connectAttr(sel+'.rotate',conName+'.target[0].targetRotate',force=1)
			mc.connectAttr(sel+'.rotatePivotTranslate',conName+'.target[0].targetRotateTranslate',force=1)
			mc.connectAttr(sel+'.rotatePivot',conName+'.target[0].targetRotatePivot',force=1)
			mc.connectAttr(conName+'.constraintTranslate',conName+'.translate',force=1)
			mc.connectAttr(conName+'.constraintRotate',conName+'.rotate',force=1)
			mc.setAttr(conName+'.displayHandle',1)
	if opt=='null':
		if mc.objExists(conName): mc.delete(conName)
		loc=mc.spaceLocator(name=conName)
		mc.parentConstraint(sel,loc)
	
		
		


#class scriptsJob:
	#def __init__(self):
		#self.myFunction()
		#self.createScriptJob()
	#def createScriptJob(self):
		#self.scriptJobNum=mc.scriptJob(ct=['delete',self.myFunction],killwithScene=1)
	#def deleteScriptJob(self):
		#mc.scriptJob(k=self.scriptJobNum,force=1)
	#def myFunction(self):
		#if (mc.objExists('AEpyList'):
			#for each in mc.iconTextScrollList('AEXObjListScroll'
		#buildUILists()
#scriptsJob=scriptsJob()	
#########UI
def UI():
	mc.columnLayout('renderLayers2AFX')
	mc.menuBarLayout(w=ui.rowWidth)
	mc.separator(h=5,style='in')
	mc.menu(l='File')
	
	mc.radioMenuItemCollection()
	mc.menuItem('New',en=0,l='New',rb=1,c=partial(runMethod,'aePrefs.write',"('Behavior','New')"))
	mc.menuItem('Replace',l='Replace',rb=1,c=partial(runMethod,'aePrefs.write',"('Behavior','Replace')"))
	mc.menuItem(aePrefs.get('Behavior'),e=1,rb=1)
	mc.menuItem(l='Set Image Presets',c=partial(runMethod,'set.globals','()'))
	
	mc.menu(l='Options',to=1)
	mc.menuItem('Force1080',l='Force Comp 1080',cb=int(aePrefs.get('Force1080')),c=partial(runMethod,'aePrefs.menuItem',"('Force1080')"))
	mc.menuItem('UseTimeline',en=0,l='Use Timeline Frame Numbers',cb=int(aePrefs.get('UseTimeline')),c=partial(runMethod,'aePrefs.menuItem',"('UseTimeline')"))
	mc.menuItem(d=True)
	#mc.menuItem(l='RenderLayers',cb=True)
	#mc.menuItem(l='Objects',cb=False)

	mc.menu(l='Label')
	mc.menuItem(d=True,l='Ae Image Label')
	mc.radioMenuItemCollection()
	mc.menuItem('Label1',l='<CompName>.<RenderLayer>[000-000]',rb=1,c=partial(runMethod,'aePrefs.set',"('ImageLabel','Label1')"))
	mc.menuItem('Label2',l='<CompName>.<RenderLayer>',rb=1,c=partial(runMethod,'aePrefs.set',"('ImageLabel','Label2')"))
	mc.menuItem('Label3',l='<RenderLayer>',rb=1,c=partial(runMethod,'aePrefs.set',"('ImageLabel','Label3')"))
	mc.menuItem(aePrefs.get('ImageLabel'),e=1,rb=1)
	
	mc.menu(l='Source')
	mc.menuItem(d=True,l='workspace')
	mc.radioMenuItemCollection()
	mc.menuItem('tmp',en=0,l='tmp',rb=1,c=partial(runMethod,'aePrefs.set',"('ImageSource','tmp')"))
	mc.menuItem('images',l='images',rb=1,c=partial(runMethod,'aePrefs.set',"('ImageSource','images')"))
	mc.menuItem(aePrefs.get('ImageSource'),e=1,rb=1)
	
	
	mc.menu(l='Path')
	mc.menuItem(d=True,l='After Effects')
	mc.menuItem('Path',l=aePrefs.get('AELoc'),itl=True,en=0)
	mc.menuItem(l='Set Path',c=partial(runMethod,'aePrefs.path','()'))
	
	mc.setParent('..')
	
	mc.separator(h=5,style='in')
	mc.rowColumnLayout(numberOfColumns=2,columnWidth=[(1, 70),(2, 215)])
	mc.text(al='right',font='tinyBoldLabelFont',label='Comp Name: ',ann='The Name of the Comp that is Anchored to this Scene in After Effects')
	mc.textField('compAnchor',font='tinyBoldLabelFont',h=20,text=rlm.get('shotName'),cc=partial(runMethod,'applyrlmAttrs','()'))#,en=mc.getAttr('renderLayerManager.EnableRenderFolder')
	mc.setParent('..')
	mc.checkBox('Layers',l='Render Layers:',v=int(aePrefs.get('Layers')),cc=partial(runMethod,'aePrefs.checkBox',"('Layers')"))
	mc.checkBox('chkImportRLSelected',l='Selected Only',vis=0,v=0,en=0)
	mc.iconTextScrollList('AEXRenderLayerScroll',w=ui.rowWidth,h=240)
	mc.setParent('renderLayers2AFX')
	########
	mc.separator(h=15,style='in')
	mc.checkBox('Objects',l='Objects:',en=0,v=int(aePrefs.get('Objects')),cc=partial(runMethod,'updateINI',"('Objects')"))
	mc.checkBox('chkImportRCam',l='Import render Cameras:',vis=0,v=0,en=0)
	
	mc.rowLayout(w=ui.rowWidth,numberOfColumns=3)
	mc.button(w=ui.rowWidth/3,h=ui.btn_large,al='left',l=' + ',c=partial(runMethod,'btnTag','(mc.ls(sl=1))')) 
	mc.button(en=0,h=ui.btn_large,w=ui.rowWidth/3,al='center',l=' - ',c=partial(runMethod,'btnNuke','("sel")')) 
	mc.button(h=ui.btn_large,w=ui.rowWidth/3,al='right',l='NUKE',c=partial(runMethod,'btnNuke','("all")'))
	mc.setParent('..')
	
	mc.iconTextScrollList('AEXObjListScroll',w=ui.rowWidth,h=200,vis=1)
	mc.setParent('renderLayers2AFX')
	########
	mc.checkBox('chkAbsFrames',l='Use Timeline Frame Numbers',vis=0,v=1)
	mc.checkBox('chkOverrideTime',l='Override Timeline',vis=0,v=0,en=0)
	mc.button(l='EXPORT',w=ui.rowWidth,bgc=[.586,.473,.725],align='center',h=ui.btn_large,c=partial(runMethod,'btnExport','()'))

	mc.setParent('..')
	buildUILists()
def applyrlmAttrs(): 
	mc.setAttr('renderLayerManager.shotName',mc.textField('compAnchor',q=1,text=1),type='string')
	buildUILists()

def buildUILists():
	scene=sceneData()
	imageLabel=aePrefs.get('ImageLabel')
	mc.iconTextScrollList('AEXObjListScroll',e=1,ams=1,ra=1)
	mc.iconTextScrollList('AEXRenderLayerScroll',e=1,ams=1,ra=1)
	for each in mc.ls():
		if mc.objExists(each+'.AECompFlag'): mc.iconTextScrollList('AEXObjListScroll',e=1,a=each,sc=tagListSelect)
	for each in scene.renderOutput()[0]:
		if imageLabel=='Label2': mc.iconTextScrollList('AEXRenderLayerScroll',e=1,a='%s.%s'%(rlm.get('shotName'),each))
		if imageLabel=='Label3': mc.iconTextScrollList('AEXRenderLayerScroll',e=1,a='%s'%each)
		#mc.iconTextScrollList('AEXRenderLayerScroll',e=1,a=each)
def tagListSelect():
	sel=[]
	for each in mc.iconTextScrollList('AEXObjListScroll',q=1,si=1): sel.append(each.replace("|","_")+'_pos')
	mc.select(sel)
def btnExport():
	jsxFile=writeJSX(sceneData(),getTaggedObjData(),getOutputFlags())
	if 'darwin' in sys.platform:
		command='open ' + aePrefs.get('AELoc').replace(' ','\ ') +'\n'+ 'osascript ' + writeAppleScript(jsxFile,os.path.basename(aePrefs.get('AELoc')).split('.')[0])
		subprocess.Popen(command,shell=True)
	else: 
		command=aePrefs.get('AELoc')+' -r ' +jsxFile
		subprocess.Popen(command)
def btnTag(sel):
	for each in sel:
		if not mc.objExists(each+'.AECompFlag') : mc.addAttr(each,ln='AECompFlag',dt='string')		
		#Determine Type
		if mc.objExists(each+'.focalLength'): mc.setAttr(each+'.AECompFlag','camera',type='string')
		elif mc.objExists(each+'.intensity'): mc.setAttr(each+'.AECompFlag','light',type='string')
		else : mc.setAttr(each+'.AECompFlag','transform',type='string')
		constrainWS(each,'null')	
		buildUILists()
def btnNuke(opt): #deletes all sets and locators
	if opt=='all':
		for each in mc.ls():
			if mc.objExists(each+'.AECompFlag'): mc.deleteAttr(each+'.AECompFlag')
			if mc.objExists(each.replace('|','_')+'_pos'):mc.delete(each.replace('|','_')+'_pos')
	if opt=='sel':
		for each in mc.ls(sl=1):
			if mc.objExists(each+'.AECompFlag'): mc.deleteAttr(each+'.AECompFlag')
			if mc.objExists(each+'_pos'):mc.delete(each+'_pos')
	buildUILists()
################
def getTaggedObjData():
	objList=[]
	cameras=[]
	lights=[]
	positions=[]
	objList=[obj for obj in mc.ls() if mc.objExists(obj+'.AECompFlag')]
	for obj in objList:
		objType=mc.getAttr(obj+'.AECompFlag')
		if objType=='camera': cameras.append(obj)
		elif objType=='light' : lights.append(obj)
		elif objType=='transform': positions.append(obj)
	
	renderLayers=[]
	
	exportList = { 'layers':renderLayers, 'cameras': cameras, 'lights' : lights, 'positions' : positions }
	return(exportList)
def getOutputFlags():
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
def writeAppleScript(jsxFile,AEApp):
	script=scriptFile(userDirectory(),'runJSX.scpt')
	script.write('set theFile to "%s"'%jsxFile)
	script.write('open for access theFile')
	script.write('set fileContents to (read theFIle)')
	script.write('close access theFile')
	script.write('tell application "%s"'%AEApp)
	script.write('  DoScript fileContents')
	script.write('end tell')
	return script.fileName
def writeJSX(sceneData,objects,flags):
	def toAELens(focalLength,debug=1):
		lens=focalLength*(sceneData.get('width')*0.03125)
		if debug: print lens
		else: return lens
	def toAERot(rotation	,debug=1):
		AErot=rotation
		if debug: print AErot
		else: return AErot
	def toAEScale(position,debug=1):
		AEpos=position
		if debug: print AEpos
		else: return AEpos
	############
	jsxFile=scriptFile(sceneData.ws()+'/data/','_AFXImport.jsx')
	imageFolderName='_images'
	minTimeName=str(sceneData.minTime()).zfill(sceneData.framePad())
	maxTimeName=str(sceneData.maxTime()).zfill(sceneData.framePad())
	############
	#imageNameExtension='[%s-%s]%s'%(minTimeName,maxTimeName,os.path.splitext(sceneData.renderOutput()[0])[1]) #[004-0091].png
	#if aePrefs.get('ImageLabel')=='Label1': layerNames=[str(rlmAttrs().get('shotName'))+'.'+str(x) + str(imageNameExtension) for x in sceneData['outputLayers']]#ShotName.Layer.[000=000]
	#if aePrefs.get('ImageLabel')=='Label2': layerNames=[str(rlmAttrs().get('shotName'))+'.'+str(x) for x in sceneData['outputLayers']]#ShotName.Layer
	#if aePrefs.get('ImageLabel')=='Label3': layerNames=[str(x) for x in sceneData['outputLayers']]#Layer
	layerNames=sceneData.renderOutput()[0]
	images=sceneData.renderOutput()[1]
	############
	jsxFile.write('app.beginUndoGroup("rcMaya2AE");')
	############
	jsxFile.write('var shotName="%s";'%mc.getAttr('renderLayerManager.shotName'))
	jsxFile.write('var imageFolderName="%s";'%imageFolderName)
	jsxFile.write('var width=%d;'%sceneData.frameWidth())
	jsxFile.write('var height=%d;'%sceneData.frameHeight())
	jsxFile.write('var fps=%d;'%sceneData.fps())
	jsxFile.write('var layers=%s;'%layerNames)#TODO format from iconTextScrollList
	if aePrefs.get('ImageSource')=='images':
		jsxFile.write('var seconds=%s;'%sceneData.timelineSeconds())
		jsxFile.write('var images=%s;'%images)
	############
	jsxFile.write('//ADD IF NOT EXISTS IMAGE FOLDER\n')
	jsxFile.write('var imageFolder="";')
	jsxFile.write('for(var i=1;i<=app.project.numItems;i++){\n')
	jsxFile.write('	var item=app.project.item(i);\n')
	jsxFile.write('	if   (item.name==imageFolderName){ imageFolder = item;};')
	jsxFile.write('	}')
	jsxFile.write('if(imageFolder==""){imageFolder=app.project.items.addFolder(imageFolderName)};')
	#ADD IF NOT EXISTS SHOT FOLDER
		#else update Shot Folder
	
	#ADD else UPDATE
	jsxFile.write('//ADD COMP')
	jsxFile.write('var shotComp="";')
	jsxFile.write('for(var i=1;i<=app.project.numItems;i++){')
	jsxFile.write('	var item=app.project.item(i);')
	jsxFile.write('	if   (item.name==shotName){ shotComp = item;};')
	jsxFile.write('	}')
	jsxFile.write('if(shotComp==""){ shotComp=app.project.items.addComp(shotName,width,height,1,seconds,fps);}')
	#ADD else UPDATE
	jsxFile.write("//IMPORT  ")
	#LAYERS
	if flags['layers']:
		jsxFile.write("//Layers ")
		jsxFile.write('for(layerIndex=0;layerIndex<=layers.length-1;layerIndex++){')
		jsxFile.write('	var layerPH="";')
		jsxFile.write('	var layer="";')
		jsxFile.write('	for(var i=1;i<=imageFolder.numItems;i++){')
		jsxFile.write('		if (imageFolder.item(i).name==layers[layerIndex]){ layerPH=imageFolder.item(i)}')
		jsxFile.write('	}')
		jsxFile.write('	if(layerPH==""){')
		jsxFile.write('		layerPH=app.project.importPlaceholder(layers[layerIndex],width,height,fps,seconds);')
		jsxFile.write('		layerPH.parentFolder=imageFolder;')
		jsxFile.write('		layer=shotComp.layers.add(layerPH,seconds);')
		jsxFile.write('		layer.enabled= false;')
		jsxFile.write('		layer.moveToEnd();')
		jsxFile.write('	}')
		jsxFile.write('	if(File(images[layerIndex].replace(/\//gi,"\\\\")).exists){')
		jsxFile.write('	layerPH.replaceWithSequence(new File(images[layerIndex].replace(/\//gi,"\\\\")),true);')
		jsxFile.write('	layerPH.name=layers[layerIndex];')
		jsxFile.write('	}')
		jsxFile.write('}')
	
	#OBJECTS WIP
	if flags['objects']:
		jsxFile.write("//OBJECTS ")
		for obj in dict.values(objects):
			if len(obj)>0:
				for each in obj:
					each=''.join(each)
					objType=mc.getAttr(each+'.AECompFlag')
					if objType=='light':
						jsxFile.write('var newObj=shotComp.layers.addLight("'+each+'",[0,0])'+'')
						jsxFile.write('   newObj.autoOrient=AutoOrientType.NO_AUTO_ORIENT;')
					if objType=='transform':
						jsxFile.write('var newObj= shotComp.layers.addNull(shotComp.duration) ')
						jsxFile.write('	newObj.name="'+each+'";')
						jsxFile.write('	newObj.threeDLayer=true;')
					if objType=='camera':
						jsxFile.write('var newObj= shotComp.layers.addCamera("'+each+'",[0,0])'+'')
						#jsxFile.write('	newObj.property("zoom").
					for index in range (int(sceneData.maxTime-sceneData.minTime+1)):#KEYFRAMES
						curAETime=(index+sceneData.minTime)/sceneData['fps']
						posValue = [i for sub in mc.getAttr(each.replace("|","_")+'_pos.translate',t=index+sceneData.minTime) for i in sub]#list with a tuple to list of the tuple 
						rotValue= [i for sub in mc.getAttr(each.replace("|","_")+'_pos.rotate',t=index+sceneData.minTime) for i in sub]
						#jsxFile.write('		newObj.position.setValueAtTime('+str(curAETime)+','+str(posValue)+');')
						#jsxFile.write('		newObj.xRotation.setValueAtTime('+str(curAETime)+','+str(rotValue[0])+');')
						#jsxFile.write('		newObj.yRotation.setValueAtTime('+str(curAETime)+','+str(rotValue[1])+');')
						#jsxFile.write('		newObj.zRotation.setValueAtTime('+str(curAETime)+','+str(rotValue[2])+');')
	jsxFile.write('app.endUndoGroup()')
	return jsxFile.fileName

#################
if __name__== 'rcMaya2AE' :
	windowName='AEExport'
	if (mc.window(windowName,exists=True)): mc.deleteUI(windowName)
	mc.window(windowName, mxb=0,menuBar=0,title='rc.Layers2Ae',tlb=True,)
	#mc.frameLayout('Export',l='Render Layer and Passes to After Effects',bs='in',fn='smallBoldLabelFont',vis=0)
	UI()
	mc.showWindow()


