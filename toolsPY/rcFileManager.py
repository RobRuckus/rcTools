import os 
import sys
import subprocess
import shutil
################
from functools import partial
def runMethod(method,string,*args): exec(method+string) #Delay Function
################
import maya.cmds as mc 
from rcTools.rcMaya import *
################
browselistWidth=250
targetlistWidth=370
row1=100
row2=20
fieldFont='boldLabelFont'
###############
ui=ui('FileMGR')
sceneData=sceneData()
def UI():
        rlmAttrs()
        images=os.path.join(mc.workspace(q=1,rd=1),"images",mc.getAttr("renderLayerManager.shotName"))
        if (mc.window('rcFileManage',exists=True)): mc.deleteUI('rcFileManage')
        mc.window('rcFileManage', mxb=0,title=' ',tlb=False,)

        ###Main
        mc.columnLayout('renderLayers2Files')#,bgc=[0.2,0.2,0.2] 
        mc.image(image=iconPath+'toptitle.png')
        mc.cmdScrollFieldReporter(clr=1,hf=0,w=700,h=80,bgc=[0,0,0])
        print '//rc.Tools'
	mc.setParent('..')

	mc.rowColumnLayout(numberOfColumns=3,columnWidth=[(1,row1),(2,row2),(3,480)])
	
	mc.text(al='right',font=ui.titleFont,label='  Image Prefix: ')
	mc.menuBarLayout()
	mc.menu(label='Shot Name/')
	mc.menuItem(label='<RenderLayer>/<RenderLayer>',c=partial(runMethod,'set.imagePrefix','("S__L__L")'))
	mc.menuItem(label='<RenderLayer>/<RenderLayer>.<RenderPass>',c=partial(runMethod,'set.imagePrefix','("S__L__L.P")'))
	mc.menuItem(label='<RenderLayer>/<RenderPass>/<RenderLayer>.<RenderPass>',c=partial(runMethod,'set.imagePrefix','("S__L__P__L.P")'))
	mc.menu(label='...')
	mc.menuItem(label='<RenderLayer>/<RenderLayer>',c=partial(runMethod,'set.imagePrefix','("L__L")'))
	mc.menuItem(label='<RenderLayer>/<RenderLayer>.<RenderPass>',c=partial(runMethod,'set.imagePrefix','("L__L.P")'))
	mc.menuItem(label='<RenderLayer>/<RenderPass>/<RenderLayer>.<RenderPass>',c=partial(runMethod,'set.imagePrefix','("L__P__L.P")'))
	mc.setParent('..')
	mc.textField('imageFilePrefix',font=ui.fieldFont,en=1,text=mc.getAttr('defaultRenderGlobals.imageFilePrefix'))    
	
	mc.setParent('..')
	mc.setParent('..')

	###ListsUI
	mc.rowColumnLayout('listLayout',numberOfColumns=3,columnWidth=[(1,102),(2,browselistWidth), (3, targetlistWidth)])#LISTS LAYOUT

	mc.columnLayout()
	mc.separator(h=10,style='in')
	
	mc.rowColumnLayout(numberOfColumns=2)
	mc.text('UNITS:  ',align='right',fn='tinyBoldLabelFont')
	mc.text(str(mc.currentUnit(query=True)),align='left',fn='tinyBoldLabelFont')
	mc.text('FPS:  ',align='right',fn='tinyBoldLabelFont')
	mc.text(str(sceneData.fps()),align='left',fn='tinyBoldLabelFont')
	mc.text('RENDER:  ',align='left',fn='tinyBoldLabelFont')
	mc.text(str(mc.getAttr('defaultResolution.width'))+'x'+str(mc.getAttr('defaultResolution.height')),align='left',fn='tinyBoldLabelFont')
	mc.setParent('..')
	mc.setParent('listLayout')
	bldBrowseList()
	mc.setParent('listLayout')
	bldTargetList('browser')
	mc.setParent('listLayout')
	mc.showWindow()	


###############
def l2fOutputFiles():
		l2fPrefix=''
		l2fFiles=[]
		if mc.objExists('renderLayerManager.shotName'):
			if mc.getAttr('renderLayerManager.enablePrefixRenderLayer'): l2fPrefix+= str(mc.getAttr('renderLayerManager.prefixRenderLayer'))+'.'
			if mc.getAttr('renderLayerManager.enableSingleFileName'): return [l2fPrefix+ str(mc.getAttr('renderLayerManager.singleFileName'))+'.mb']
			else:
				for each in sceneData.outputLayers() : l2fFiles.append(l2fPrefix+each+'.mb')
		return l2fFiles
def l2fOutputFolder():
		l2fOutput=''
		if mc.objExists('renderLayerManager.shotName'):
			shotName=mc.getAttr('renderLayerManager.shotName')
			if mc.getAttr('renderLayerManager.enableAbsoluteRenderFolder'): l2fOutput = str(mc.getAttr('renderLayerManager.absoluteRenderFolder')+'/')
			else: l2fOutput += str(mc.workspace(q=1,rd=1)) + 'scenes/' + str(mc.getAttr('renderLayerManager.shotName')) + '/render/'
			return l2fOutput


def strArchive(src,verStr='_old_v',add=1): #String Output for Custom suffix modification
        assert isinstance(add,int)
        assert isinstance(verStr,str) 
        if '.' in src: (filename,extension) = os.path.splitext(src)
        else: extension='';
        prefix = src.rsplit(verStr,1)[0] #verStr check
        dest = prefix
        suffix = int(src.rsplit(verStr,1)[1]) if len(src.rsplit(verStr,1))>1 else 0
        suffix = suffix + add
        if suffix>0: 
            dest = dest + verStr + '%0*d'%(2,suffix)
        if not str(extension)==None:
            return dest + str(extension)
        else: return dest 
###############
def toggleL2F(opt):
	if opt==True:
		mc.checkBox('EnableAbsRenderFolder',e=1,v=0)
		mc.textField('absoluteFolder',e=1,en=0)
		mc.symbolButton('absFolderButton',e=1,en=0)
	if opt==False:
		mc.checkBox('EnableAbsRenderFolder',e=1,v=1)
		mc.textField('absoluteFolder',e=1,en=1) 
		mc.symbolButton('absFolderButton',e=1,en=1)


def setImagePrefix():
	mc.setAttr('defaultRenderGlobals.imageFilePrefix',mc.textField('imageFilePrefix',q=1,text=1),type='string')
def commitUI():	
	mc.setAttr('renderLayerManager.enableAbsoluteRenderFolder',mc.checkBox('EnableAbsRenderFolder',q=1,v=1))
	#mc.setAttr('defaultRenderGlobals.imageFilePrefix',mc.textField('imageFilePrefix',q=1,text=1),type='string')
	#mc.setAttr('renderLayerManager.EnableImageFolder',mc.checkBox('EnableImageFolder',q=1,v=1))	
	mc.setAttr('renderLayerManager.enablePrefixRenderLayer',mc.checkBox('EnablePrefixName',q=1,v=1))
	mc.setAttr('renderLayerManager.prefixRenderLayer',mc.textField('Prefix',q=1,tx=1),type='string')		
	mc.setAttr("renderLayerManager.enableSingleFileName",mc.checkBox('EnableSingleFile',q=1,v=1))
	mc.setAttr('renderLayerManager.shotName',mc.textField('renderFolder',q=1,text=1),type='string')
	mc.setAttr('renderLayerManager.absoluteRenderFolder',mc.textField('absoluteFolder',q=1,text=1),type='string')
	mc.setAttr('renderLayerManager.singleFileName',mc.textField('singleFile',q=1,tx=1),type='string')
	#mc.setAttr('renderLayerManager.project',mc.textField('ProjectName',q=1,text=1),type='string')
	#mc.text('outputTEXT',e=1,font=fieldFont,l=l2fOutputFolder(),align='left')
	mc.optionMenu('browseOpt',e=1,sl=4)
	bldBrowseList_scroll(l2fOutputFolder())
	bldTargetList_column('browser')
	
	
	
###############
def bldBrowseList():#only on init
	mc.columnLayout('browser')
	mc.rowColumnLayout(numberOfColumns=4,w=browselistWidth)
	mc.button(l='     Explore     ',c=partial(runMethod,'btnSpawnBrowser','()'))
	mc.button(l=' ^ ',c=partial(runMethod,'bldBrowseList_nav','("up")'))
	mc.button(l=' v ',c=partial(runMethod,'bldBrowseList_nav','("down")'))
	mc.optionMenu('browseOpt',l='',cc=partial(runMethod,'bldBrowseList_opt','()'))#,cc=partial(runMethod,'list','(lister=\'browse\')'))
	mc.menuItem(l='Project')
	mc.menuItem(l='Scenes')
	mc.menuItem(l='Images')
	mc.menuItem(l='Layers2Files Output')
	mc.optionMenu('browseOpt',e=1,sl=2)#Default
	
	mc.setParent('..')
	bldBrowseList_scroll(os.path.join(sceneData.ws(),'scenes/'))#Default
def bldBrowseList_nav(opt):
	if opt=='up':
		bldBrowseList_scroll(mc.iconTextScrollList('browserlist',q=1,ann=1).rsplit('/',1)[0])
	if not mc.iconTextScrollList('browserlist',q=1,si=1)==None:
		if len (mc.iconTextScrollList('browserlist',q=1,si=1))==1:
			
			if opt=='down':
				bldBrowseList_scroll( os.path.join(str(mc.iconTextScrollList('browserlist',q=1,ann=1)),str(mc.iconTextScrollList('browserlist',q=1,si=1)[0])).replace('\\','/'))
def bldTargetList(source):#only on init
	mc.columnLayout('target')
	mc.rowColumnLayout(numberOfColumns=2)
	mc.optionMenu('targetOpt',l='  Procedure:',cc=partial(runMethod,'bldTargetList_column','("%s")'%source))
        mc.menuItem(l='Layers2Files')
        mc.menuItem(l='AfterEffects')
        mc.menuItem(l='Backup')
        mc.menuItem(l='Archive')
        mc.menuItem(l='Restore')
        mc.setParent('target')
        bldTargetList_column(source)
##############
def bldBrowseList_scroll(source):#init and refresh
	#Delete
	if mc.iconTextScrollList('browserlist',q=1,ex=1):mc.deleteUI('browserlist')
	#Build
	mc.iconTextScrollList('browserlist',parent='browser',ams=1,w=browselistWidth,h=600,ra=1,dcc=partial(runMethod,'bldBrowseList_dcc','()'),sc=partial(runMethod,'bldTargetList_column','("%s")'%('browser')))
	#Right-Click
	mc.popupMenu()
	mc.menuItem(l='Archive')
	mc.menuItem(l='Restore')
	try:
		files=[each for each in os.listdir(source) if os.path.isfile(os.path.join(source,each))]
		directories=[each for each in os.listdir(source) if os.path.isdir(os.path.join(source,each))]
	except:
		files=[];directories=[]
	#Decide
	if (files,directories)== ([],[]) : mc.iconTextScrollList('browserlist',e=1,ann=source)#Annotate if empty
	else:
		for index, each in enumerate(directories): mc.iconTextScrollList('browserlist',e=1,a=each,ann=source,itc=[index+1,.9,.5,0])
		for each in files: mc.iconTextScrollList('browserlist',ann=source,e=1,a=each)
	
def bldTargetList_column(source):#init and proc change
	apply_commitUI=partial(runMethod,'commitUI','()')
	mc.setParent('target')
	opt=mc.optionMenu('targetOpt',q=1,sl=1)
	#Delete
	if mc.columnLayout('targetColumn',q=1,ex=1):mc.deleteUI('targetColumn')
	#Build
	mc.columnLayout('targetColumn')
	#Decide
	if opt==1:
		mc.rowColumnLayout(numberOfColumns=3,columnWidth=[(1,55),(2,15),(3,275)])

		mc.setParent('..')
		mc.rowColumnLayout(numberOfColumns=4,columnWidth=[(1, 55),(2,15), (3, 275), (4, 25)])
		mc.text(al='right',font='tinyBoldLabelFont',label='Shot: ')
		mc.text('')
		mc.textField('renderFolder',font='tinyBoldLabelFont',text=mc.getAttr('renderLayerManager.shotName'),cc=apply_commitUI)#,en=mc.getAttr('renderLayerManager.EnableRenderFolder')
		mc.symbolButton('renderFolderButton',w=25,h=25,image=iconPath+'openFolder_30.png',c=partial(runMethod,'browse','(\'renderFolder\')'))#,en=mc.getAttr('renderLayerManager.EnableRenderFolder'),
		
		mc.text(al='right',font='tinyBoldLabelFont',label='Custom: ') 
		mc.checkBox('EnableAbsRenderFolder',l='',onc=partial(runMethod,'toggleL2F','(0)'),ofc=partial(runMethod,'toggleL2F','(1)'),v=mc.getAttr('renderLayerManager.enableAbsoluteRenderFolder'),cc=apply_commitUI)	
		mc.textField('absoluteFolder',font='tinyBoldLabelFont',en=mc.getAttr('renderLayerManager.enableAbsoluteRenderFolder'),text=mc.getAttr('renderLayerManager.absoluteRenderFolder'), h=15,cc=apply_commitUI)
		mc.symbolButton('absFolderButton',w=25,h=25,image=iconPath+'openFolder_30.png',en=mc.getAttr('renderLayerManager.enableAbsoluteRenderFolder'),c=partial(runMethod,'browse','(\'absoluteFolder\')'))
		mc.setParent('..')
		mc.rowColumnLayout('optList',numberOfColumns=3,columnWidth=[(1,55),(2,15),(3,275)])#,bgc=[0.105,0.105,0.105]
		mc.text(al='right',font='tinyBoldLabelFont',label='  Prefix: ')
		mc.checkBox('EnablePrefixName',l='',v=mc.getAttr('renderLayerManager.enablePrefixRenderLayer'),onc=partial(runMethod,'mc.textField','("Prefix",e=1,en=1)'),ofc=partial(runMethod,'mc.textField','("Prefix",e=1,en=0)'),cc=apply_commitUI)	
		mc.textField('Prefix',font=fieldFont,en=mc.getAttr('renderLayerManager.enablePrefixRenderLayer'),text=mc.getAttr('renderLayerManager.prefixRenderLayer'),cc=apply_commitUI)
		mc.text(al='right',font='tinyBoldLabelFont',label=' One File: ')
		mc.checkBox('EnableSingleFile',l='',v=mc.getAttr('renderLayerManager.enableSingleFileName'),onc=partial(runMethod,'mc.textField','("singleFile",e=1,en=1)'),ofc=partial(runMethod,'mc.textField','("singleFile",e=1,en=0)'),cc=apply_commitUI)
		mc.textField('singleFile',font='tinyBoldLabelFont',en=mc.getAttr('renderLayerManager.enableSingleFileName'),text=mc.getAttr('renderLayerManager.singleFileName'),cc=apply_commitUI)
		mc.setParent('..')
		bldTargetList_scroll(source)
	if opt==2:
		AE.UI()
	else:
		bldTargetList_scroll(source)

def bldTargetList_scroll(source):#init and refresh 
	opt=mc.optionMenu('targetOpt',q=1,sl=1)
	#Delete
	if mc.iconTextScrollList('targetlist',q=1,ex=1):mc.deleteUI('target'+'list')
	if mc.iconTextScrollList('targetObj',q=1,ex=1):mc.deleteUI('target'+'Obj')
	if mc.button('btnApply',q=1,ex=1): mc.deleteUI('btnApply')
	#Build
	mc.iconTextScrollList('targetlist',w=350,ams=1,ra=1)
	
	sel=mc.iconTextScrollList(source+'list',q=1,si=1)
	#Decide
	if opt==1:#Layers2Files
		for each in l2fOutputFiles():
			mc.iconTextScrollList('targetlist',e=1,a=each,en=0,ann=l2fOutputFolder())
	if opt==2:#Not Called!!
		for each in sceneData.outputLayers():
			mc.iconTextScrollList('targetlist',e=1,a=each,ann=l2fOutputFolder())
		mc.iconTextScrollList('targetObj',ams=1,ra=1)
	if not sel==None : 
		if opt==3:#Backup
			mc.iconTextScrollList('targetlist',e=1,a=backupFolder()+'/',itc=[1,.9,.5,0])
			for each in sel:
				mc.iconTextScrollList('targetlist',e=1,a='\t'+each)	
		if opt==4:#Archive
			for each in sel:
				mc.iconTextScrollList('targetlist',e=1,a=strArchive(src=each))
		if opt==5:#Restore
			for each in sel:
				mc.iconTextScrollList('targetlist',e=1,a=strArchive(src=each,add=(-1)))
	mc.button('btnApply',align='center',w=350,l='        ',bgc=[.9,.5,0],c=partial(runMethod,'btnApplyFm','()'))
def bldBrowseList_opt():#refresh Browse list only on 
	opt=mc.optionMenu('browseOpt',q=1,sl=1)
	if opt==1:
		bldBrowseList_scroll(sceneData.ws())
	if opt==2:
		bldBrowseList_scroll(os.path.join(sceneData.ws(),'scenes/'))	
	if opt==3:
		bldBrowseList_scroll(sceneData.ws())
	if opt==4:
		bldBrowseList_scroll(l2fOutputFolder())
	bldTargetList_column('browser')	
def bldBrowseList_dcc():
	print 'YES'
	pass
	#sel=mc.iconTextScrollList(self,q=1,si=1)
	#ui_list(self,parent,os.path.join(source,sel))
def btnApplyFm():
	sel=mc.iconTextScrollList('browserlist',q=1,si=1)
	selIndex=mc.iconTextScrollList('browserlist',q=1,sii=1)
	sourcedir=mc.iconTextScrollList('browserlist',q=1,ann=1)
	opt=mc.optionMenu('targetOpt',q=1,sl=1)
	sourceFiles=[]
	targetFiles=[]
	if opt==1:#Layers2Files
		exportL2F()
		#Change to output
		mc.optionMenu('browseOpt',e=1,sl=4)
		sourcedir=l2fOutputFolder()
	if opt==2:#AfterEffectsExport
		AE.btnExport()
	if not sel==None:
		for index,each in enumerate(sel) : sourceFiles.append(sourcedir+sel[index])
		if opt==3:#Backup
			if not os.path.exists(sourcedir+backupFolder()): os.makedirs(sourcedir+backupFolder())
			for index,each in enumerate(sel): targetFiles.append(sourcedir+backupFolder()+'/'+each)
			for index,each in enumerate(sourceFiles):
				if os.path.isfile(each): shutil.copyfile(sourceFiles[index],targetFiles[index])
				if os.path.isdir(each): shutil.copytree(sourceFiles[index],targetFiles[index])
		if opt==4:#Archive
			for index,each in enumerate(sel): targetFiles.append(sourcedir+ strArchive(sel[index]))
			for index,each in enumerate(targetFiles):
				try:
					os.rename(sourceFiles[index],targetFiles[index])
				except:
					pass
		if opt==5:#Archive
			for index,each in enumerate(sel): targetFiles.append(sourcedir+ strArchive(sel[index],add=-1))
			for index,each in enumerate(targetFiles):
				try: os.rename(sourceFiles[index],targetFiles[index])
				except: pass
	#Refresh
	bldBrowseList_scroll(sourcedir)
	bldTargetList_column('browser')
	if not selIndex== None :
		for each in selIndex :
			if opt==3: each+=1#account for added backed up folder 
			mc.iconTextScrollList('browserlist',e=1,sii=int(each))	
def btnSpawnBrowser(): spawnBrowser(mc.iconTextScrollList('browserlist',q=1,ann=1))
##############Procedures
def spawnBrowser(path):
    '''
    open the given folder in the default OS browser
    '''
    path=os.path.abspath(path)
    if sys.platform == 'win32':
        subprocess.Popen('explorer "%s"' % (path))
    elif sys.platform == 'darwin':  # macOS
        subprocess.Popen(['open', path])
    else:  # linux
        try:
            subprocess.Popen(['xdg-open', path])
        except OSError:
            raise OSError('unsupported xdg-open call??')
	

def exportL2F():#EXPORT RL 2 FILES
	#list ON LAYERS
	onlayers=[] 
	for each in getSceneData()['layers']:
		if mc.getAttr(str(each)+'.renderable'):
			if not ':' in each:
				onlayers.append(each)       
	fileNames=[]
	for each in l2fOutputFiles():
		fileNames.append(l2fOutputFolder()+each)
		
	#PROCEDURE
	if mc.getAttr('renderLayerManager.enableSingleFileName')==True:#IF SINGLE FILE OPTION 
		try:
			mc.file(os.path.normpath(fileNames[0]),ea=1,typ='mayaBinary')
		finally:
			print 'OUTPUT FILE:\n'+ os.path.normpath(fileNames[0])
	else:#MULTI FILE OPTION
		progress=1/len(onlayers)
		for each in onlayers: mc.setAttr(str(each)+'.renderable',0) #TURN OFF ON
		#MULTIPLE EXPORT
		mc.progressWindow(t='Saving..',min=0,max=len(onlayers),pr=progress,st='Copying\n'+onlayers[0])
		try:
			for index,each in enumerate(onlayers): #SEQUENTIALLY TURN ON, EXPORT, THEN TURN OFF
				mc.setAttr(str(each)+'.renderable',1)
				mc.file(os.path.normpath(fileNames[index]),ea=1,typ='mayaBinary')
				print 'OUTPUT FILE:'+ os.path.normpath(os.path.join(l2fOutputFolder()+each+'.mb'))
				progress=progress+1
				mc.progressWindow(e=1,pr=progress,st='Save Success \n'+ each)  
				mc.setAttr(str(each)+'.renderable',0)
		finally: mc.progressWindow(ep=1)        
		for each in onlayers: mc.setAttr(str(each)+'.renderable',1)#TURN BACK ON ONLAYERS
		

def browse(folder,*args):
	if folder=='renderFolder':
		mc.textField(str(folder),edit=1,text=mc.fileDialog2(ds=2,dir=os.path.join(mc.workspace(q=1,rd=1),'scenes'),fm=3,okc="Set",cc="Cancel")[0].split('/')[-1])  
	else: 
		mc.textField(str(folder),edit=1,text=mc.fileDialog2(ds=2,dir=os.path.join(mc.workspace(q=1,rd=1),'scenes'),fm=3,okc="Set",cc="Cancel")[0])
	commitUI()
	UI()
################
