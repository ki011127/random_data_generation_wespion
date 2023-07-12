import matplotlib.pyplot as plt
import random
import pandas as pd
from openpyxl import load_workbook
location = 0.0
min_location = random.randrange(0,141)
exerRange = random.randrange(20,101)
min_location = 100
exerRange = 40
print(min_location)
print(exerRange)
isUp = -2
time = round(0.0,2)
count = 0
is_done=0
temp_time=0.0
rep = random.randrange(1,10)
rep = 10
rand_start_time = round(random.uniform(1.0,2.5), 2)
rand_ready_time = round(random.uniform(1.0,1.5),2)
def randomData(location, rep,min_location, exerRange):
    global count
    global isUp
    global time
    global is_done
    global temp_time
    if round(time,2)<= rand_start_time:
        location = 0
    elif location<= min_location and isUp == -2:
        #0.25~0.35
        location+=round(random.uniform(0.25,0.35),4)
        if location >= min_location:
            isUp = -1
            temp_time=time+0.01
    elif isUp == -1 and round(time,2)<=round(rand_ready_time+temp_time,2):
        choice = random.choices([1,2], [1,1])
        #print(choice) 
        if choice[0] == 1 :
            location+= round(random.uniform(0,0.03),4)
        else :
            location-= round(random.uniform(0,0.03),4)
        if round(time+0.01,2) > round(rand_ready_time+temp_time,2):
            isUp = 1 
    elif isUp == 1:
        choice = random.choices([1,2], [150*exerRange/40,1])
        #0.2~0.3
        if choice[0] == 1 and (location <= min_location+exerRange+20):
            location += round(random.uniform(0.2,0.3),4)
        else :
            print(location)
            print(min_location+exerRange+20)
            print("")
            location += round(random.uniform(0.2,0.3),4)
            isUp=0
            count+=1
            if count == rep:
                is_done = 1
    elif isUp == 0:
        choice = random.choices([1,2], [150*exerRange/40,1])
        #0.2~0.3
        if choice[0] == 1 and (location > min_location-20 and location!=0):
            location -= round(random.uniform(0.2,0.3),4)
            if(location<0):
                location = 0
        else :
            #location -= round(random.uniform(0.2,0.3),4)
            isUp=1
    
    time+=0.01
    return location


data = []
time_data = []
T_workbook = load_workbook("random_generator.xlsx" , data_only=True )
T_worksheet = T_workbook.active
col1 = "A"
col2 = "B"
num = 1
while is_done==0:
    location = randomData(location,rep,min_location, exerRange)
    time_data.append(round(time,2))
    data.append(round(location,4))
    T_worksheet[col1+str(num)] = round(location,4)
    T_worksheet[col2+str(num)] = time
    num = num +1
    
# DataFrame 생성

T_workbook.save("random_generator.xlsx") 

plt.plot(time_data,data)
plt.show()
