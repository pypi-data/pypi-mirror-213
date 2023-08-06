

def bmi(height, weight):
    return (weight/((height/100)**2))

def message(bmi):
    message = ''
    if bmi <= 18.5:
        message = '저체중'
    elif bmi <= 22.9:
        message = '정상'
    elif bmi <= 24.9:
        message = '과체중'
    else:
        message = '비만'
    return message