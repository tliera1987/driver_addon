bl_info = {
    "name": "Delete Object Drivers",
    "blender": (2, 80, 0),
    "category": "Object",
    "description": "Delete shape key drivers or all drivers from an object",
    "author": "Your Name",
    "version": (1, 0),
    "location": "View3D > Sidebar > Driver Tools",
}

import bpy

def delete_shape_key_drivers(obj):
    if not (obj.data.shape_keys and obj.data.shape_keys.animation_data):
        return
    drivers = obj.data.shape_keys.animation_data.drivers
    for fcurve in drivers:
        if fcurve.data_path.startswith("key_blocks["):
            drivers.remove(fcurve)

def delete_all_object_drivers(obj):
    if obj.animation_data:
        drivers_to_remove = list(obj.animation_data.drivers)
        for driver in drivers_to_remove:
            obj.animation_data.drivers.remove(driver)

class DeleteShapeKeyDriversOperator(bpy.types.Operator):
    """Delete Shape Key Drivers"""
    bl_idname = "object.delete_shape_key_drivers"
    bl_label = "Delete Shape Key Drivers"

    def execute(self, context):
        delete_shape_key_drivers(context.active_object)
        self.report({'INFO'}, "Shape Key Drivers Deleted")
        return {'FINISHED'}

class DeleteAllObjectDriversOperator(bpy.types.Operator):
    """Delete All Object Drivers"""
    bl_idname = "object.delete_all_object_drivers"
    bl_label = "Delete All Object Drivers"

    def execute(self, context):
        delete_all_object_drivers(context.active_object)
        self.report({'INFO'}, "All Object Drivers Deleted")
        return {'FINISHED'}

class DriverDeletionPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Driver Deletion Tools"
    bl_idname = "OBJECT_PT_driver_deletion"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Driver Tools'

    def draw(self, context):
        layout = self.layout
        layout.label(text="<현재 드라이버를 초기화>")
        # 새로운 행 생성
        row = layout.row()
        layout.label(text="쉐이프키가 있는 오브젝트를 선택해야합니다")
        row = layout.row()
        layout.label(text="1번>2번 모두 해야 완전히 초기화 됩니다.")
        row = layout.row()
        # 행을 두 개의 섹션으로 나누기 (각각 50%의 너비를 가짐)
        split = row.split(factor=0.5)        
        # 첫 번째 섹션에 첫 번째 버튼 배치
        split.operator(DeleteShapeKeyDriversOperator.bl_idname, text="1.Delete Shape Keys")       
        # 두 번째 섹션에 두 번째 버튼 배치
        split.operator(DeleteAllObjectDriversOperator.bl_idname, text="2.Delete All Drivers")

def register():
    bpy.utils.register_class(DeleteShapeKeyDriversOperator)
    bpy.utils.register_class(DeleteAllObjectDriversOperator)
    bpy.utils.register_class(DriverDeletionPanel)

def unregister():
    bpy.utils.unregister_class(DeleteShapeKeyDriversOperator)
    bpy.utils.unregister_class(DeleteAllObjectDriversOperator)
    bpy.utils.unregister_class(DriverDeletionPanel)

if __name__ == "__main__":
    register()
