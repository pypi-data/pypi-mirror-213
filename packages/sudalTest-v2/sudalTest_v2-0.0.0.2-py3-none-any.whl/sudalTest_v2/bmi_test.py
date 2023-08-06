def print_test1():
    weight=float(input("당신의 몸무게는:"))
    height=float(input("당신의 키는:"))
    bmi=weight/((height/100)**2)
    print("당신의 bmi지수는:",round(bmi,2))

    if 0<bmi<18.5:
        print("저체중입니다.")
    elif 18.5<bmi<23:
        print("정상입니다.")
    elif 23<bmi<25:
        print("과체중입니다.")
    elif 25<bmi<30:
        print("경도비만입니다.")
    else:
        print("중등도비만입니다.")

print_test1()