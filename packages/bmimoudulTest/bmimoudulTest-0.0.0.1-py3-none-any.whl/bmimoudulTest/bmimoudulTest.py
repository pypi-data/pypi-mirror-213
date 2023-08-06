height = int(input())
weight = int(input())

user = weight/((height/100)*(height/100))
if user<=18.5:
    print(f'나의 BMI(신체질량지수)는{round(user, 1)}이고,저체중입니다.')
elif user<18.5 or user<=22.8:
    print(f'나의 BMI(신체질량지수)는{round(user, 1)}이고,정상입니다.')
elif user<23.0 or user<=24.9:
    print(f'나의 BMI(신체질량지수)는{round(user, 1)}이고,과체중입니다.')
else:
    print(f'나의 BMI(신체질량지수)는{round(user, 1)}이고,비만입니다.')