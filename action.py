import bpy
import json

# a 파일과 b 파일 로드
a_file_path = '/Users/hun/GoodGangLabs Dropbox/Individuals/Jeonghun/rnd/PoC/blender_drive/json/drivers_04.json'
b_file_path = '/Users/hun/GoodGangLabs Dropbox/Individuals/Jeonghun/rnd/PoC/blender_drive/json/poc_shapekey_01_shape_keys.json'

with open(a_file_path, 'r') as f:
    a_data = json.load(f)

with open(b_file_path, 'r') as f:
    b_data = json.load(f)

# a 파일에서 필요한 정보 추출
shape_key_name = a_data['data_path'].split('["')[1].split('"]')[0]  # "test_up"
object_name = a_data['variables'][0]['target_id_name']  # "con"

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
