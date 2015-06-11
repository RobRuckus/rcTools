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
from rcTools.rcMaya import *

###########
from functools import partial
def runMethod(method,string,*args): exec(method+string) #Delay Function
###########
#UI VARIABLES FROM MAIN
ui=ui('Maya2AE')
###########
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
##########
rlm=customAttr('renderLayerManager')
rlmAttrs()
########Actions
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
	
	mc.radioMenuItemCollection()
	mc.menuItem('New',en=0,l='New',rb=1,c=partial(runMethod,'aePrefs.write',"('Behavior','New')"))
	mc.menuItem('Replace',l='Replace',rb=1,c=partial(runMethod,'aePrefs.write',"('Behavior','Replace')"))
	mc.menuItem(aePrefs.get('Behavior'),e=1,rb=1)
	mc.menuItem(l='Set Image Presets',c=partial(runMethod,'set.globals','()'))
	
	mc.menu(l='Options',to=1)
	mc.menuItem('Force1080',l='Force Comp 1080',cb=int(aePrefs.get('Force1080')),c=partial(runMethod,'aePrefs.menuItem',"('Force1080')"))
	mc.menuItem('UseGlobalTime',l='Use Global Frame Range',cb=int(aePrefs.get('UseGlobalTime')),c=partial(runMethod,'aePrefs.menuItem',"('UseGlobalTime')"))
	#mc.menuItem('UseRenderGlobals',l='Use Render Globals Frame Range',cb=int(aePrefs.get('UseGlobals')),c=partial(runMethod,'aePrefs.menuItem',"('UseGlobals')"))
	mc.menuItem(d=True)
	

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
	mc.menuItem('tmp',l='tmp',rb=1,c=partial(runMethod,'aePrefs.set',"('ImageSource','tmp')"))
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
	mc.checkBox('Objects',l='Objects:',v=int(aePrefs.get('Objects')),cc=partial(runMethod,'aePrefs.checkBox',"('Objects')"))
	mc.checkBox('chkImportRCam',l='Import render Cameras:',vis=0,v=0,en=0)
	
	mc.rowLayout(w=ui.rowWidth,numberOfColumns=3)
	mc.button(w=ui.rowWidth/3,h=ui.btn_large,al='left',l=' + ',c=partial(runMethod,'btnPlus','(mc.ls(sl=1))')) 
	mc.button(en=0,h=ui.btn_large,w=ui.rowWidth/3,al='center',l=' - ',c=partial(runMethod,'btnNuke','("sel")')) 
	mc.button(h=ui.btn_large,w=ui.rowWidth/3,al='right',l='NUKE',c=partial(runMethod,'btnNuke','("all")'))
	mc.setParent('..')
	
	mc.iconTextScrollList('AEXObjListScroll',w=ui.rowWidth,h=200)
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
	
	#xport=jsx.write(os.path.join(sceneData.ws(),'data','_AFXImport.jsx'))
	#xport.comp(sceneData())
	#xport.layers(sceneData())
	#xport.run()
	
	jsxFile=writeJSX(sceneData(),getTaggedObjData(),getOutputFlags())
	if 'darwin' in sys.platform:#MAC COMMAND LINE
		command='open ' + aePrefs.get('AELoc').replace(' ','\ ') +'\n'+ 'osascript ' + writeAppleScript(jsxFile,os.path.basename(aePrefs.get('AELoc')).split('.')[0])
		subprocess.Popen(command,shell=True)
	else: #WIN COMMAND LINE
		command=aePrefs.get('AELoc')+' -r ' +jsxFile
		subprocess.Popen(command)
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
	
def writeAppleScript(jsxFile,AEApp):
	#script=scriptFile(userDirectory(),'runJSX.scpt')
	script=scriptFile(os.path.join(userDirectory(),'runJSX.scpt'))
	script.write('set theFile to "%s"'%jsxFile)
	script.write('open for access theFile')
	script.write('set fileContents to (read theFIle)')
	script.write('close access theFile')
	script.write('tell application "%s"'%AEApp)
	script.write('  DoScript fileContents')
	script.write('end tell')
	return script.fileName
def writeJSX(sceneData,objects,flags):
	imageFolderName='_fromMaya'
	
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
	jsx=scriptFile(os.path.join(sceneData.ws(),'data','_AFXImport.jsx'))
	if aePrefs.get('ImageSource')=='images':
		minTimeName=str(sceneData.minTime()).zfill(sceneData.framePad())
		maxTimeName=str(sceneData.maxTime()).zfill(sceneData.framePad())
		images=sceneData.renderOutput()[1]
	else:#TMP Imagelocation
		minTimeName=str(str(int(mc.currentTime(q=True))).zfill(sceneData.framePad()))
		maxTimeName=str((str(mc.currentTime(q=True)+1)).zfill(sceneData.framePad()))
		images=sceneData.renderOutput()[1]
		images=[str(img.replace(sceneData.wsImagesFolder(),os.path.join(sceneData.wsImagesFolder(),'tmp'))) for img in images]
		images=[str(img.replace('0001',minTimeName)) for img in images]
	############
	#imageNameExtension='[%s-%s]%s'%(minTimeName,maxTimeName,os.path.splitext(sceneData.renderOutput()[0])[1]) #[004-0091].png
	#if aePrefs.get('ImageLabel')=='Label1': layerNames=[str(rlmAttrs().get('shotName'))+'.'+str(x) + str(imageNameExtension) for x in sceneData['outputLayers']]#ShotName.Layer.[000=000]
	#if aePrefs.get('ImageLabel')=='Label2': layerNames=[str(rlmAttrs().get('shotName'))+'.'+str(x) for x in sceneData['outputLayers']]#ShotName.Layer
	#if aePrefs.get('ImageLabel')=='Label3': layerNames=[str(x) for x in sceneData['outputLayers']]#Layer
	############
	jsx.write('app.beginUndoGroup("rcMaya2AE");')
	############
	jsx.write('var shotName="%s";'%mc.getAttr('renderLayerManager.shotName'))
	jsx.write('var imageFolderName="%s";'%imageFolderName)
	jsx.write('var width=%d;'%sceneData.frameWidth())
	jsx.write('var height=%d;'%sceneData.frameHeight())
	jsx.write('var fps=%d;'%sceneData.fps())
	jsx.write('var layers=%s;'%sceneData.renderOutput()[0])#TODO format from iconTextScrollList
	if aePrefs.get('ImageSource')=='images': jsx.write('var seconds=%s;'%sceneData.timelineSeconds())
	else: jsx.write('var seconds=%s;'%10)#default 10sec for stills
	jsx.write('var images=%s;'%images)
	jsx.write('//ADD IF NOT EXISTS IMAGE FOLDER AND INDEX \n')
	jsx.write('var imageFolder="";')
	jsx.write('for(var i=1;i<=app.project.numItems;i++){\n')
	jsx.write('	var item=app.project.item(i);\n')
	jsx.write('	if   (item.name==imageFolderName){ imageFolder = item;};')
	jsx.write('	}')
	jsx.write('if(imageFolder==""){imageFolder=app.project.items.addFolder(imageFolderName)};')
	#else update Shot Folder
	jsx.write('//ADD COMP ELSE UPDATE')
	jsx.write('var shotComp="";')
	jsx.write('for(var i=1;i<=app.project.numItems;i++){')
	jsx.write('	var item=app.project.item(i);')
	jsx.write('	if   (item.name==shotName){ shotComp = item;};')
	jsx.write('	}')
	jsx.write('if(shotComp==""){ shotComp=app.project.items.addComp(shotName,width,height,1,seconds,fps);}')
	jsx.write(' else {')
	jsx.write('		shotComp.name=shotName;')
    	jsx.write('		shotComp.width=width;')
    	jsx.write('		shotComp.height=height;')
    	jsx.write('		shotComp.seconds=seconds;')
    	jsx.write('		shotComp.fps=fps;')
    	jsx.write('		}')
	jsx.write("//IMPORT  ")
	#LAYERS
	if flags['layers']:
		jsx.write("//Layers ")
		jsx.write('for(layerIndex=0;layerIndex<=layers.length-1;layerIndex++){')
		jsx.write('	var layerPH="";')
		jsx.write('	var layer="";')
		jsx.write('	for(var i=1;i<=imageFolder.numItems;i++){')
		jsx.write('		if (imageFolder.item(i).name==layers[layerIndex]){ layerPH=imageFolder.item(i)}')
		jsx.write('	}')
		jsx.write('	if(layerPH==""){')
		jsx.write('		layerPH=app.project.importPlaceholder(layers[layerIndex],width,height,fps,seconds);')
		jsx.write('		layerPH.parentFolder=imageFolder;')
		jsx.write('		layer=shotComp.layers.add(layerPH,seconds);')
		jsx.write('		layer.enabled= false;')
		jsx.write('		layer.moveToEnd();')
		jsx.write('	}')
		jsx.write('	if(File(images[layerIndex]).exists){')#replace(/\//gi,"\\\\")) OS BACKSLASHING
		jsx.write('	layerPH.replaceWithSequence(new File(images[layerIndex]),true);')#replace(/\//gi,"\\\\")
		jsx.write('	layerPH.name=layers[layerIndex];')
		jsx.write('	layer.enabled=true;')
		jsx.write('	app.executeCommand(app.findMenuCommandId("Fit to Comp Width"));')
		jsx.write('	}')
		jsx.write('}')
		jsx.write('	for(index=1;index<=shotComp.numLayers;index++){')
		jsx.write('		shotComp.layers[index].selected=true;')
		jsx.write('		app.executeCommand(app.findMenuCommandId("Fit to Comp")); }')

	#OBJECTS WIP
	if flags['objects']:
		jsx.write("//OBJECTS ")
		jsx.write('app.endUndoGroup()')
	return jsx.fileName

#################
if __name__== 'rcMaya2AE' :
	ui.win(floating=True)
	UI()
