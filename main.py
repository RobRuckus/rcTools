####IMPORT
import os 
import sys
import maya.cmds as mc
import maya.mel as mel 
from datetime import datetime
import ctypes
###########PATH VARIABLES
importPath= os.path.dirname(__file__)
iconPath=os.path.join(importPath,'icons','')
toolsPY=os.path.join(importPath,'toolsPY','')
toolsMEL=os.path.join(importPath,'toolsMEL','')
scriptsMEL=os.path.join(importPath,'scriptsMEL','')
scriptsPY=os.path.join(importPath,'scriptsPY','')
##########
def nameConvert(string):#Convert Node Names with | to _ 
	string=string.replace('|','_')
	if string.startswith('_'): return string[1:]
	else: return string
def backupFolder(): return str(datetime.now()).replace('-','.').replace(' ','-').replace(':','.')
def userDirectory():#RETURN USERDIRECTORY FOR MAC/WIN
	if 'darwin' in sys.platform:
		userDirectory=os.environ['HOME']
	else:
		userDirectory=os.environ['USERPROFILE']
	return userDirectory
#########
class ui():
	def __init__(self,name):
		if 'dar' not in sys.platform: 
			user32= ctypes.windll.user32
			self.screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
		else: self.screensize=(1920,1080)
		self.btn_small=20
		self.btn_med=25
		self.btn_large=30
		self.checkBoxHeight=15
		self.textSize=17
		self.textHeight=10
		self.rowWidth=300
		self.iconDim=15
		self.iconSize=13
		self.borders=2
		self.tabWidth=765
		self.rowWidth=300
		self.titleFont='boldLabelFont'
		self.fieldFont='fixedWidthFont'
		
		self.name=name
		self.window=self.name+'Window'
		self.dock=self.name+'Dock'
		self.tabs=self.name+'TABS'
	
	def win(self,**kwargs):
		if mc.window(self.window,ex=True):mc.deleteUI(self.window,window=True)
		if mc.dockControl(self.dock,ex=True): mc.deleteUI(self.dock)
		
		mc.window(self.window,t=self.name)
		mc.formLayout(w=self.rowWidth)
		
		mc.dockControl(self.dock,area='left',content=self.window,label=self.name,**kwargs)
	###toolBox
	def toolBox(self):
		self.win()
		mc.tabLayout(self.tabs,w=self.rowWidth+35,imw=15)
	def tab(self,name):#tab command for toolBox
		mc.setParent(self.tabs)
		mc.scrollLayout(name,w=self.rowWidth+15,h=self.screensize[1]-360)	
	def frame(self,name): mc.frameLayout(self.name+name,bgc=[.2,.2,.2],fn='smallBoldLabeFont',bs='in',l=name)
	def buttonRow(self,columns=8,**kwargs):
		mc.rowColumnLayout(numberOfColumns=columns)
		for each in range(columns):
			pass
			#mc.iconTextButton(w=self.rowWidth/columns,h=self.rowWidth/columns,args)#pass each arg of each button 
class sceneData(object):
	def __init__(self):
		pass
	def ws(self): return os.path.normpath(mc.workspace(q=True,rd=True))
	def wsImagesName(self): return mc.workspace('images',q=True,fileRuleEntry=True)
	def wsImagesFolder(self): return os.path.normpath(os.path.join(self.ws,self.wsImagesName))
	def frameWidth(self): return mc.getAttr('defaultResolution.width')
	def frameHeight(self): return mc.getAttr('defaultResolution.height')
	def framePad(self): return mc.getAttr('defaultRenderGlobals.extensionPadding')
	def minTime(self): return int(mc.playbackOptions(q=True,minTime=True))
	def maxTime(self): return int(mc.playbackOptions(q=True,maxTime=True))
	def fps(self): return  {"game":15.0, "film":24.0, "pal":25.0, "ntsc":30.0, "show":48.0, "palf":50.0, "ntscf":60.0}[mc.currentUnit(q=True, fullName=True, time=True)]
	def timelineSeconds(self): return  (mc.playbackOptions(q=1,maxTime=1)+1)/self.fps()
	def cameras(self): return [str(mc.listRelatives(sceneCamera,p=1,f=1)[0]) for sceneCamera in mc.ls(ca=1)]
	def renderCameras(self): return [str(mc.listRelatives(renderCamera,p=1,f=1)[0]) for renderCamera in mc.ls(ca=1) if mc.getAttr(str(renderCamera)+'.renderable')]
	def renderLayers(self): return  [str(x) for x in mc.ls(typ='renderLayer')]#convert unicode list to string list USES defaultRenderlayer = NEEDED for Logic
	def renderLayerNames(self): return  ['masterLayer' if 'defaultRenderLayer' in x else x for x in self.renderLayers()]
	def imageFilePrefix(self): return mc.getAttr('defaultRenderGlobals.imageFilePrefix')# Prefix from Render Globals : <RenderLayers>/<RenderPass>/<RenderLayer>.<RenderPass>
	def imageFileSuffix(self): return  ''.join(mc.renderSettings(fin=1,lut=1))#masterLayer/<RenderPass>/masterLayer.0001.png
	def imageFilePath(self): return  ''.join(mc.renderSettings(fin=1,lut=1,fp=1))#PROJECT/IMAGES/masterLayer/<RenderPass>/masterLayer.0001.png
	def outputLayers(self): return self.renderOutput[0]
	def outputImages(self): return self.renderOutput[1]
	def renderOutput(self):
		outputLayers= []
		outputImages=[]
		currentLayer=str(mc.editRenderLayerGlobals(q=1,crl=1)).replace('defaultRenderLayer','masterLayer')
		for layer in self.renderLayers():
			if not self.imageFilePrefix()== None:
				connections= mc.listConnections(layer+'.renderPass')
				if len(self.renderCameras())==1:
					outReplacedLayer=self.imageFilePath().replace(currentLayer,layer)
					if connections: connections.append('masterBeauty')
					else: connections=['masterBeauty']
					for connection in connections: 
						outputImages.append(outReplacedLayer.replace('<RenderPass>',connection).replace('defaultRenderLayer','masterLayer'))
						outputLayers.append('%s.%s'%(layer.replace('defaultRenderLayer','masterLayer'),connection))
				else:#More Than One Render Camera
					outReplacedLayer=self.imageFilePath().replace(currentLayer,layer)
					if connections: connections.append('masterBeauty')
					else: connections=['masterBeauty']
					for camera in self.renderCameras():       
						for connection in connections:
							outputImages.append(outReplacedLayer.replace('<RenderPass>',connection).replace('defaultRenderLayer','masterLayer').replace(nameConvert(self.renderCameras[0]),camera))
							outputLayers.append('%s.%s.%s'%(camera,layer.replace('defaultRenderLayer','masterLayer'),connection))      
		return[[str(x) for x in outputLayers],[str(x) for x in outputImages]]
#####
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
class iniFile():#CRUD iniFiles
    def __init__(self,fileName):
        self.fileName=fileName
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
########
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
########
########TOOL Classes
class ls():
    def renderAtts(self):#return custom Attribute List 
        renderFlags=[]
        renderFlags.append('castsShadows')
        renderFlags.append('receiveShadows')
        renderFlags.append('visibleInReflections')
        renderFlags.append('visibleInRefractions')
        renderFlags.append('doubleSided')
        #renderFlags.append('motionBlur')
        #renderFlags.append('smoothShading')
        #renderFlags.append('useSmoothPreviewForRender')
        renderFlags.append('opposite')
        renderFlags.append('motionBlur')
        renderFlags.append('miFinalGatherCast')
        renderFlags.append('miFinalGatherReceive')
        return renderFlags
    def shaders(self): return [shader for shader in mc.ls(mat=1) if not 'particleCloud1' in shader and not 'lambert1' in shader and not 'displace' in shader and not ':' in shader] #WIP if not NOT WORKING
    def shaderColor(self,shader):
        Attr=mc.listAttr(shader)
        for each in Attr:
            if 'outColor' in each : return mc.getAttr(shader+'.outcolor')
            if 'color' in each : return mc.getAttr(shader+'.color')
            if 'diffuse_color' in each : return mc.getAttr(shader+'.diffuse_color')
    def dir(self,src,folder=1):
    	try: return [name for name in os.listdir(src) if not os.path.isfile(os.path.join(src,name))== folder and not name.startswith('.')  ] #Folders and files , folder=0 returns files 
    	except Exception: return []
    def musterCL(self,scrollSel):
        appLoc= '"' + str(os.environ.get('MUSTER') + 'mrtool.exe' )+ '"'#os.path.normpath
        conDispatcher=mc.textField('conDispatcher',q=1,text=1)#'192.168.1.72'
        conDispatcherPort=mc.textField('conDispatcherPort',q=1,text=1)#'8681'
        conUserName='"admin"'
        conPassword='""'
        conPacketSize=mc.textField('conPacketSize',q=1,text=1)#'5'
        conPriority=mc.textField('conPriority',q=1,text=1)#'50'
        conMaxInstances=mc.textField('conMaxInstances',q=1,text=1)#'5'
        
        conStartFrame=str(mc.getAttr('defaultRenderGlobals.startFrame')).rsplit('.',1)[0]#removes decimal from float using string rsplit
        conEndFrame=str(mc.getAttr('defaultRenderGlobals.endFrame')).rsplit('.',1)[0]#these need to be strings so i can concatenate them for command line
        
        conMayaProj=os.path.normpath(mc.workspace(q=1,rd=1))
        conProjName=mc.textField('ProjectName',q=1,text=1)
        conShotName=mc.getAttr('renderLayerManager.shotName')
        
        
        if not mc.textScrollList(scrollSel,q=1,si=1)== None:
        	if mc.textScrollList(scrollSel,q=1,si=1)[0] == conShotName: conSelected=ls.dir(l2fOutputFolder(),folder=0)#set Output for selection ALL or selected
        	else: conSelected= mc.textScrollList(scrollSel,q=1,si=1)
        	
		for each in conSelected:
			conJobName= conProjName + '_' + conShotName + '_' + each.rsplit('.',1)[0] #MUSTER JOB NAME
			if os.path.isfile(os.path.normpath(l2fOutputFolder()+ each)):
				conJobFile= os.path.normpath(l2fOutputFolder()+ each) #MUSTER FILE NAME
				#os and mrtool spawn WIP
				returnLine= appLoc  +' -b ' #Batch mode
				assert isinstance(returnLine,str)   
				
				returnLine+= '-s '  + conDispatcher + ' -port ' + conDispatcherPort #ip and port
				returnLine+= ' -u '  + conUserName   + ' -p '    + conPassword
				
				returnLine+= ' -e 2 ' #TEMPLATE
				
				returnLine+=' -pk ' + conPacketSize + ' -pr ' + conPriority + ' -max ' + conMaxInstances
				returnLine+=' -sf  ' + conStartFrame + ' -ef ' + conEndFrame
				#returnLine+= ' -folder ' +'"' + conProjName + '"'
				returnLine+= ' -proj ' + '"' + conMayaProj + '"' 
				returnLine+= ' -n '  + '"' + conJobName + '"'
				returnLine+= ' -f '  + '"' + conJobFile + '"'#addsQuotes around
				
				for line in list.pipe(returnLine): 
					pass
				    #print line
				#print returnLine
    def pipe(self,command):
        p=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        return iter(p.stdout.readline,b'')
class create():
 	def imageCard(self):
		selImage=mc.fileDialog()
		material=mc.shadingNode('lambert',asShader=1)
		fileNode=mc.shadingNode('file',asTexture=1)
		mc.setAttr(fileNode+'.fileTextureName',selImage,typ='string')
		mc.connectAttr(fileNode+'.outColor', material+'.color')
		sizeFactor=0.01
		imageSize=mc.getAttr(fileNode+'.outSize')
		modelPlane=mc.polyPlane(w=imageSize[0][0]*sizeFactor,h=imageSize[0][1]*sizeFactor,sx=1,sy=1,n='modelPlane',ax=[0,1,0],ch=0)
		mc.hyperShade(modelPlane,assign=material)
	def grp(self):#WIP
		mc.promptDialog(title='Ctrl_GRP',m='Name:',tx='Ctrl_')
		sel=mc.ls(sl=1)
		mc.group(n=mc.promptDialog(q=1,text=1))
		mc.xform(os=1,piv=[0,0,0])
		mc.select(add=1)	

	def shader(self,mat):
	    self.mat = mat
	    self.Name=mat+'_MAT'
	    self.SG=mat+'SG'
	    if not mc.objExists(self.Name):
		mc.shadingNode('surfaceShader',n=self.Name,asShader=1)
		mc.sets(renderable=True,noSurfaceShader=True,empty=1,name=self.SG)
		if mat=='RED' :
		    mc.connectAttr(self.Name+'.outColor', self.SG+'.surfaceShader',f=1)
		    mc.setAttr(self.Name+'.outColor',1,0,0,type='double3')
		    mc.setAttr(self.Name+'.outMatteOpacity',1,1,1,type='double3')
    
		if mat=='GREEN' :
		    mc.connectAttr(self.Name+'.outColor', self.SG+'.surfaceShader',f=1)
		    mc.setAttr(self.Name+'.outColor',0,1,0,type='double3')
		    mc.setAttr(self.Name+'.outMatteOpacity',1,1,1,type='double3')
    
		if mat=='BLUE' :
		    mc.connectAttr(self.Name+'.outColor', self.SG+'.surfaceShader',f=1)
		    mc.setAttr(self.Name+'.outColor',0,0,1,type='double3')
		    mc.setAttr(self.Name+'.outMatteOpacity',1,1,1,type='double3')
		if mat=='CYAN' :
		    mc.connectAttr(self.Name+'.outColor', self.SG+'.surfaceShader',f=1)
		    mc.setAttr(self.Name+'.outColor',0,1,1,type='double3')
		    mc.setAttr(self.Name+'.outMatteOpacity',1,1,1,type='double3')
		if mat=='MAGENTA' :
		    mc.connectAttr(self.Name+'.outColor', self.SG+'.surfaceShader',f=1)
		    mc.setAttr(self.Name+'.outColor',1,0,1,type='double3')
		    mc.setAttr(self.Name+'.outMatteOpacity',1,1,1,type='double3')
		if mat=='YELLOW' :
		    mc.connectAttr(self.Name+'.outColor', self.SG+'.surfaceShader',f=1)
		    mc.setAttr(self.Name+'.outColor',1,1,0,type='double3')
		    mc.setAttr(self.Name+'.outMatteOpacity',1,1,1,type='double3')		
		if mat=='ALPHA':
			#different than template
			mc.delete(self.Name)
			mc.shadingNode('useBackground',n=self.Name,asShader=1)
			#custom
			mc.connectAttr(self.Name+'.outColor', self.SG+'.surfaceShader',f=1)
			mc.sets(renderable=True,noSurfaceShader=True,empty=1,name=self.SG)
			mc.setAttr(self.Name+'.specularColor',0,0,0,)
			mc.setAttr(self.Name+'.reflectivity',0)
			mc.setAttr(self.Name+'.reflectionLimit',0)
			mc.setAttr(self.Name+'.shadowMask',0 );	
		if mat=='BLACK' :
		    mc.connectAttr(self.Name+'.outColor', self.SG+'.surfaceShader',f=1)
		    mc.setAttr(self.Name+'.outColor',0,0,0,type='double3')
		    mc.setAttr(self.Name+'.outMatteOpacity',1,1,1,type='double3')		
		if mat=='INC':
			if not mc.objExists('rc.sInfo'): sampleri=mc.createNode('samplerInfo',n='rc.sInfo')
			else: sampleri='rc.sInfo'	
			rampi=mc.createNode('ramp',n='FacingRatioRamp')
			mc.setAttr(rampi+'.colorEntryList[1].color',0,0,0,type='double3')
			mc.setAttr(rampi+'.colorEntryList[0].color',1,1,1,type='double3')
			mc.setAttr(rampi+'.colorEntryList[1].position',1)
			mc.connectAttr(self.Name+'.outColor', self.SG+'.surfaceShader',f=1)
			mc.connectAttr(sampleri+'.facingRatio', rampi+'.vCoord',f=1)
			mc.connectAttr(rampi+'.outColor', self.Name+'.outColor',f=1)
			
		if mat=='CONTOUR':
		    mc.setAttr(self.SG+'.miContourEnable',1)
		    mc.setAttr(self.SG+'.miContourWidth',int(mc.textField('CONDIA',q=1,tx=1)))
		    mc.setAttr(self.Name+'.outColor',0,0,0,type='double3')
		    mc.setAttr(self.Name+'.outMatteOpacity',1,1,1,type='double3')
		if mat=='AO':
			occNode=mel.eval('mrCreateCustomNode -asTexture "" mib_amb_occlusion')
			mc.connectAttr(self.Name+'.outColor', self.SG+'.surfaceShader',f=1)
			mc.connectAttr(occNode+'.outValue',self.Name+'.outColor')
			mc.text()
			
	def layer(self,layer):
		if not mc.objExists(layer): mc.createRenderLayer(n=layer)
		#mc.editRenderLayerGlobals(currentRenderLayer=layer)
		#if layer='AODPTHINC':
			#mc.editRenderLayerAdjustment('miDefaultOptions.lensShaders')
			#mc.setAttr('miDefaultOptions.lensShaders',0)
		
	
class set():
    def shader(self,shader):
    	shaderName=shader +'_MAT'
    	selShort=mc.ls(sl=1)
    	selObj=mc.ls(sl=1,dag=1)
    	if not mc.objExists(shaderName):
    		create.shader(shader)
    	#
    	for each in selObj:
    		if mc.nodeType(each)=='mesh' or mc.nodeType(each)=='nurbsSurface':
    			mc.select(each)
    			eachSn=mc.pickWalk(d='up')
    			mc.select(eachSn)
    			mc.hyperShade(assign=shaderName)
    def camera(self,cam):
    	for each in mc.ls(ca=1): 
    		if mc.getAttr(each+'.renderable'): mc.setAttr(each+'.renderable',0)
    	mc.setAttr(cam+'.renderable',1)
    def layer(self,layer):
    	selObjShort=mc.ls(sl=1)
        selObj=ls(sl=1,dag=1)
        if not layer in mc.lsType('renderLayer'): createLayer(layer)
        mc.editRenderLayerMembers(layer,selObj,noRecurse=0)
        set.shader (layer)
        for each in selObj:  
        	mc.select(each)
    def view(self,opt):
        panels=mc.getPanel(vis=1)
        for pane in panels:
            if mc.getPanel(to=pane) == 'modelPanel' : 
                mc.modelEditor(pane,e=1,sel=True)
                mc.modelEditor(pane,e=1,sel=False)
                mc.modelEditor(pane,e=1,sel=True)
                
    def pluginMR(self):
        if not mc.pluginInfo('Mayatomr',q=1,l=1): 
            mc.loadPlugin('Mayatomr.mll')
        mel.eval('miCreateDefaultNodes')#sets up MR Globals
    def renderMR(self):
        if not mc.getAttr('defaultRenderGlobals.currentRenderer') =='mentalRay':
            if not mc.confirmDialog(t='rc.Tools',button=['Yes','No'],m='Set Render to MR?',cb='No',ma='center',ds='No')=='No':
                mc.setAttr('defaultRenderGlobalist.currentRenderer','mentalRay',type='string')
    rlmAttrs()
    def imagePrefix(self,option='L__L'):
    	if option=='S__L__L': prefix =str(mc.getAttr('renderLayerManager.shotName'))+"/<RenderLayer>/<RenderLayer>"
    	if option=='S__L__L.P': prefix =str(mc.getAttr('renderLayerManager.shotName'))+"/<RenderLayer>/<RenderLayer>.<RenderPass>"
    	if option=='S__L__P__L.P': prefix =str(mc.getAttr('renderLayerManager.shotName'))+"/<RenderLayer>/<RenderPass>/<RenderLayer>.<RenderPass>"	
    	if option=='L__L': prefix =str("<RenderLayer>/<RenderLayer>")
    	if option=='L__L.P': prefix =str("<RenderLayer>/<RenderLayer>.<RenderPass>")
    	if option=='L__P__L.P': prefix =str("<RenderLayer>/<RenderPass>/<RenderLayer>.<RenderPass>")
    	mc.setAttr('defaultRenderGlobals.imageFilePrefix',prefix,type='string')
    	#mc.textField('imageFilePrefix',edit=1,text=prefix)
    	#commitUI()
    	
    def globals(self,opt=None):
	    #DEFAULTS
	    mc.setAttr('defaultRenderGlobals.extensionPadding',4)#FRAME PADDING
	    mc.setAttr('defaultRenderGlobals.outFormatControl',0)#
	    mc.setAttr('defaultRenderGlobals.animation',1)
	    mc.setAttr('defaultRenderGlobals.putFrameBeforeExt',1)
	    if not mc.getAttr('defaultRenderGlobals.imageFormat')==51:#FORCE PNG IF NOT EXR
		mc.setAttr('mentalrayGlobals.imageCompression',1)
		mc.setAttr('defaultRenderGlobals.imageFormat',32)
		mc.setAttr('defaultRenderGlobals.outFormatControl',0)
		#mc.setAttr('miDefaultFrameBuffer.datatype',16)
            mel.eval('unifiedRenderGlobalsWindow')
    def viewport(self,value):
        if value==0:
         layout=mc.panelConfiguration(l='tempLayout',sc=0)
         evalStr='updatePanelLayoutFromCurrent "' +'tempLayout'+'"'
         mel.eval(evalStr)
         evalStr = 'setNamedPanelLayout "Single Perspective View" '
         mel.eval(evalStr)
         perspPane=mc.getPanel(vis=1)
         mc.scriptedPanel('graphEditor1',e=1,rp=perspPane[0])
         return 'tempLayout'
        if value==1:
         evalStr= 'setNamedPanelLayout "'+ 'tempLayout' + '"'
         mel.eval(evalStr)
         killMe=mc.getPanel(cwl='tempLayout')
         mc.deleteUI(killMe,pc=1)
    def pivot(opt):#WIP
        sel=mc.ls(sl=1)
        lastsel=mc.ls(sl=1,tail=1)
        selPivot=mc.xform(lastsel[0],q=1,piv=1,ws=1)
        for each in sel:
            if opt=='Y+': bounds=mc.xform(each,q=1,bb=1)
			    	#mc.move((bounds[3]+bounds[0])/2),bounds[4],(bounds[5]+bounds[2])/2,each+'.rotatePivot',each+'.scalePivot'))
    def smooth(opt):	
        for each in mc.ls(sl=1):
                if opt==1:
                    mc.displaySmoothness(each,divisionsU=0,divisionsV=0, pointsWire=4,pointsShaded=1,polygonObject=1)
                    mc.sets(each,edit=1,fe='smoothSet')
                    mc.setAttr(each+'.useSmoothPreviewForRender',1 )
                    mc.setAttr(each+'.smoothLevel',2)
                    mc.setAttr(each+'.renderSmoothLevel',int(mc.textFieldGrp('rsmoothField',q=1,text=1)) )
                else:
                    mc.displaySmoothness(each,divisionsU=3,divisionsV=3, pointsWire=16,pointsShaded=4,polygonObject=3)
                    #mc.sets(each,edit=1,fe='smoothSet')
                    mc.setAttr(each+'.useSmoothPreviewForRender',0 )
                    mc.setAttr(each+'.smoothLevel',int(mc.textFieldGrp('dsmoothField',q=1,text=1)) )
                    mc.setAttr(each+'.renderSmoothLevel',int(mc.textFieldGrp('rsmoothField',q=1,text=1)) )
    def flags(self,value):#Attribute Render Flag Assigner
        if value=='Apply':
            for sel in mc.ls(sl=1,dag=1):
                objType=mc.nodeType(sel)
                if objType== 'mesh' or objType == 'nurbsSurface' or objType == 'subdiv':
                    for att in ls.renderAtts():
                        if not mc.getAttr(sel + '.' + att) == mc.checkBoxGrp(att,q=1, v1=1):
                            mc.setAttr( sel + '.' + att , mc.checkBoxGrp(att,q=1, v1=1))
        else:
            for each in ls.renderAtts(): mc.checkBoxGrp(each,e=1,v1=value)
#######
ls=ls()
create=create()
set=set()
