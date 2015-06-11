import os
import sys
import subprocess
import rcTools.main as main
import rcTools.toolsPY.rcMaya2AE as AE
class write(main.scriptFile):
	def __init__(self,filePath):
		self.folder=filePath
		main.scriptFile.__init__(self,self.folder)
		#self.folder=os.path.join(main.sceneData().ws(),'data')
		#main.scriptFile.__init__(self,self.folder,'_AFXImport.jsx')
		
		##MOVE THIS TO CUSTOM 
		self.imageFolderName='_fromMaya'
		self.imageFolderIndex=self.imageFolderName+'Index'
		self.write('app.beginUndoGroup("rcCommand")')
		self.addFolder(self.imageFolderName)
		
	def _writeAppleScript(self,jsxFile,AELoc):#write Applescript to Execute Javascript
		script=main.scriptFile(os.path.join(main.userDirectory(),'runJSX.scpt'))
		script.write('set theFile to "%s"'%jsxFile)
		script.write('open for access theFile')
		script.write('set fileContents to (read theFile)')
		script.write('close access theFile')
		script.write('tell application "%s"'%AELoc)
		script.write('  DoScript fileContents')
		script.write('end tell')
		return script.fileName
	#####
	def addFolder(self,folderName):#Creates Folder and/or Variable of Location 
		folderIndex=folderName+'Index'
		self.write('//ADDFOLDER %s'%(folderName))
		self.write('var %s="";'%folderIndex)
		self.write('for(var i=1;i<=app.project.numItems;i++){')
		self.write('	var item=app.project.item(i);')
		self.write('	if   (item.name=="%s"){ %s = item;};'%(folderName,folderIndex))
		self.write('	}')
		self.write('if(%s==""){%s=app.project.items.addFolder("%s")};'%(folderIndex,folderIndex,folderName))	
		self.write(' ')
	def comp(self,sceneData):#COMP 
		self.write('//ADD COMP')
		self.write('var shotName="%s";'%sceneData.shotName())
		self.write('var width=%d;'%sceneData.frameWidth())
		self.write('var height=%d;'%sceneData.frameHeight())
		self.write('var fps=%d;'%sceneData.fps())
		self.write('var seconds=%s;'%sceneData.timelineSeconds())
		self.write(' ')
		self.write('var shotComp="";')
		self.write('for(var i=1;i<=app.project.numItems;i++){')
		self.write('	var item=app.project.item(i);')
		self.write('	if   (item.name==shotName){ shotComp = item;};')
		self.write('	}')
		self.write('if(shotComp==""){ shotComp=app.project.items.addComp(shotName,width,height,1,seconds,fps);}')
		
		self.write(' else {')
		self.write('		shotComp.name=shotName;')
		self.write('		shotComp.width=width;')
		self.write('		shotComp.height=height;')
		self.write('		shotComp.seconds=seconds;')
		self.write('		shotComp.fps=fps;')
		self.write('		}')
		self.write(' ')
		
	def layers(self,sceneData):#LAYERS
		if AE.aePrefs.get('ImageSource')=='images':
			minTimeName=str(sceneData.minTime()).zfill(sceneData.framePad())
			maxTimeName=str(sceneData.maxTime()).zfill(sceneData.framePad())
			images=sceneData.renderOutput()[1]
		else:#TMP Imagelocation
			minTimeName=str(str(int(mc.currentTime(q=True))).zfill(sceneData.framePad()))
			maxTimeName=str((str(mc.currentTime(q=True)+1)).zfill(sceneData.framePad()))
			images=sceneData.renderOutput()[1]
			images=[str(img.replace(sceneData.wsImagesFolder(),os.path.join(sceneData.wsImagesFolder(),'tmp'))) for img in images]
			images=[str(img.replace('0001',minTimeName)) for img in images]
		self.write('var layers=%s;'%sceneData.outputLayers())
		self.write('var images=%s;'%images)
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
		self.write('	if(File(images[layerIndex].replace(/\//gi,"\\\\")).exists){')
		self.write('	layerPH.replaceWithSequence(new File(images[layerIndex].replace(/\//gi,"\\\\")),true);')
		self.write('	layerPH.name=layers[layerIndex];')
		self.write('	}')
		self.write('}') 
		self.write(' ')		
	def nulls(self,nullObjects):#NULLS
		pass
	def retrieve(self,itemType):
		pass
	#########
	def run(self):#execute written jsx by commandline (writesApplescript for mac)
		#TODO check to see if endUNDO already exists (remove)
		#self.write('app.endUndoGroup()')
		if 'darwin' in sys.platform:
			command='open '+AE.aePrefs.get('AELoc').replace(' ','\ ') +'\n'+ 'osascript ' + self._writeAppleScript(self.fileName,os.path.basename(AE.aePrefs.get('AELoc')).split('.')[0])
			subprocess.Popen(command,shell=True)
		else:
			command=AE.aePrefs.get('AELoc') +' -r ' +self.fileName
			subprocess.Popen(command)
			

