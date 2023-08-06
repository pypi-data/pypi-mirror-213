def print_test2():
  import random

  print("주사위전사 게임에 오신걸 환영합니다")

  print("주사위를 굴려보자~")

  knife=2
  bow=3
  shield=2
  armor=3
  i=0

  user_hp=10
  for i in range(10):
    abc=[1,2,3,4,5,6]
    dice=random.choice(abc)

    if dice==1:
      print("운이 없네요 함정에 걸렸습니다.")
      user_hp=user_hp-6
      print(user_hp)
    if dice==2:
      print(f"{dice}가 나왔습니다.칼에 맞았습니다.")
      user_hp=user_hp-knife
      print(user_hp)
    if dice==3:
      print(f"{dice}가 나왔습니다.활에 맞았습니다.")
      user_hp=user_hp-bow
      print(user_hp)
    if dice==4:
      print(f"{dice}가 나왔습니다.방패를 얻었습니다!.")
      user_hp=user_hp+shield
      print(user_hp)
    if dice==5:
      print(f"{dice}가 나왔습니다.갑옷을 얻었습니다!.")
      user_hp=user_hp+armor
      print(user_hp)
    if dice==6:
      print("운이 좋으시군요! 구급상자를 얻었습니다.")
      user_hp=user_hp+6
      print(user_hp)
    if user_hp<=0:
      print("당신은 사망했습니다.")
      break


print_test2()