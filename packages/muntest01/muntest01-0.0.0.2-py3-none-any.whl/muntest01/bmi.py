def bmi(a,b):
    key = a*0.01
    bmi = round(b/(key*key),1)
    if bmi <23:
        result = '정상'
    elif bmi<25:
        result = '과체중'
    elif bmi<30:
        result = '경도비만'
    else:
        result = '중등도비만'
    print('MY BMI : {}'. format(bmi))
    print('나의BMI(신체질량지수)는 {}이고, {}입니다.'.format(bmi,result))