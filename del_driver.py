import bpy

def delete_shape_key_drivers(obj):
    # 쉐이프 키가 있는지 확인합니다.
    if not (obj.data.shape_keys and obj.data.shape_keys.animation_data):
        return
    
    # 쉐이프 키의 애니메이션 데이터에서 드라이버 목록을 가져옵니다.
    drivers = obj.data.shape_keys.animation_data.drivers
    
    # 모든 드라이버를 삭제합니다.
    for fcurve in drivers:
        # 드라이버가 쉐이프 키에 연결되어 있는지 확인합니다.
        if fcurve.data_path.startswith("key_blocks["):
            drivers.remove(fcurve)

# 사용 예시:
delete_shape_key_drivers(bpy.context.active_object)

def delete_all_object_drivers(obj):
    if obj.animation_data:
        # 드라이버를 삭제하기 전에 리스트에 담습니다. (삭제 도중 컬렉션을 변경하지 않기 위함)
        drivers_to_remove = list(obj.animation_data.drivers)
        for driver in drivers_to_remove:
            # 드라이버 제거
            obj.animation_data.drivers.remove(driver)

# 현재 선택된 오브젝트의 모든 드라이버를 삭제합니다.
delete_all_object_drivers(bpy.context.active_object)

