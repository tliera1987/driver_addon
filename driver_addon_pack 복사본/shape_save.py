# bl_info = {
#     "name": "Export Shape Key Animation",
#     "blender": (2, 80, 0),
#     "category": "Object",
#     "description": "Export shape key animation data to JSON file",
#     "author": "Your Name",
#     "version": (1, 0),
#     "location": "View3D > Sidebar > Export Tools",
# }

import bpy
import json

def export_shape_key_animation(obj, filepath):
    shape_keys_data = {}
    if obj and obj.data.shape_keys and obj.data.shape_keys.animation_data and obj.data.shape_keys.animation_data.action:
        key_blocks = obj.data.shape_keys.key_blocks
        action = obj.data.shape_keys.animation_data.action
        for shape_key in key_blocks:
            if shape_key.name != "Basis":
                shape_keys_data[shape_key.name] = []
        frame_start = int(action.frame_range[0])
        frame_end = int(action.frame_range[1])
        for frame in range(frame_start, frame_end + 1):
            bpy.context.scene.frame_set(frame)
            for shape_key in key_blocks:
                if shape_key.name != "Basis":
                    value_rounded = round(shape_key.value, 6)
                    shape_keys_data[shape_key.name].append(value_rounded)
    json_data = json.dumps(shape_keys_data, indent=4)

    with open(filepath, 'w') as file:
        file.write(json_data)
    print(f"Data exported to {filepath}")

# class ExportShapeKeyAnimationOperator(bpy.types.Operator):
#     """Export Shape Key Animation"""
#     bl_idname = "object.export_shape_key_animation"
#     bl_label = "Export Shape Key Animation"
#     filepath: bpy.props.StringProperty(subtype="FILE_PATH") # type: ignore
#     filename_ext = ".json"  # 파일 확장자 명시

#     filter_glob: bpy.props.StringProperty(
#         default="*.json",  # 파일 브라우저에 표시할 파일 필터 설정
#         options={'HIDDEN'}
#     ) # type: ignore

#     def execute(self, context):
#         export_shape_key_animation(context.active_object, self.filepath)
#         self.report({'INFO'}, "Shape Key Animation Data Exported")
#         return {'FINISHED'}

#     def invoke(self, context, event):
#         context.window_manager.fileselect_add(self)
#         return {'RUNNING_MODAL'}

# class ExportShapeKeyAnimationPanel(bpy.types.Panel):
#     """Creates a Panel in the Object properties window"""
#     bl_label = "Export Shape Key Animation"
#     bl_idname = "OBJECT_PT_export_shape_key_animation"
#     bl_space_type = 'VIEW_3D'
#     bl_region_type = 'UI'
#     bl_category = 'Export Tools'

#     def draw(self, context):
#         layout = self.layout
#         layout.label(text="뒤에 확장자를 지워주세요")
#         layout.operator(ExportShapeKeyAnimationOperator.bl_idname)

# def register():
#     bpy.utils.register_class(ExportShapeKeyAnimationOperator)
#     bpy.utils.register_class(ExportShapeKeyAnimationPanel)

# def unregister():
#     bpy.utils.unregister_class(ExportShapeKeyAnimationOperator)
#     bpy.utils.unregister_class(ExportShapeKeyAnimationPanel)

# if __name__ == "__main__":
#     register()
