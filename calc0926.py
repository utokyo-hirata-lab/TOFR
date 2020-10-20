import glob
import pandas as pd
import numpy as np
import csv

filelist = glob.glob("*.csv")
print(filelist)


filelist_sorted = []
num = 0
for i in range(len(filelist)):
    for item in filelist:
        x = item
        y = x.split("_")
        z = y[1].split(".")
        f_num =z[0].split("t")[2]
        if f_num == "":
            f_num = "0"
        else:
            f_num = f_num
#        print(f_num)

        if int(i) == int(f_num):
            filelist_sorted.append(item)
        else:
            continue
print(filelist_sorted)



g = open("data_summation.csv", 'w')
writer = csv.writer(g, lineterminator='\n')

csvlist = []
csvlist.append("Sample#")

for i in range(len(filelist_sorted)):
    df = pd.read_csv(filelist_sorted[i])
    column = df.columns.values
    if i == 0:
        for j in range(len(column)-2):
            csvlist.append(column[j+1])
        writer.writerow(csvlist)
    else:
        print("")
    csvlist = []
#    print(column)
    csvlist.append(filelist_sorted[i])

    for i in range(len(column)-2):
        #print(df[column[i+1]])
        s = np.sum(df[column[i+1]])
        csvlist.append(s)
    writer.writerow(csvlist)
g.close()
print("O.K.")
