bl_info = {
    "name": "Load JSON Driver Data",
    "blender": (2, 80, 0),
    "category": "Object",
    "description": "Load driver data from a JSON file into the active object",
    "author": "Your Name",
    "version": (1, 0),
    "location": "View3D > Sidebar > My Tab",
}

import bpy
import json

def load_drivers(obj, filepath):
    with open(filepath, 'r') as f:
        drivers_data = json.load(f)

    if not obj.animation_data:
        obj.animation_data_create()

    for driver_data in drivers_data:
        data_path = driver_data['data_path'].replace('.value[0]', '.value')
        if data_path.startswith('key_blocks["'):
            fcurve = obj.data.shape_keys.key_blocks[data_path.split('"')[1]].driver_add("value").driver
            fcurve.type = driver_data['type']
            fcurve.expression = driver_data['expression']

            for var_data in driver_data['variables']:
                var = fcurve.variables.new()
                var.name = var_data['name']
                var.type = var_data['variable_type']
                target = var.targets[0]
                target.id = bpy.data.objects.get(var_data['target_id_name'])
                target.data_path = var_data['data_path']
                if var.type == 'TRANSFORMS':
                    if 'transform_type' in var_data:
                        target.transform_type = var_data['transform_type']
                    if 'transform_space' in var_data:
                        target.transform_space = var_data['transform_space']

class LoadJSONDriverDataOperator(bpy.types.Operator):
    """Load JSON Driver Data"""
    bl_idname = "object.load_json_driver_data"
    bl_label = "Load JSON Driver Data"
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    filename_ext = ".json"  # 파일 확장자 명시

    filter_glob: bpy.props.StringProperty(
        default="*.json",  # 파일 브라우저에 표시할 파일 필터 설정
        options={'HIDDEN'}
    ) # type: ignore

    def execute(self, context):
        if not context.active_object:
            self.report({'WARNING'}, "No active object selected. Please select an object.")
            return {'CANCELLED'}
        
        try:
            load_drivers(context.active_object, self.filepath)
            self.report({'INFO'}, "Driver data loaded successfully")
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}
        
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class LoadJSONDriverDataPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Load JSON Driver Data"
    bl_idname = "OBJECT_PT_load_json_driver_data"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Load Driver Data'

    def draw(self, context):
        layout = self.layout
        layout.label(text="쉐이프키가 있는 오브젝트를 선택해야합니다")
        layout.operator(LoadJSONDriverDataOperator.bl_idname, text="Load JSON Driver Data")

def register():
    bpy.utils.register_class(LoadJSONDriverDataOperator)
    bpy.utils.register_class(LoadJSONDriverDataPanel)

def unregister():
    bpy.utils.unregister_class(LoadJSONDriverDataOperator)
    bpy.utils.unregister_class(LoadJSONDriverDataPanel)

if __name__ == "__main__":
    register()
