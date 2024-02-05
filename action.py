import bpy
import json

# JSON 파일 로드
shape_keys_file_path = '/Users/hun/GoodGangLabs Dropbox/Individuals/Jeonghun/rnd/PoC/blender_drive/poc_driver_04_shape_keys.json'
with open(shape_keys_file_path, 'r') as file:
    shape_keys_data = json.load(file)
# 'con' 오브젝트 선택
con_object = bpy.data.objects["con"]

# 모든 쉐입키 애니메이션 값 순회
for index, animation_values in enumerate(shape_keys_data['shape_keys_values']):
    # 각 애니메이션 값에 대한 프레임별 키 프레임 설정
    for frame_number, value in enumerate(animation_values, start=1 + index*len(animation_values)):
        # 위치 Z 값 설정
        con_object.location.z = value
        # 키 프레임 삽입
        con_object.keyframe_insert(data_path="location", index=2, frame=frame_number)
