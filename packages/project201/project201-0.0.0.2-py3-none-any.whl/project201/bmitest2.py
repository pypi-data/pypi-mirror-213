'''BMI 지수를 계산하는 기능'''
def calculate_bmi(height, weight):
    var = height * 0.01
    result = round(weight / (var * var), 1)
    return result


'''BMI 지수에 따라 적절한 멘트를 주는 기능'''
def get_bmi_comment(result):
    if result <= 18:
        return f"당신의 BMI 지수는 {result}이며 저체중입니다."
    elif 18.5 <= result <= 22.9:
        return f"당신의 BMI 지수는 {result}이며 정상입니다."
    elif 23.0 <= result <= 24.9:
        return f"당신의 BMI 지수는 {result}이며 과체중입니다."
    elif result > 25.0:
        return f"당신의 BMI 지수는 {result}이며 비만입니다."


'''BMI 지수는 보여주는 기능'''
def show_bmi():
    height = int(input("키 입력: "))
    weight = int(input("몸무게 입력: "))
    bmi_result = calculate_bmi(height, weight)
    comment = get_bmi_comment(bmi_result)
    print(comment)
