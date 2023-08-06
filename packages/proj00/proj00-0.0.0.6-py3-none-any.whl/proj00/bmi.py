
def calculateBMI(height, weight):
    return (weight/((height/100)**2))

def BMItoString(bmi):
    string = ''
    if bmi <= 18.5:
        string = '저체중'
    elif bmi <= 22.9:
        string = '정상'
    elif bmi <= 24.9:
        string = '과체중'
    else:
        string = '비만'
    return string

def returnMessage(bmi):
    return f'MY BMI{bmi}\n나의BMI(신체질량지수)는 {bmi:f=.1f}이고, {BMItoString(bmi)}입니다.'

def printBMIMessage(bmi):
    print(returnMessage(bmi))


def printHeightWeightMessage(height, weight):
    bmi = calculateBMI(height, weight)
    print(returnMessage(bmi))


