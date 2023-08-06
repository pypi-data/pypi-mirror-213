def bmi_cal(x,y):
    '''bmi 계산기 - x:체중 y:키'''
    bmi = round(x / (y*y) * 10000, 2)
    print("당신의 BMI수치는 {}입니다.".format(bmi))

    if bmi <= 18.5:
        print('저체중 입니다.')
    elif bmi < 23:
        print('정상 입니다.')
    elif bmi < 25:
        print('과체중 입니다.')
    else:
        print('비만 입니다.')




bmi_cal(65,169)