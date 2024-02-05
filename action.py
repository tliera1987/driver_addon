import bpy

# 현재 선택된 오브젝트
selected_obj = bpy.context.object

# 선택된 오브젝트의 쉐이프키 블록 확인
if selected_obj.data.shape_keys:
    key_blocks = selected_obj.data.shape_keys.key_blocks
else:
    key_blocks = []
    print("선택된 오브젝트에 쉐이프키가 없습니다.")
    # 스크립트 종료
    exit()

# 쉐이프키에 연결된 드라이버를 통해 영향을 받는 오브젝트 찾기
affected_objects = set()  # 영향을 받는 오브젝트 저장을 위한 집합
for kb in key_blocks:
    if kb.animation_data:
        for driver in kb.animation_data.drivers:
            # 드라이버를 통해 영향을 받는 데이터 경로 찾기
            data_path = driver.data_path
            # 드라이버 변수 확인
            for var in driver.driver.variables:
                for target in var.targets:
                    if target.id:  # 드라이버로 연결된 ID가 있으면
                        affected_objects.add(target.id)  # 집합에 추가

# 각 영향을 받는 오브젝트에 대해 애니메이션 데이터 적용
for obj in affected_objects:
    if obj.type == 'MESH':  # 메쉬 타입 오브젝트인 경우에만 처리
        # 해당 오브젝트에 새 액션 생성 및 할당
        action = bpy.data.actions.new(name=f"{obj.name}_Action")
        obj.animation_data_create()
        obj.animation_data.action = action

        # 쉐이프키 애니메이션 데이터를 새 액션에 복사 (예시 코드와 유사한 로직 적용)
        for kb in key_blocks:
            if kb.animation_data:
                for fcurve in kb.animation_data.action.fcurves:
                    # 새 F-Curve 생성 (이 부분은 수정이 필요할 수 있음)
                    new_fcurve = action.fcurves.new(data_path=f'key_blocks["{kb.name}"].value', index=0)
                    for keyframe in fcurve.keyframe_points:
                        new_fcurve.keyframe_points.insert(frame=keyframe.co[0], value=keyframe.co[1])
                    new_fcurve.update()

print("쉐이프키 애니메이션을 영향을 받는 오브젝트의 액션으로 변환 완료")
