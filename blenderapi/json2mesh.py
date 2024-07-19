import bpy
import json
import os
bpy.ops.preferences.addon_enable(module='io_scene_3ds')
bpy.ops.preferences.addon_enable(module='export_mesh_stl')
bpy.ops.preferences.addon_enable(module='io_scene_obj')


def import_mesh_from_json(json_path):
    # Ensure the OBJ import/export addon is enabled

    # Load the JSON file
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    # Loop through each mesh entry in the JSON file
    for mesh_data in data['meshes']:
        mesh_path = mesh_data['path']
        coordinates = mesh_data['coordinates']
        
        # Import the mesh into Blender
        if file_path.endswith(".obj"):
            imported_object = bpy.ops.wm.obj_import(filepath=file_path)
        elif file_path.endswith(".stl"):
            imported_object = bpy.ops.wm.stl_import(filepath=file_path)
        elif file_path.endswith(".glb") or file_path.endswith(".gltf"):
            imported_object = bpy.ops.wm.stl_import(filepath=file_path)
        elif file_path.endswith(".fbx"):
            imported_object =  bpy.ops.import_scene.fbx(filepath=file_path)
        # elif file_path.endswith(".blend"):
        #     imported_object =  load_blend(filepath=file_path)
        else:
            print(f"Failed loading 3D Model -> unknown/unsupported datatype:'{file_path}'\n-------")
            return "TRIGGER_CONTINUE"
        
        # Get the last imported object
        imported_obj = bpy.context.selected_objects[-1]
        
        # Set the location of the imported object
        imported_obj.location = coordinates

class ImportMeshJSONOperator(bpy.types.Operator):
    """Import Mesh from JSON"""
    bl_idname = "import_mesh.json"
    bl_label = "Import Mesh from JSON"
    bl_options = {'REGISTER', 'UNDO'}
    
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    
    def execute(self, context):
        import_mesh_from_json(self.filepath)
        return {'FINISHED'}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

def menu_func_import(self, context):
    self.layout.operator(ImportMeshJSONOperator.bl_idname, text="Import Mesh from JSON5")

def register():
    bpy.utils.register_class(ImportMeshJSONOperator)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)

def unregister():
    bpy.utils.unregister_class(ImportMeshJSONOperator)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)

if __name__ == "__main__":
    register()
