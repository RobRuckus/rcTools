import shutil
import os
from rcTools import main 
from rcTools.toolsPY import rcMaya2AE as AE 

#Copy ALL scripts from rcTools to Ae Application Scripts Folder 
def scripts():
	try:
		for each in os.listdir(
	
	#for each in os.listdir(os.path.join(AE.aePrefs.get('AELoc'),'../','Scripts')):
		print each 
	for each in os.listdir(main.toolsJSX):
		print os.path.join(main.toolsJSX,each)
	#try:
		#if os.path.isfile(each): shutil.copyfile(sourceFiles[index],targetFiles[index])
		#if os.path.isdir(each): shutil.copytree(sourceFiles[index],targetFiles[index])
	#Copy ALL SCRIPTS 

