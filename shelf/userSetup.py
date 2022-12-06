import os 
import sys 
def userDirectory():
	if 'darwin' in sys.platform:
		userDirectory=os.environ['HOME']
	else:
		userDirectory=os.environ['USERPROFILE']
	return userDirectory
	
def nasDirectory():
	return '//dig_nas/art/'
	
sys.path.append(os.path.join(userDirectory()))
sys.path.append(os.path.join(nasDirectory()))
