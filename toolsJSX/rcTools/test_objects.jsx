//OBJECTS
var shotCAM='';
for(index=1;index<=shotComp.numLayers;index++){
    if (shotComp.layers[index].name==shotName){
        shotCAM=shotComp.layers[index]
        alert(shotCAM)
        }
    }
if (shotCAM== ''){
   shotCAM= shotComp.layers.addCamera(shotName,[0,0])
}
    