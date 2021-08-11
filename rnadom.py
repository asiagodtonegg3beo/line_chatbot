import random
import datetime

random.seed(datetime.datetime.now())
total = 20
li = [i for i in range(total)]
num=1
#print (random.sample(li, num)[0])

print(random.randint(0,total))