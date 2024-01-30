import bpy
import json

def delete_all_drivers(obj):
    if obj.animation_data:
        drivers_data = obj.animation_data.drivers
        while drivers_data:
            drivers_data.remove(drivers_data[0])

def load_drivers(obj, filepath):
    # 드라이버 데이터를 불러오기 전에 모든 드라이버를 삭제합니다.
    delete_all_drivers(obj)
    
    with open(filepath, 'r') as f:
        drivers_data = json.load(f)

    if not obj.animation_data:
        obj.animation_data_create()
    
    # 불러온 드라이버 데이터를 기반으로 드라이버를 다시 생성합니다.
    for driver_data in drivers_data:
        # 올바른 데이터 경로를 설정합니다.
        # key_blocks["ShapeKeyName"].value 형태로 데이터 경로를 정정합니다.
        data_path = driver_data['data_path'].replace('[0]', '')
        
        # 드라이버를 추가하거나 찾습니다.
        fcurve = obj.data.shape_keys.key_blocks[data_path.split('"')[1]].driver_add("value").driver
        fcurve.type = driver_data['type']
        fcurve.expression = driver_data['expression']
        
        # 기존의 모든 드라이버 변수를 삭제합니다.
        while fcurve.variables:
            fcurve.variables.remove(fcurve.variables[0])
        
        # 드라이버 변수를 다시 생성합니다.
        for var_data in driver_data['variables']:
            var = fcurve.variables.new()
            var.name = var_data['name']
            var.targets[0].id_type = var_data['id_type']
            var.targets[0].id = bpy.data.objects.get(var_data['target_id_name'])
            var.targets[0].data_path = var_data['data_path']

# 사용 예시:
load_drivers(bpy.context.active_object, '/Users/hun/GoodGangLabs Dropbox/Individuals/Jeonghun/rnd/PoC/blender_drive/json/drivers_02.json')
