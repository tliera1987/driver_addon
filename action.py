import bpy
import json

# JSON 파일 경로
json_file_path = '/Users/hun/GoodGangLabs Dropbox/Individuals/Jeonghun/rnd/PoC/blender_drive/json/drivers_04.json'

# JSON 파일에서 드라이버 설정 읽기
with open(json_file_path, 'r') as file:
    driver_settings = json.load(file)

# 현재 선택된 오브젝트
source_obj = bpy.context.object
source_action = source_obj.animation_data.action if source_obj.animation_data else None

# 드라이버 설정에서 각 대상 오브젝트에 대해 처리
for setting in driver_settings:
    # 드라이버 설정에서 대상 오브젝트 이름을 가져옵니다.
    target_id_name = setting['variables'][0]['target_id_name']
    target_obj = bpy.data.objects.get(target_id_name)

    # 새 액션 생성 및 설정
    new_action_name = f"{source_obj.name}_to_{target_id_name}"
    new_action = bpy.data.actions.new(name=new_action_name)

    # 소스 액션의 F-Curves를 새 액션에 복사
    if source_action:
        for fcurve in source_action.fcurves:
            if 'key_blocks' in fcurve.data_path:
                new_fcurve = new_action.fcurves.new(data_path=fcurve.data_path, index=fcurve.array_index)
                for keyframe in fcurve.keyframe_points:
                    new_keyframe = new_fcurve.keyframe_points.insert(frame=keyframe.co[0], value=keyframe.co[1])
                    # 핸들 타입과 인터폴레이션 타입도 복사합니다.
                    new_keyframe.handle_left_type = keyframe.handle_left_type
                    new_keyframe.handle_right_type = keyframe.handle_right_type
                    new_keyframe.interpolation = keyframe.interpolation

    # 대상 오브젝트의 애니메이션 데이터에 새 액션을 할당
    if target_obj:
        target_obj.animation_data_create()
        target_obj.animation_data.action = new_action
        print(f"애니메이션 데이터가 {target_id_name} 오브젝트에 이식되었습니다.")
    else:
        print(f"대상 오브젝트 '{target_id_name}'을(를) 찾을 수 없습니다.")
