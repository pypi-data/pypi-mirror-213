def check_your_BMI(height, weight):
    '''height_신장(키 cm)와 weight_몸무게(Kg)을 입력하면,
    자신의 BMI 계수와 그에 따른 등급을 출력'''
    height = height * (1 / 100)     # cm단위로 입력을 받고, 미터 단위의 변환

    bmi = weight / height ** 2      # BMI 지수 계산 공식
                                    # 지수에 따른 등급 판별 로직
    if bmi < 20:
        grade_bmi = "저체중"
    elif bmi >= 20 and bmi < 25:
        grade_bmi = "정상"
    elif bmi >= 25 and bmi < 30:
        grade_bmi = "과체중"
    elif bmi > 30:
        grade_bmi = "비만"

    print(f"당신의 bmi 지수는 {bmi}로, {grade_bmi}입니다.")