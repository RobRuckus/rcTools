import os 
import sys 
def userDirectory():
	if 'darwin' in sys.platform:
		userDirectory=os.environ['HOME']
	else:
		userDirectory=os.environ['USERPROFILE']
	return userDirectory
#sys.path.append(#location on NAS)
sys.path.append(os.path.join(userDirectory()))