import bpy
import json

<<<<<<< HEAD
#쉐이프 키 애니메이션을 액션 키 애니메이션으로 변환

# 파일 경로
# a = 드라이버 셋팅 저장 파일 
# b = 쉐입키 애니메이션 파일
a_file_path = '/Users/hun/GoodGangLabs Dropbox/Individuals/Jeonghun/project/kikiz/3d/blender/json/kz_avatar_kikiz_driver_00.json'  # 예시 경로, 실제 경로로 변경 필요
b_file_path = '/Users/hun/GoodGangLabs Dropbox/Individuals/Jeonghun/project/kikiz/3d/blender/json/kz_avatar_kikiz_facecontroller_script_02_shape_keys.json'  # 예시 경로, 실제 경로로 변경 필요
=======
# a 파일과 b 파일 로드
a_file_path = '/Users/hun/GoodGangLabs Dropbox/Individuals/Jeonghun/rnd/PoC/blender_drive/json/drivers_04.json'
b_file_path = '/Users/hun/GoodGangLabs Dropbox/Individuals/Jeonghun/rnd/PoC/blender_drive/json/poc_shapekey_01_shape_keys.json'
>>>>>>> parent of 148853f (20240206_11:40)

with open(a_file_path, 'r') as f:
    a_data = json.load(f)

with open(b_file_path, 'r') as f:
    b_data = json.load(f)

# a 파일에서 필요한 정보 추출
shape_key_name = a_data['data_path'].split('["')[1].split('"]')[0]  # "test_up"
object_name = a_data['variables'][0]['target_id_name']  # "con"

<<<<<<< HEAD
# 여러 오브젝트에 대한 설정 반영
for driver in a_data:  # a_data는 드라이버 설정 리스트로 가정
    object_name = driver['variables'][0]['target_id_name']
    print(object_name)
    expression = driver['expression']  # 가중치 적용을 위한 표현식
    print(expression)
    shape_key_name = driver['data_path'].split('["')[1].split('"]')[0]  # 쉐입키 이름 추출
    print(shape_key_name)
      
    # b 파일에서 해당 쉐입키에 대한 값 로드
    if shape_key_name in b_data:
        animation_values = b_data[shape_key_name]
        print(animation_values)  
    else:
        continue  # b 파일에 해당 쉐입키 데이터가 없다면 다음 드라이버로 넘어감

    obj = bpy.data.objects.get(object_name)
    print(obj)

    if obj:
        # 액션 생성 및 오브젝트에 할당
        action = bpy.data.actions.new(name=f"{object_name}_Action")
        obj.animation_data_create()
        obj.animation_data.action = action

        # 키프레임 설정
        for frame_number, value in enumerate(animation_values, start=1):
            # 가중치 적용
            applied_value = eval(expression.replace('var', str(value)))

    #         # transform_type에 따라 적용
    #         if transform_type == "LOC_Z":
    #             obj.location.z = applied_value
    #         elif transform_type == "LOC_X":
    #             obj.location.x = applied_value
    #         # 다른 transform_type 조건 추가 가능

    #         # 키프레임 삽입
    #         data_path = "location" if "LOC" in transform_type else "rotation_euler" if "ROT" in transform_type else "scale"
    #         index = 0 if "X" in transform_type else 1 if "Y" in transform_type else 2 if "Z" in transform_type else 0
    #         obj.keyframe_insert(data_path=data_path, index=index, frame=frame_number)

    #     print(f"애니메이션 적용 완료: {object_name}")
    # else:
    #     print(f"오브젝트 {object_name}를 찾을 수 없습니다.")
=======
# b 파일에서 쉐입키 애니메이션 값 로드
animation_values = b_data[shape_key_name]

# 오브젝트 및 쉐입키 찾기
obj = bpy.data.objects[object_name]
shape_key = obj.data.shape_keys.key_blocks[shape_key_name]

# 애니메이션 값 적용
for frame_number, value in enumerate(animation_values):
    shape_key.value = value
    shape_key.keyframe_insert(data_path="value", frame=frame_number + 1)  # 프레임 번호는 1부터 시작

print(f"애니메이션 적용 완료: {shape_key_name} on {object_name}")
>>>>>>> parent of 148853f (20240206_11:40)
