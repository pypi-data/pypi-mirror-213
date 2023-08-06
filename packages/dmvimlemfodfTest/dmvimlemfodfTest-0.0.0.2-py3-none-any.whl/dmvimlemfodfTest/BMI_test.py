def BMI_check(weight, height):
    BMI = weight/((height*0.01)**2)
    list = ['저체중', '최적 범위', '과체중', '1급 비만', '2급 비만', '3급 비만']
    if BMI < 18.5:
        i = 0
    elif BMI < 25:
        i = 1
    elif BMI < 30:
        i = 2
    elif BMI < 35:
        i = 3
    elif BMI < 40:
        i = 4
    else:
        i = 5
    return print(f'당신의 BMI는 {int(BMI)}이며, {list[i]}입니다.')