import os 
import sys
import subprocess
import shutil
################
import maya.cmds as mc 
import maya.mel as mel 
################
from functools import partial
def btnDelay(method,string,*args): exec(method+string) #Delay Function
################
from rcTools.rcMaya import *
###########subMODULES 
#from rcTools.toolsPY import rcMaya2AE 
from rcTools.toolsPY import toElement 
from rcTools.toolsPY import rcRoterra 

for each in os.listdir(toolsMEL):#source every mel in toolsMEL: toolsMEL
	file,ext=os.path.splitext(each)
	path= os.path.join(toolsMEL.replace('\\','/'),each)
	if ext =='.mel': mel.eval('source "%s"'%path)

ui=ui('rcTools')
def UI():#toolbox UI 
	ui.toolBox()
	ui.tab('MAIN')
	assignUI()
	rcRoterra.UI()
	mc.setParent('MAIN')
	rigUI()
	materialsUI()
	ui.tab('SCRIPTS')
	mc.rowColumnLayout(numberOfColumns=8)
	ui.iconTextButton()
	ui.iconTextButton()
	ui.iconTextButton()
	ui.iconTextButton()  
	ui.iconTextButton()
	ui.iconTextButton(ann="Export to AFX",l= "L2F" ,i= (iconPath +"AE_Export_32.png"),c=partial(btnDelay,'mel.eval','("rcExport2AE")'))
	ui.iconTextButton(ann="Export RenderLayers to Files",l= "L2F" ,i= (iconPath +"L2F.png"),c=partial(btnDelay,'mel.eval','("rcLayers2Files")'))
	ui.iconTextButton(ann="Render Manager",l= "RenderManager" ,i= (iconPath +"renderMGR.png"),c=partial(btnDelay,'mel.eval','("rcRenderMGR")'))
	mc.setParent('..')
	scriptsUI()
	mc.showWindow()
###############UI Schemes from Templates in rcMaya.ui class 
def rigUI():
    ui.frameGRP('Rig Controls',cl=1)
    mc.rowColumnLayout(numberOfColumns=8)
    ui.iconTextButton(en=1,l= "Square" ,i= (iconPath +"ctrl_square.png"),c=partial(btnDelay,'mel.eval','(\'ctrlIcon(\"Square\")\')'))
    ui.iconTextButton(en=1,l= "Circle" ,i= (iconPath +"ctrl_circle.png"),c=partial(btnDelay,'mel.eval','(\'ctrlIcon(\"Circle\")\')'))
    ui.iconTextButton(en=1,l= "Arrow" ,i= (iconPath +"ctrl_arrow.png"),c=partial(btnDelay,'mel.eval','(\'ctrlIcon(\"Arrow\")\')'))
    ui.iconTextButton(en=1,l= "TwoDir" ,i= (iconPath +"ctrl_twoDir.png"),c=partial(btnDelay,'mel.eval','(\'ctrlIcon(\"TwoDir\")\')'))
    ui.iconTextButton(en=1,l= "FourDir" ,i= (iconPath +"ctrl_fourDir.png"),c=partial(btnDelay,'mel.eval','(\'ctrlIcon(\"FourDir\")\')'))
    ui.iconTextButton(en=1,l= "FourDir2" ,i= (iconPath +"ctrl_fourDir2.png"),c=partial(btnDelay,'mel.eval','(\'ctrlIcon(\"FourDir2\")\')'))
    ui.iconTextButton(en=1,l= "Box" ,i= (iconPath +"ctrl_box.png"),c=partial(btnDelay,'mel.eval','(\'ctrlIcon(\"Box\")\')'))
    ui.iconTextButton(en=1,l= "Tri" ,i= (iconPath +"ctrl_tri.png"),c=partial(btnDelay,'mel.eval','(\'ctrlIcon(\"Tri\")\')'))
    ui.iconTextButton(en=1,l= "FourDir2" ,i= (iconPath +"ctrl_box.png"),c=partial(btnDelay,'mel.eval','(\'ctrlIcon(\"FourDir2\")\')'))
    ui.iconTextButton(en=1,l= "FourDir2" ,i= (iconPath +"ctrl_box.png"),c=partial(btnDelay,'mel.eval','(\'ctrlIcon(\"FourDir2\")\')'))
    ui.iconTextButton(en=1,l= "FourDir2" ,i= (iconPath +"ctrl_box.png"),c=partial(btnDelay,'mel.eval','(\'ctrlIcon(\"FourDir2\")\')'))
    ui.iconTextButton(en=1,l= "FourDir2" ,i= (iconPath +"ctrl_box.png"),c=partial(btnDelay,'mel.eval','(\'ctrlIcon(\"FourDir2\")\')'))
    ui.iconTextButton(en=1,l= "FourDir2" ,i= (iconPath +"ctrl_box.png"),c=partial(btnDelay,'mel.eval','(\'ctrlIcon(\"FourDir2\")\')'))
    ui.iconTextButton(en=1,l= "FourDir2" ,i= (iconPath +"ctrl_box.png"),c=partial(btnDelay,'mel.eval','(\'ctrlIcon(\"FourDir2\")\')'))
    mc.setParent('MAIN')   
def scriptsUI(): 
	mc.frameLayout(l='TOADSTORM',w=ui.rowWidth,cll=1,cl=1)
	mc.rowColumnLayout(w=ui.rowWidth,numberOfColumns=1)
	mc.button(w=ui.rowWidth,l='Highlight Component Shading',c=partial(btnDelay,'btnSourcePy','(hfShading,hfHighlightBadShaded)'))
	mc.button(w=ui.rowWidth,l='Split Component Shading')#partial(btnDelay,'button','('+each+')'))
	mc.button(w=ui.rowWidth,l='Nuke Component Shading')
	mc.button(w=ui.rowWidth,l='Rename Duplicate Nodes')
	mc.setParent('..')
	mc.setParent('..')
	#Frame Layout each Folder with button for each Mel inside It 
	for folder in ls.dir(scriptsMEL):
		mc.frameLayout(l=folder,w=ui.rowWidth,cll=1,cl=0)#mc.text(l=folder+':',align='left')
		mc.rowColumnLayout(w=ui.rowWidth,numberOfColumns=1)
		for item in sorted(ls.dir(os.path.join(scriptsMEL,folder),folder=0)):
			file,ext=os.path.splitext(item)
			path= os.path.join(scriptsMEL,folder) 
			if ext =='.mel': 
				mc.button(w=ui.rowWidth,l=file,c=partial(btnDelay,'btnScript','("'+file+'","'+folder+'")'))
		mc.setParent('..')
		mc.setParent('..')
	
	#Frame Layout for Mels in Main folder 
	mc.frameLayout(l='GENERAL',w=ui.rowWidth,cll=1,cl=0)
	mc.rowColumnLayout(w=ui.rowWidth,numberOfColumns=1)
	for each in sorted(each for each in ls.dir(scriptsMEL,folder=0)):
		file,ext=os.path.splitext(each)
		path= scriptsMEL +'\\'+each
		if ext =='.mel':
			mc.button(w=ui.rowWidth,l=file,c=partial(btnDelay,'btnScript','("'+file+'")'))
def callWhiteBox():
	try:
		reload(whiteBox)
	except:
		from rcTools.scriptsPY import WhiteBoxTool as whiteBox 
def assignUI():
	ui.frameGRP('ASSIGN')
	mc.rowColumnLayout('ASSIGNROW',numberOfColumns=2,cal=[2,'right'],columnWidth=[(1,ui.rowWidth/2-2),(2,ui.rowWidth/2-2)])

	ui.frameSUB('PIVOTS');
	mc.gridLayout(numberOfColumns=4,cellWidthHeight=[30,30])
	mc.button(l='')
	mc.button(l='Y+',ann='Set Selected Pivot to',bgc=[.6,.6,.6],c=partial(btnDelay,'mel.eval','("rcSetPivot YMax")'))
	mc.button(l='Z-',ann='Set Selected Pivot to',bgc=[.6,.6,.6],c=partial(btnDelay,'mel.eval','("rcSetPivot ZMin")'))
	mc.button(l='Sel',bgc=[.2,.2,.2],c=partial(btnDelay,'mel.eval','("rcSetPivot SELECTED")'))
	mc.button(l='X-',ann='Set Selected Pivot to',bgc=[.6,.6,.6],c=partial(btnDelay,'mel.eval','("rcSetPivot XMin")'))
	mc.button(l='Cntr',bgc=[.2,.2,.2],c=partial(btnDelay,'mel.eval','("rcSetPivot CENTER")'))
	mc.button(l='X+',ann='Set Selected Pivot to',bgc=[.6,.6,.6],c=partial(btnDelay,'mel.eval','("rcSetPivot XMax")'))
	mc.button(l='')
	mc.button(l='Z+',ann='Set Selected Pivot to',bgc=[.6,.6,.6],c=partial(btnDelay,'mel.eval','("rcSetPivot ZMax")'))
	mc.button(l='Y-',ann='Set Selected Pivot to',bgc=[.6,.6,.6],c=partial(btnDelay,'mel.eval','("rcSetPivot YMin")'))
	mc.button(l='')
	mc.button(l='')
	mc.setParent('ASSIGNROW')

	ui.frameSUB('ROTATE')
	mc.rowColumnLayout(numberOfColumns=1)  
	mc.gridLayout(numberOfColumns=4,cellWidthHeight=[30,30])  
	mc.iconTextCheckBox(w=ui.iconSize,h=ui.iconSize,ann="Rotate",l= "Tile" ,i= "snapValue.png",onc=partial(btnDelay,'rotSnap','(45,1)'),ofc=partial(btnDelay,'rotSnap','(45,0)'))
	mc.button(l='Y+',ann='Set Selected Pivot to',bgc=[.6,.6,.6],c=partial(btnDelay,'rotAmt ','(mc.intField("RotField",q=1,v=1),"y")'))
	mc.button(l='Z-',ann='Set Selected Pivot to',bgc=[.6,.6,.6],c=partial(btnDelay,'rotAmt ','(-mc.intField("RotField",q=1,v=1),"z")'))
	mc.button(l='') 
	mc.button(l='X+',ann='Set Selected Pivot to',bgc=[.6,.6,.6],c=partial(btnDelay,'rotAmt ','(mc.intField("RotField",q=1,v=1),"x")'))
	mc.intField('RotField',v=90)#
	mc.button(l='X-',ann='Set Selected Pivot to',bgc=[.6,.6,.6],c=partial(btnDelay,'rotAmt ','(-mc.intField("RotField",q=1,v=1),"x")'))
	mc.button(l='')
	mc.button(l='Z+',ann='Set Selected Pivot to',bgc=[.6,.6,.6],c=partial(btnDelay,'rotAmt ','(mc.intField("RotField",q=1,v=1),"z")'))
	mc.button(l='Y-',ann='Set Selected Pivot to',bgc=[.6,.6,.6],c=partial(btnDelay,'rotAmt ','(-mc.intField("RotField",q=1,v=1),"y")'))
	mc.button(l='')
	mc.button(l='0,0,0',ann='Set Selected Pivot to',bgc=[.6,.6,.6],c=partial(btnDelay,'rotAmt ','(-mc.intField("RotField",q=1,v=1),"0")'))
	mc.setParent('ASSIGNROW')

	ui.frameSUB('TRANSFORMS');
	mc.gridLayout(numberOfColumns=5,cellWidthHeight=[30,30])
	mc.iconTextCheckBox(w=ui.iconSize,h=ui.iconSize,ann="Snap",l= "Tile" ,i= "snapGrid.png",onc=partial(btnDelay,'stepSnap','(5,1)'),ofc=partial(btnDelay,'stepSnap','(5,0)'))
	mc.text(l='')
	mc.text(l='')
	mc.button(l='Orig',ann='Move Object To World Origin',bgc=[.2,.2,.2],c=partial(btnDelay,'mel.eval','("rcMoveSel ORIGIN")'))
	mc.button(l='Sel',ann='Move First Selected to Second',bgc=[.2,.2,.2],c=partial(btnDelay,'mel.eval','("rcMoveSel SELECTED")'))
	mc.button(l='fObj',ann='Freeze Object\'s Transform, Rotation, Scale',bgc=[.3,.7,1],c=partial(btnDelay,'mc.makeIdentity','(mc.ls(sl=1),apply=True,t=1,r=1,s=1,n=0,pn=1)')) 
	mc.button(l='Tx',ann='Freeze Transforms',bgc=[.3,.7,1],c=partial(btnDelay,'mc.makeIdentity','(mc.ls(sl=1),apply=True,t=1,r=0,s=0,n=0,pn=1)')) 
	mc.button(l='Rx',ann='Freeze Rotations',bgc=[.3,.7,1],c=partial(btnDelay,'mc.makeIdentity','(mc.ls(sl=1),apply=True,t=0,r=1,s=0,n=0,pn=1)')) 
	mc.button(l='Sx',ann='Freeze Scales',bgc=[.3,.7,1],c=partial(btnDelay,'mc.makeIdentity','(mc.ls(sl=1),apply=True,t=0,r=0,s=1,n=0,pn=1)'))
	mc.button(l='Mov',ann='WhiteBox',bgc=[0,0,0],c=partial(btnDelay,'callWhiteBox','()'))
	mc.button(l='Crv',ann='Create Curve from Selected Joint Group',c=partial(btnDelay,'mel.eval','("Ctrl_Curve")')) 
	mc.button(l='Grp',ann='Custom Naming Grouping Procedure',bgc=[.2,.2,.2],c=partial(btnDelay,'mel.eval','("rcCtGrp")'))
	mc.setParent('ASSIGNROW')

	ui.frameSUB('COPY')
	mc.rowColumnLayout(numberOfColumns=1)  
	mc.gridLayout(numberOfColumns=4,cellWidthHeight=[30,30])  
	mc.button(l='Inst',ann='Instance',bgc=[.3,.3,.3],c=partial(btnDelay,'mel.eval','("instance")'))
	mc.button(l='DpI',ann='Duplicate Input Graph',bgc=[.3,.3,.3],c=partial(btnDelay,'mel.eval','("duplicate -rr -un")'))
	mc.button(l='Y+',ann='Set Selected Pivot to',bgc=[.6,.6,.6],c=partial(btnDelay,'copyAmt ','(mc.intField("AmtField",q=1,v=1),"0","10","0")'))
	mc.button(l='Z-',ann='Set Selected Pivot to',bgc=[.6,.6,.6],c=partial(btnDelay,'copyAmt ','(mc.intField("AmtField",q=1,v=1),"0","0","-10")'))
	mc.button(l='')
	mc.button(l='X-',ann='Set Selected Pivot to',bgc=[.6,.6,.6],c=partial(btnDelay,'copyAmt ','(mc.intField("AmtField",q=1,v=1),"-10","0","0")'))
	mc.intField('AmtField',v=5)#
	mc.button(l='X+',ann='Set Selected Pivot to',bgc=[.6,.6,.6],c=partial(btnDelay,'copyAmt ','(mc.intField("AmtField",q=1,v=1),"10","0","0")'))
	mc.button(l='')
	mc.button(l='Z+',ann='Set Selected Pivot to',bgc=[.6,.6,.6],c=partial(btnDelay,'copyAmt ','(mc.intField("AmtField",q=1,v=1),"0","0","10")'))
	mc.button(l='Y-',ann='Set Selected Pivot to',bgc=[.6,.6,.6],c=partial(btnDelay,'copyAmt ','(mc.intField("AmtField",q=1,v=1),"0","-10","0")'))
	mc.iconTextCheckBox(ann="Instance",l= "Inst" ,i= "instancer.svg",onc=partial(btnDelay,'rc.stepSnap','(5,1)'),ofc=partial(btnDelay,'stepSnap','(5,0)'))
	mc.setParent('ASSIGNROW')

	ui.frameSUB('VIEWPORT')
	mc.rowColumnLayout(numberOfColumns=4)
	ui.iconTextButton(ann="Fix Render Globals",l= "FIX" ,i="overrideSettings.png",c=partial(btnDelay,'set.globals','(opt="fix")'))
	mc.menuBarLayout()
	# mc.menuItem(label='<RenderLayer>/<RenderLayer>',c=partial(btnDelay,'set.imagePrefix','("S__L__L")'))
	# mc.menuItem(label='<RenderLayer>/<RenderLayer>.<RenderPass>',c=partial(btnDelay,'set.imagePrefix','("S__L__L.P")'))
	# mc.menuItem(label='<RenderLayer>/<RenderPass>/<RenderLayer>.<RenderPass>',c=partial(btnDelay,'set.imagePrefix','("S__L__P__L.P")'))
	mc.menu(label='Image Prefix')
	mc.menuItem(label='<RenderLayer>/<RenderLayer>',c=partial(btnDelay,'set.imagePrefix','("L__L")'))
	mc.menuItem(label='<RenderLayer>/<RenderLayer>.<RenderPass>',c=partial(btnDelay,'set.imagePrefix','("L__L.P")'))
	mc.menuItem(label='<RenderLayer>/<RenderPass>/<RenderLayer>.<RenderPass>',c=partial(btnDelay,'set.imagePrefix','("L__P__L.P")'))
	mc.menu(label='Resolution Preset')
	mc.menuItem(label='4k',c=partial(btnDelay,'set.imagePrefix','("L__L")'))
	mc.menuItem(label='1024x768_IPAD',c=partial(btnDelay,'set.imagePrefix','("L__L.P")'))
	mc.menuItem(label='16:9_IPHONE',c=partial(btnDelay,'set.imagePrefix','("L__P__L.P")'))

	mc.setParent('..')
	ui.iconTextButton(ann="Fix Meter Camera Near/Far",l= "Set Camera" ,i= "CameraAE.png",c=partial(btnDelay,'set.camera','(near=.1,far=10000)'))
	ui.iconTextButton(i=iconPath+'unity.png') 
	ui.iconTextButton()
	mc.button(w=ui.iconSize,h=ui.iconSize,ann='Set Viewport Color',l='BG',c=partial(btnDelay,'mel.eval','("rcSetView GREY")'))
	mc.popupMenu()  
	mc.menuItem(l='GREEN',c=partial(btnDelay,'mel.eval','("rcSetView GREEN")'))
	mc.menuItem(l='GREY',c=partial(btnDelay,'mel.eval','("rcSetView GREY")'))
	mc.menuItem(l='GRAD',c=partial(btnDelay,'mel.eval','("rcSetView GRAD")'))
	mc.button(w=ui.iconSize,h=ui.iconSize,bgc=[0,.2,0],l='RE',c=partial(btnDelay,'mel.eval','("rcSetView SHOWALL")'))  
	mc.popupMenu()  
	mc.menuItem(l='CTRL',c=partial(btnDelay,'mel.eval','("rcSetView CTRL")'))
	mc.menuItem(l='POLY',c=partial(btnDelay,'mel.eval','("rcSetView POLY")'))
	mc.menuItem(l='ALL',c=partial(btnDelay,'mel.eval','("rcSetView SHOWALL")'))  
	# mc.button(w=ui.iconSize,h=ui.iconSize,l='CTRL',c=partial(btnDelay,'mel.eval','("rcSetView CTRL")'))    
	#mc.button(w=ui.iconSize,h=ui.iconSize,l='ALL',c=partial(btnDelay,'mel.eval','("rcSetView SHOWALL")'))
   	mc.iconTextCheckBox(i= "polyQuad",cc=partial(btnDelay,'mel.eval','("TogglePolyCount")'))
	mc.setParent('..')
	# mc.setParent('..')

	ui.frameSUB('NORMALS');
	mc.gridLayout(numberOfColumns=3,cellWidthHeight=[42,25])
	mc.text(l='Normal:')
	mc.iconTextButton(l='Hard',i='polyHardEdge.png',ann='Set Selected Pivot to',c=partial(btnDelay,'mc.polySetToFaceNormal','(setUserNormal=True)'))
	mc.iconTextButton(l='Soft',i='polySoftEdge.png',ann='Set Selected Pivot to',c=partial(btnDelay,'mc.polySoftEdge','(a=180,ch=1)'))
	mc.text(l='')
	mc.textField('angleparameter',tx='70')
	mc.button(l='Set',h=ui.btn_small,ann='Set Selected Pivot to',bgc=[.6,.6,.6],c=partial(btnDelay,'mc.polySoftEdge','(a=mc.textField(\'angleparameter\',q=True,tx=1),ch=1)'))
	
	mc.setParent('ASSIGNROW')
	'''
	mc.separator(style='in',h=ui.borders*3)
	mc.checkBoxGrp('smoothPreview',h=ui.checkBoxHeight,ncb=1,vr=1,l1='Smooth Preview',v1=1)
	mc.textFieldGrp('rsmoothField',l='  Render Smooth:',text='2',cw2=[90,30],cat=[1,'left',1])
	mc.textFieldGrp('dsmoothField',l='  Display Smooth:',text='0',cw2=[90,30],cat=[1,'left',1])
	mc.button(h=ui.btn_large,w=ui.rowWidth/2-8,l='APPLY',c=partial(btnDelay,'set.smooth','(0)')) 
	mc.button(h=ui.btn_small,w=ui.rowWidth/2-8,l='RESET',ann='Remove Overrides for object',c=partial(btnDelay,'set.smooth','(1)'))
	mc.separator(style='in',h=ui.borders*10)
    '''
	mc.setParent('ASSIGNROW')


	ui.frameSUB('ATTRIBUTES'); mc.columnLayout()
	#mc.separator(style='in',bgc=[.2,.2,.2],h=ui.borders*3)
	for each in ls.renderAtts(): mc.checkBoxGrp(each,ncb=1,vr=1,h=ui.checkBoxHeight,l1=each,v1=1)
	mc.separator(style='in',h=ui.borders*3)
	
	mc.button(h=ui.btn_large,w=ui.rowWidth/2-8,l='APPLY',c=partial(btnDelay,'set.flags','(value="Apply")')) 
	
	
	mc.rowColumnLayout(numberOfColumns=4)
	mc.button(h=ui.btn_small,l='ON',c=partial(btnDelay,'set.flags','(value=1)'))
	mc.button(h=ui.btn_small,l='OFF',c=partial(btnDelay,'set.flags','(value=0)'))
	mc.button(h=ui.btn_small,l='NUKE',en=0,ann='Remove Overrides for object',c=partial(btnDelay,'setRenderFlags','(value=0)'))
	mc.setParent('..')
	mc.button(h=ui.btn_large,l='XRAY',w=ui.rowWidth/2-8,ann='Remove Overrides for object',c=partial(btnDelay,'set.xray','()'))

	mc.setParent('MAIN')  
def materialsUI():
	ui.frameGRP('MATERIALS',cl=1,bgc=[.4,.2,.4])
	#if mc.frameLayout('GLOBAL',q=1,ex=1)==1: mc.frameLayout('GLOBAL',e=1,cl=1)#CLOSE GLOBALS WIN
	mc.floatSliderGrp('lambertslider',label='Lambert1 Transparent',minValue=0,maxValue=1,cc=partial(btnDelay,'lambertset','()'))
	mc.separator(style='in')

	mc.rowColumnLayout(numberOfColumns=2)
	mc.text( font= "tinyBoldLabelFont" ,w= ui.rowWidth/2, h= 8,l ="    Create/Assign Layers:",al= "left")
	mc.text( font= "tinyBoldLabelFont" ,w= ui.rowWidth/2, h= 8,l ="    Scripts:",al= "left")
	mc.setParent('..')
	
	mc.rowColumnLayout(numberOfColumns=8)
	ui.iconTextButton(ann="Assign/Create Layer AODPTHINC",l= "AODPTHINC" ,i= (iconPath +"AODPTHINC_32.png"),c=partial(btnDelay,'mel.eval','("rcAssignLayer AODPTHINC")'))
	ui.iconTextButton(ann="Assign/Create Layer MASK_RGB" ,l= "MASK_RGB" ,i=(iconPath+"MASK_RGB.png"),c=partial(btnDelay,'mel.eval','("rcAssignLayer MASK_RGB")'))
	ui.iconTextButton(ann="Assign/Create Layer CONTOUR" ,l= "" ,i= 'baseLattice.svg',c=partial(btnDelay,'createMat','("CONTOUR")'))
	mc.textField('CONDIA',w=ui.iconSize-5,fn='boldLabelFont',tx='01')
	ui.iconTextButton(ann='Seperate Objects For Element',i=iconPath+'VC',c=partial(btnDelay,'toElement.seperate','()'))
	ui.iconTextButton(ann='Rename Shading Groups',i=iconPath+'VC',c=partial(btnDelay,'toElement.renameSG','()'))
	ui.iconTextButton(ann="Unity Conform",l= "BLINN" ,i= "annotation.png",c=partial(btnDelay,'conform','()'))
	ui.iconTextButton(ann='Create Image Card From File',i=iconPath+'picture_32',c=partial(btnDelay,'create.imageCard','()'))
	#ui.iconTextButton(ann= "Add Gamma Correct Nodes to Selected Shader" ,i= 'gammaCorrect.svg', c=partial(btnDelay,'mel.eval','( "gammaUIMain")'))
	mc.setParent('..')

	mc.text( font= "tinyBoldLabelFont" ,w=ui.iconSize, h= 8,l ="    Create/Assign Materials:",al= "left")
	mc.rowColumnLayout(numberOfColumns=8)
	ui.iconTextButton(en=0,ann="Assign/Create Phong",l= "PHONG" ,i= "render_phong.png",c=partial(btnDelay,'mel.eval','("rcAssignShader AO")'))
	ui.iconTextButton(en=0,ann="Assign/Create Lambert",l= "LAMBERT" ,i= "render_lambert",c=partial(btnDelay,'mel.eval','("rcAssignShader DPTH")'))
	mc.iconTextButton(w=ui.iconSize,ann= "Convert Selected Shader to MIA",i= iconPath +"MIA.png", c= partial(btnDelay,'mel.eval','( "convert2MIA")'))
	ui.iconTextButton(ann="Assign/Create AODPTHINC",l= "AODPTHINC" ,i= (iconPath +"AODPTHINC_32.png"),c=partial(btnDelay,'mel.eval','("rcAssignShader AODPTHINC")'))
	ui.iconTextButton(ann="Assign/Create AO",l= "AO" ,i= (iconPath +"OCC_32.png"),c=partial(btnDelay,'mel.eval','("rcAssignShader AO")'))
	ui.iconTextButton(ann="Assign/Create DPTH",l= "DPTH" ,i= (iconPath +"DPTH_32.png"),en=0,c=partial(btnDelay,'mel.eval','("rcAssignShader DPTH")'))
	ui.iconTextButton(ann="Assign/Create INC",l= "INC" ,i= (iconPath +'INC_32.png'),c=partial(btnDelay,'set.shader','("INC")'))
	ui.iconTextButton(ann="Assign/Create ALPHA RAMP",l= "A" ,i= (iconPath +'RAMP_A_32.png'),c=partial(btnDelay,'mel.eval','("rcAssignShader RAMP_A")'))
  
	
	mc.button(h=ui.btn_large,w=ui.iconSize,bgc=[.5,0,0],l="R",c= partial(btnDelay,'set.shader','("RED")'))
	mc.button(h=ui.btn_large,w=ui.iconSize,bgc= [0 ,.5 ,0 ],l= "G" ,c=partial(btnDelay,'set.shader','( "GREEN")'))
	mc.button(h=ui.btn_large,w=ui.iconSize,bgc= [0 ,0 ,.5] ,l= "B" ,c= partial(btnDelay,'set.shader','( "BLUE")'))
	mc.iconTextButton(h=ui.btn_large,w=ui.iconSize,bgc= [0 ,0 ,0] ,l= "A" ,c=partial(btnDelay,'set.shader','( "ALPHA")'),i='textureEditorDisplayAlpha.png')
	mc.button(h=ui.btn_large,w=ui.iconSize,bgc= [0 ,.5 ,.5],l= "C" ,c= partial(btnDelay,'set.shader','( "CYAN")'))
	mc.button(h=ui.btn_large,w=ui.iconSize,bgc= [.5 ,0, .5],l= "M" ,c= partial(btnDelay,'set.shader','( "MAGENTA")'))
	mc.button(h=ui.btn_large,w=ui.iconSize,bgc= [.5 ,.5 ,0],l= "Y" ,c= partial(btnDelay,'set.shader','( "YELLOW")'))
	mc.button(h=ui.btn_large,w=ui.iconSize,bgc= [0 ,0 ,0],l= "K" ,c= partial(btnDelay,'set.shader','( "BLACK")'))
	mc.setParent('..')
	mc.separator(style='in')
	mc.setParent('..')
	mc.setParent('MAIN')     
def globalsUI():#MENTALRAY DEPRICATED
	mc.frameLayout('GLOBAL',w=ui.rowWidth,l='GLOBALS',bgc=[.4,.2,.4],bs='in',fn='smallBoldLabelFont',cl=1)
	mc.rowColumnLayout(w=ui.rowWidth,numberOfColumns=4)
	#mc.text(l='Anti\nAlias:',w=35,font='tinyBoldLabelFont',h=textHeight,al='right')
	#mc.button(h=buttons_med,w=ui.rowWidth/4,l='LOW -2/0 \n .10',c=partial(btnDelay,'mel.eval','("rcSetGlobals LOW")'))
	#mc.button(h=buttons_med,w=ui.rowWidth/4,l='MED  0/2 \n .05',c=partial(btnDelay,'mel.eval','("rcSetGlobals MED")'))
	#mc.button(h=buttons_med,w=ui.rowWidth/4,l='HI 2/0 \n .02',c=partial(btnDelay,'mel.eval','("rcSetGlobals HIGH")')) 
	mc.text(l='Final\nGather:',w=35,font='tinyBoldLabelFont',h=textHeight,al='right')
	mc.button(h=buttons_med,w=ui.rowWidth/4,l='LOW 50/.1 \n .10',c=partial(btnDelay,'mel.eval','("rcSetGlobals LOW")'))
	mc.button(h=buttons_med,w=ui.rowWidth/4,l='MED  250/.1 \n .05',c=partial(btnDelay,'mel.eval','("rcSetGlobals MED")'))
	mc.button(h=buttons_med,w=ui.rowWidth/4,l='HI 2/0 \n .02',c=partial(btnDelay,'mel.eval','("rcSetGlobals HIGH")'))
	
	mc.text(l='Image\nFormat:',w=35,font='tinyBoldLabelFont',h=textHeight,al='right')
	mc.button(h=buttons_med,w=ui.rowWidth/4,l='PNG\n 16BIT',c=partial(btnDelay,'mel.eval','("rcSetGlobals PNG")'))
	mc.button(h=buttons_med,w=ui.rowWidth/4,l='TIF \n 16Bit',c=partial(btnDelay,'mel.eval','("rcSetGlobals TIF")'))
	mc.button(h=buttons_med,w=ui.rowWidth/4,l='EXR\n 32BIT',c=partial(btnDelay,'mel.eval','("rcSetGlobals EXR")'))
	
	mc.text(l='Image\nPrefix:',w=35,font='tinyBoldLabelFont',h=textHeight,al='right')
	mc.button(h=buttons_med,w=ui.rowWidth/4,l='Layers',c=partial(btnDelay,'mel.eval','("rcSetGlobals -layers")'))
	mc.button(h=buttons_med,w=ui.rowWidth/4,l='Passes',c=partial(btnDelay,'mel.eval','("rcSetGlobals -passes")'))
	mc.button(h=buttons_med,w=ui.rowWidth/4,l='',c=partial(btnDelay,'mel.eval','("rcSetGlobals ")'))
	
	mc.setParent('..')
	mc.setParent('..')
############### 
def browse(location=None):#location default sourceimages
    if not location: location=mc.workspace(q=1,dir=1)
    try:
        dialogReturn=mc.fileDialog2(fm=1,okc='OK',fileFilter='*_color.png',dir=location)[0]
        if dialogReturn:
            return dialogReturn   
        else:
            sys.exit()
    except:
        sys.exit()
def lambertset():#transparancy slider for toolbox
	num=mc.floatSliderGrp('lambertslider',q=1,value=1)
	mc.setAttr('lambert1.transparency',num,num,num,type='double3')
def btnScript(script,folder=''):#passing and sourcing for mel script lists 
	if folder is not None: mel.eval('source "'+scriptsMEL.replace('\\','/')+folder+'/'+str(script)+'"')
	else: mel.eval('source "'+scriptsMEL+str(script)+'"')
	mel.eval(str(script))
def btnSourcePy(file,command):#wip py scripts
		import file
		reload (file)
		file.command

if __name__== 'toolBox' :
	ui.win()
	UI()
