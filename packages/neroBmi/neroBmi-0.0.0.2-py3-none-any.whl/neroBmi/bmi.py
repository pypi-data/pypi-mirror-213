def bmiTest(w,h):
    return round((w / (h**2))*10000, 1)


height=float(input('키를 입력하세요: '))
weight=float(input('몸무게를 입력하세요: '))



bmi=bmiTest(weight, height)

print(f"MY BMI: {bmi}")

if bmi >25.0:
    print(f"나의BMI(신체질량지수)는 {bmi} 이고, 비만입니다.")
elif bmi > 22.9 and bmi <25.0:
    print(f"나의BMI(신체질량지수)는 {bmi} 이고, 과체중입니다.")
elif bmi > 18.4 and bmi < 23.0:
    print(f"나의BMI(신체질량지수)는 {bmi} 이고, 정상입니다.")
else:
    print(f"나의BMI(신체질량지수)는 {bmi} 이고, 저체중입니다.")
