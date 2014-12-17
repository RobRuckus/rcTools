####IMPORT
import os 
import sys
from datetime import datetime
import ctypes
###########PATH VARIABLES
importPath= os.path.dirname(__file__)
iconPath=os.path.join(importPath,'icons','')
toolsPY=os.path.join(importPath,'toolsPY','')
toolsMEL=os.path.join(importPath,'toolsMEL','')
toolsJSX=os.path.join(importPath,'toolsJSX','')
scriptsMEL=os.path.join(importPath,'scriptsMEL','')
scriptsPY=os.path.join(importPath,'scriptsPY','')
##########
def nameConvert(string):#Convert Node Names with | to _ 
	string=string.replace('|','_')
	if string.startswith('_'): return string[1:]
	else: return string
def backupFolder(): return str(datetime.now()).replace('-','.').replace(' ','-').replace(':','.')
def userDirectory():#IN usersetup.py for Maya RETURN USERDIRECTORY FOR MAC/WIN
	if 'darwin' in sys.platform:
		userDirectory=os.environ['HOME']
	else:
		userDirectory=os.environ['USERPROFILE']
	return userDirectory
def scriptsDrive(folder=None):
	if folder: return os.path.join(main.userDirectory(),'Google Drive','scripts',folder,'')
	else: return os.path.join(main.userDirectory(),'Google Drive','scripts','')
####################	
class scriptFile():#Creates/Writes Files Line by Line
    def __init__(self,fileName):
        self.fileName= fileName.replace('\\','/')
        #self.fileName= os.path.join(path,fileName).replace('\\','/')
        #if not os.path.os.path.dirname(self.fileName)
        file=open(self.fileName,'w')
        file.close() 
    def write(self,line):
		file=open(self.fileName,'a')
		file.write('%s\n'%line)
		file.close()	
class iniFile():#CRUD iniFiles
    def __init__(self,fileName):
        self.fileName=fileName
    def read(self):#Reads Contents of File
        with open(self.fileName,'r') as f:
            content=[w.replace('\n','') for w in f.readlines()]
        return content
    def get(self,att):
        for each in self.read():
            if att in each:
                return each.replace(att+'= ','')
        return None
    def write(self,att,value):
        if self.get(att)==None:
            file=open(self.fileName,'a')
            file.write('%s= %s\n'%(att,str(value)))
            file.close()
        else:
            contents=self.read()
            file=open(self.fileName,'w')
            for each in contents:
                if att in each:
                    each=r'%s= %s'%(att,str(value))
                file.write('%s\n'%each)
            file.close()

