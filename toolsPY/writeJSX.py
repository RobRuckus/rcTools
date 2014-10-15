
class jsxWrite(object):
    def __init__(self):
        self.scene=rcTools2.sceneData()
        self.AELocation='Location of After Effects'
        self.fileName='_AFXImport.jsx'
        self.commands=[]
        self.imageFolderName='_images'
		
    def addCommand(self,command):
        #add command to self.commands
        pass
    def addReturn(self):
        #add '\n' to commands
        pass
    def addTab(self):
        print 'yes'
        #add '\t' to commands 
        pass
        
    def variableDict():
		width='width'
		height='height'
		fps='fps'
		seconds='seconds'
		shotName=mc.getAttr('renderLayerManager.shotName')
		imageFolderName='images'
		layers='layerNames'
		images='outputImages'
		pass
		
  
    def writeaVariable(self,variable):
		#write( 'var key=value')
		pass
    def writeToFile(commands):
        file=open(fileName,'w')
        file.write(commands)
        file.close()
		
scene=jsxWrite()
scene.addTab()




