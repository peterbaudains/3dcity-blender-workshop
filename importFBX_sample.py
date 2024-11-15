import bpy
from pathlib import Path

def delete_default_scene():
    ''' 
    Delete the default scene in a Blender new project.
    '''
    for o in ("Cube", "Camera", "Light"):
        obj = bpy.context.scene.objects.get(o)
        if obj: 
            obj.select_set(True)
        bpy.ops.object.delete()

if __name__=="__main__":

    delete_default_scene()
    
    # Define path to fbx file
    model_sample_directory = '/ResearchData/AccuCities-Sample-2024/'
    file_name = 'AccuCities-FBX-sample-3D Model-of-London-Level-3-TQ3280.fbx'
    model_fbx_path = str(Path(str(Path.home()) + model_sample_directory + file_name))
    
    # Import scene
    bpy.ops.import_scene.fbx(filepath=model_fbx_path)
