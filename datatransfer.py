import glob
import os
list = glob.glob("*.csv")
print(list)
for i in range(len(list)):
    x = "mv "+list[i]+" csvfile"
    print(x)
    os.system(x)
print("O.K.")
