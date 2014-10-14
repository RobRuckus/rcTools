####IMPORT
import os 
import sys
import maya.cmds as mc
import maya.mel
from datetime import datetime
###UI VARIABLES 
buttons_small=20
buttons_med=25
buttons_large=30
checkBoxHeight=15
textSize=17
textHeight=10
rowWidth=300
iconDim=15
iconSize=13
borders=2
tabWidth=765
titleFont='boldLabelFont'
fieldFont='fixedWidthFont'
###########PATH VARIABLES
importPath= os.path.dirname(__file__)
iconPath=os.path.join(importPath,'icons','')
toolsPY=os.path.join(importPath,'toolsPY','')
toolsMEL=os.path.join(importPath,'toolsMEL','')
scriptsMEL=os.path.join(importPath,'scriptsMEL','')
scriptsPY=os.path.join(importPath,'scriptsPY','')
###########
def nameConvert(string):
	string=string.replace('|','_')
	if string.startswith('_'): return string[1:]
	else: return string
def backupFolder(): return str(datetime.now()).replace('-','.').replace(' ','-').replace(':','.')
def userDirectory():
	if 'darwin' in sys.platform:
		userDirectory=os.environ['HOME']
	else:
		userDirectory=os.environ['USERPROFILE']
	return userDirectory
class sceneData(object):
	def __init__(self):
		self.ws=os.path.normpath(mc.workspace(q=True,rd=True))
		self.wsImagesName=mc.workspace('images',q=True,fileRuleEntry=True)
		self.wsImagesFolder=os.path.normpath(os.path.join(self.ws,self.wsImagesName))
		self.frameWidth=mc.getAttr('defaultResolution.width')
		self.frameHeight=mc.getAttr('defaultResolution.height')
		self.framePad=mc.getAttr('defaultRenderGlobals.extensionPadding')
		self.minTime=int(mc.playbackOptions(q=True,minTime=True))
		self.maxTime=int(mc.playbackOptions(q=True,maxTime=True))
		self.fps= {"game":15.0, "film":24.0, "pal":25.0, "ntsc":30.0, "show":48.0, "palf":50.0, "ntscf":60.0}[mc.currentUnit(q=True, fullName=True, time=True)]
		self.timelineSeconds= (mc.playbackOptions(q=1,maxTime=1)+1)/self.fps
		self.cameras=[str(mc.listRelatives(sceneCamera,p=1,f=1)[0]) for sceneCamera in mc.ls(ca=1)]
		self.renderCameras=[str(mc.listRelatives(renderCamera,p=1,f=1)[0]) for renderCamera in mc.ls(ca=1) if mc.getAttr(str(renderCamera)+'.renderable')]
		self.renderLayers= [str(x) for x in mc.ls(typ='renderLayer')]#convert unicode list to string list USES defaultRenderlayer = NEEDED for Logic
		self.renderLayerNames=['masterLayer' if 'defaultRenderLayer' in x else x for x in self.renderLayers]
		self.imageFilePrefix=mc.getAttr('defaultRenderGlobals.imageFilePrefix')# Prefix from Render Globals : <RenderLayers>/<RenderPass>/<RenderLayer>.<RenderPass>
		self.imageFileSuffix=''.join(mc.renderSettings(fin=1,lut=1))#masterLayer/<RenderPass>/masterLayer.0001.png
		self.imageFilePath=''.join(mc.renderSettings(fin=1,lut=1,fp=1))#PROJECT/IMAGES/masterLayer/<RenderPass>/masterLayer.0001.png
	def renderOutput(self):
		outputLayers= []
		outputImages=[]
		currentLayer=str(mc.editRenderLayerGlobals(q=1,crl=1)).replace('defaultRenderLayer','masterLayer')
		for layer in self.renderLayers:
			if not self.imageFilePrefix== None:
				connections= mc.listConnections(layer+'.renderPass')
				if len(self.renderCameras)==1:
					outReplacedLayer=self.imageFilePath.replace(currentLayer,layer)
					if connections: connections.append('masterBeauty')
					else: connections=['masterBeauty']
					for connection in connections: 
						outputImages.append(outReplacedLayer.replace('<RenderPass>',connection).replace('defaultRenderLayer','masterLayer'))
						outputLayers.append('%s.%s'%(layer.replace('defaultRenderLayer','masterLayer'),connection))
				else:#More Than One Render Camera
					outReplacedLayer=self.imageFilePath.replace(currentLayer,layer)
					if connections: connections.append('masterBeauty')
					else: connections=['masterBeauty']
					for camera in self.renderCameras:       
						for connection in connections:
							outputImages.append(outReplacedLayer.replace('<RenderPass>',connection).replace('defaultRenderLayer','masterLayer').replace(nameConvert(self.renderCameras[0]),camera))
							outputLayers.append('%s.%s.%s'%(camera,layer.replace('defaultRenderLayer','masterLayer'),connection))      
		return[outputLayers,outputImages]



###########
def getSceneData():#OLD NEED TO REMOVE
	workspace=mc.workspace(q=1,rd=1)
	wsImagesName=mc.workspace('images',q=1,fileRuleEntry=1)# 'images'
	wsImagesFolder=workspace+wsImagesName+'/'
	
	framePadding=mc.getAttr('defaultRenderGlobals.extensionPadding')
	frameWidth=mc.getAttr('defaultResolution.width')
	frameHeight=mc.getAttr('defaultResolution.height')

	minTime=int(mc.playbackOptions(q=1,minTime=1))
	maxTime=int(mc.playbackOptions(q=1,maxTime=1))
	fps= {"game":15.0, "film":24.0, "pal":25.0, "ntsc":30.0, "show":48.0, "palf":50.0, "ntscf":60.0}[mc.currentUnit(q=True, fullName=True, time=True)]
	shotSeconds= (mc.playbackOptions(q=1,maxTime=1)+1)/fps
	
	sceneCameras=[str(mc.listRelatives(sceneCamera,p=1,f=1)[0]) for sceneCamera in mc.ls(ca=1)]
	renderCameras=[str(mc.listRelatives(renderCamera,p=1,f=1)[0]) for renderCamera in mc.ls(ca=1) if mc.getAttr(str(renderCamera)+'.renderable')]
	
	layers=[str(x) for x in mc.ls(typ='renderLayer')]#convert unicode list to string list USES defaultRenderlayer = NEEDED for Logic
	layerNames=['masterLayer' if 'defaultRenderLayer' in x else x for x in layers]
	imageFilePrefix= mc.getAttr('defaultRenderGlobals.imageFilePrefix')# Prefix from Render Globals : <RenderLayers>/<RenderPass>/<RenderLayer>.<RenderPass>
	outImageSuffix=''.join(mc.renderSettings(fin=1,lut=1))#masterLayer/<RenderPass>/masterLayer.0004.png
	outImageFilePath=''.join(mc.renderSettings(fin=1,lut=1,fp=1))
	
	
	def renderOutput():
		outputLayers= []
		outputImages=[]
		currentLayer=str(mc.editRenderLayerGlobals(q=1,crl=1)).replace('defaultRenderLayer','masterLayer')
		for layer in layers:
			if not imageFilePrefix== None:
				connections= mc.listConnections(layer+'.renderPass')
				if len(renderCameras)==1:
					outReplacedLayer=outImageFilePath.replace(currentLayer,layer)
					if connections: connections.append('masterBeauty')
					else: connections=['masterBeauty']
					for connection in connections: 
						outputImages.append(outReplacedLayer.replace('<RenderPass>',connection).replace('defaultRenderLayer','masterLayer'))
						outputLayers.append('%s.%s'%(layer.replace('defaultRenderLayer','masterLayer'),connection))
				else:#More Than One Render Camera
					outReplacedLayer=outImageFilePath.replace(currentLayer,layer)
					if connections: connections.append('masterBeauty')
					else: connections=['masterBeauty']
					for camera in renderCameras:       
						for connection in connections:
							outputImages.append(outReplacedLayer.replace('<RenderPass>',connection).replace('defaultRenderLayer','masterLayer').replace(nameConvert(renderCameras[0]),camera))
							outputLayers.append('%s.%s.%s'%(camera,layer.replace('defaultRenderLayer','masterLayer'),connection))      
		return[outputLayers,outputImages]
			
			
	#Return
	sceneData ={
			'workspace' : workspace,
			'wsImagesName':wsImagesName,
			'wsImagesFolder':wsImagesFolder,
			
			'cameras': sceneCameras,
			'renderCameras':renderCameras,
			
			'width': frameWidth,
			'height':frameHeight,
			'fps':fps,
			'minTime':minTime,
			'maxTime':maxTime,
			'seconds':shotSeconds,
			
			'outputLayers':renderOutput()[0],
			'outputImages':renderOutput()[1],

			'layers':layers,
			'layerNames':layerNames,
			'framePadding':framePadding,
			}
	return(sceneData)
def shelf(shelfName='rcTools'):#WIP
	#getMainWindow of Maya
	if not mc.shelfTabLayout(shelf,q=True, exists=True):
		mc.shelfTabLayout(tl=('mainWindow',shelfName))
def rlmAttrs():#custom renderLayerManager Attributes for tools using customAttr class
	rlm=customAttr('renderLayerManager')
	rlm.define('project',mc.workspace(q=1,rd=1))
	rlm.define('shotName','SH01')
	rlm.define('enableAbsoluteRenderFolder',False)
	rlm.define('absoluteRenderFolder',os.path.join(mc.workspace(q=1,rd=1),'scenes'))
	rlm.define('enablePrefixRenderLayer',False)
	rlm.define('prefixRenderLayer','L')
	rlm.define('enableSingleFileName',False)
	rlm.define('singleFileName','custom')
	rlm.define('notes',' ')

###########
class customAttr():#CRUD attributes on Nodes
    def __init__(self,holder):
        self.holder=holder	
    def _attName(self,att):
        return r'%s.%s'%(self.holder,att)
    def _type(self,value):
        return ('%s'%type(value)).replace('<type \'str\'>','string').replace('<type \'bool\'>','bool').replace('<type \'unicode\'>','string')
    def define(self,att,value):
    	 if not mc.objExists(self._attName(att)):
            if self._type(value) =='string': mc.addAttr(self.holder,ln=att,keyable=True,dt=self._type(value))
            if self._type(value) =='bool': mc.addAttr(self.holder,ln=att,keyable= True,at=self._type(value))
            self.set(att,value)	
    def set(self,att,value):
        if not mc.objExists(self._attName(att)): 
        	self.define(att,value)
        if self._type(value) =='string':  mc.setAttr(self._attName(att),value,e=1,keyable=True,type=self._type(value))
        if self._type(value) =='bool': mc.setAttr(self._attName(att),value,e=1)
    def get(self,att):
        return mc.getAttr(self._attName(att))	
	
class scriptFile():#Creates/Writes Files Line by Line
    def __init__(self,path,fileName):
        self.fileName= os.path.join(path,fileName).replace('\\','/')
        file=open(self.fileName,'w')
        file.close() 
    def write(self,line):
		file=open(self.fileName,'a')
		file.write('%s\n'%line)
		file.close()	
class iniFile():#custom rcMaya2AE class for prefs
    def __init__(self):
        self.fileName=os.path.join(userDirectory(),'rcMaya2AE.ini').replace('\\','/')
        if not os.path.isfile(self.fileName):
            file=open(self.fileName,'w')
            file.close()
            mc.confirmDialog(m='Set Path to After Effects')
            self.AEPath=mc.fileDialog2(fm=1,ds=1,okc='Set',cc='Cancel')[0]
            self.write('AELoc',self.AEPath)
            self.write('Force1080','1')
            self.write('UseTimeline','1')
            self.write('Layers','1')
            self.write('Objects','0')
            self.write('Behavior','Replace')
            self.write('ImageSource', 'images')
            self.write('ImageLabel', 'Label3')
    def read(self):#Reads Contents of File
        with open(self.fileName,'r') as f:
            content=[w.replace('\n','') for w in f.readlines()]
        return content
    def get(self,att):
        for each in self.read():
            if att in each:
                return each.replace(att+'= ','')
        return None
    def write(self,att,value):
        if self.get(att)==None:
            file=open(self.fileName,'a')
            file.write('%s= %s\n'%(att,str(value)))
            file.close()
        else:
            contents=self.read()
            file=open(self.fileName,'w')
            for each in contents:
                if att in each:
                    each=r'%s= %s'%(att,str(value))
                file.write('%s\n'%each)
            file.close()
    def set(self,checkBox):#Used to write checkBox value
    	self.write(checkBox,int(mc.menuItem(checkBox,q=1,cb=1)))
    	

