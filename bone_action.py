import bpy
import json

#쉐이프 키 애니메이션을 액션 키 애니메이션으로 변환

# 파일 경로
# a = 드라이버 셋팅 저장 파일 
# b = 쉐입키 애니메이션 파일
a_file_path = '/Users/hun/GoodGangLabs Dropbox/Individuals/Jeonghun/project/kikiz/3d/blender/json/kz_avatar_kikiz_driver_00.json'  # 예시 경로, 실제 경로로 변경 필요
b_file_path = '/Users/hun/GoodGangLabs Dropbox/Individuals/Jeonghun/project/kikiz/3d/blender/json/kz_avatar_kikiz_facecontroller_script_04_shape_keys.json'  # 예시 경로, 실제 경로로 변경 필요



# 파일 로드
with open(a_file_path, 'r') as file:
    a_data = json.load(file)

with open(b_file_path, 'r') as file:
    b_data = json.load(file)

# 암쳐 객체 설정
armature_name = a_data[0]['variables'][0]['target_id_name']  # 첫 번째 드라이버 설정에서 암쳐 이름 추정
armature = bpy.data.objects.get(armature_name)
if not armature or armature.type != 'ARMATURE':
    print(f"암쳐 {armature_name}를 찾을 수 없습니다.")
else:
    # 애니메이션 데이터 생성 및 액션 설정
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
        
        # b_data에서 해당 쉐입키의 애니메이션 값을 가져옴
        animation_values = b_data[shapekey_name]
        for frame_number, k_var in enumerate(animation_values, start=1):
            # 역산으로 var과 var_001 계산
            var = var_001 = k_var / (30.04 * 2)

            # 본 위치 설정 및 키프레임 삽입
            for var_data in driver['variables']:
                bone_name = var_data['data_path'].split('["')[1].split('"]')[0]
                bone = armature.pose.bones.get(bone_name)
                if not bone:
                    print(f"본 {bone_name}를 찾을 수 없습니다.")
                    continue
                
                # 위치 설정 및 키프레임 삽입
                if "location[0]" in var_data['data_path']:
                    bone.location.x = var  # X축에 var 값 적용
                    bone.keyframe_insert(data_path="location", index=0, frame=frame_number)
                elif "location[2]" in var_data['data_path']:
                    bone.location.z = var_001  # Z축에 var_001 값 적용
                    bone.keyframe_insert(data_path="location", index=2, frame=frame_number)

print("스크립트 실행 완료")
