import bpy

context = bpy.context
scene = context.scene
object = context.object

# 드라이버들의 애니메이션 프레임 범위를 구하는 함수
def get_drivers_frame_range(obj):
    max_frame = float('-inf')
    
    if obj.type == 'MESH' and obj.data.shape_keys and obj.data.shape_keys.animation_data:
        for fcurve in obj.data.shape_keys.animation_data.drivers:
            for keyframe_point in fcurve.keyframe_points:
                frame = keyframe_point.co[0]
                max_frame = max(max_frame, frame)
    
    return max_frame if max_frame != float('-inf') else None

# 드라이버들의 최대 프레임을 구함
max_driver_frame = get_drivers_frame_range(object)
if max_driver_frame is not None:
    end_frame = max_driver_frame
else:
    end_frame = scene.frame_end

# 시작 프레임부터 드라이버들의 최대 프레임까지 키 프레임 삽입
frame = scene.frame_start
while frame <= end_frame:
    scene.frame_set(frame)
    print("현재 프레임:", frame)  # 현재 프레임 출력
    if object.type == 'MESH' and object.data.shape_keys and object.data.shape_keys.animation_data:
        for fcurve in object.data.shape_keys.animation_data.drivers:
            print("data_path:", fcurve.data_path, "index:", -1)  # keyframe_insert에 사용되는 값 출력
            object.data.shape_keys.keyframe_insert(data_path=fcurve.data_path, index=-1)
    frame += 1
