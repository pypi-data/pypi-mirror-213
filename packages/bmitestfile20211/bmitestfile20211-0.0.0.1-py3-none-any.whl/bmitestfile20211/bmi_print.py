from bmitestfile20211.bmitestfile20211.bmi_module import bmi_calculate, bmi_message

weight = float(input("체중(kg)을 입력하세요 :"))
height = float(input("키(cm)를 입력하세요 :"))

bmi = bmi_calculate(weight, height)
message = bmi_message(bmi)

print("당신의 BMI 지수는 {:1f}입니다.".format(bmi))
print("따라서 :", message)