height=float(input("키를 입력하세요\n"))
weight=float(input("몸무게를 입력하세요\n"))
bmi=round((float(weight/(height/100)**2)),2)

if bmi <= 18.5:
    print("MY BMI:{}\n 나의 BMI(신체질량지수)는{}이고, 저체중입니다.".format(bmi,bmi))
elif bmi <=22.9:
    print("MY BMI:{}\n 나의 BMI(신체질량지수)는{}이고, 정상입니다.".format(bmi,bmi))
elif bmi <=24.9:
    print("MY BMI:{}\n 나의 BMI(신체질량지수)는{}이고, 과체중입니다.".format(bmi,bmi))
else:
    print("MY BMI:{}\n 나의 BMI(신체질량지수)는{}이고, 비만입니다.".format(bmi,bmi))
