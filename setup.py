import shutil
import os
from rcTools import main 
from rcTools.toolsPY import rcMaya2AE as AE 

def copytree(src, dst, symlinks=False, ignore=None):
	'''
	reimplementation of copytree to copy when changed, and merge when folder exists
	'''
	if not os.path.exists(dst): os.makedirs(dst)
	for item in os.listdir(src):
		s = os.path.join(src, item)
		d = os.path.join(dst, item)
		if os.path.isdir(s): copytree(s, d, symlinks, ignore)
		else:
			if not os.path.exists(d) or os.stat(src).st_mtime - os.stat(dst).st_mtime > 1: shutil.copy2(s, d) 
			
def copy(source,target):
	'''
	Copy Files and Folders 
	'''
	for each in os.listdir(source):
		sourceItem=os.path.join(source,each)
		targetItem=os.path.join(target,each)
		if os.path.isfile(sourceItem): shutil.copyfile(sourceItem,targetItem)
		if os.path.isdir(sourceItem): copytree(sourceItem,targetItem)

def AFX():
	'''
	Setup User Prefs and Scripts in After Effects 
	
	'''
	#copy personal scripts
	source=main.toolsJSX
	target=os.path.join(AE.aePrefs.get('AELoc'),'../','Scripts')
	copy (source,target)
	
	#copy 3rd Party 
	#source=os.path.join(main.userDirect(),'Google Drive','scripts','scriptsJSX')
	#target=os.path.join(AE.aePrefs.get('AELoc'),'../','Scripts')
	#copy (source,target)
	
def MAYA():
	'''
	Setup Maya Scripts 
	'''
	# copy 3rd Party Python and MEL scripts 
	
	pass
def remove():
	pass
	
