def start_Check():
    print('* ' * 23,
          '\n*                                           *\n'
          '*                                           *\n'
          '*           BMI 계산 프로그램입니다             *\n'
          '*                                           *\n'
          '*                                           *\n',
          '* ' * 23)

    height = float(input('당신의 키를 입력해주세요 (단위 : cm) : '))
    weight = float(input('당신의 몸무게를 입력해주세요 (단위 : kg) : '))
    bmi = weight / ((height/100)**2)
    if bmi < 18.6:
        print()
        print('당신의 BMI는 %.2f 입니다.' % bmi)
        print()
        print('당신은 저체중이니 좀 더 먹으세요 ㅋㅋ')
    elif 18.5 < bmi < 23:
        print()

        print('당신의 BMI는 %.2f 입니다.' % bmi)
        print()

        print('당신은 정상입니다?')
    elif 22.9 < bmi < 25:
        print()

        print('당신의 BMI는 %.2f 입니다.' % bmi)
        print()

        print('당신은 과체중이니 좀 덜 먹으세요 ㅋㅋ')
    elif bmi > 24.9:
        print()

        print('당신의 BMI는 %.2f 입니다.' % bmi)
        print()

        print('비만이니까 그만 드세요 ㅎㅎ')