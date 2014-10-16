import os 
import sys
import subprocess
import shutil
################
from functools import partial
def runMethod(method,string,*args): exec(method+string) #Delay Function
################
import maya.cmds as mc 
import maya.mel as mel 
################
from rcTools.main import *
import rcTools.toolsPY.rcMaya2AE as AE
import rcTools.toolsPY.rcFileManager as fileMGR
################source every mel in toolsMEL: toolsMEL
for each in os.listdir(toolsMEL):
	file,ext=os.path.splitext(each)
	path= os.path.join(toolsMEL.replace('\\','/'),each)
	if ext =='.mel': mel.eval('source "%s"'%path)
ui=ui()
###############
def UI():
		if mc.window('rcToolsWin',ex=1): mc.deleteUI('rcToolsWin',window=1)
		if mc.dockControl('rcToolsDock',ex=1): mc.deleteUI('rcToolsDock')
		mc.window('rcToolsWin',t='rcToolBox')
		
		mc.tabLayout('TABS',w=ui.rowWidth+35,imw=15)
		
		#MAIN
		mc.scrollLayout('MAIN',w=ui.rowWidth+15,h=ui.screensize[1]-360)
		#globalsUI()
		assignUI()
		materialsUI()
		#existMATUI()

		#mc.scrollLayout('MATERIALS')
		#mel.eval('source "'+toolsMEL.replace('\\','/')+'ddoMaterialManager.mel''"') 
		#mel.eval("ddoMaterialManager_2013")
		mc.setParent('TABS')
		#mc.setParent('TABS')
		
		#OUTPUT
		mc.scrollLayout('OUTPUT')
		AE.UI()
		mc.setParent('TABS')
		#SCRIPTS

		mc.scrollLayout('SCRIPTS')
		mc.rowColumnLayout(numberOfColumns=8)
		mc.iconTextButton(w=ui.rowWidth/8,h=ui.rowWidth/8)
		mc.iconTextButton(w=ui.rowWidth/8,h=ui.rowWidth/8)
		mc.iconTextButton(w=ui.rowWidth/8,h=ui.rowWidth/8)
		mc.iconTextButton(w=ui.rowWidth/8,h=ui.rowWidth/8)  
		mc.iconTextButton(w=ui.rowWidth/8,h=ui.rowWidth/8)
		mc.iconTextButton(w=ui.rowWidth/8,h=ui.rowWidth/8,ann="Export to AFX",l= "L2F" ,i= (iconPath +"AE_Export_32.png"),c=partial(runMethod,'mel.eval','("rcExport2AE")'))
		mc.iconTextButton(w=ui.rowWidth/8,h=ui.rowWidth/8,ann="Export RenderLayers to Files",l= "L2F" ,i= (iconPath +"L2F.png"),c=partial(runMethod,'mel.eval','("rcLayers2Files")'))
		mc.iconTextButton(w=ui.rowWidth/8,h=ui.rowWidth/8,ann="Render Manager",l= "RenderManager" ,i= (iconPath +"renderMGR.png"),c=partial(runMethod,'mel.eval','("rcRenderMGR")'))
		mc.setParent('..')
		scriptsUI()
		mc.setParent('TABS')
		
		mc.tabLayout('TABS',e=1,st='MAIN')#FOCUS AE
		mc.dockControl('rcToolsDock',area='left',floating=0,content='rcToolsWin',label='rcToolBox')
		mc.showWindow() 
###############
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
ls=ls() 
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
		
create=create() 	
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
		mc.setAttr('miDefaultFrameBuffer.datatype',16)
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
set=set()
###############
def scriptsUI():
	mc.frameLayout(l='TOADSTORM',w=ui.rowWidth,cll=1,cl=1)
	mc.button(w=ui.rowWidth,l='Highlight Component Shading',c=partial(runMethod,'btnSourcePy','(hfShading,hfHighlightBadShaded)'))
	mc.button(w=ui.rowWidth,l='Split Component Shading')#partial(runMethod,'button','('+each+')'))
	mc.button(w=ui.rowWidth,l='Nuke Component Shading')
	mc.button(w=ui.rowWidth,l='Rename Duplicate Nodes')
	mc.setParent('..')
	#Frame Layout each Folder with button for each Mel inside It 
	for folder in ls.dir(scriptsMEL):
		mc.frameLayout(l=folder,w=ui.rowWidth,cll=1,cl=0)#mc.text(l=folder+':',align='left')
		mc.rowColumnLayout(w=ui.rowWidth,numberOfColumns=1)
		for item in sorted(ls.dir(os.path.join(scriptsMEL,folder),folder=0)):
			file,ext=os.path.splitext(item)
			path= os.path.join(scriptsMEL,folder) 
			if ext =='.mel': 
				mc.button(w=ui.rowWidth,l=file,c=partial(runMethod,'btnScript','("'+file+'","'+folder+'")'))
		mc.setParent('..')
		mc.setParent('..')
		
	#Frame Layout for Mels in Main folder 
	mc.frameLayout(l='GENERAL',w=ui.rowWidth,cll=1,cl=0)
	mc.rowColumnLayout(w=ui.rowWidth,numberOfColumns=1)
	for each in sorted(each for each in ls.dir(scriptsMEL,folder=0)):
		file,ext=os.path.splitext(each)
		path= scriptsMEL +'\\'+each
		if ext =='.mel':
			mc.button(w=ui.rowWidth,l=file,c=partial(runMethod,'btnScript','("'+file+'")'))
def assignUI():
	mc.frameLayout('ASSIGNFRAME',w=ui.rowWidth,cll=1,bgc=[.2,.2,.2],fn='smallBoldLabelFont',bs='in',l='ASSIGN')
	mc.rowColumnLayout(numberOfColumns=2,columnWidth=[(1,ui.rowWidth/2),(2,ui.rowWidth/2)])
	
	mc.columnLayout('SHAPECTRL',w=ui.rowWidth/2-5)
	mc.gridLayout(numberOfColumns=5,cellWidthHeight=[25,25])
	mc.text(l='Piv'); mc.separator(style='in'); mc.button(l='Cntr',bgc=[.2,.2,.2],c=partial(runMethod,'mel.eval','("rcSetPivot CENTER")'))
	mc.button(l='Orig',bgc=[.2,.2,.2],c=partial(runMethod,'mel.eval','("rcSetPivot ORIGIN")'))
	mc.button(l='Sel',bgc=[.2,.2,.2],c=partial(runMethod,'mel.eval','("rcSetPivot SELECTED")'))
	mc.button(l='',c=partial(runMethod,'mel.eval','(toMiddle(\"max\" ,\"max\", \"max\")'))
	mc.button(l='')
	mc.text(l='')
	mc.button(l='')
	mc.button(l='')
	mc.button(l='')
	mc.button(l='')
	mc.button(l='Y+',ann='Set Selected Pivot to',bgc=[.6,.6,.6],c=partial(runMethod,'mel.eval','("rcSetPivot YMax")'))
	mc.button(l='')
	mc.button(l='')
	mc.text(l='')
	mc.button(l='X+',ann='Set Selected Pivot to',bgc=[.6,.6,.6],c=partial(runMethod,'mel.eval','("rcSetPivot XMax")'))
	mc.text(l='')
	mc.button(l='X-',ann='Set Selected Pivot to',bgc=[.6,.6,.6],c=partial(runMethod,'mel.eval','("rcSetPivot XMin")'))
	mc.text(l='')
	mc.text(l='')
	mc.button(l='Z+',ann='Set Selected Pivot to',bgc=[.6,.6,.6],c=partial(runMethod,'mel.eval','("rcSetPivot ZMax")'))
	mc.button(l='Y-',ann='Set Selected Pivot to',bgc=[.6,.6,.6],c=partial(runMethod,'mel.eval','("rcSetPivot YMin")'))
	mc.button(l='Z-',ann='Set Selected Pivot to',bgc=[.6,.6,.6],c=partial(runMethod,'mel.eval','("rcSetPivot ZMin")'))
	mc.text(l='')
	mc.text(l='Obj')
	mc.button(l='fObj',ann='Freeze Object\'s Transform, Rotation, Scale',bgc=[.3,.7,1],c=partial(runMethod,'mc.makeIdentity','(mc.ls(sl=1),apply=True,t=1,r=1,s=1,n=0,pn=1)')) 
	mc.button(l='DpI',ann='Duplicate Input Graph',bgc=[.2,.2,.2],c=partial(runMethod,'mel.eval','("duplicate -rr -un")'))
	mc.button(l='Orig',ann='Move Object To World Origin',bgc=[.2,.2,.2],c=partial(runMethod,'mel.eval','("rcMoveSel ORIGIN")'))
	mc.button(l='Sel',ann='Move First Selected to Second',bgc=[.2,.2,.2],c=partial(runMethod,'mel.eval','("rcMoveSel SELECTED")')) 
	mc.button(l='Tx',ann='Freeze Transforms',bgc=[.3,.7,1],c=partial(runMethod,'mc.makeIdentity','(mc.ls(sl=1),apply=True,t=1,r=0,s=0,n=0,pn=1)')) 
	mc.button(l='Rx',ann='Freeze Rotations',bgc=[.3,.7,1],c=partial(runMethod,'mc.makeIdentity','(mc.ls(sl=1),apply=True,t=0,r=1,s=0,n=0,pn=1)')) 
	mc.button(l='Sx',ann='Freeze Scales',bgc=[.3,.7,1],c=partial(runMethod,'mc.makeIdentity','(mc.ls(sl=1),apply=True,t=0,r=0,s=1,n=0,pn=1)'))  
	mc.button(l='Crv',ann='Create Curve from Selected Joint Group',c=partial(runMethod,'mel.eval','("Ctrl_Curve")')) 
	mc.button(l='Grp',ann='Custom Naming Grouping Procedure',bgc=[.2,.2,.2],c=partial(runMethod,'mel.eval','("rcCtGrp")'))
	mc.setParent('..')
   
	mc.separator(style='in',h=ui.borders*3)
	mc.checkBoxGrp('smoothPreview',h=ui.checkBoxHeight,ncb=1,vr=1,l1='Smooth Preview',v1=1)
   

	mc.textFieldGrp('rsmoothField',l='  Render Smooth:',text='2',cw2=[90,30],cat=[1,'left',1])
	mc.textFieldGrp('dsmoothField',l='  Display Smooth:',text='0',cw2=[90,30],cat=[1,'left',1])
	mc.button(h=ui.btn_large,w=ui.rowWidth/2-8,l='APPLY',c=partial(runMethod,'set.smooth','(0)')) 
	mc.button(h=ui.btn_small,w=ui.rowWidth/2-8,l='RESET',ann='Remove Overrides for object',c=partial(runMethod,'set.smooth','(1)'))
	mc.separator(style='in',h=ui.borders*10)
	mc.setParent('..')
	
	
	mc.columnLayout(w=ui.rowWidth/2)#h=(len(ls.renderAtts())*(ui.checkBoxHeight+ui.borders+2))+(ui.btn_large+ui.btn_small)
	
	mc.gridLayout(numberOfColumns=5,cellWidthHeight=[25,25])
	mc.text(l='Disp');mc.separator(style='in');mc.separator(style='in');mc.separator(style='in');mc.button(h=25,w=42,ann='Set Viewport to Green for PlayBlast',l='RE',bgc=[.0,.5,.0],c=partial(runMethod,'set.view','(opt=1)'))
	
	mc.setParent('..')
	
	mc.rowColumnLayout(numberOfColumns=3,rat=[1,'both',0])
	mc.button(h=25,w=42,ann='Set Viewport to Green for PlayBlast',l='GREEN',bgc=[.0,1,.0],c=partial(runMethod,'mel.eval','("rcSetView GREEN")'))    
	mc.button(h=25,w=42,ann='Set Viewport to Standard Grey',l='GREY',bgc=[.8,.8,.8],c=partial(runMethod,'mel.eval','("rcSetView GREY")'))    
	mc.button(h=25,w=42,ann='Set Viewport to Gradient',l='GRAD',c=partial(runMethod,'mel.eval','("rcSetView GRAD")'))    
	mc.button(h=25,w=42,l='POLY',c=partial(runMethod,'mel.eval','("rcSetView POLY")'))    
	mc.button(h=25,w=42,l='CTRL',c=partial(runMethod,'mel.eval','("rcSetView CTRL")'))    
	mc.button(h=25,w=42,l='ALL',c=partial(runMethod,'mel.eval','("rcSetView SHOWALL")'))    
	mc.setParent('..')
	
	mc.gridLayout(numberOfColumns=5,cellWidthHeight=[25,25])
	mc.text(l='Attr');mc.separator(style='in');mc.separator(style='in');mc.separator(style='in');mc.separator(style='in')
	mc.setParent('..')
	
	mc.separator(style='in',bgc=[.2,.2,.2],h=ui.borders*3)
	for each in ls.renderAtts(): mc.checkBoxGrp(each,h=ui.checkBoxHeight,ncb=1,vr=1,l1=each,v1=1)
	mc.separator(style='in',bgc=[.2,.2,.2],h=ui.borders*3)
	mc.button(h=ui.btn_large,w=ui.rowWidth/2-8,l='APPLY',c=partial(runMethod,'set.flags','(value="Apply")')) 
	
	mc.rowColumnLayout(numberOfColumns=4)
	mc.button(h=ui.btn_small,l='ON',c=partial(runMethod,'set.flags','(value=1)'))
	mc.button(h=ui.btn_small,l='OFF',c=partial(runMethod,'set.flags','(value=0)'))
	mc.button(h=ui.btn_small,l='NUKE',en=0,ann='Remove Overrides for object',c=partial(runMethod,'setRenderFlags','(value=0)'))
	mc.button(h=ui.btn_small,l='XRAY',en=0,ann='Remove Overrides for object',c=partial(runMethod,'setRenderFlags','(value=0)'))
   
	mc.setParent('MAIN')  




def materialsUI():
	icon=ui.rowWidth/8
	mc.frameLayout('rcMATERIALS',bgc=[.4,.2,.4],w=ui.rowWidth,bs='in',fn='smallBoldLabelFont',cll=1)
	if mc.frameLayout('GLOBAL',q=1,ex=1)==1: mc.frameLayout('GLOBAL',e=1,cl=1)#CLOSE GLOBALS WIN

	mc.separator(style='in')
	mc.rowColumnLayout(numberOfColumns=2)
	mc.text( font= "tinyBoldLabelFont" ,w= ui.rowWidth/2, h= 8,l ="    Create/Assign Layers:",al= "left")
	mc.text( font= "tinyBoldLabelFont" ,w= ui.rowWidth/2, h= 8,l ="    Scripts:",al= "left")
	mc.setParent('..')
	
	mc.rowColumnLayout(numberOfColumns=8)
	mc.iconTextButton(w=icon,h=icon,ann="Assign/Create Layer AODPTHINC",l= "AODPTHINC" ,i= (iconPath +"AODPTHINC_32.png"),c=partial(runMethod,'mel.eval','("rcAssignLayer AODPTHINC")'))
	mc.iconTextButton(w=icon,h=icon,ann="Assign/Create Layer MASK_RGB" ,l= "MASK_RGB" ,i=(iconPath+"MASK_RGB.png"),c=partial(runMethod,'mel.eval','("rcAssignLayer MASK_RGB")'))
	mc.iconTextButton(w=icon,h=icon,ann="Assign/Create Layer CONTOUR" ,l= "" ,i= 'baseLattice.svg',c=partial(runMethod,'createMat','("CONTOUR")'))
	mc.textField('CONDIA',w=icon-5,fn='boldLabelFont',tx='01')
	mc.iconTextButton(w=icon,h=icon)
	mc.iconTextButton(w=icon,h=icon,ann='Create Image Card From File',i=iconPath+'picture_32',c=partial(runMethod,'create.imageCard','()'))
	mc.iconTextButton(w=icon,ann= "Convert Selected Shader to MIA",i= iconPath +"MIA.png", c= partial(runMethod,'mel.eval','( "convert2MIA")'))
	mc.iconTextButton(w=icon,h=icon,ann= "Add Gamma Correct Nodes to Selected Shader" ,i= 'gammaCorrect.svg', c=partial(runMethod,'mel.eval','( "gammaUIMain")'))
	mc.setParent('..')

	mc.text( font= "tinyBoldLabelFont" ,w= icon, h= 8,l ="    Create/Assign Materials:",al= "left")
	mc.rowColumnLayout(numberOfColumns=8)
	mc.iconTextButton(w=icon,h=icon,en=0,ann="Assign/Create Blinn",l= "BLINN" ,i= "render_blinn.png",c=partial(runMethod,'mel.eval','("rcAssignShader AODPTHINC")'))
	mc.iconTextButton(w=icon,h=icon,en=0,ann="Assign/Create Phong",l= "PHONG" ,i= "render_phong.png",c=partial(runMethod,'mel.eval','("rcAssignShader AO")'))
	mc.iconTextButton(w=icon,h=icon,en=0,ann="Assign/Create Lambert",l= "LAMBERT" ,i= "render_lambert",c=partial(runMethod,'mel.eval','("rcAssignShader DPTH")'))
	mc.iconTextButton(w=icon,h=icon,ann="Assign/Create AODPTHINC",l= "AODPTHINC" ,i= (iconPath +"AODPTHINC_32.png"),c=partial(runMethod,'mel.eval','("rcAssignShader AODPTHINC")'))
	mc.iconTextButton(w=icon,h=icon,ann="Assign/Create AO",l= "AO" ,i= (iconPath +"OCC_32.png"),c=partial(runMethod,'mel.eval','("rcAssignShader AO")'))
	mc.iconTextButton(w=icon,h=icon,ann="Assign/Create DPTH",l= "DPTH" ,i= (iconPath +"DPTH_32.png"),en=0,c=partial(runMethod,'mel.eval','("rcAssignShader DPTH")'))
	mc.iconTextButton(w=icon,h=icon,ann="Assign/Create INC",l= "INC" ,i= (iconPath +'INC_32.png'),c=partial(runMethod,'set.shader','("INC")'))
	mc.iconTextButton(w=icon,h=icon,ann="Assign/Create ALPHA RAMP",l= "A" ,i= (iconPath +'RAMP_A_32.png'),c=partial(runMethod,'mel.eval','("rcAssignShader RAMP_A")'))
  
	
	mc.button(h=ui.btn_large,w=icon,bgc=[.5,0,0],l="R",c= partial(runMethod,'set.shader','("RED")'))
	mc.button(h=ui.btn_large,w=icon,bgc= [0 ,.5 ,0 ],l= "G" ,c=partial(runMethod,'set.shader','( "GREEN")'))
	mc.button(h=ui.btn_large,w=icon,bgc= [0 ,0 ,.5] ,l= "B" ,c= partial(runMethod,'set.shader','( "BLUE")'))
	mc.iconTextButton(h=ui.btn_large,w=icon,bgc= [0 ,0 ,0] ,l= "A" ,c=partial(runMethod,'set.shader','( "ALPHA")'),i='textureEditorDisplayAlpha.png')
	mc.button(h=ui.btn_large,w=icon,bgc= [0 ,.5 ,.5],l= "C" ,c= partial(runMethod,'set.shader','( "CYAN")'))
	mc.button(h=ui.btn_large,w=icon,bgc= [.5 ,0, .5],l= "M" ,c= partial(runMethod,'set.shader','( "MAGENTA")'))
	mc.button(h=ui.btn_large,w=icon,bgc= [.5 ,.5 ,0],l= "Y" ,c= partial(runMethod,'set.shader','( "YELLOW")'))
	mc.button(h=ui.btn_large,w=icon,bgc= [0 ,0 ,0],l= "K" ,c= partial(runMethod,'set.shader','( "BLACK")'))
	
	
	mc.setParent('..')
	
	mc.separator(style='in')
	
	
	#mc.frameLayout('frame_MATERIAL',w=ui.rowWidth,l='Existing Materials List',ec=partial(runMethod,'existMAT','()'),cll=1)
	#existMAT()
	mc.setParent('..')
	mc.setParent('MAIN')
def existMATUI():
	if mc.scrollLayout('materiallist',q=1,ex=1)==True: mc.deleteUI('materiallist')
	mc.setParent('MAIN')
	mc.scrollLayout('materiallist',w=ui.rowWidth,h=390)#h=len(ls.shaders())*25)
	mc.rowColumnLayout(w=ui.rowWidth-10,numberOfColumns=2)
	for each in sorted(ls.shaders()):
		mc.button(w=ui.rowWidth-55,l=each,c=partial(runMethod,'mc.select','(\''+ str(each)+'\')'))
		mc.button(w=45,l='ASSIGN',c=partial(runMethod,'mc.hyperShade','(assign=\''+ str(each)+'\')'))
		#mc.button(w=40,l='GRAPH')
	   
	mc.setParent('..');mc.setParent('..')     
def globalsUI():
	mc.frameLayout('GLOBAL',w=ui.rowWidth,l='GLOBALS',bgc=[.4,.2,.4],bs='in',fn='smallBoldLabelFont',cl=1)
	mc.rowColumnLayout(w=ui.rowWidth,numberOfColumns=4)
	#mc.text(l='Anti\nAlias:',w=35,font='tinyBoldLabelFont',h=textHeight,al='right')
	#mc.button(h=buttons_med,w=ui.rowWidth/4,l='LOW -2/0 \n .10',c=partial(runMethod,'mel.eval','("rcSetGlobals LOW")'))
	#mc.button(h=buttons_med,w=ui.rowWidth/4,l='MED  0/2 \n .05',c=partial(runMethod,'mel.eval','("rcSetGlobals MED")'))
	#mc.button(h=buttons_med,w=ui.rowWidth/4,l='HI 2/0 \n .02',c=partial(runMethod,'mel.eval','("rcSetGlobals HIGH")')) 
	mc.text(l='Final\nGather:',w=35,font='tinyBoldLabelFont',h=textHeight,al='right')
	mc.button(h=buttons_med,w=ui.rowWidth/4,l='LOW 50/.1 \n .10',c=partial(runMethod,'mel.eval','("rcSetGlobals LOW")'))
	mc.button(h=buttons_med,w=ui.rowWidth/4,l='MED  250/.1 \n .05',c=partial(runMethod,'mel.eval','("rcSetGlobals MED")'))
	mc.button(h=buttons_med,w=ui.rowWidth/4,l='HI 2/0 \n .02',c=partial(runMethod,'mel.eval','("rcSetGlobals HIGH")'))
	
	mc.text(l='Image\nFormat:',w=35,font='tinyBoldLabelFont',h=textHeight,al='right')
	mc.button(h=buttons_med,w=ui.rowWidth/4,l='PNG\n 16BIT',c=partial(runMethod,'mel.eval','("rcSetGlobals PNG")'))
	mc.button(h=buttons_med,w=ui.rowWidth/4,l='TIF \n 16Bit',c=partial(runMethod,'mel.eval','("rcSetGlobals TIF")'))
	mc.button(h=buttons_med,w=ui.rowWidth/4,l='EXR\n 32BIT',c=partial(runMethod,'mel.eval','("rcSetGlobals EXR")'))
	
	mc.text(l='Image\nPrefix:',w=35,font='tinyBoldLabelFont',h=textHeight,al='right')
	mc.button(h=buttons_med,w=ui.rowWidth/4,l='Layers',c=partial(runMethod,'mel.eval','("rcSetGlobals -layers")'))
	mc.button(h=buttons_med,w=ui.rowWidth/4,l='Passes',c=partial(runMethod,'mel.eval','("rcSetGlobals -passes")'))
	mc.button(h=buttons_med,w=ui.rowWidth/4,l='',c=partial(runMethod,'mel.eval','("rcSetGlobals ")'))
	
	mc.setParent('..')
	mc.setParent('..')

###############
def btnScript(script,folder=''):
	if folder is not None: mel.eval('source "'+scriptsMEL.replace('\\','/')+folder+'/'+str(script)+'"')
	else: mel.eval('source "'+scriptsMEL.replace('\\','/')+str(script)+'"')
	mel.eval(str(script))
################
def btnSourcePy(file,command):
		import file
		reload (file)
		file.command

