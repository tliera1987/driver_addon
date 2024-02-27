import bpy

# 선택한 오브젝트
obj = bpy.context.active_object

# 쉐이프 키 데이터 확인
if obj.data.shape_keys:
    key_blocks = obj.data.shape_keys.key_blocks
    action = obj.data.shape_keys.animation_data.action if obj.data.shape_keys.animation_data else None

    if action:
        # 쉐이프 키의 fcurves를 선택합니다.
        for fcurve in action.fcurves:
            # fcurve의 data_path에서 쉐이프 키 블록 이름을 찾습니다.
            if any(kb.name in fcurve.data_path for kb in key_blocks):
                fcurve.select = True  # 해당 fcurve를 선택합니다.

        # Dope Sheet 에디터의 컨텍스트 오버라이드를 찾기
        area = None
        for area in bpy.context.screen.areas:
            if area.type == 'DOPESHEET_EDITOR':
                override = bpy.context.copy()
                override['area'] = area
                break

        # 선택된 쉐이프 키의 애니메이션 채널을 삭제
        if area:
            bpy.ops.anim.channels_delete(override)
        else:
            print("Dope Sheet 에디터 영역을 찾을 수 없습니다.")
    else:
        print("쉐이프 키에 애니메이션 액션이 없습니다.")

    # 쉐이프 키 값을 0으로 초기화
    for key_block in key_blocks:
        key_block.value = 0
    print("모든 쉐이프 키 값을 0으로 초기화했습니다.")

else:
    print("선택한 오브젝트에 쉐이프 키 데이터가 없습니다.")
