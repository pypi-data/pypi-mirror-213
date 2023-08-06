def bmi_calculate(weight, height) :
    """weight(몸무게)와 height(키)를 이용해 bmi를 구하는 함수"""
    bmi = weight / ((height/100) **2)
    return bmi

def bmi_message(bmi) :
    """bmi 지수에 따라 적절한 메세지를 출력하는 함수"""
    if bmi < 18.5 :
        return "저체중 입니다."
    elif bmi < 23 :
        return "정상 체중입니다."
    elif bmi < 25 :
        return "과체중입니다."
    else :
        return "비만입니다. "