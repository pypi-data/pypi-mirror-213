height = int(input())
weight = int(input())
height2 = height / 100

def bmi_check():
    '''키와 몸무게를 입력받아 BMI 지수를 출력합니다. '''
    bmi = round(weight / (height2 * height2),1)
    if bmi >= 25.0:
        print(f'MY BMI : {bmi}')
        print(f'나의BMI(신체질량지수)는 {bmi} 이고, 비만입니다')
    elif bmi >= 23.0:
        print(f'MY BMI : {bmi}')
        print(f'나의BMI(신체질량지수)는 {bmi} 이고, 과체중입니다')
    elif bmi >= 18.5:
        print(f'MY BMI : {bmi}')
        print(f'나의BMI(신체질량지수)는 {bmi} 이고, 정상입니다')
    else:
        print(f'MY BMI : {bmi}')
        print(f'나의BMI(신체질량지수)는 {bmi} 이고, 저체중입니다')

bmi_check()