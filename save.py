import bpy
import json

#드라이브 셋팅을 저장
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
# 사용 예시:
save_driver_data(bpy.context.active_object, '/Users/hun/GoodGangLabs Dropbox/Individuals/Jeonghun/project/kikiz/3d/blender/json/kz_avatar_kikiz_driver_00.json')

