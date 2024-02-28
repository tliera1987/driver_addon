# bl_info = {
#     "name": "Save Driver Data",
#     "blender": (2, 93, 0),
#     "category": "Object",
#     "description": "Save driver data to a JSON file",
#     "author": "Your Name",
#     "version": (1, 0),
#     "location": "View3D > Sidebar > My Tab",
# }

import bpy
import json

# 드라이버 데이터를 저장하는 함수
def save_driver_data(obj, filepath):
    drivers_data = []

    if obj.data.shape_keys and obj.data.shape_keys.animation_data:
        for fcurve in obj.data.shape_keys.animation_data.drivers:
            driver = fcurve.driver
            driver_info = {
                'data_path': fcurve.data_path,
                'type': driver.type,
                'expression': driver.expression,
                'variables': []
            }
            for var in driver.variables:
                var_info = {
                    'name': var.name,
                    'id_type': var.targets[0].id_type,
                    'target_id_name': var.targets[0].id.name if var.targets[0].id else '',
                    'data_path': var.targets[0].data_path,
                    'variable_type': var.type,
                    'transform_type': var.targets[0].transform_type if var.type == 'TRANSFORMS' else None,
                    'transform_space': var.targets[0].transform_space if hasattr(var.targets[0], 'transform_space') else None
                }
                driver_info['variables'].append(var_info)
            drivers_data.append(driver_info)

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(drivers_data, f, ensure_ascii=False, indent=4)

# 파일 경로를 선택하고 저장하는 연산자
# class SaveDriverDataOperator(bpy.types.Operator):
#     """Save driver data to a JSON file"""
#     bl_idname = "object.save_driver_data"
#     bl_label = "Save Driver Data"
#     filepath: bpy.props.StringProperty(subtype='FILE_PATH') # type: ignore
#     filename_ext = ".json"  # 파일 확장자 명시

#     filter_glob: bpy.props.StringProperty(
#         default="*.json",  # 파일 브라우저에 표시할 파일 필터 설정
#         options={'HIDDEN'}
#     ) # type: ignore

#     def execute(self, context):
#         save_driver_data(context.active_object, self.filepath)
#         self.report({'INFO'}, f"Driver data saved to {self.filepath}")
#         return {'FINISHED'}

#     def invoke(self, context, event):
#         context.window_manager.fileselect_add(self)
#         return {'RUNNING_MODAL'}

# # UI 패널 정의
# class SaveDriverDataPanel(bpy.types.Panel):
#     """Creates a Panel in the Object properties window"""
#     bl_label = "Save Driver Data"
#     bl_idname = "OBJECT_PT_save_driver_data"
#     bl_space_type = 'VIEW_3D'
#     bl_region_type = 'UI'
#     bl_category = 'Save Driver Data'

#     def draw(self, context):
#         layout = self.layout
#         layout.label(text="저장시 확장지를 지워주세요")
#         layout.operator(SaveDriverDataOperator.bl_idname, text="Save Driver Data")

# 등록 및 해제 함수
# def register():
#     bpy.utils.register_class(SaveDriverDataOperator)
#     bpy.utils.register_class(SaveDriverDataPanel)

# def unregister():
#     bpy.utils.unregister_class(SaveDriverDataOperator)
#     bpy.utils.unregister_class(SaveDriverDataPanel)

# if __name__ == "__main__":
#     register()
