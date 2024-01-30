import bpy
import json

def load_drivers(obj, filepath):
    with open(filepath, 'r') as f:
        drivers_data = json.load(f)

    if not obj.animation_data:
        obj.animation_data_create()

    # 기존 드라이버를 모두 삭제합니다.
    while obj.animation_data.drivers:
        obj.animation_data.drivers.remove(obj.animation_data.drivers[0])

    # 불러온 드라이버 데이터를 사용하여 드라이버를 생성합니다.
    for driver_data in drivers_data:
        # 데이터 경로에서 '.value[0]'를 '.value'로 변경합니다.
        data_path = driver_data['data_path'].replace('.value[0]', '.value')
        
        # 드라이버를 쉐이프 키에 추가합니다.
        fcurve = obj.data.shape_keys.key_blocks[data_path.split('"')[1]].driver_add("value").driver
        fcurve.type = driver_data['type']
        fcurve.expression = driver_data['expression']

        # 드라이버 변수를 설정합니다.
        for var_data in driver_data['variables']:
            var = fcurve.variables.new()
            var.name = var_data['name']
            var.type = var_data['variable_type']
            target = var.targets[0]
            # 타겟 오브젝트를 직접 할당합니다.
            target.id = bpy.data.objects.get(var_data['target_id_name'])
            target.data_path = var_data['data_path']
            # 'transform_space' 값을 설정합니다, 이 값이 제공되는 경우에만.
            if 'transform_space' in var_data:
                target.transform_space = var_data['transform_space']
            # 'transform_type' 값을 설정합니다, 이 값이 제공되는 경우에만.
            if 'transform_type' in var_data:
                target.transform_type = var_data['transform_type']

# 사용 예시:
load_drivers(bpy.context.active_object, '/Users/hun/GoodGangLabs Dropbox/Individuals/Jeonghun/rnd/PoC/blender_drive/json/drivers_04.json')
