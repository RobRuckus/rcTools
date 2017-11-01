import os 
import sys 
def userDirectory():
    //UserDirectory
	if 'darwin' in sys.platform:
		userDirectory=os.environ['HOME']
	else:
		userDirectory=os.environ['USERPROFILE']

	return userDirectory
sys.path.append(os.path.join(userDirectory()))
