def bmi():
  height = input('키(cm) :')
  weight = input('몸무게(kg) :')
  height = float(height)
  weight = float(weight)
  def bmi1(x,y):
    result = y/((x/100)**2)
    return round(result,1)

  my_bmi = bmi1(height,weight)
  if my_bmi <= 18.5:
    print(f'나의 BMI(신체질량지수)는 {my_bmi} 이고, 저체중입니다.')
  elif my_bmi <= 22.9 and my_bmi > 18.5:
    print(f'나의 BMI(신체질량지수)는 {my_bmi} 이고, 정상입니다.')
  elif my_bmi <= 24.9 and my_bmi > 22.9:
    print(f'나의 BMI(신체질량지수)는 {my_bmi} 이고, 과체중입니다.')
  elif my_bmi > 25.0:
    print(f'나의 BMI(신체질량지수)는 {my_bmi} 이고, 비만입니다.')