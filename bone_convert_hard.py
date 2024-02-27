expressions_updated = {
    'mouthUpperUpLeft': lambda var, var_001: (var * 30.04) + (-var_001 * 30.04),
    'mouthUpperUpRight': lambda var, var_001: (var * 30.04) + (var_001 * 30.04),
    'mouthLowerDownLeft': lambda var, var_001: (-var * 30.04) + (-var_001 * 30.04),
    'mouthLowerDownRight': lambda var, var_001: (-var * 30.04) + (var_001 * 30.04)
}

animation_values_b_file = {
    'mouthUpperUpLeft': [0.0, 0.008988, 0.034644, 0.075008, 0.128119, 0.192015, 0.264736, 0.34432, 0.428807, 0.516235, 0.604644, 0.692072, 0.776559, 0.856143, 0.928863, 0.992759, 1.0, 1.0, 1.0, 1.0],
    'mouthUpperUpRight': [0.0, 0.005883, 0.022676, 0.049095, 0.083857, 0.125679, 0.173276, 0.225366, 0.280665, 0.337889, 0.395754, 0.452979, 0.508277, 0.560367, 0.607964, 0.649786, 0.684548, 0.710968, 0.72776, 0.733643],
    'mouthLowerDownLeft': [0.0] * 20,
    'mouthLowerDownRight': [0.0] * 20
}

def find_variables_per_frame(expressions, animation_values):
    frame_results = {}

    for frame in range(20): 
        target_values = {key: animation_values[key][frame] for key in animation_values}

        def residuals(vars):
            var, var_001 = vars
            return [expressions[key](var, var_001) - target_value for key, target_value in target_values.items()]

        initial_guess = [0, 0]

        result = least_squares(residuals, initial_guess)

        frame_results[frame + 1] = result.x

    return frame_results

variables_per_frame = find_variables_per_frame(expressions_updated, animation_values_b_file)
variables_per_frame
