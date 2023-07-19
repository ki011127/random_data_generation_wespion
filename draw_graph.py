import numpy as np
from scipy.interpolate import make_interp_spline
import matplotlib.pyplot as plt
import random
import pandas as pd
from openpyxl import load_workbook
import sys

rep_data = [float(item) for item in sys.argv[1].split(',')]
rep_time = [float(item) for item in sys.argv[2].split(',')]


print(rep_data)
print(rep_time)
filename = "random_generator.xlsx"
df = pd.read_excel(filename, engine='openpyxl')
rep = 0
location = df.iloc[:, 1].tolist()
time = df.iloc[:, 2].tolist()
plt.plot(time,location)
plt.scatter(rep_time,rep_data,c='red', edgecolor='red',s=50)
for i, v in enumerate(rep_time):
    rep += 1
    plt.text(v,rep_data[i] - 10,'rep : '+str(rep),
             fontsize = 7,
             color='red',
             horizontalalignment='center',
             verticalalignment='bottom',
            )
plt.show()
# 결과 출력
# print("second:", column2_data)
# print("third:", column3_data)