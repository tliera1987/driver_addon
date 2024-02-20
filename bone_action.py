import bpy
import json

#쉐이프 키 애니메이션을 액션 키 애니메이션으로 변환

# 파일 경로
# a = 드라이버 셋팅 저장 파일 
# b = 쉐입키 애니메이션 파일
a_file_path = '/Users/hun/GoodGangLabs Dropbox/Individuals/Jeonghun/project/kikiz/3d/blender/json/kz_avatar_kikiz_driver_00.json'  # 예시 경로, 실제 경로로 변경 필요
b_file_path = '/Users/hun/GoodGangLabs Dropbox/Individuals/Jeonghun/project/kikiz/3d/blender/json/kz_avatar_kikiz_facecontroller_script_02_shape_keys.json'  # 예시 경로, 실제 경로로 변경 필요

# 파일 a 로드
with open(a_file_path, 'r') as file:
    drivers_data = json.load(file)

# 파일 b 로드
with open(b_file_path, 'r') as file:
    shape_keys_data = json.load(file)

