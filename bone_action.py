import bpy
import json

def find_closest_xy_combination(a, multiplier=30.04, x_min=-0.0333, x_max=0.0333, y_min=-0.0333, y_max=0.0333):
    best_diff = float('inf')
    best_x, best_y = 0, 0

    # 주어진 범위 내에서 x와 y의 조합 탐색
    for x in [x_min + i * (x_max - x_min) / 100.0 for i in range(101)]:
        y = (a / multiplier) - x
        # y가 주어진 범위 내에 있는지 확인하고, 범위를 벗어나면 스킵
        if y < y_min or y > y_max:
            continue
        # x - y의 절대값이 현재까지의 최소값보다 작은지 확인
        current_diff = abs(x - y)
        if current_diff < best_diff:
            best_diff = current_diff
            best_x, best_y = x, y

    # x - y가 0에 가장 가까운 조합 반환
    return best_x, best_y

# 파일 경로
a_file_path = '/Users/hun/GoodGangLabs Dropbox/Individuals/Jeonghun/project/kikiz/3d/blender/json/kz_avatar_kikiz_driver_00.json'  
b_file_path = '/Users/hun/GoodGangLabs Dropbox/Individuals/Jeonghun/project/kikiz/3d/blender/json/kz_avatar_kikiz_facecontroller_script_04_01_shape_keys.json'  

with open(a_file_path, 'r') as file:
    a_data = json.load(file)

with open(b_file_path, 'r') as file:
    b_data = json.load(file)

# 암쳐 객체 설정
armature_name = a_data[0]['variables'][0]['target_id_name']
armature = bpy.data.objects.get(armature_name)
if not armature or armature.type != 'ARMATURE':
    print(f"암쳐 {armature_name}를 찾을 수 없습니다.")
else:
    if not armature.animation_data:
        armature.animation_data_create()
    action = bpy.data.actions.new(name=f"{armature_name}_Action")
    armature.animation_data.action = action

    # a_data 순회하여 각 드라이버 처리
    for driver in a_data:
        shapekey_name = driver['data_path'].split('["')[1].split('"]')[0]
        if shapekey_name not in b_data:
            print(f"{shapekey_name}에 해당하는 쉐입키 데이터가 b_file 내에 없습니다.")
            continue
        
        animation_values = b_data[shapekey_name]
        for frame_number, a in enumerate(animation_values, start=1):
            var, var_001 = find_closest_xy_combination(a)

            # 본 위치 설정 및 키프레임 삽입
            for var_data in driver['variables']:
                bone_name = var_data['data_path'].split('["')[1].split('"]')[0]
                bone = armature.pose.bones.get(bone_name)
                if not bone:
                    print(f"본 {bone_name}를 찾을 수 없습니다.")
                    continue
                
                # 설정된 위치에 따라 본 위치 업데이트 및 키프레임 삽입
                if "location[0]" in var_data['data_path']:
                    bone.location.x = var
                    bone.keyframe_insert(data_path="location", index=0, frame=frame_number)
                elif "location[2]" in var_data['data_path']:
                    bone.location.z = var_001
                    bone.keyframe_insert(data_path="location", index=2, frame=frame_number)

print("스크립트 실행 완료")
