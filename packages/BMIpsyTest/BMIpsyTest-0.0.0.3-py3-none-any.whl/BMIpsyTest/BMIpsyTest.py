def BMIcheck():
    print("비만도 측정(BMI지수")
    print()
    print("BMI를 이용한 비만도 계산은 자신의 몸무게를 키의 제곱으로 나누는 것으로 공식은 Kg/m^.'''"
          "BMI가 18.5 이하면 저체중 / 18.2 ~ 22.9 사이면 정상 / 23.0 ~ 24.9 사이면 과체중 / 25.0 이상부터는 비만으로 판정")
    print("ex)키 170cm에 몸무게 73kg에면, 계산식: 73 / (1.7*1.7) = 25.26 -> 과체중")
    height = int(input("신장?"))
    weight = int(input("체중?"))
    BMI=weight/(height/100*height/100)
    BMIstate = ""
    if BMI <=18.5:
        BMIstate = "저체중"
    elif BMI<=22.9:
        BMIstate = "정상"
    elif BMI<=24.9:
        BMIstate = "과체중"
    else:
        BMIstate = "비만"
    print("MY BMI: {:.1f}\n나의BMI(신체질량지수)는 {:.1f}이고, {}입니다".format(BMI,BMI,BMIstate))


