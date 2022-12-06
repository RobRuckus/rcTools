"""
shutil copyfile

Author: Rob Coakley (robcoakley@gmail.com)
Copyright (C) 2017 Robert Coakley
http://robocolabo.com/blog/
Version: 0.1
Function:
try:
    reload(rcRoterra)
except:
    import rcRoterra
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
ui=rc.ui('Roterra')
class RoterraPrefs(iniFile):#RoterraPrefs
    def __init__(self):
        iniFile.__init__(self,os.path.join(userDirectory(),'rcFuri.ini').replace('\\','/'))
        if not os.path.isfile(self.fileName):#Defaults 
                file=open(self.fileName,'w')
                file.close()
                mc.confirmDialog(m='Set Path to Model Folder')
                self.path()
                self.write('Flag','1')
                self.write('Material','0')
                self.write('Object','1')
                self.write('IncludeNamespace','1')
                self.write('prefix','forest_')
                self.write('suffix','_material')
                self.write('importBehavior', 'reference')
                self.write('include',1)
                self.write('ExcludePrefixSuffix',0)
                #self.write('ImageLabel', 'Label3')	
    def path(self):#Write Obj List Location to pref File and Update UI
        self.importPath=mc.fileDialog2(fm=3,ds=1,okc='Set',cc='Cancel')[0]
        self.write('importPath',self.importPath)
    def checkBox(self,name):#Write checkBox Value
        self.write(name,int(mc.checkBox(name,q=1,v=1)))
    def menuItem(self,name):#Write menuItem Value
        self.write(name,int(mc.menuItem(name,q=1,cb=1)))
    def set(self,att,value):#Write Value
            self.write(att,value)
            #importListUI()
            #conformedListUI()
RoterraPrefs=RoterraPrefs()
def UI():
    
    ui.frameGRP('Roterra',cl=0)
    mc.rowColumnLayout('FURIROW',numberOfColumns=2,columnWidth=[(1,ui.rowWidth/2),(2,ui.rowWidth/2)])
    ui.frameSUB('CREATE');
    mc.rowColumnLayout(numberOfColumns=4)
    ui.iconButton(ann="Create 10x10 Tile",l= "Tile" ,i= "polyPlane.png",c=partial(delay,'mel.eval','("polyPlane -w 10 -h 10 -sx 10 -sy 10 -ax 0 1 0 -cuv 2 -ch 1")'))	
    ui.iconButton(ann="Create 1x1 Tile",l= "Tile" ,i= iconPath+"polyPlanenDiv.png",c=partial(delay,'mel.eval','("polyPlane -w 10 -h 10 -sx 1 -sy 1 -ax 0 1 0 -cuv 2 -ch 1;")'))
    ui.iconButton(i= "cube.png",c=partial(delay,'mel.eval','("polyCube -w 10 -h 10 -d 10 -sx 1 -sy 1 -sz 1 -ax 0 1 0 -cuv 2 -ch 1;")'))
    mc.setParent('FURIROW')

    ui.frameSUB('MODIFY');
    mc.rowColumnLayout(numberOfColumns=4)
    mc.iconTextButton(w=ui.iconSize,h=ui.iconSize)
    mc.iconTextButton(w=ui.iconSize,h=ui.iconSize)
    ui.iconButton(i= "rotateUVcw.png",c=partial(delay,'mel.eval','("polyRotateUVs 90 1")'))
    ui.iconButton(i= "DeleteHistory.png",c=partial(delay,'mel.eval','("DeleteHistory")')) 
    mc.setParent('FURIROW')
    mc.setParent('..')
    mc.rowColumnLayout(numberOfColumns=1)
    mc.menuBarLayout('conformmenu')
    mc.separator(h=5,style='in') 
    mc.menu('Options',l='Options')
    mc.menuItem('Material',l='Material',cb=int(RoterraPrefs.get('Material')),c=partial(delay,'RoterraPrefs.menuItem',"('Material')"))
    mc.menuItem('Flag',en=0,l='Flag',cb=int(RoterraPrefs.get('Flag')),c=partial(delay,'RoterraPrefs.menuItem',"('Flag')"))
    mc.menuItem('Object',en=0,l='Object',cb=int(RoterraPrefs.get('Flag')),c=partial(delay,'RoterraPrefs.menuItem',"('Object')"))
    mc.rowColumnLayout(w=ui.rowWidth,numberOfColumns=5)
    ui.iconButton(i= "fileNew.png",c=partial(delay,'planeFromTexture','()'))
    mc.button(w=ui.iconSize*2.5,h=ui.btn_small,al='left',l=' + ',c=partial(delay,'addObj','(mc.ls(sl=1))'))  #
    mc.button(w=ui.iconSize*2.5,h=ui.btn_small,al='center',l=' - ',c=partial(delay,'removeObj','("sel")')) 
    mc.button(w=ui.iconSize*2.5,h=ui.btn_small,al='right',l='NUKE',c=partial(delay,'removeObj','("all")'))
    mc.setParent('..')

    mc.iconTextScrollList('RoterraObjScroll',vis=1,w=ui.rowWidth,h=150)
    mc.setParent('FURIROW')
    mc.setParent('..')
    mc.setParent('..')

    ui.frameGRP('Materials',cl=1,pec=partial(delay,'materialListUI','("Materials")'))
    mc.menuBarLayout('materialmenu')
    mc.separator(h=5,style='in') 
    mc.menu(l='Options')
    mc.menuItem(d=True,l='Behavior')
    mc.menuItem('IncludeNamespace',l='Include Namespaced Materials',cb=int(RoterraPrefs.get('IncludeNamespace')),c=partial(delay,'RoterraPrefs.menuItem',"('IncludeNamespace')"))
    mc.menuItem('ExcludePrefixSuffix',l='Only Materials with Prefix and Suffix',cb=int(RoterraPrefs.get('ExcludePrefixSuffix')),c=partial(delay,'RoterraPrefs.menuItem',"('ExcludePrefixSuffix')"))
    mc.rowColumnLayout(numberOfColumns=4)
    mc.text('Prefix: ',align='left')
    mc.textField('prefix',tx='forest_',cc=partial(delay,'updateMaterials','()'))
    mc.text('Suffix: ',align='left')
    mc.textField('suffix',tx='_material',cc=partial(delay,'updateMaterials','()'))
    mc.setParent('..')

    mc.setParent('..')


    materialListUI('Materials')
    mc.setParent('..')
    ui.frameGRP('Objects',cl=1,pec=partial(delay,'importListUI','("Objects")'))
    mc.menuBarLayout('objmenu')
    mc.separator(h=5,style='in') 
    mc.menu(l='Options')
    mc.menuItem(d=True,l='Behavior')
    mc.radioMenuItemCollection()
    mc.menuItem('import',l='Import',rb=1,c=partial(delay,'RoterraPrefs.set',"('importBehavior','import')"))
    mc.menuItem('reference',l='Reference',rb=1,c=partial(delay,'RoterraPrefs.set',"('importBehavior','reference')"))
    mc.menuItem(RoterraPrefs.get('importBehavior'),e=1,rb=1)
    mc.menu('Path',l='Path')
    mc.menuItem(l='Set Path',c=partial(delay,'RoterraPrefs.path',"('')"))
    mc.menu(l='Repair Transparency',pmc=partial(delay,'rc.set.fileNode','()'))
    importListUI('Objects')
    updateMenu()
    # mc.scriptJob('toolBox.materialListUI()',event='SceneOpened')
def importListUI(parentFrame):#furiImportList
    location=RoterraPrefs.get('importPath')
    if mc.scrollLayout('importObjScroll',q=1,ex=1)==True: mc.deleteUI('importObjScroll')
    mc.setParent(parentFrame)
    mc.scrollLayout('importObjScroll',w=ui.rowWidth,h=600)
    # ui.fileList(location=RoterraPrefs.get('path'))
    for folder in rc.ls.dir(location):
        mc.frameLayout(l=folder,w=ui.rowWidth-10,cll=1,cl=1)#mc.text(l=folder+':',align='left')
        mc.columnLayout(w=ui.rowWidth)
        for item in sorted(rc.ls.dir(os.path.join(location,folder),folder=0)):
            file,ext=os.path.splitext(item)#split file and Extension 
            path= os.path.join(location,folder,item).replace('\\','/')
            if ext =='.fbx': 
                mc.button(w=ui.rowWidth,l=file,c=partial(delay,'inScene','("'+path+'","'+file+'")'))
        mc.setParent('..')
        mc.setParent('..')
def materialListUI(parentFrame):
    if mc.scrollLayout('materiallist',q=1,ex=1)==True: mc.deleteUI('materiallist')
    mc.setParent(parentFrame)
    mc.scrollLayout('materiallist',bgc=[0.1,0.1,0.1],w=ui.rowWidth-20,h=min(int(len(rc.ls.shaders()*30))+30,630))#h=len(ls.shaders())*25)

    prefix=RoterraPrefs.get('prefix')#mc.textField('prefix',q=1,tx=1)
    suffix=mc.textField('suffix',q=1,tx=1)
    mc.rowColumnLayout(w=ui.rowWidth,numberOfColumns=3)
    for each in sorted(rc.ls.shaders()):
        if int(RoterraPrefs.get('ExcludePrefixSuffix'))==1:
            if each.startswith(prefix) and each.endswith(suffix):
                sName=each
                if each.endswith(suffix): 
                    sName=each[:-len(suffix)]
                if each.startswith(prefix):
                    sName=sName[len(prefix):]
                mc.button(w=15,l='?',bgc=[0.5,0.5,0.5],c=partial(delay,'mc.hyperShade','(objects=\''+ str(each)+'\')'))#rc.ls.shaderColor(each)[0],   
                mc.button(w=ui.rowWidth-65,bgc=[0.1,0.1,0.1],l=sName.split(':')[-1],c=partial(delay,'mc.select','(\''+ str(each)+'\')'))
                mc.button(w=55,l='ASSIGN',bgc=[0.1,0.3,0.1],c=partial(delay,'mc.hyperShade','(assign=\''+ str(each)+'\')'))#rc.ls.shaderColor(each)[0],
        else:
            sName=each
            if each.endswith(suffix): 
                sName=each[:-len(suffix)]
            if each.startswith(prefix):
                sName=sName[len(prefix):]
            mc.button(w=15,l='?',bgc=[0.5,0.5,0.5],c=partial(delay,'mc.hyperShade','(objects=\''+ str(each)+'\')'))#rc.ls.shaderColor(each)[0],   
            mc.button(w=ui.rowWidth-65,bgc=[0.1,0.1,0.1],l=sName.split(':')[-1],c=partial(delay,'mc.select','(\''+ str(each)+'\')'))
            mc.button(w=45,l='ASSIGN',bgc=[0.1,0.3,0.1],c=partial(delay,'mc.hyperShade','(assign=\''+ str(each)+'\')'))#rc.ls.shaderColor(each)[0],

            #mc.text(sName.split(':'),al='left')
            #mc.button(w=40,l='GRAPH')   
    mc.setParent('..');mc.setParent('..') 
def updateMaterials():
    RoterraPrefs.write('prefix',mc.textField('prefix',q=1,tx=1))
    RoterraPrefs.write('suffix',mc.textField('suffix',q=1,tx=1))
    materialListUI('Materials')
def updateMenu():#UPDATE
    
    mc.menu('Path',e=True,dai=True)
    mc.menuItem(p='Path',d=True,dl='Folder')
    #for each in sceneData.outputImages():
        #mc.menuItem(each,l=each,itl=True,c=partial(delay,'spawnBrowser','("%s")'%os.path.dirname(each)))
    #mc.menuItem(l='Set Path Presets',c=partial(delay,'rc.set.globals','()'))
    #mc.menuItem(d=True,dl='Path')
    #mc.menuItem('Image Output',l=RoterraPrefs.get('importPath'),itl=True,en=0)
    mc.menuItem(p='Path',l='Set Path',c=partial(delay,'RoterraPrefs.path','()'))
    mc.setParent('..')	
def inScene(fileLocation,folder=''):
    if RoterraPrefs.get('importBehavior')=='import':
        behavior='i=1'
    else:
        behavior='r=1'
    if folder is not None: 
            obj=mc.file(fileLocation,r=1,shd=["displayLayers","shadingNetworks"],ignoreVersion=0,gl=1,mergeNamespacesOnClash=0,namespace='')
            #mel.eval ('file '+behavior+' -ignoreVersion -gl -mergeNamespacesOnClash false -namespace "" "'+fileLocation+'"')
            print ('object=',obj)
    else: print ('source "'+scriptsMEL+str(script)+'"')
def conformedListUI():#furiItemList
    mc.iconTextScrollList('RoterraObjScroll',e=1,ams=1,ra=1)
    mc.popupMenu('menuObj',p='RoterraObjScroll')
    mc.menuItem('Rename Material',l='Rename Material',c=partial(delay,'aePrefs.write',"('Behavior','New')"))
    mc.menuItem('Pivot Conform',l='Pivot Conform',c=partial(delay,'aePrefs.write',"('Behavior','New')"))
    index=0
    for each in mc.ls():
        if mc.objExists(each+'.RoterraFlag'):
            fileColor=[index+1,1,0,0]
            if checkConform(each) :
                 fileColor=[index+1,0,1,0] 
            index=index+1
            mc.iconTextScrollList('RoterraObjScroll',e=1,a=each.rsplit('_mesh')[0],itc=fileColor,sc=tagListCallBack)
def tagListCallBack():
    sel=[]
    try:
        [sel.append(each+'_mesh') for each in mc.iconTextScrollList('RoterraObjScroll',q=1,si=1) if mc.iconTextScrollList('RoterraObjScroll',q=1,si=1) ]
    except:
        pass
    if sel: 
        if sel=='_mesh':
            pass
        else:
            mc.select(sel)

def addObj(sel):
    for each in sel:
        if int(RoterraPrefs.get('Material'))==1:
            material=conformMat(each.rsplit('_mesh')[0]+'_material')
            mc.select(each)
            mc.hyperShade(assign=material)

        mc.select(each)
        tagRoterraFlag(each)
    conformedListUI()
def removeObj(opt): #deletes all sets and locators
    if opt=='all':
        for each in mc.ls():
            if mc.objExists(each+'.RoterraFlag'): mc.deleteAttr(each+'.RoterraFlag')
    if opt=='sel':
        for each in mc.ls(sl=1):
            if mc.objExists(each+'.RoterraFlag'): mc.deleteAttr(each+'.RoterraFlag')
    conformedListUI()
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
def tagRoterraFlag(sel):
    if not mc.objExists(sel+'.RoterraFlag') : 
        mc.addAttr(sel,ln='RoterraFlag',dt='string')		
    mc.setAttr(sel+'.RoterraFlag',sel.rstrip('_mesh'),type='string')
def checkConform(sel):
    conform=1
    objWS=mc.xform(sel,q=1,sp=1)
    for each in objWS:
        if each :
            conform=0
    return conform  
def conform(sel):#Roterra obj naming : *_mesh on mesh, *_material on material, auto link file nodes *_color and *_spec
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
def copyAmt(x,y,z):
    obj=mc.duplicate(rr=1)
    mc.move(x,y,z,obj,r=1)
    for each in range(0,mc.intField('AmtField',q=1,v=1)-1):
        mc.duplicate(rr=1,st=1)
def fileNode(name,outAttr):
    if outAttr == 'spec' : connectedAttr = 'specularColor'
    else: connectedAttr = outAttr
    obj=name.rsplit('_material')[0]+'_file_' + outAttr   
    if not mc.objExists(obj):
        print ('obj doesnt exist')
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
            else: print (textureFile + ' Already Connected')
       
#################
if __name__== 'rcRoterra' :
    ui.win()
    ui.toolBox()
    ui.tab('Roterra')
    UI()
