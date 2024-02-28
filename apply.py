bl_info = {
    "name": "Convert Controller to Shape Key Animation",
    "blender": (2, 80, 0),
    "category": "Animation",
    "description": "Convert controller animation to shape key animation for the active object",
    "author": "Your Name",
    "version": (1, 0),
    "location": "View3D > Sidebar > Animation Tools",
}

import bpy

def convert_controller_to_shape_key_animation(context):
    scene = context.scene
    max_frame = 0

    for obj in scene.objects:
        if obj.animation_data and obj.animation_data.action:
            for fcurve in obj.animation_data.action.fcurves:
                for keyframe_point in fcurve.keyframe_points:
                    if keyframe_point.co.x > max_frame:
                        max_frame = keyframe_point.co.x

    frame = scene.frame_start
    while frame <= max_frame:
        scene.frame_set(frame)
        obj = context.active_object
        if obj and obj.data.shape_keys:
            for fcurve in obj.data.shape_keys.animation_data.drivers:
                obj.data.shape_keys.keyframe_insert(fcurve.data_path)
        frame += 1

class OBJECT_OT_ConvertControllerToShapeKey(bpy.types.Operator):
    """Convert Controller to Shape Key Animation"""
    bl_idname = "object.convert_controller_to_shape_key"
    bl_label = "Convert Controller to Shape Key"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and \
               context.active_object.data.shape_keys is not None

    def execute(self, context):
        convert_controller_to_shape_key_animation(context)
        self.report({'INFO'}, "Converted controller animation to shape key animation.")
        return {'FINISHED'}

class VIEW3D_PT_ControllerToShapeKey(bpy.types.Panel):
    """Panel to convert controller animation to shape key animation"""
    bl_label = "Controller to Shape Key"
    bl_idname = "VIEW3D_PT_controller_to_shape_key"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Animation Tools'

    def draw(self, context):
        layout = self.layout
        layout.label(text="도프 시트에서 액션을 활성화 후, 적용할 오브젝트를 선택 후 작동")
        layout.operator(OBJECT_OT_ConvertControllerToShapeKey.bl_idname)

def register():
    bpy.utils.register_class(OBJECT_OT_ConvertControllerToShapeKey)
    bpy.utils.register_class(VIEW3D_PT_ControllerToShapeKey)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_ConvertControllerToShapeKey)
    bpy.utils.unregister_class(VIEW3D_PT_ControllerToShapeKey)

if __name__ == "__main__":
    register()