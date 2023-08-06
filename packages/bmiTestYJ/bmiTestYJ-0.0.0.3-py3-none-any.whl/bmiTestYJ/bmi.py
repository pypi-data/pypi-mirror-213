height = float(input("신장 :"))
weight = float(input("몸무게 :"))

height2 = height / 100               # bmi 계산을 위한 단위 조정
bmi = weight / (height2 * height2)

def level(bmi_n):
    if 0 <= bmi_n <= 18.5:
        a = "저체중"
    elif bmi_n <= 22.9:
        a = "정상"
    elif bmi_n <= 24.9:
        a = "과체중"
    else:
        a = "비만"
    return a

print("MY BMI : {0:.1f}".format(bmi))
print("나의 BMI(신체질량지수)는 {0:.1f}이고, {1}입니다.".format(bmi, level(bmi)))