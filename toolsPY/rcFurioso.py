"""
shutil copyfile

Author: Rob Coakley (robcoakley@gmail.com)
Copyright (C) 2017 Robert Coakley
http://robocolabo.com/blog/
Version: 0.1
Function:
try:
	reload(rcFurioso)
except:
	import rcFurioso
"""
###########
import subprocess
import os
import maya.cmds as mc
import maya.mel as mel
import rcTools.rcMaya as rc
from rcTools.main import *
###########
from functools import partial
def delay(method,string,*args): exec(method+string) #Button Delay Function
###########
#UI VARIABLES FROM MAIN
ui=rc.ui('Furioso')
class furiosoPrefs(iniFile):#aePrefs.ini 
	def __init__(self):
		iniFile.__init__(self,os.path.join(userDirectory(),'rcFurioso.ini').replace('\\','/'))
		if not os.path.isfile(self.fileName):#Defaults 
				file=open(self.fileName,'w')
				file.close()
				mc.confirmDialog(m='Set Path to Model Folder')
				self.path()
				self.write('Flag','1')
				self.write('Material','0')
				self.write('Object','1')
				#self.write('Behavior','Replace')
				self.write('importBehavior', 'reference')
				#self.write('ImageLabel', 'Label3')
	def path(self):#Write Ae Location to pref File and Update UI
		self.importPath=mc.fileDialog2(fm=3,ds=1,okc='Set',cc='Cancel')[0]
		self.write('importPath',self.importPath)
	def checkBox(self,name):#Write checkBox Value
		self.write(name,int(mc.checkBox(name,q=1,v=1)))
	def set(self,att,value):#Write Value
    		self.write(att,value)
    		buildUILists()
furiosoPrefs=furiosoPrefs()

def UI():
    #ui.frame('FURIOSO',bgc=(.2,.2,.2))
    mc.menuBarLayout(w=ui.rowWidth)
    mc.separator(h=5,style='in') 
    mc.menu(l='Options')
    mc.menuItem(d=True,l='Behavior')
    mc.radioMenuItemCollection()
    mc.menuItem('Import',l='Import',rb=1,c=partial(delay,'furiosoPrefs.set',"('importBehavior','import')"))
    mc.menuItem('Reference',l='Reference',rb=1,c=partial(delay,'furiosoPrefs.set',"('importBehavior','reference')"))
    mc.menu('Path',l='Path')
    mc.menuItem(d=True,l=furiosoPrefs.get('importPath'))
	#mc.menuItem(aePrefs.get('ImageSource'),e=1,rb=1)
	#mc.frameLayout('Furioso',w=ui.rowWidth,cll=1,bgc=[.2,.2,.2],fn='smallBoldLabelFont',bs='in',l='Furioso')
    mc.rowColumnLayout('FURIROW',numberOfColumns=2,columnWidth=[(1,ui.rowWidth/2),(2,ui.rowWidth/2)])
    mc.columnLayout('furiosoObjectConform',cal='center',w=ui.rowWidth-10)
    mc.frameLayout('CREATE',cll=0,bgc=[.0,.0,.0]);
    mc.rowColumnLayout(numberOfColumns=4)
    mc.iconTextButton(w=ui.iconSize,h=ui.iconSize,i= "fileNew.png",c=partial(delay,'planeFromTexture','()'))
    mc.iconTextButton(w=ui.iconSize,h=ui.iconSize,ann="Create 10x10 Tile",l= "Tile" ,i= "polyPlane.png",c=partial(delay,'mel.eval','("polyPlane -w 10 -h 10 -sx 10 -sy 10 -ax 0 1 0 -cuv 2 -ch 1")'))	
    mc.iconTextButton(w=ui.iconSize,h=ui.iconSize,ann="Create 1x1 Tile",l= "Tile" ,i= iconPath+"polyPlanenDiv.png",c=partial(delay,'mel.eval','("polyPlane -w 10 -h 10 -sx 1 -sy 1 -ax 0 1 0 -cuv 2 -ch 1;")'))
    mc.iconTextButton(w=ui.iconSize,h=ui.iconSize,i= "cube.png",c=partial(delay,'mel.eval','("polyCube -w 10 -h 10 -d 10 -sx 1 -sy 1 -sz 1 -ax 0 1 0 -cuv 2 -ch 1;")'))
    mc.setParent('..')
    mc.setParent('..')
    mc.frameLayout('SCENE- J to snap',cll=0,bgc=[.0,.0,.0]);
    mc.rowColumnLayout(numberOfColumns=4)
    mc.iconTextButton(w=ui.iconSize,h=ui.iconSize,i= "polyQuad",c=partial(delay,'mel.eval','("TogglePolyCount")'))
    mc.iconTextButton(w=ui.iconSize,h=ui.iconSize,ann="Set Camera to Meters",en=1,l= "Set Camera" ,i= "CameraAE.png",c=partial(delay,'mel.eval','("rcSetCameraClip .5 100000")'))
    mc.iconTextCheckBox(w=ui.iconSize,h=ui.iconSize,ann="Snap",l= "Tile" ,i= "snapGrid.png",onc=partial(delay,'rc.stepSnap','(5,1)'),ofc=partial(delay,'rc.stepSnap','(5,0)'))
    mc.iconTextCheckBox(w=ui.iconSize,h=ui.iconSize,ann="Rotate",l= "Tile" ,i= "rotate_M.png",onc=partial(delay,'rc.rotSnap','(45,1)'),ofc=partial(delay,'rc.rotSnap','(45,0)'))
    mc.setParent('..')
    mc.setParent('..')
    mc.setParent('..')
    mc.frameLayout('CONFORM',cll=0,bgc=[.0,.0,.0]);
    mc.rowColumnLayout(numberOfColumns=4)
    mc.button(w=ui.rowWidth/6,h=ui.btn_large,al='left',l=' + ',c=partial(delay,'btnPlus','(mc.ls(sl=1))'))  #
    mc.button(h=ui.btn_large,w=ui.rowWidth/6,al='center',l=' - ',c=partial(delay,'btnDel','("sel")')) 
    mc.button(h=ui.btn_large,w=ui.rowWidth/6,al='right',l='NUKE',c=partial(delay,'btnDel','("all")'))
    mc.setParent('..')
    mc.setParent('..')
    mc.frameLayout('MODIFY',cll=0,bgc=[.0,.0,.0]);
    mc.rowColumnLayout(numberOfColumns=4)
    mc.iconTextButton(w=ui.iconSize,h=ui.iconSize,i= "rotateUVcw.png",c=partial(delay,'mel.eval','("polyRotateUVs 90 1")'))
    mc.iconTextButton(w=ui.iconSize,h=ui.iconSize,i= "historyPulldownIcon.png",bgc=[.5,0,0],c=partial(delay,'mel.eval','("DeleteHistory")'))
    mc.setParent('..')
    mc.checkBox('Object',vis=0,l='Object',v=int(furiosoPrefs.get('Object')),cc=partial(delay,'furiosoPrefs.checkBox',"('Object')"))
    mc.checkBox('Material',l='Material',vis=1,v=int(furiosoPrefs.get('Material')),cc=partial(delay,'furiosoPrefs.checkBox',"('Material')"))
    mc.checkBox('Flag',l='Flag',vis=0,v=int(furiosoPrefs.get('Flag')),cc=partial(delay,'furiosoPrefs.checkBox',"('Flag')"))
    mc.iconTextScrollList('FuriosoObjScroll',vis=0,w=ui.rowWidth,h=150)
    mc.setParent('furiosoObjectConform')
    mc.setParent('..')
    mc.setParent('..')
    mc.frameLayout('frame_furiMAT',w=ui.rowWidth,l='Materials',bgc=[0.2,.2,.2],cc=partial(delay,'buildUIMats','("frame_furiMAT")'),cll=1)
    buildUIMats('frame_furiMAT')
    mc.setParent('..')
    filesUI()
    buildUILists()
    updateMenu()
	#mc.scriptJob('import rcFurioso',event=SceneOpened)
def filesUI(location=furiosoPrefs.get('importPath')):#furiImportList
    mc.frameLayout('frame_furiOBj',w=ui.rowWidth,l='Objects',bgc=[0.2,.2,.2],cc=partial(delay,'buildUIMats','("frame_furiMAT")'),cll=1)
    mc.scrollLayout(w=ui.rowWidth,h=600)
    for folder in rc.ls.dir(location):
		mc.frameLayout(l=folder,w=ui.rowWidth-10,cll=1,cl=1)#mc.text(l=folder+':',align='left')
		mc.columnLayout(w=ui.rowWidth)
		for item in sorted(rc.ls.dir(os.path.join(location,folder),folder=0)):
			file,ext=os.path.splitext(item)#split file and Extension 
			path= os.path.join(location,folder,item).replace('\\','/')
			if ext =='.fbx': 
				mc.button(w=ui.rowWidth,l=file,c=partial(delay,'btnScript','("'+path+'","'+folder+'")'))
		mc.setParent('..')
		mc.setParent('..')
def btnScript(fileLocation,folder=''):
	if folder is not None: mel.eval ('file -r -ignoreVersion -gl -mergeNamespacesOnClash false -namespace "" "'+fileLocation+'"')
	else: print ('source "'+scriptsMEL+str(script)+'"')
	#mel.eval(str(script))
def buildUIMats(parentFrame):
	if mc.scrollLayout('materiallist',q=1,ex=1)==True: mc.deleteUI('materiallist')
	mc.setParent(parentFrame)
	mc.scrollLayout('materiallist',bgc=[0.1,0.1,0.1],w=ui.rowWidth,h=min(int(len(rc.ls.shaders()*30))+15,630))#h=len(ls.shaders())*25)
	mc.rowColumnLayout(w=ui.rowWidth-20,numberOfColumns=2)
	for each in sorted(rc.ls.shaders()):
	    sName=each
	    if each.endswith('_material'): 
	        sName=each[:-8] 
		mc.button(w=ui.rowWidth-65,al='right',bgc=[0.1,0.1,0.1],l=each,c=partial(delay,'mc.select','(\''+ str(each)+'\')'))
		mc.button(w=45,l='ASSIGN',bgc=[0.1,0.1,0.1],c=partial(delay,'mc.hyperShade','(assign=\''+ str(each)+'\')'))#rc.ls.shaderColor(each)[0],
		#mc.button(w=40,l='GRAPH')   
	mc.setParent('..');mc.setParent('..') 
def updateMenu():#UPDATE
	
	mc.menu('Path',e=True,dai=True)
	#mc.menuItem(d=True,dl='Maya Render Images')
	#for each in sceneData.outputImages():
		#mc.menuItem(each,l=each,itl=True,c=partial(delay,'spawnBrowser','("%s")'%os.path.dirname(each)))
	#mc.menuItem(l='Set Path Presets',c=partial(delay,'rc.set.globals','()'))
	#mc.menuItem(d=True,dl='Path')
	#mc.menuItem('Image Output',l=furiosoPrefs.get('importPath'),itl=True,en=0)
	mc.menuItem(l='Set Path',c=partial(delay,'furiosoPrefs.path','()'))
	mc.setParent('..')
	
def buildUILists():#furiItemList
	mc.iconTextScrollList('FuriosoObjScroll',e=1,ams=1,ra=1)
	mc.popupMenu('menuObj',p='FuriosoObjScroll')
	mc.menuItem('Rename Material',l='Rename Material',c=partial(delay,'aePrefs.write',"('Behavior','New')"))
	mc.menuItem('Pivot Conform',l='Pivot Conform',c=partial(delay,'aePrefs.write',"('Behavior','New')"))
	index=0
	for each in mc.ls():
		if mc.objExists(each+'.FuriosoFlag'):
		    fileColor=[index+1,1,0,0]
		    if checkConform(each) :
		         fileColor=[index+1,0,1,0] 
		    index=index+1
		    mc.iconTextScrollList('FuriosoObjScroll',e=1,a=each.rsplit('_mesh')[0],itc=fileColor,sc=tagListCallBack)
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

def btnPlus(sel):
	for each in sel:
	    obj=conformObj(each)
	    if int(furiosoPrefs.get('Material'))==1:
	        print 'yes'
	        material=conformMat(obj.rsplit('_mesh')[0]+'_material')
	        mc.select(obj)
	        mc.hyperShade(assign=material)

	    mc.select(obj)
	    tagFuriosoFlag(obj)
	buildUILists()
def btnDel(opt): #deletes all sets and locators
	if opt=='all':
		for each in mc.ls():
			if mc.objExists(each+'.FuriosoFlag'): mc.deleteAttr(each+'.FuriosoFlag')
	if opt=='sel':
		for each in mc.ls(sl=1):
			if mc.objExists(each+'.FuriosoFlag'): mc.deleteAttr(each+'.FuriosoFlag')
	buildUILists()
################
def prompt(initial):
    prompt=mc.promptDialog(t="Conform",m="Name:                                     ",tx=initial,button="Go")
    if prompt=='dismiss': sys.exit()
    objName= mc.promptDialog(q=1,t=1)
    return objName
    
def planeFromTexture():
  selfile=browse()
  split=(selfile.split('/')[-1:])[0][:-len("_color.png")]
  plane=mel.eval("polyPlane -w 10 -h 10 -sx 1 -sy 1 -ax 0 1 0 -cuv 2 -ch 1;")
  meshName=mc.rename(plane[0],split+'_mesh')
  if not meshName==split+'_mesh':
        mc.rename(split+'_mesh',split+'_mesh'+'_old')
        mc.rename(plane,split+'_mesh')
        mc.confirmDialog(b='Ok',m='Existing Objects Renamed '+split+'_old')
  #conformObj(meshName)
  material=conformMat(meshName.rsplit('_mesh')[0]+'_material')
  mc.select(meshName)
  mc.hyperShade(assign=material)
  #print 'selfie='+ selfile
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
def prefabName(fileName,suffix):
    return (filename.split('/')[-1:])[0][:-len("_color.png")]
def conformObj(sel):
    mc.select(sel)
    #prompt=mc.promptDialog(t="Conform",m="Name:                                     ",tx=sel.rsplit('_mesh')[0],button="Go")
    #if prompt=='dismiss': sys.exit()
    objName= prompt(sel.rsplit('_mesh')[0])
    mesh= mc.rename(sel,objName+'_mesh')
    if not mesh==objName+'_mesh':
        mc.rename(objName+'_mesh',objName+'_mesh'+'_old')
        mc.rename(mesh,objName+'_mesh')
        mc.confirmDialog(b='Ok',m='Existing Objects Renamed '+objName+'_old') 
    return objName+'_mesh'
def conformMat(name):
        if not mc.objExists(name): 
            mc.shadingNode('blinn',name=name,asShader=1)
            fileNode(name,'color')
            fileNode(name,'spec')
        else:
            mc.confirmDialog(b='Ok',m=name+ ' Already Exists')
        return name
def tagFuriosoFlag(sel):
	if not mc.objExists(sel+'.FuriosoFlag') : 
	    mc.addAttr(sel,ln='FuriosoFlag',dt='string')		
	mc.setAttr(sel+'.FuriosoFlag',sel.rstrip('_mesh'),type='string')
def checkConform(sel):
    conform=1
    objWS=mc.xform(sel,q=1,sp=1)
    for each in objWS:
        if each :
            conform=0
    return conform  
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
        mc.rename(mesh,objName+'_mesh')
        mc.confirmDialog(b='Ok',m='Existing Objects Renamed '+objName+'_old')      
    conformMat(objName+'_material')
    selObj=objName+'_mesh'
    mc.select(selObj)
    mc.hyperShade(assign=material)
    return selObj

def fileNode(name,outAttr):
    if outAttr == 'spec' : connectedAttr = 'specularColor'
    else: connectedAttr = outAttr
    obj=name.rsplit('_material')[0]+'_file_' + outAttr   
    if not mc.objExists(obj):
        print 'obj doesnt exist'
        image=mc.shadingNode('file',asTexture=True,name=obj)
        mc.setAttr(image+'.fileTextureName','sourceimages/'+name.rsplit('_material')[0]+'_'+outAttr+'.png',type='string')
        mc.connectAttr(image+'.outColor',name+'.'+connectedAttr)
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
       
#################
if __name__== 'rcFurioso' :
	ui.win()
	UI()
