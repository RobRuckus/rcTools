import shutil
import os

from rcTools import main 
from rcTools.toolsPY import rcMaya2AE as AE 

def _copyTree(src, dst, symlinks=False, ignore=None):
	'''
	reimplementation of copytree to copy when changed, and merge when folder exists
	'''
	if not os.path.exists(dst): os.makedirs(dst)
	for item in os.listdir(src):
		s = os.path.join(src, item)
		d = os.path.join(dst, item)
		if os.path.isdir(s): _copyTree(s, d, symlinks, ignore)
		else:
			if not os.path.exists(d) or os.stat(src).st_mtime - os.stat(dst).st_mtime > 1: shutil.copy2(s, d) 
			
def _copy(source,target):
	'''
	Copy Files and Folders 
	'''
	for each in os.listdir(source):
		sourceItem=os.path.join(source,each)
		targetItem=os.path.join(target,each)
		if os.path.isfile(sourceItem): shutil.copyfile(sourceItem,targetItem)
		if os.path.isdir(sourceItem): _copyTree(sourceItem,targetItem)

##Procedures	
def AFX():
	'''
	Setup User Prefs and Scripts in After Effects 
	
	'''
	#copy personal scripts
	source=main.toolsJSX
	target=os.path.join(AE.aePrefs.get('AELoc'),'../','Scripts')
	_copy (source,target)
	
	#copy 3rd Party 
	source=os.path.join(main.userDirectory(),'Google Drive','scripts','scriptsJSX')
	_copy (source,target)
	
def MAYA():
	'''
	Setup Maya Scripts 

	'''
	# copy 3rd Party Python and MEL scripts to GIT/rcTools
	# copy plugins from GDrive to plugins path of Maya
	
	pass
def remove():
	pass
