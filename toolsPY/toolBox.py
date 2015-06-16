import os 
import sys
import subprocess
import shutil
################
import maya.cmds as mc 
import maya.mel as mel 
################
from functools import partial
def delay(method,string,*args): exec(method+string) #Delay Function
################
from rcTools.rcMaya import *
from rcTools.toolsPY import toElement 
################source every mel in toolsMEL: toolsMEL
for each in os.listdir(toolsMEL):
	file,ext=os.path.splitext(each)
	path= os.path.join(toolsMEL.replace('\\','/'),each)
	if ext =='.mel': mel.eval('source "%s"'%path)
###############
ui=ui('rcTools')
def UI():
	ui.toolBox()
	ui.tab('MAIN')
	assignUI()
	materialsUI()
	
	ui.tab('SCRIPTS')
	mc.rowColumnLayout(numberOfColumns=8)
	mc.iconTextButton(w=ui.rowWidth/8,h=ui.rowWidth/8)
	mc.iconTextButton(w=ui.rowWidth/8,h=ui.rowWidth/8)
	mc.iconTextButton(w=ui.rowWidth/8,h=ui.rowWidth/8)
	mc.iconTextButton(w=ui.rowWidth/8,h=ui.rowWidth/8)  
	mc.iconTextButton(w=ui.rowWidth/8,h=ui.rowWidth/8)
	mc.iconTextButton(w=ui.rowWidth/8,h=ui.rowWidth/8,ann="Export to AFX",l= "L2F" ,i= (iconPath +"AE_Export_32.png"),c=partial(delay,'mel.eval','("rcExport2AE")'))
	mc.iconTextButton(w=ui.rowWidth/8,h=ui.rowWidth/8,ann="Export RenderLayers to Files",l= "L2F" ,i= (iconPath +"L2F.png"),c=partial(delay,'mel.eval','("rcLayers2Files")'))
	mc.iconTextButton(w=ui.rowWidth/8,h=ui.rowWidth/8,ann="Render Manager",l= "RenderManager" ,i= (iconPath +"renderMGR.png"),c=partial(delay,'mel.eval','("rcRenderMGR")'))
	mc.setParent('..')
	
	scriptsUI()
###############
def scriptsUI():
	mc.frameLayout(l='TOADSTORM',w=ui.rowWidth,cll=1,cl=1)
	mc.button(w=ui.rowWidth,l='Highlight Component Shading',c=partial(delay,'btnSourcePy','(hfShading,hfHighlightBadShaded)'))
	mc.button(w=ui.rowWidth,l='Split Component Shading')#partial(delay,'button','('+each+')'))
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
				mc.button(w=ui.rowWidth,l=file,c=partial(delay,'btnScript','("'+file+'","'+folder+'")'))
		mc.setParent('..')
		mc.setParent('..')
		
	#Frame Layout for Mels in Main folder 
	mc.frameLayout(l='GENERAL',w=ui.rowWidth,cll=1,cl=0)
	mc.rowColumnLayout(w=ui.rowWidth,numberOfColumns=1)
	for each in sorted(each for each in ls.dir(scriptsMEL,folder=0)):
		file,ext=os.path.splitext(each)
		path= scriptsMEL +'\\'+each
		if ext =='.mel':
			mc.button(w=ui.rowWidth,l=file,c=partial(delay,'btnScript','("'+file+'")'))
def assignUI():
	mc.frameLayout('ASSIGNFRAME',w=ui.rowWidth,h=330,cll=1,bgc=[.2,.2,.2],fn='smallBoldLabelFont',bs='in',l='ASSIGN')
	
	mc.rowColumnLayout(numberOfColumns=2,columnWidth=[(1,ui.rowWidth/2),(2,ui.rowWidth/2)])
	
	mc.columnLayout('SHAPECTRL',w=ui.rowWidth/2-5)
	mc.gridLayout(numberOfColumns=5,cellWidthHeight=[25,25])
	mc.text(l='Piv'); mc.separator(style='in'); mc.button(l='Cntr',bgc=[.2,.2,.2],c=partial(delay,'mel.eval','("rcSetPivot CENTER")'))
	mc.button(l='Orig',bgc=[.2,.2,.2],en=0,c=partial(delay,'mel.eval','("rcSetPivot ORIGIN")'))
	mc.button(l='Sel',bgc=[.2,.2,.2],c=partial(delay,'mel.eval','("rcSetPivot SELECTED")'))
	mc.button(l='',c=partial(delay,'mel.eval','(toMiddle(\"max\" ,\"max\", \"max\")'))
	mc.button(l='')
	mc.text(l='')
	mc.button(l='')
	mc.button(l='')
	mc.button(l='')
	mc.button(l='')
	mc.button(l='Y+',ann='Set Selected Pivot to',bgc=[.6,.6,.6],c=partial(delay,'mel.eval','("rcSetPivot YMax")'))
	mc.button(l='')
	mc.button(l='')
	mc.text(l='')
	mc.button(l='X+',ann='Set Selected Pivot to',bgc=[.6,.6,.6],c=partial(delay,'mel.eval','("rcSetPivot XMax")'))
	mc.text(l='')
	mc.button(l='X-',ann='Set Selected Pivot to',bgc=[.6,.6,.6],c=partial(delay,'mel.eval','("rcSetPivot XMin")'))
	mc.text(l='')
	mc.text(l='')
	mc.button(l='Z+',ann='Set Selected Pivot to',bgc=[.6,.6,.6],c=partial(delay,'mel.eval','("rcSetPivot ZMax")'))
	mc.button(l='Y-',ann='Set Selected Pivot to',bgc=[.6,.6,.6],c=partial(delay,'mel.eval','("rcSetPivot YMin")'))
	mc.button(l='Z-',ann='Set Selected Pivot to',bgc=[.6,.6,.6],c=partial(delay,'mel.eval','("rcSetPivot ZMin")'))
	mc.text(l='')
	mc.text(l='Obj')
	mc.button(l='fObj',ann='Freeze Object\'s Transform, Rotation, Scale',bgc=[.3,.7,1],c=partial(delay,'mc.makeIdentity','(mc.ls(sl=1),apply=True,t=1,r=1,s=1,n=0,pn=1)')) 
	mc.button(l='DpI',ann='Duplicate Input Graph',bgc=[.2,.2,.2],c=partial(delay,'mel.eval','("duplicate -rr -un")'))
	mc.button(l='Orig',ann='Move Object To World Origin',bgc=[.2,.2,.2],c=partial(delay,'mel.eval','("rcMoveSel ORIGIN")'))
	mc.button(l='Sel',ann='Move First Selected to Second',bgc=[.2,.2,.2],c=partial(delay,'mel.eval','("rcMoveSel SELECTED")')) 
	mc.button(l='Tx',ann='Freeze Transforms',bgc=[.3,.7,1],c=partial(delay,'mc.makeIdentity','(mc.ls(sl=1),apply=True,t=1,r=0,s=0,n=0,pn=1)')) 
	mc.button(l='Rx',ann='Freeze Rotations',bgc=[.3,.7,1],c=partial(delay,'mc.makeIdentity','(mc.ls(sl=1),apply=True,t=0,r=1,s=0,n=0,pn=1)')) 
	mc.button(l='Sx',ann='Freeze Scales',bgc=[.3,.7,1],c=partial(delay,'mc.makeIdentity','(mc.ls(sl=1),apply=True,t=0,r=0,s=1,n=0,pn=1)'))  
	mc.button(l='Crv',ann='Create Curve from Selected Joint Group',c=partial(delay,'mel.eval','("Ctrl_Curve")')) 
	mc.button(l='Grp',ann='Custom Naming Grouping Procedure',bgc=[.2,.2,.2],c=partial(delay,'mel.eval','("rcCtGrp")'))
	mc.setParent('..')
   
	mc.separator(style='in',h=ui.borders*3)
	mc.checkBoxGrp('smoothPreview',h=ui.checkBoxHeight,ncb=1,vr=1,l1='Smooth Preview',v1=1)
   

	mc.textFieldGrp('rsmoothField',l='  Render Smooth:',text='2',cw2=[90,30],cat=[1,'left',1])
	mc.textFieldGrp('dsmoothField',l='  Display Smooth:',text='0',cw2=[90,30],cat=[1,'left',1])
	mc.button(h=ui.btn_large,w=ui.rowWidth/2-8,l='APPLY',c=partial(delay,'set.smooth','(0)')) 
	mc.button(h=ui.btn_small,w=ui.rowWidth/2-8,l='RESET',ann='Remove Overrides for object',c=partial(delay,'set.smooth','(1)'))
	mc.separator(style='in',h=ui.borders*10)
	mc.setParent('..')
	
	
	mc.columnLayout(w=ui.rowWidth/2)#h=(len(ls.renderAtts())*(ui.checkBoxHeight+ui.borders+2))+(ui.btn_large+ui.btn_small)
	
	mc.gridLayout(numberOfColumns=5,cellWidthHeight=[25,25])
	mc.text(l='Disp');
	mc.separator(style='in');
	mc.separator(style='in');
	mc.button(h=25,w=42,ann='Set Camera Clips',l='CC',c=partial(delay,'mel.eval','("rcSetCameraClip")'));
	mc.button(h=25,w=42,ann='Set Viewport to Green for PlayBlast',l='RE',bgc=[.0,.5,.0],c=partial(delay,'set.view','(opt=1)'))
	
	mc.setParent('..')
	
	mc.rowColumnLayout(numberOfColumns=3,rat=[1,'both',0])
	mc.button(h=25,w=42,ann='Set Viewport to Green for PlayBlast',l='GREEN',bgc=[.0,1,.0],c=partial(delay,'mel.eval','("rcSetView GREEN")'))    
	mc.button(h=25,w=42,ann='Set Viewport to Standard Grey',l='GREY',bgc=[.8,.8,.8],c=partial(delay,'mel.eval','("rcSetView GREY")'))    
	mc.button(h=25,w=42,ann='Set Viewport to Gradient',l='GRAD',c=partial(delay,'mel.eval','("rcSetView GRAD")'))    
	mc.button(h=25,w=42,l='POLY',c=partial(delay,'mel.eval','("rcSetView POLY")'))    
	mc.button(h=25,w=42,l='CTRL',c=partial(delay,'mel.eval','("rcSetView CTRL")'))    
	mc.button(h=25,w=42,l='ALL',c=partial(delay,'mel.eval','("rcSetView SHOWALL")'))    
	mc.setParent('..')
	
	mc.gridLayout(numberOfColumns=5,cellWidthHeight=[25,25])
	mc.text(l='Attr');mc.separator(style='in');mc.separator(style='in');mc.separator(style='in');mc.separator(style='in')
	mc.setParent('..')
	
	mc.separator(style='in',bgc=[.2,.2,.2],h=ui.borders*3)
	for each in ls.renderAtts(): mc.checkBoxGrp(each,h=ui.checkBoxHeight,ncb=1,vr=1,l1=each,v1=1)
	mc.separator(style='in',bgc=[.2,.2,.2],h=ui.borders*3)
	mc.button(h=ui.btn_large,w=ui.rowWidth/2-8,l='APPLY',c=partial(delay,'set.flags','(value="Apply")')) 
	
	mc.rowColumnLayout(numberOfColumns=4)
	mc.button(h=ui.btn_small,l='ON',c=partial(delay,'set.flags','(value=1)'))
	mc.button(h=ui.btn_small,l='OFF',c=partial(delay,'set.flags','(value=0)'))
	mc.button(h=ui.btn_small,l='NUKE',en=0,ann='Remove Overrides for object',c=partial(delay,'setRenderFlags','(value=0)'))
	mc.button(h=ui.btn_small,l='XRAY',ann='Remove Overrides for object',c=partial(delay,'set.xray','()'))
   
	mc.setParent('MAIN')  


def materialsUI():
	icon=ui.rowWidth/8
	mc.frameLayout('rcMATERIALS',bgc=[.4,.2,.4],w=ui.rowWidth,bs='in',fn='smallBoldLabelFont',cll=1)
	if mc.frameLayout('GLOBAL',q=1,ex=1)==1: mc.frameLayout('GLOBAL',e=1,cl=1)#CLOSE GLOBALS WIN
	mc.floatSliderGrp('lambertslider',label='Lambert1 Transparent',minValue=0,maxValue=1,cc=partial(delay,'lambertset','()'))
	mc.separator(style='in')

	mc.rowColumnLayout(numberOfColumns=2)
	mc.text( font= "tinyBoldLabelFont" ,w= ui.rowWidth/2, h= 8,l ="    Create/Assign Layers:",al= "left")
	mc.text( font= "tinyBoldLabelFont" ,w= ui.rowWidth/2, h= 8,l ="    Scripts:",al= "left")
	mc.setParent('..')
	
	mc.rowColumnLayout(numberOfColumns=8)
	mc.iconTextButton(w=icon,h=icon,ann="Assign/Create Layer AODPTHINC",l= "AODPTHINC" ,i= (iconPath +"AODPTHINC_32.png"),c=partial(delay,'mel.eval','("rcAssignLayer AODPTHINC")'))
	mc.iconTextButton(w=icon,h=icon,ann="Assign/Create Layer MASK_RGB" ,l= "MASK_RGB" ,i=(iconPath+"MASK_RGB.png"),c=partial(delay,'mel.eval','("rcAssignLayer MASK_RGB")'))
	mc.iconTextButton(w=icon,h=icon,ann="Assign/Create Layer CONTOUR" ,l= "" ,i= 'baseLattice.svg',c=partial(delay,'createMat','("CONTOUR")'))
	mc.textField('CONDIA',w=icon-5,fn='boldLabelFont',tx='01')
	mc.iconTextButton(w=icon,h=icon,ann='Seperate Objects For Element',i=iconPath+'VC',c=partial(delay,'toElement.seperate','()'))
	mc.iconTextButton(w=icon,h=icon,ann='Rename Shading Groups',i=iconPath+'VC',c=partial(delay,'toElement.renameSG','()'))
	mc.iconTextButton(w=icon,h=icon,ann='Create Image Card From File',i=iconPath+'picture_32',c=partial(delay,'create.imageCard','()'))
	mc.iconTextButton(w=icon,ann= "Convert Selected Shader to MIA",i= iconPath +"MIA.png", c= partial(delay,'mel.eval','( "convert2MIA")'))
	#mc.iconTextButton(w=icon,h=icon,ann= "Add Gamma Correct Nodes to Selected Shader" ,i= 'gammaCorrect.svg', c=partial(delay,'mel.eval','( "gammaUIMain")'))
	mc.setParent('..')

	mc.text( font= "tinyBoldLabelFont" ,w= icon, h= 8,l ="    Create/Assign Materials:",al= "left")
	mc.rowColumnLayout(numberOfColumns=8)
	mc.iconTextButton(w=icon,h=icon,en=0,ann="Assign/Create Blinn",l= "BLINN" ,i= "render_blinn.png",c=partial(delay,'mel.eval','("rcAssignShader AODPTHINC")'))
	mc.iconTextButton(w=icon,h=icon,en=0,ann="Assign/Create Phong",l= "PHONG" ,i= "render_phong.png",c=partial(delay,'mel.eval','("rcAssignShader AO")'))
	mc.iconTextButton(w=icon,h=icon,en=0,ann="Assign/Create Lambert",l= "LAMBERT" ,i= "render_lambert",c=partial(delay,'mel.eval','("rcAssignShader DPTH")'))
	mc.iconTextButton(w=icon,h=icon,ann="Assign/Create AODPTHINC",l= "AODPTHINC" ,i= (iconPath +"AODPTHINC_32.png"),c=partial(delay,'mel.eval','("rcAssignShader AODPTHINC")'))
	mc.iconTextButton(w=icon,h=icon,ann="Assign/Create AO",l= "AO" ,i= (iconPath +"OCC_32.png"),c=partial(delay,'mel.eval','("rcAssignShader AO")'))
	mc.iconTextButton(w=icon,h=icon,ann="Assign/Create DPTH",l= "DPTH" ,i= (iconPath +"DPTH_32.png"),en=0,c=partial(delay,'mel.eval','("rcAssignShader DPTH")'))
	mc.iconTextButton(w=icon,h=icon,ann="Assign/Create INC",l= "INC" ,i= (iconPath +'INC_32.png'),c=partial(delay,'set.shader','("INC")'))
	mc.iconTextButton(w=icon,h=icon,ann="Assign/Create ALPHA RAMP",l= "A" ,i= (iconPath +'RAMP_A_32.png'),c=partial(delay,'mel.eval','("rcAssignShader RAMP_A")'))
  
	
	mc.button(h=ui.btn_large,w=icon,bgc=[.5,0,0],l="R",c= partial(delay,'set.shader','("RED")'))
	mc.button(h=ui.btn_large,w=icon,bgc= [0 ,.5 ,0 ],l= "G" ,c=partial(delay,'set.shader','( "GREEN")'))
	mc.button(h=ui.btn_large,w=icon,bgc= [0 ,0 ,.5] ,l= "B" ,c= partial(delay,'set.shader','( "BLUE")'))
	mc.iconTextButton(h=ui.btn_large,w=icon,bgc= [0 ,0 ,0] ,l= "A" ,c=partial(delay,'set.shader','( "ALPHA")'),i='textureEditorDisplayAlpha.png')
	mc.button(h=ui.btn_large,w=icon,bgc= [0 ,.5 ,.5],l= "C" ,c= partial(delay,'set.shader','( "CYAN")'))
	mc.button(h=ui.btn_large,w=icon,bgc= [.5 ,0, .5],l= "M" ,c= partial(delay,'set.shader','( "MAGENTA")'))
	mc.button(h=ui.btn_large,w=icon,bgc= [.5 ,.5 ,0],l= "Y" ,c= partial(delay,'set.shader','( "YELLOW")'))
	mc.button(h=ui.btn_large,w=icon,bgc= [0 ,0 ,0],l= "K" ,c= partial(delay,'set.shader','( "BLACK")'))
	
	mc.setParent('..')
	mc.separator(style='in')
	#mc.frameLayout('frame_MATERIAL',w=ui.rowWidth,l='Existing Materials List',ec=partial(delay,'existMAT','()'),cll=1)
	#existMAT()
	mc.setParent('..')
	mc.setParent('MAIN')
def existMATUI():
	if mc.scrollLayout('materiallist',q=1,ex=1)==True: mc.deleteUI('materiallist')
	mc.setParent('MAIN')
	mc.scrollLayout('materiallist',w=ui.rowWidth,h=390)#h=len(ls.shaders())*25)
	mc.rowColumnLayout(w=ui.rowWidth-10,numberOfColumns=2)
	for each in sorted(ls.shaders()):
		mc.button(w=ui.rowWidth-55,l=each,c=partial(delay,'mc.select','(\''+ str(each)+'\')'))
		mc.button(w=45,l='ASSIGN',c=partial(delay,'mc.hyperShade','(assign=\''+ str(each)+'\')'))
		#mc.button(w=40,l='GRAPH')   
	mc.setParent('..');mc.setParent('..')     
def globalsUI():
	mc.frameLayout('GLOBAL',w=ui.rowWidth,l='GLOBALS',bgc=[.4,.2,.4],bs='in',fn='smallBoldLabelFont',cl=1)
	mc.rowColumnLayout(w=ui.rowWidth,numberOfColumns=4)
	#mc.text(l='Anti\nAlias:',w=35,font='tinyBoldLabelFont',h=textHeight,al='right')
	#mc.button(h=buttons_med,w=ui.rowWidth/4,l='LOW -2/0 \n .10',c=partial(delay,'mel.eval','("rcSetGlobals LOW")'))
	#mc.button(h=buttons_med,w=ui.rowWidth/4,l='MED  0/2 \n .05',c=partial(delay,'mel.eval','("rcSetGlobals MED")'))
	#mc.button(h=buttons_med,w=ui.rowWidth/4,l='HI 2/0 \n .02',c=partial(delay,'mel.eval','("rcSetGlobals HIGH")')) 
	mc.text(l='Final\nGather:',w=35,font='tinyBoldLabelFont',h=textHeight,al='right')
	mc.button(h=buttons_med,w=ui.rowWidth/4,l='LOW 50/.1 \n .10',c=partial(delay,'mel.eval','("rcSetGlobals LOW")'))
	mc.button(h=buttons_med,w=ui.rowWidth/4,l='MED  250/.1 \n .05',c=partial(delay,'mel.eval','("rcSetGlobals MED")'))
	mc.button(h=buttons_med,w=ui.rowWidth/4,l='HI 2/0 \n .02',c=partial(delay,'mel.eval','("rcSetGlobals HIGH")'))
	
	mc.text(l='Image\nFormat:',w=35,font='tinyBoldLabelFont',h=textHeight,al='right')
	mc.button(h=buttons_med,w=ui.rowWidth/4,l='PNG\n 16BIT',c=partial(delay,'mel.eval','("rcSetGlobals PNG")'))
	mc.button(h=buttons_med,w=ui.rowWidth/4,l='TIF \n 16Bit',c=partial(delay,'mel.eval','("rcSetGlobals TIF")'))
	mc.button(h=buttons_med,w=ui.rowWidth/4,l='EXR\n 32BIT',c=partial(delay,'mel.eval','("rcSetGlobals EXR")'))
	
	mc.text(l='Image\nPrefix:',w=35,font='tinyBoldLabelFont',h=textHeight,al='right')
	mc.button(h=buttons_med,w=ui.rowWidth/4,l='Layers',c=partial(delay,'mel.eval','("rcSetGlobals -layers")'))
	mc.button(h=buttons_med,w=ui.rowWidth/4,l='Passes',c=partial(delay,'mel.eval','("rcSetGlobals -passes")'))
	mc.button(h=buttons_med,w=ui.rowWidth/4,l='',c=partial(delay,'mel.eval','("rcSetGlobals ")'))
	
	mc.setParent('..')
	mc.setParent('..')

###############

def lambertset():#transparancy slider for toolbox
	num=mc.floatSliderGrp('lambertslider',q=1,value=1)
	mc.setAttr('lambert1.transparency',num,num,num,type='double3')
def btnScript(script,folder=''):
	if folder is not None: mel.eval('source "'+scriptsMEL.replace('\\','/')+folder+'/'+str(script)+'"')
	else: mel.eval('source "'+scriptsMEL.replace('\\','/')+str(script)+'"')
	mel.eval(str(script))
def btnSourcePy(file,command):
		import file
		reload (file)
		file.command

