import bpy

def convert_controller_to_shape_key_animation():
    context = bpy.context
    scene = context.scene

    # 가장 큰 키 프레임 값을 찾기 위한 변수 초기화
    max_frame = 0

    # 씬에 있는 모든 오브젝트들의 애니메이션 데이터 확인
    for obj in scene.objects:
        if obj.animation_data and obj.animation_data.action:
            for fcurve in obj.animation_data.action.fcurves:
                for keyframe_point in fcurve.keyframe_points:
                    # 가장 큰 키 프레임 값 갱신
                    if keyframe_point.co.x > max_frame:
                        max_frame = keyframe_point.co.x

    # 현재 프레임 설정
    frame = scene.frame_start

    # 가장 큰 키 프레임 값까지만 반복
    while frame <= max_frame:
        scene.frame_set(frame)
        if context.object and context.object.data.shape_keys:
            for fcurve in context.object.data.shape_keys.animation_data.drivers:
                # 드라이버의 데이터 경로로 keyframe_insert를 호출합니다.
                context.object.data.shape_keys.keyframe_insert(fcurve.data_path)
        frame += 1

    print("Controller animation converted to shape key animation.")

# 함수 사용 예시
convert_controller_to_shape_key_animation()
