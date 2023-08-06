def calculate_bmi () :
    height = float(input("키를 입력하세요 : "))/100
    weight = float(input("몸무게를 입력하세요 : "))

    bmi = weight/(height**2)
    my_bmi = ''

    if bmi <=18.5 :
        my_bmi = '저체중'
    elif 18.5<bmi<23 :
        my_bmi = '정상'
    elif 23<=bmi<25 :
        my_bmi = '과체중'
    elif 25<= bmi :
        my_bmi = '비만'

    return my_bmi

