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
def delay(method,string,*args): exec(method+string) #Button Delay Function
###########
#UI VARIABLES FROM MAIN
ui=rc.ui('Maya2AE')
##########
class aePrefs(iniFile):#aePrefs.ini 
	def __init__(self):
		iniFile.__init__(self,os.path.join(userDirectory(),'rcMaya2AE.ini').replace('\\','/'))
		if not os.path.isfile(self.fileName):#Defaults 
				file=open(self.fileName,'w')
				file.close()
				mc.confirmDialog(m='Set Path to After Effects')
				self.path()
				self.write('Force1080','1')
				self.write('UseGlobalTime','1')
				self.write('Layers','1')
				self.write('Objects','0')
				self.write('Behavior','Replace')
				self.write('ImageSource', 'images')
				self.write('ImageLabel', 'Label3')
	def path(self):#Write Ae Location to pref File and Update UI
		self.AEPath=mc.fileDialog2(fm=1,ds=1,okc='Set',cc='Cancel')[0]
		self.write('AELoc',self.AEPath)
		if mc.objExists('Path'): mc.menuItem('Path',e=1,l=self.get('AELoc'))
	def menuItem(self,name):#Write menuItem Value
			self.write(name,int(mc.menuItem(name,q=1,cb=1)))
	def checkBox(self,name):#Write checkBox Value
		self.write(name,int(mc.checkBox(name,q=1,v=1)))
	def set(self,att,value):#Write Value
    		self.write(att,value)
    		buildUILists()
aePrefs=aePrefs()
class scene(rc.sceneData):#Output Modifiers for Layers and Images Based on Prefs
	def outputLayer(self):
		layers=self.renderOutput()[0]
		print layers
		if aePrefs.get('ImageLabel')=='Label2':
			layers=[str(layer.replace(layer,self.shotName()+'.'+layer)) for layer in layers]
		return layers
	def outputImages(self):
		images=self.renderOutput()[1]
		if aePrefs.get('ImageSource')=='tmp':
			minTimeName=str(str(int(mc.currentTime(q=True))).zfill(self.framePad()))
			images=[str(img.replace(self.wsImagesFolder(),(self.wsImagesFolder()+'/tmp'))) for img in images]
			images=[str(img.replace('0001',minTimeName)) for img in images]
		return images		

sceneData=scene()
class writeAEX(scriptFile):
	def __init__(self,filePath):
		self.filePath=filePath
		self.sceneData=scene()
		scriptFile.__init__(self,self.filePath)
		#Globals
		self.write('var shotName="%s";'%self.sceneData.shotName())
		self.write('var width=%d;'%self.sceneData.frameWidth())
		self.write('var height=%d;'%self.sceneData.frameHeight())
		self.write('var fps=%d;'%self.sceneData.fps())
		self.write('var seconds=%s;'%self.sceneData.timelineSeconds())
		
		##CUSTOM Image Folder
		self.imageFolderName='_fromMaya'
		
		self.imageFolderIndex=self.imageFolderName+'Index'
		self.write('app.beginUndoGroup("rcMaya2AE_v1.2")')
		self.folder(self.imageFolderName)
		###ADD/EDIT
		self.write('//ADD/EDIT COMP')
		self.write(' ')
		self.write('var shotComp="";')
		self.write('for(var i=1;i<=app.project.numItems;i++){')
		self.write('	var item=app.project.item(i);')
		self.write('	if   (item.name==shotName){ shotComp = item;};')
		self.write('	}')
		self.write('if(shotComp==""){ shotComp=app.project.items.addComp(shotName,width,height,1,seconds,fps);}')
		
		self.write('else {')
		self.write('		shotComp.name=shotName;')
		self.write('		shotComp.width=width;')
		self.write('		shotComp.height=height;')
		self.write('		shotComp.seconds=seconds;')
		self.write('		shotComp.fps=fps;')
		self.write('		}')
		self.write(' ')
	
		
	def _writeAppleScript(self,jsxFile,AELoc):#write Applescript to Execute Javascript
		script=scriptFile(os.path.join(userDirectory(),'runJSX.scpt'))
		script.write('set theFile to "%s"'%jsxFile)
		script.write('open for access theFile')
		script.write('set fileContents to (read theFile)')
		script.write('close access theFile')
		script.write('tell application "%s"'%AELoc)
		script.write('  DoScript fileContents')
		script.write('end tell')
		return script.fileName
	#####
	def folder(self,folderName):#Creates Folder and/or Variable of Location 
		folderIndex=folderName+'Index'
		self.write('//ADDFOLDER %s'%(folderName))
		self.write('var %s="";'%folderIndex)
		self.write('for(var i=1;i<=app.project.numItems;i++){')
		self.write('	var item=app.project.item(i);')
		self.write('	if   (item.name=="%s"){ %s = item;};'%(folderName,folderIndex))
		self.write('	}')
		self.write('if(%s==""){%s=app.project.items.addFolder("%s")};'%(folderIndex,folderIndex,folderName))	
		self.write(' ')
	
	def layers(self):#Output Layers
		self.write('var layers=%s;'%self.sceneData.outputLayers())
		self.write('var images=%s;'%self.sceneData.outputImages())
		self.write("//Layers ")
		self.write('for(layerIndex=0;layerIndex<=layers.length-1;layerIndex++){')
		self.write('	var layerPH="";')
		self.write('	var layer="";')
		self.write('	for(var i=1;i<=%s.numItems;i++){'%self.imageFolderIndex)
		self.write('		if (%s.item(i).name==layers[layerIndex]){ layerPH=%s.item(i)}'%(self.imageFolderIndex,self.imageFolderIndex))
		self.write('	}')
		self.write('	if(layerPH==""){')
		self.write('		layerPH=app.project.importPlaceholder(layers[layerIndex],width,height,fps,seconds);')
		self.write('		layerPH.parentFolder=%s;'%self.imageFolderIndex)
		self.write('		layer=shotComp.layers.add(layerPH,seconds);')
		self.write('		layer.enabled= false;')
		self.write('		layer.moveToEnd();')
		self.write('	}')
		self.write('	if(File(images[layerIndex]).exists){')
		self.write('	layerPH.replaceWithSequence(new File(images[layerIndex]),true);')
		self.write('	layerPH.name=layers[layerIndex];')
		self.write('	layer.enabled=true;')
		self.write('	app.executeCommand(app.findMenuCommandId("Fit to Comp Width"));')
		self.write('	}')
		self.write('}')
		self.write('for(index=1;index<=shotComp.numLayers;index++){')
		self.write('	shotComp.layers[index].selected=true;}')
		self.write('app.executeCommand(app.findMenuCommandId("Fit to Comp"));')	
	
	def objects(self):#Output Objects
		self.write('//CAMERA')
		self.write('var shotCAM="";')
		self.write('for(i=1;i<=shotComp.numLayers-1;i++){')
		self.write('	if (shotComp.layers[i].name==shotName){')
		self.write('		shotCAM=shotComp.layers[i];')
		self.write('	}')
		self.write('}')
		self.write('if (shotCAM==""){')
		self.write('	shotCAM=shotComp.layers.addCamera(shotName,[0,0])')
		self.write('shotCAM.autoOrient=AutoOrientType.NO_AUTO_ORIENT;')#One Node Camera 
		self.write('}')
		
		for each in dict.values(getTaggedObjData()):
			if len(each)>0:
				each=''.join(each)#list with a string to string 
				for index in range(int(self.sceneData.endFrame()-self.sceneData.startFrame()+1)):
					curAETime=index/self.sceneData.fps()
					posValue = [i for sub in mc.getAttr(each.replace("|","_")+'_pos.translate',t=index+self.sceneData.minTime()) for i in sub]#list with a tuple to list of the tuple
					self.write('shotCAM.position.setValueAtTime(%s,%s);'%(str(curAETime),str(posValue)))
				
		self.write('//NULLS')
		#self.write('shotCAM.property("Angle of View").setValueAtTime(%f,%f);\n'%(1,70))
	#########
	def run(self):#execute written jsx by commandline (writesApplescript for mac)
		#TODO check to see if endUNDO already exists (remove)
		#self.write('app.endUndoGroup()')
		if 'darwin' in sys.platform:
			command='open '+aePrefs.get('AELoc').replace(' ','\ ') +'\n'+ 'osascript ' + self._writeAppleScript(self.fileName,os.path.basename(aePrefs.get('AELoc')).split('.')[0])
			subprocess.Popen(command,shell=True)
		else:
			command=aePrefs.get('AELoc') +' -r ' +self.fileName
			subprocess.Popen(command)

##########
rlm=rc.customAttr('renderLayerManager')
rc.rlmAttrs()
########Maya Actions
def tagAEFlag(sel):#AE COMP FLAG
	if not mc.objExists(sel+'.AECompFlag') : mc.addAttr(sel,ln='AECompFlag',dt='string')		
	#Determine Type
	if mc.objExists(sel+'.focalLength'): mc.setAttr(sel+'.AECompFlag','camera',type='string')
	elif mc.objExists(sel+'.intensity'): mc.setAttr(sel+'.AECompFlag','light',type='string')
	else : mc.setAttr(sel+'.AECompFlag','transform',type='string')	

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
#########UI
def UI():
	mc.columnLayout('renderLayers2AFX')
	mc.menuBarLayout(w=ui.rowWidth)
	mc.separator(h=5,style='in')
	mc.menu(l='File')
	
	mc.menuItem(d=True)
	mc.radioMenuItemCollection()
	mc.menuItem('New',en=0,l='New',rb=1,c=partial(delay,'aePrefs.write',"('Behavior','New')"))
	mc.menuItem('Replace',en=0,l='Replace',rb=1,c=partial(delay,'aePrefs.write',"('Behavior','Replace')"))
	mc.menuItem(aePrefs.get('Behavior'),e=1,rb=1)
	mc.menuItem(d=True)
	mc.menuItem(l='Export',c=partial(delay,'btnExport','()'))
	
	mc.menu(l='Options',to=1)
	mc.menuItem('Force1080',l='Force Comp 1080',cb=int(aePrefs.get('Force1080')),c=partial(delay,'aePrefs.menuItem',"('Force1080')"))
	mc.menuItem('UseGlobalTime',l='Use Global Frame Range',cb=int(aePrefs.get('UseGlobalTime')),c=partial(delay,'aePrefs.menuItem',"('UseGlobalTime')"))
	mc.menuItem(d=True)
	

	mc.menu(l='Label')
	mc.menuItem(d=True,l='After Effects Image Label')
	mc.radioMenuItemCollection()
	mc.menuItem('Label1',l='<CompName>.<RenderLayer>[000-000]',rb=1,c=partial(delay,'aePrefs.set',"('ImageLabel','Label1')"),en=0)
	mc.menuItem('Label2',l='<CompName>.<RenderLayer>',rb=1,c=partial(delay,'aePrefs.set',"('ImageLabel','Label2')"))
	mc.menuItem('Label3',l='<RenderLayer>',rb=1,c=partial(delay,'aePrefs.set',"('ImageLabel','Label3')"))
	mc.menuItem(aePrefs.get('ImageLabel'),e=1,rb=1)
	
	mc.menu(l='Source')
	mc.menuItem(d=True,l='workspace')
	mc.radioMenuItemCollection()
	mc.menuItem('tmp',l='tmp',rb=1,c=partial(delay,'aePrefs.set',"('ImageSource','tmp')"))
	mc.menuItem('images',l='images',rb=1,c=partial(delay,'aePrefs.set',"('ImageSource','images')"))
	mc.menuItem(aePrefs.get('ImageSource'),e=1,rb=1)
	mc.menu('Path',l='Path')
	updateMenu()
	
	
	
	
	mc.separator(h=5,style='in')
	mc.rowColumnLayout(numberOfColumns=2,columnWidth=[(1, 70),(2, 215)])
	mc.text(al='right',font='tinyBoldLabelFont',label='Comp Name: ',ann='The Name of the Comp that is Anchored to this Scene in After Effects')
	mc.textField('compAnchor',font='tinyBoldLabelFont',h=20,text=rlm.get('shotName'),cc=partial(delay,'applyrlmAttrs','()'))#,en=mc.getAttr('renderLayerManager.EnableRenderFolder')
	mc.setParent('..')
	mc.checkBox('Layers',l='Render Layers:',v=int(aePrefs.get('Layers')),cc=partial(delay,'aePrefs.checkBox',"('Layers')"))
	mc.checkBox('chkImportRLSelected',l='Selected Only',vis=0,v=0,en=0)
	mc.iconTextScrollList('AEXRenderLayerScroll',w=ui.rowWidth,h=240)
	mc.setParent('renderLayers2AFX')
	########
	mc.separator(h=15,style='in')
	mc.checkBox('Objects',l='Objects:',v=int(aePrefs.get('Objects')),cc=partial(delay,'aePrefs.checkBox',"('Objects')"))
	mc.checkBox('chkImportRCam',l='Import render Cameras:',vis=0,v=0,en=0)
	
	mc.rowLayout(w=ui.rowWidth,numberOfColumns=3)
	mc.button(w=ui.rowWidth/3,h=ui.btn_large,al='left',l=' + ',c=partial(delay,'btnPlus','(mc.ls(sl=1))')) 
	mc.button(en=0,h=ui.btn_large,w=ui.rowWidth/3,al='center',l=' - ',c=partial(delay,'btnNuke','("sel")')) 
	mc.button(h=ui.btn_large,w=ui.rowWidth/3,al='right',l='NUKE',c=partial(delay,'btnNuke','("all")'))
	mc.setParent('..')
	
	mc.iconTextScrollList('AEXObjListScroll',w=ui.rowWidth,h=200)
	mc.setParent('renderLayers2AFX')
	########
	mc.checkBox('chkAbsFrames',l='Use Timeline Frame Numbers',vis=0,v=1)
	mc.checkBox('chkOverrideTime',l='Override Timeline',vis=0,v=0,en=0)
	mc.button(l='EXPORT',w=ui.rowWidth,bgc=[.586,.473,.725],align='center',h=ui.btn_large,c=partial(delay,'btnExport','()'))
	mc.setParent('..')
	
	buildUILists()
	#mc.scriptJob('import rcMaya2AE',event=SceneOpened)
def applyrlmAttrs(): 
	mc.setAttr('renderLayerManager.shotName',mc.textField('compAnchor',q=1,text=1),type='string')
	buildUILists()
	
def updateMenu():#UPDATE
	
	mc.menu('Path',e=True,dai=True)
	mc.menuItem(d=True,dl='Maya Render Images')
	for each in sceneData.outputImages():
		mc.menuItem(each,l=each,itl=True,c=partial(delay,'spawnBrowser','("%s")'%os.path.dirname(each)))
	mc.menuItem(l='Set Path Presets',c=partial(delay,'rc.set.globals','()'))
	mc.menuItem(d=True,dl='After Effects')
	
	mc.menuItem('Image Output',l=aePrefs.get('AELoc'),itl=True,en=0)
	
	mc.menuItem(l='Set Path',c=partial(delay,'aePrefs.path','()'))
	mc.setParent('..')
	
def buildUILists():
	imageLabel=aePrefs.get('ImageLabel')
	mc.iconTextScrollList('AEXObjListScroll',e=1,ams=1,ra=1)
	mc.iconTextScrollList('AEXRenderLayerScroll',e=1,ams=0,ra=1)
	for each in mc.ls():
		if mc.objExists(each+'.AECompFlag'): mc.iconTextScrollList('AEXObjListScroll',e=1,a=each,sc=tagListCallBack)
	for i, each in enumerate(sceneData.outputLayers()):
		fileColor=[i+1,.7,0,0]
		print 
		if os.path.exists(sceneData.outputImages()[i]):
			fileColor=[i+1,0,.7,0]
		location=os.path.dirname(sceneData.outputImages()[i])
		if imageLabel=='Label2': 
			mc.iconTextScrollList('AEXRenderLayerScroll',e=1,itc=fileColor,a='%s.%s'%(rlm.get('shotName'),each))
		if imageLabel=='Label3':
			mc.iconTextScrollList('AEXRenderLayerScroll',e=1,itc=fileColor,dcc=partial(delay,'spawnBrowser','("%s")'%location),a='%s'%each)
	updateMenu()
def tagListCallBack():
	sel=[]
	[sel.append(each.replace("|","_")+'_pos') for each in mc.iconTextScrollList('AEXObjListScroll',q=1,si=1) if mc.iconTextScrollList('AEXObjListScroll',q=1,si=1) ]
			
	mc.select(sel)
###
def btnExport():
	sceneData=scene()
	xport = writeAEX(os.path.join(sceneData.ws(),'data','_AFXImport.jsx'))
	if aePrefs.get('Layers')=='1':
		xport.layers()
	if aePrefs.get('Objects')=='1':
		
		xport.objects()
	xport.run()
def btnPlus(sel):
	for each in sel: 
		tagAEFlag(each)
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
def getTaggedObjData():#WIP
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
