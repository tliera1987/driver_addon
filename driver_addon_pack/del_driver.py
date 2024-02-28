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
