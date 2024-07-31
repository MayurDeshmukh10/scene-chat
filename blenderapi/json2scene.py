import bpy
import json
import math

# Sample JSON data
# json_data = '''
# { 
#      "area_name": "Living Room", 
#      "X": 0.0, 
#      "Y": 0.0, 
#      "Z": 0.0, 
#      "area_size_X": 10, 
#      "area_size_Y": 10, 
#      "area_objects_list": [ { 
#              "object_name": "Sofa_1", 
#              "X": -4.5, 
#              "Y": 2.0, 
#              "Z": 0.5, 
#              "rotation_Z": 180, 
#              "scale_X": 6.0, 
#              "scale_Y": 2.0, 
#              "scale_Z": 1.0, 
#              "Material": "Fabric, Foam" 
#          }, { 
#              "object_name": "TV_1", 
#              "X": -3.5, 
#              "Y": -4.0, 
#              "Z": 1.25, 
#              "rotation_Z": 180, 
#              "scale_X": 3.0, 
#              "scale_Y": 2.0, 
#              "scale_Z": 1.5, 
#              "Material": "Metal, Plastic" 
#          }, { 
#              "object_name": "Rocking_Chiar_1", 
#              "X": -6.0, 
#              "Y": 0.0, 
#              "Z": 0.75, 
#              "rotation_Z": 180, 
#              "scale_X": 2.0, 
#              "scale_Y": 2.0, 
#              "scale_Z": 1.5, 
#              "Material": "Wood, Leather" 
#          }, { 
#              "object_name": "Bean_Bag_1", 
#              "X": -7.0, 
#              "Y": 3.0, 
#              "Z": 0.75, 
#              "rotation_Z": 180, 
#              "scale_X": 3.0, 
#              "scale_Y": 3.0, 
#              "scale_Z": 1.5, 
#              "Material": "Fabric, Foam" 
#          } ] }
# '''

# bpy.ops.preferences.addon_enable(module='io_scene_3ds')
# bpy.ops.preferences.addon_enable(module='export_mesh_stl')
# bpy.ops.preferences.addon_enable(module='io_scene_obj')


# Function to create a cube representing an object
def create_cube_objects(obj_data):
    name = obj_data['object_name']
    x = obj_data['X']
    y = obj_data['Y']
    z = obj_data['Z']
    scale_x = obj_data['scale_X']
    scale_y = obj_data['scale_Y']
    scale_z = obj_data['scale_Z']
#    rotation_x = math.radians(obj_data['rotation_X'])
#    rotation_y = math.radians(obj_data['rotation_Y'])
    rotation_z = math.radians(obj_data['rotation_Z'])

    # Create a cube
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z))
    obj = bpy.context.object
    obj.name = name

    # Scale the cube to the specified dimensions
    obj.scale = (scale_x, scale_y, scale_z)
    
    # Rotate the cube to the specified rotations
    obj.rotation_euler = (0.0, 0.0, rotation_z)


def create_generated_objects(obj_data):
    name = obj_data['object_name']
    x = obj_data['X']
    y = obj_data['Y']
    z = obj_data['Z']
    scale_x = obj_data['scale_X']
    scale_y = obj_data['scale_Y']
    scale_z = obj_data['scale_Z']
    rotation_z = math.radians(obj_data['rotation_Z'])
    object_type = obj_data['object_type']
    # breakpoint()
    object_filepath = obj_data['generated_asset_path'][f'{object_type}_path']

    # Import the downloaded asset into Blender
    if object_type == "obj":
        imported_object = bpy.ops.wm.obj_import(filepath=object_filepath)
    elif object_type == "stl":
        imported_object = bpy.ops.wm.stl_import(filepath=object_filepath)
    elif object_type == "glb" or object_type == "gltf":
        imported_object = bpy.ops.import_scene.gltf(filepath=object_filepath)
    elif object_type == "fbx":
        imported_object = bpy.ops.import_scene.fbx(filepath=object_filepath)
    else:
        print(f"Failed loading 3D Model -> unknown/unsupported datatype:'{name}.{object_type}'\n-------")
        return "TRIGGER_CONTINUE"

    # Get the last imported object
    imported_object
    imported_obj = bpy.context.selected_objects[-1]

    # Set the location of the imported object
    imported_obj.name = name
    imported_obj.location = (x, y, z)
    imported_obj.scale = (scale_x, scale_y, scale_z)
    imported_obj.rotation_euler = (0.0, 0.0, rotation_z)


def create_blender_scene(scene_json, filename, type="cube"):

    # Clear all objects in the scene
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

    # Iterate over objects in JSON and create them in Blender
    for obj_data in scene_json['area_objects_list']:
        if type == "cube":
            create_cube_objects(obj_data)
        else:
            create_generated_objects(obj_data)
            filename = "scene_with_generated_assets"

    filepath = f"./outputs/{filename}.blend"

    bpy.ops.wm.save_as_mainfile(filepath=filepath)

    return filename
