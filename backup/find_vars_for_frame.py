def find_vars_for_frame(b_data_frame_values):
    from scipy.optimize import least_squares

    # 정의된 표현식에 대한 B-데이터 값
    expressions = ["mouthLowerDownLeft", "mouthLowerDownRight", "mouthUpperUpLeft", "mouthUpperUpRight"]

    # B-데이터 프레임 값과 모델 예측 사이의 차이를 계산하는 함수
    def model_diff(vars):
        var, var_001 = vars
        predictions = {
            "mouthLowerDownLeft": (-var * 30.04) + (-var_001 * 30.04),
            "mouthLowerDownRight": (-var * 30.04) + (var_001 * 30.04),
            "mouthUpperUpLeft": (var * 30.04) + (-var_001 * 30.04),
            "mouthUpperUpRight": (var * 30.04) + (var_001 * 30.04),
        }
        return [predictions[exp] - b_data_frame_values[exp] for exp in expressions]

    # 초기 추정값 및 변수 범위 설정
    initial_guess = [0.0, 0.0]
    bounds = ([-0.0333, -0.0333], [0.0333, 0.0333])

    # 최소 제곱 문제를 풀어 `var`와 `var_001` 찾기
    result = least_squares(model_diff, initial_guess, bounds=bounds)

    return result.x
