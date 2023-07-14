import numpy as np
from scipy.interpolate import make_interp_spline
import matplotlib.pyplot as plt
import random
import pandas as pd
from openpyxl import load_workbook
location = 0.0
min_location = int(input("min : "))
exerRange = int(input("range : "))
duration = float(input("time per rep : "))
# min_location = 100
# exerRange = 40
print(min_location)
print(exerRange)
isUp = -2
time = round(0.0,2)
count = 0
is_done=0
temp_time=0.0
rep = random.randrange(3,7)
#rep = 6
rand_start_time = round(random.uniform(1.0,2.5), 2)
rand_ready_time = round(random.uniform(1.0,1.5),2)
def randomData(location, rep,min_location, exerRange):
    global count
    global isUp
    global time
    global is_done
    global temp_time
    if is_done==1:
        location-=round(random.uniform(0.25,0.35),4)
        if(location<=0):
            location = 0
            is_done=2
    elif round(time,2)<= rand_start_time:
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
        temp=0
        vibe = random.choices([1,2], [10,1])
        if location>min_location+1.4*exerRange:
            choice = [2]
        elif exerRange*0.6+min_location<location:
            choice = random.choices([1,2], [exerRange*3.0,1])
        else :
            choice = random.choices([1,2], [100000,1])
            temp=1
        #0.2~0.3
        if(temp==1 and choice[0]==2):
            print("up..")
            temp=0
        if choice[0] == 2:
            print("max")
            print(location)
            print("")
            isUp=0
            count+=1
        if vibe[0] == 2 :
            location -= round(random.uniform(0.0,0.1),4)
        else :
            location += round(random.uniform(0.2,0.3),4)
        if count == rep:
            is_done = 1
    elif isUp == 0:
        vibe = random.choices([1,2], [10,1])
        temp=0
        if min_location-0.4*exerRange >location:
            choice = [2]
        elif min_location+(exerRange*0.2)>location:
            choice = random.choices([1,2], [exerRange*3.0,1])
        else :
            choice = random.choices([1,2], [100000,1])
            temp=1
        if(temp==1 and choice[0]==2):
            print("down..")
            temp=0
        #0.2~0.3
        if choice[0] == 2 :
            isUp=1
            print("min")
            print(location)
            print("")
        if vibe[0] == 2 :
            location += round(random.uniform(0.0,0.1),4)
        else:
            location -= round(random.uniform(0.2,0.3),4)
        if(location<0):
            location = 0    
    time+=0.01
    return location


data = []
time_data = []
#T_workbook = load_workbook("random_generator.xlsx" , data_only=True )
#T_worksheet = T_workbook.active
col1 = "A"
col2 = "B"
num = 1
while is_done==0 or is_done==1:
    location = randomData(location,rep,min_location, exerRange)
    time_data.append(round(time,2))
    data.append(round(location,4))
    #T_worksheet[col1+str(num)] = round(location,4)
    #T_worksheet[col2+str(num)] = time
    num = num +1
    
# DataFrame ?��?��

#T_workbook.save("random_generator.xlsx") 

save_data = {'location': data, 'time':time_data}
save_data = pd.DataFrame(save_data)
save_data.to_excel(excel_writer='random_generator.xlsx')

plt.plot(time_data, data)

plt.show()