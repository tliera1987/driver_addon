import bpy

# 씬 내의 모든 오브젝트를 반복
for obj in bpy.data.objects:
    # 오브젝트가 애니메이션 데이터를 가지고 있는지 확인
    if obj.animation_data:
        # 오브젝트의 액션을 검사
        action = obj.animation_data.action
        if action:
            # 쉐입키 애니메이션인지 확인
            if not any(fcurve.data_path.startswith('key_blocks') for fcurve in action.fcurves):
                # 쉐입키 애니메이션이 아닌 경우 액션 삭제
                bpy.data.actions.remove(action)

        # NLA 트랙을 검사하여 쉐입키 애니메이션이 아닌 모든 트랙 삭제
        for track in obj.animation_data.nla_tracks:
            for strip in track.strips:
                if not any(fcurve.data_path.startswith('key_blocks') for fcurve in strip.action.fcurves):
                    track.strips.remove(strip)
