##########IMPORT
import os 
import sys
import subprocess
from datetime import datetime
import ctypes
#########PATH VARIABLES
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
def scriptsDrive(folder=None):#Google Drive Scripts Folder Location
	if folder: return os.path.join(main.userDirectory(),'Google Drive','scripts',folder,'')
	else: return os.path.join(main.userDirectory(),'Google Drive','scripts','')
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
	


####################	
class scriptFile():#Creates/Writes Files Line by Line
    def __init__(self,fileName):
        self.fileName= fileName.replace('\\','/')
        file=open(self.fileName,'w')
        file.close() 
    def write(self,line):
		file=open(self.fileName,'a')
		file.write('%s\n'%line)
		file.close()	
class iniFile():#CRUD iniFiles
    def __init__(self,fileName):
        self.fileName=fileName
    def _read(self):#Reads Contents of File
        with open(self.fileName,'r') as f:
            content=[w.replace('\n','') for w in f.readlines()]
        return content
    def get(self,att):
        for each in self._read():
            if att in each:
                return each.replace(att+'= ','')
        return None
    def write(self,att,value):
        if self.get(att)==None:
            file=open(self.fileName,'a')
            file.write('%s= %s\n'%(att,str(value)))
            file.close()
        else:
            contents=self._read()
            file=open(self.fileName,'w')
            for each in contents:
                if att in each:
                    each=r'%s= %s'%(att,str(value))
                file.write('%s\n'%each)
            file.close()

