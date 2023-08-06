height = int(input("키(cm)를 입력해주세요. ex) 165, 183, 172 등등\n"))
weight = int(input("체중(kg)을 입력해주세요. ex) 48, 76, 135 등등\n"))
bmi = round(weight/(height*0.01)**2, 1)
status = ""
if bmi < 18.5:
    status = "저체중"
elif 18.5 <= bmi < 23.0:
    status = "정상"
elif 23.0 <= bmi < 25.0:
    status = "과체중"
else:
    status = "비만"
print("MY BMI:{}".format(bmi))
print("나의 BMI(신체질량지수)는 {bmi}이고, {status}입니다.".format(bmi=bmi, status=status))
