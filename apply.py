import bpy

# 컨트롤러 애니메이션을 쉐입키 애니메이션으로 변환하는 기능

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
        for fcurve in context.object.data.shape_keys.animation_data.drivers.values():
            context.object.data.shape_keys.keyframe_insert(fcurve.data_path)
    frame += 1
