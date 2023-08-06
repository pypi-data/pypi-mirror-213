def print_test2():
    '''테스트 문장을 출력합니다.'''
    print('Hi, This is Test2')

from proj00 import test1, test2

test1.print_test1()

test2.print_test2()

from proj00 import bmi

h, w = 175, 66

bmi.printMessage(h, w)