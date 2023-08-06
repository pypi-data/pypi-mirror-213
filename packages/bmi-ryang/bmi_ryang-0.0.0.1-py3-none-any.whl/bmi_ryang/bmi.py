def calculator():
    height = float(input("신장을 입력하세요(cm): "))
    weight = float(input("체중을 입력하세요(kg): "))

    bmi= weight/((height*0.01)*(height*0.01))

    if bmi<=18.5:
        result = "저체중입니다."

    elif bmi>18.5 and bmi<22.9:
        result = "정상입니다."

    elif bmi>23.0 and bmi<24.9:
        result = "과체중입니다."

    else:
        result = "비만입니다."

    return print(result)



