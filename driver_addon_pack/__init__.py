bl_info = {
    "name": "Driver Addon",
    "blender": (2, 80, 0),
    "category": "Animation",
    "description": "Convert controller animation to shape key animation",
    "author": "jh kim",
    "version": (1, 0),
    "location": "View3D > Sidebar > Driver_Addon",
}

import bpy
import json

from .apply import convert_controller_to_shape_key_animation
from .bone_action import apply_transformations
from .del_driver import delete_shape_key_drivers
from .del_driver import delete_all_object_drivers
from .driver_load import load_drivers
from .driver_save import save_driver_data
from .shape_save import export_shape_key_animation


#오퍼레이터 
#오퍼레이터from .apply import convert_controller_to_shape_key_animation
class OBJECT_OT_ConvertControllerToShapeKey(bpy.types.Operator):
    """Convert Controller to Shape Key Animation"""
    bl_idname = "object.convert_controller_to_shape_key"
    bl_label = "Convert Controller to Shape Key"

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (obj is not None and obj.type == 'MESH' and 
                obj.data.shape_keys is not None)

    def execute(self, context):
        convert_controller_to_shape_key_animation(context)
        self.report({'INFO'}, "Converted controller animation to shape key animation.")
        return {'FINISHED'}

#오퍼레이터from .bone_action import apply_transformations
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
    
#오퍼레이터from .del_driver import delete_shape_key_drivers
class DeleteShapeKeyDriversOperator(bpy.types.Operator):
    """Delete Shape Key Drivers"""
    bl_idname = "object.delete_shape_key_drivers"
    bl_label = "Delete Shape Key Drivers"

    def execute(self, context):
        delete_shape_key_drivers(context.active_object)
        self.report({'INFO'}, "Shape Key Drivers Deleted")
        return {'FINISHED'}
    
class DeleteAllObjectDriversOperator(bpy.types.Operator):
    """Delete All Object Drivers"""
    bl_idname = "object.delete_all_object_drivers"
    bl_label = "Delete All Object Drivers"

    def execute(self, context):
        delete_all_object_drivers(context.active_object)
        self.report({'INFO'}, "All Object Drivers Deleted")
        return {'FINISHED'}    
    
#오퍼레이터from .driver_load import load_drivers
class LoadJSONDriverDataOperator(bpy.types.Operator):
    """Load JSON Driver Data"""
    bl_idname = "object.load_json_driver_data"
    bl_label = "Load JSON Driver Data"
    filepath: bpy.props.StringProperty(subtype="FILE_PATH") # type: ignore
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

#오퍼레이터from .driver_save import save_driver_data
class SaveDriverDataOperator(bpy.types.Operator):
    """Save driver data to a JSON file"""
    bl_idname = "object.save_driver_data"
    bl_label = "Save Driver Data"
    filepath: bpy.props.StringProperty(subtype='FILE_PATH') # type: ignore
    filename_ext = ".json"  # 파일 확장자 명시

    filter_glob: bpy.props.StringProperty(
        default="*.json",  # 파일 브라우저에 표시할 파일 필터 설정
        options={'HIDDEN'}
    ) # type: ignore

    def execute(self, context):
        save_driver_data(context.active_object, self.filepath)
        self.report({'INFO'}, f"Driver data saved to {self.filepath}")
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
    
#오퍼레이터from .shape_save import export_shape_key_animation
class ExportShapeKeyAnimationOperator(bpy.types.Operator):
    """Export Shape Key Animation"""
    bl_idname = "object.export_shape_key_animation"
    bl_label = "Export Shape Key Animation"
    filepath: bpy.props.StringProperty(subtype="FILE_PATH") # type: ignore
    filename_ext = ".json"  # 파일 확장자 명시

    filter_glob: bpy.props.StringProperty(
        default="*.json",  # 파일 브라우저에 표시할 파일 필터 설정
        options={'HIDDEN'}
    ) # type: ignore

    def execute(self, context):
        export_shape_key_animation(context.active_object, self.filepath)
        self.report({'INFO'}, "Shape Key Animation Data Exported")
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

#####패널부분
#from .apply import convert_controller_to_shape_key_animation

class VIEW3D_PT_ControllerToShapeKey(bpy.types.Panel):
    bl_label = "Export shape animation"
    bl_idname = "VIEW3D_PT_controller_to_shape_key"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Driver_ADDON'

    def draw(self, context):
        layout = self.layout
        layout.label(text="도프 시트에서 액션을 활성화 후, 적용할 오브젝트를 선택 후 작동")
        layout.operator(OBJECT_OT_ConvertControllerToShapeKey.bl_idname)

#from .bone_action import apply_transformations
class OBJECT_PT_CustomPanel(bpy.types.Panel):
    bl_label = "Shape to Bone"
    bl_idname = "convert controller animation"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Driver_ADDON'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row()
        layout.label(text="Driver Settings Path:")
        layout.operator(OpenDriverSettingsFile.bl_idname, text="드라이버 셋팅 파일")
        layout.prop(scene, "driver_settings_path", text="")

        row = layout.row()
        layout.label(text="Shape Key Animations Path:")
        layout.operator(OpenShapeKeyAnimationsFile.bl_idname, text="쉐이프키 애니메이션 파일")
        layout.prop(scene, "shape_key_animations_path", text="")

        row = layout.row()
        layout.label(text="반드시 아마튜어를 선택해 주세요")
        layout.operator(ApplyTransformationsOperator.bl_idname)

#from .del_driver import delete_shape_key_drivers
class DriverDeletionPanel(bpy.types.Panel):
    bl_label = "Driver_Deletion"
    bl_idname = "Driver_Deletion_ID"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Driver_ADDON'

    def draw(self, context):
        layout = self.layout
        # 새로운 행 생성
        row = layout.row()
        layout.label(text="쉐이프키가 있는 오브젝트를 선택해야합니다")
        row = layout.row()
        layout.label(text="1번>2번 모두 해야 완전히 초기화 됩니다.")
        row = layout.row()
        split = row.split(factor=0.5)        
        split.operator(DeleteShapeKeyDriversOperator.bl_idname, text="1.Delete Shape Keys")       
        split.operator(DeleteAllObjectDriversOperator.bl_idname, text="2.Delete All Drivers")
    
#from .driver_load import load_drivers
class LoadJSONDriverDataPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Load JSON Driver Data"
    bl_idname = "OBJECT_PT_load_json_driver_data"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Driver_ADDON'

    def draw(self, context):
        layout = self.layout
        layout.label(text="쉐이프키가 있는 오브젝트를 선택해야합니다")
        layout.operator(LoadJSONDriverDataOperator.bl_idname, text="Load JSON Driver Data")

#from .driver_save import save_driver_data  
class SaveDriverDataPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Save Driver Data"
    bl_idname = "OBJECT_PT_save_driver_data"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Driver_ADDON'

    def draw(self, context):   
        layout = self.layout
        layout.label(text="저장시 확장지를 지워주세요")
        layout.operator(SaveDriverDataOperator.bl_idname, text="Save Driver Data")

#from .shape_save import export_shape_key_animation
class ExportShapeKeyAnimationPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Export Shape Key Animation"
    bl_idname = "OBJECT_PT_export_shape_key_animation"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Driver_ADDON'

    def draw(self, context):
        layout = self.layout
        layout.label(text="뒤에 확장자를 지워주세요")
        layout.operator(ExportShapeKeyAnimationOperator.bl_idname)

#레지스터
def register():
    #from .apply import convert_controller_to_shape_key_animation
    bpy.utils.register_class(OBJECT_OT_ConvertControllerToShapeKey)
    bpy.utils.register_class(VIEW3D_PT_ControllerToShapeKey)
    #from .bone_action import apply_transformations
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
    #from .del_driver import delete_shape_key_drivers
    bpy.utils.register_class(DeleteShapeKeyDriversOperator)
    bpy.utils.register_class(DeleteAllObjectDriversOperator)
    bpy.utils.register_class(DriverDeletionPanel)
    #from .driver_load import load_drivers
    bpy.utils.register_class(LoadJSONDriverDataOperator)
    bpy.utils.register_class(LoadJSONDriverDataPanel)
    #from .driver_save import save_driver_data
    bpy.utils.register_class(SaveDriverDataOperator)
    bpy.utils.register_class(SaveDriverDataPanel)
    #from .shape_save import export_shape_key_animation
    bpy.utils.register_class(ExportShapeKeyAnimationOperator)
    bpy.utils.register_class(ExportShapeKeyAnimationPanel)

def unregister():
    #from .apply import convert_controller_to_shape_key_animation
    bpy.utils.unregister_class(OBJECT_OT_ConvertControllerToShapeKey)
    bpy.utils.unregister_class(VIEW3D_PT_ControllerToShapeKey)
    #from .bone_action import apply_transformations
    bpy.utils.unregister_class(ApplyTransformationsOperator)
    bpy.utils.unregister_class(OpenDriverSettingsFile)
    bpy.utils.unregister_class(OpenShapeKeyAnimationsFile)
    bpy.utils.unregister_class(OBJECT_PT_CustomPanel)
    del bpy.types.Scene.driver_settings_path
    del bpy.types.Scene.shape_key_animations_path
    #from .del_driver import delete_shape_key_drivers
    bpy.utils.unregister_class(DeleteShapeKeyDriversOperator)
    bpy.utils.unregister_class(DeleteAllObjectDriversOperator)
    bpy.utils.unregister_class(DriverDeletionPanel)
    #from .driver_load import load_drivers
    bpy.utils.unregister_class(LoadJSONDriverDataOperator)
    bpy.utils.unregister_class(LoadJSONDriverDataPanel)
    #from .driver_save import save_driver_data
    bpy.utils.unregister_class(SaveDriverDataOperator)
    bpy.utils.unregister_class(SaveDriverDataPanel)
    #from .shape_save import export_shape_key_animation
    bpy.utils.unregister_class(ExportShapeKeyAnimationOperator)
    bpy.utils.unregister_class(ExportShapeKeyAnimationPanel)

if __name__ == "__main__":
    register()