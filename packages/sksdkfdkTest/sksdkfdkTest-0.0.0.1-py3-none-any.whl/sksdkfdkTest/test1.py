def myBmi(h,w):
    '''BMI를 계산해주는 프로그램 입니다 키 몸무게 순으로 입력해주세요'''
    height = float(h)
    weight = float(w)

    bmi = round(weight / ((height/100)*(height/100)),1)
    bmi_percent = ""

    if bmi <= 18.5:
        bmi_percent = "저체중"
    elif bmi <= 22.9:
        bmi_percent = "정상"
    elif bmi <= 24.9:
        bmi_percent = "과체중"
    else:
        bmi_percent = "비만"

    my_bmi = "My BMI : {}".format(bmi)
    print(my_bmi.center(40))
    print("나의 BMI(신체질량지수)는 {}이고,{}입니다.".format(bmi,bmi_percent))