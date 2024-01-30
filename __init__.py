
class DriverPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "DriverAddon"
    bl_idname = "DRIVER_PT_SAVELOAD"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Driver_save_load' 

    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.label(text="DriverAddon")

        row = layout.row()
        row.label(text="Active object is: " + obj.name)
       


def register():
    bpy.utils.register_class(DriverPanel)


def unregister():
    bpy.utils.unregister_class(DriverPanel)


if __name__ == "__main__":
    register()
