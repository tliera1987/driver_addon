bl_info = {
    "name": "Bone Action Addon",
    "blender": (2, 80, 0),
    "category": "Object",
    "description": "Custom Addon to apply transformations based on provided settings",
    "author": "Your Name",
    "version": (1, 0),
    "location": "View3D > Sidebar > My Tab",
}

import bpy
import json

def apply_transformations(driver_settings, shape_key_animations, armature_name):
    armature = bpy.data.objects.get(armature_name)
    if not armature:
        print(f"Armature '{armature_name}' not found.")
        return
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='POSE')

    for setting in driver_settings:
        shape_key_name = setting["data_path"].split('"')[1]
        expression = setting["expression"]
        multiplier = float(expression.split('*')[1].strip())
        if expression.strip().startswith('-'):
            multiplier = -multiplier

        for variable in setting["variables"]:
            bone_name = variable["data_path"].split('"')[1]
            axis_index = int(variable["data_path"].split('[')[-1][0])
            bone = armature.pose.bones.get(bone_name)
            if not bone:
                print(f"Bone '{bone_name}' not found.")
                continue

            if shape_key_name in shape_key_animations:
                for frame, shape_key_value in enumerate(shape_key_animations[shape_key_name], start=1):
                    calculated_value = shape_key_value / multiplier
                    bone.location[axis_index] = calculated_value
                    bone.keyframe_insert(data_path='location', index=axis_index, frame=frame)

class ApplyTransformationsOperator(bpy.types.Operator):
    """Apply Custom Transformations"""
    bl_idname = "object.apply_transformations"
    bl_label = "Apply Transformations"
    bl_options = {'REGISTER', 'UNDO'}

    @staticmethod
    def load_json_data(filepath):
        abs_filepath = bpy.path.abspath(filepath)
        with open(abs_filepath, 'r') as file:
            return json.load(file)

    def execute(self, context):
        driver_settings_path = context.scene.driver_settings_path
        shape_key_animations_path = context.scene.shape_key_animations_path
        driver_settings = self.load_json_data(driver_settings_path)
        shape_key_animations = self.load_json_data(shape_key_animations_path)
        armature_name = "face_ctrl_animator"
        apply_transformations(driver_settings, shape_key_animations, armature_name)
        return {'FINISHED'}

class OpenDriverSettingsFile(bpy.types.Operator):
    """Open a file browser to select the driver settings JSON file"""
    bl_idname = "object.open_driver_settings_file"
    bl_label = "Select Driver Settings File"
    filepath: bpy.props.StringProperty(subtype="FILE_PATH") # type: ignore

    def execute(self, context):
        context.scene.driver_settings_path = self.filepath
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class OpenShapeKeyAnimationsFile(bpy.types.Operator):
    """Open a file browser to select the shape key animations JSON file"""
    bl_idname = "object.open_shape_key_animations_file"
    bl_label = "Select Shape Key Animations File"
    filepath: bpy.props.StringProperty(subtype="FILE_PATH") # type: ignore

    def execute(self, context):
        context.scene.shape_key_animations_path = self.filepath
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class OBJECT_PT_CustomPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Bone Action Panel"
    bl_idname = "OBJECT_PT_custom_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Bone Action'
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.label(text="Driver Settings Path:")
        layout.operator(OpenDriverSettingsFile.bl_idname, text="드라이버 셋팅 파일")
        layout.prop(scene, "driver_settings_path", text="")

        layout.label(text="Shape Key Animations Path:")
        layout.operator(OpenShapeKeyAnimationsFile.bl_idname, text="쉐이프키 애니메이션 파일")
        layout.prop(scene, "shape_key_animations_path", text="")

        layout.label(text="반드시 아마튜어를 선택해 주세요")
        layout.operator(ApplyTransformationsOperator.bl_idname)

def register():
    bpy.utils.register_class(ApplyTransformationsOperator)
    bpy.utils.register_class(OpenDriverSettingsFile)
    bpy.utils.register_class(OpenShapeKeyAnimationsFile)
    bpy.utils.register_class(OBJECT_PT_CustomPanel)
    bpy.types.Scene.driver_settings_path = bpy.props.StringProperty(
        name="Driver Settings Path",
        description="Path to the driver settings JSON file",
        default="",
    )   
    bpy.types.Scene.shape_key_animations_path = bpy.props.StringProperty(
        name="Shape Key Animations Path",
        description="Path to the shape key animations JSON file",
        default="",  
    )

def unregister():
    bpy.utils.unregister_class(ApplyTransformationsOperator)
    bpy.utils.unregister_class(OpenDriverSettingsFile)
    bpy.utils.unregister_class(OpenShapeKeyAnimationsFile)
    bpy.utils.unregister_class(OBJECT_PT_CustomPanel)
    del bpy.types.Scene.driver_settings_path
    del bpy.types.Scene.shape_key_animations_path

if __name__ == "__main__":
    register()
