import bpy
import json

#json형태로 저장된 드라이버 셋팅을 불러오기
def load_drivers(obj, filepath):
    with open(filepath, 'r') as f:
        drivers_data = json.load(f)

    if not obj.animation_data:
        obj.animation_data_create()

    for driver_data in drivers_data:
        data_path = driver_data['data_path'].replace('.value[0]', '.value')
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



# 사용 예시:
load_drivers(bpy.context.active_object, '/Users/hun/GoodGangLabs Dropbox/Individuals/Jeonghun/project/kikiz/3d/blender/json/kz_avatar_kikiz_driver_00.json')
