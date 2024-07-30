import bpy
import json
import math

# Sample JSON data
json_data = '''
{ 
     "area_name": "Living Room", 
     "X": 0.0, 
     "Y": 0.0, 
     "Z": 0.0, 
     "area_size_X": 10, 
     "area_size_Y": 10, 
     "area_objects_list": [ { 
             "object_name": "Sofa_1", 
             "X": -4.5, 
             "Y": 2.0, 
             "Z": 0.5, 
             "rotation_Z": 180, 
             "scale_X": 6.0, 
             "scale_Y": 2.0, 
             "scale_Z": 1.0, 
             "Material": "Fabric, Foam" 
         }, { 
             "object_name": "TV_1", 
             "X": -3.5, 
             "Y": -4.0, 
             "Z": 1.25, 
             "rotation_Z": 180, 
             "scale_X": 3.0, 
             "scale_Y": 2.0, 
             "scale_Z": 1.5, 
             "Material": "Metal, Plastic" 
         }, { 
             "object_name": "Rocking_Chiar_1", 
             "X": -6.0, 
             "Y": 0.0, 
             "Z": 0.75, 
             "rotation_Z": 180, 
             "scale_X": 2.0, 
             "scale_Y": 2.0, 
             "scale_Z": 1.5, 
             "Material": "Wood, Leather" 
         }, { 
             "object_name": "Bean_Bag_1", 
             "X": -7.0, 
             "Y": 3.0, 
             "Z": 0.75, 
             "rotation_Z": 180, 
             "scale_X": 3.0, 
             "scale_Y": 3.0, 
             "scale_Z": 1.5, 
             "Material": "Fabric, Foam" 
         } ] }
'''

# Parse JSON data
data = json.loads(json_data)

# Clear all objects in the scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Function to create a cube representing an object
def create_object(obj_data):
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

# Iterate over objects in JSON and create them in Blender
for obj_data in data['area_objects_list']:
    create_object(obj_data)
