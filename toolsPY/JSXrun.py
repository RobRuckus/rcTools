import rcTools
import rcTools.main as main 
import rcTools.toolsPY.jsx as jsx

scene=rcTools.rcMaya.sceneData()
	Ae=self.write('C:\Users\RobC\event.jsx')
	Ae.addFolder('_footage')
	Ae.addFolder('_pre')
	Ae.comp(scene)
	Ae.layers(scene)
	Ae.do()


