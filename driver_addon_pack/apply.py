bl_info = {
    "name": "Convert Controller to Shape Key Animation",
    "blender": (2, 80, 0),
    "category": "Animation",
    "description": "Convert controller animation to shape key animation",
    "author": "Your Name",
    "version": (1, 0),
    "location": "View3D > Sidebar > Animation Tools",
}

import bpy

class ConvertControllerToShapeKeyAnimationOperator(bpy.types.Operator):
    """Convert Controller Animation to Shape Key Animation"""
    bl_idname = "animation.convert_controller_to_shape_key"
    bl_label = "Convert Controller to Shape Key"
    
    def execute(self, context):
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
            if context.object and context.object.data.shape_keys:
                for fcurve in context.object.data.shape_keys.animation_data.drivers:
                    context.object.data.shape_keys.key_blocks[fcurve.data_path.split('"')[1]].keyframe_insert("value")
            frame += 1
        
        self.report({'INFO'}, "Controller Animation Converted to Shape Key Animation")
        return {'FINISHED'}

class ControllerToShapeKeyAnimationPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Controller to Shape Key Animation"
    bl_idname = "OBJECT_PT_controller_to_shape_key_animation"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Animation Tools'

    def draw(self, context):
        layout = self.layout
        layout.label(text="도프 시트에서 액션을 활성화 후, 적용할 오브젝트를 선택 후 작동")
        layout.operator(ConvertControllerToShapeKeyAnimationOperator.bl_idname)

def register():
    bpy.utils.register_class(ConvertControllerToShapeKeyAnimationOperator)
    bpy.utils.register_class(ControllerToShapeKeyAnimationPanel)

def unregister():
    bpy.utils.unregister_class(ConvertControllerToShapeKeyAnimationOperator)
    bpy.utils.unregister_class(ControllerToShapeKeyAnimationPanel)

if __name__ == "__main__":
    register()
