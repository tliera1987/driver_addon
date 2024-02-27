import bpy
import json
from scipy.optimize import least_squares

# 파일 경로
a_file_path = '/Users/hun/GoodGangLabs Dropbox/Individuals/Jeonghun/project/kikiz/3d/blender/json/kz_avatar_kikiz_driver_00.json'  
b_file_path = '/Users/hun/GoodGangLabs Dropbox/Individuals/Jeonghun/project/kikiz/3d/blender/json/kz_avatar_kikiz_facecontroller_script_04_01_shape_keys.json' 

# 파일 로드
with open(a_file_path, 'r') as file:
    a_data = json.load(file)

with open(b_file_path, 'r') as file:
    b_data = json.load(file)

same_bone_shape = []
shape_keys_weights = {}

# Iterate through the JSON data to find shape keys that use the same bone
for item in a_data:
    # Identify the bone used by checking the variables in the driver's expression
    used_bones = set()
    for variable in item.get('variables', []):
        bone_name = variable.get('data_path').split('"')[1] if 'data_path' in variable and 'pose.bones[' in variable.get('data_path') else None
        if bone_name:
            used_bones.add(bone_name)

    # If only one bone is used for the driver, consider its shape keys as using the same bone
    if len(used_bones) == 1:
        shape_key_name = item['data_path'].split('"')[1]
        if shape_key_name not in same_bone_shape:
            same_bone_shape.append(shape_key_name)
            shape_keys_weights[shape_key_name] = item['expression']

# Results
print(same_bone_shape)
print(shape_keys_weights)

animation_values_by_frame = {}

for shape_key in same_bone_shape:
    if shape_key in b_data:
        # Each value in the list corresponds to a frame, starting from frame 1
        animation_values = b_data[shape_key]
        # Creating a list of tuples (frame number, value)
        animation_values_by_frame[shape_key] = [(frame + 1, value) for frame, value in enumerate(animation_values)]

print(animation_values_by_frame)

# expressions_updated = {
#     'mouthUpperUpLeft': lambda var, var_001: (var * 30.04) + (-var_001 * 30.04),
#     'mouthUpperUpRight': lambda var, var_001: (var * 30.04) + (var_001 * 30.04),
#     'mouthLowerDownLeft': lambda var, var_001: (-var * 30.04) + (-var_001 * 30.04),
#     'mouthLowerDownRight': lambda var, var_001: (-var * 30.04) + (var_001 * 30.04)
# }

# # Loading the animation values for each shape key from the 'b' file previously loaded
# animation_values_b_file = {
#     'mouthUpperUpLeft': [0.0, 0.008988, 0.034644, 0.075008, 0.128119, 0.192015, 0.264736, 0.34432, 0.428807, 0.516235, 0.604644, 0.692072, 0.776559, 0.856143, 0.928863, 0.992759, 1.0, 1.0, 1.0, 1.0],
#     'mouthUpperUpRight': [0.0, 0.005883, 0.022676, 0.049095, 0.083857, 0.125679, 0.173276, 0.225366, 0.280665, 0.337889, 0.395754, 0.452979, 0.508277, 0.560367, 0.607964, 0.649786, 0.684548, 0.710968, 0.72776, 0.733643],
#     # Placeholder values for mouthLowerDownLeft and mouthLowerDownRight, actual values should be used
#     'mouthLowerDownLeft': [0.0] * 20,
#     'mouthLowerDownRight': [0.0] * 20
# }

# Function to calculate the variable values for each frame that satisfy all the expressions
def find_variables_per_frame(expressions, animation_values):
    frame_results = {}

    # For each frame, try to find the variable values that satisfy the expressions for all shape keys
    for frame in range(20):  # Assuming 20 frames based on the provided animation values
        # Extract the target values for this frame for each shape key
        target_values = {key: animation_values[key][frame] for key in animation_values}

        # Define a function to compute residuals between calculated and target shape key values
        def residuals(vars):
            var, var_001 = vars
            return [expressions[key](var, var_001) - target_value for key, target_value in target_values.items()]

        # Initial guess for the optimization
        initial_guess = [0, 0]

        # Perform the optimization
        result = least_squares(residuals, initial_guess)

        # Store the result
        frame_results[frame + 1] = result.x

    return frame_results

# Calculate variable values for each frame
variables_per_frame = find_variables_per_frame(shape_keys_weights, animation_values_by_frame)
print(variables_per_frame)