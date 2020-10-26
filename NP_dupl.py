# ナノ・ヨシクニの"CSV Out"で出てくるcsvの整理用
# 指定した同位体の信号が、""同時かつ一定以上の強度""で検出されたピークのみを選出＆まとめて出力

import pandas as pd
#import matplotlib.pyplot as plt
#import matplotlib.colors as plc
#import matplotlib.ticker as tic
#from matplotlib import rcParams
import numpy as np
import csv
import pathlib

data_num = 2
sample_label = "107_109_10_Aridus"
sample = ["{}{}".format(sample_label, str(i).zfill(4)) for i in range(1,data_num+1)]
print(sample)

# 測定した全ての同位体の数
meas_num = 4

# 信号の重なりを見たい同位体を指定
dupl_elements = ["Ag"]  # [Pt","Au]"て感じで入力．
dupl_mass = [[107,109]]  # [[195,196],[197]]て感じ（元素ごとに[]でまとめる）．
thres = [5,5]  # NP判別のしきい値（counts/event以上）（この値以上の信号積分値でNPと判別．）
thres_sum = [0,0]  # NP判別のしきい値（元素ごと合計カウント）

# 除外したい同位体を指定
excl_elements = []  # 同上
excl_mass = []  # 同上
excl_thres = []  # 除外したい同位体のしきい値（counts/event以下）
excl_thres_sum = []  # 除外したい同位体のしきい値（元素ごと合計カウント）

folder = "{}/{}{}{}{}".format(sample_label,dupl_elements,dupl_mass,thres,thres_sum)
pathlib.Path(folder).mkdir(parents=True, exist_ok=True)

"""------------------------------------------------------"""

dupl_block_all = []

for run in range(0, len(sample)):
    datasheet1 = "{}.csv".format(sample[run])
    print("\n{}".format(datasheet1))

    #isotopes = []
    #for i in range(0, len(elements)):
    #    isotopes_i = []
    #    for j in range(0, len(mass[i])):
    #        isotopes_i.append("{}({})".format(elements[i], mass[i][j]))
    #    isotopes.append(isotopes_i)
    #print(isotopes)

    #meas_isotopes = []
    #for i in range(0, len(meas_elements)):
    #    for j in range(0, len(meas_mass[i])):
    #        meas_isotopes.append("{}({})".format(meas_elements[i], meas_mass[i][j]))
    #print("\nmeasured: {}".format(meas_isotopes))
    #iso_num = len(meas_isotopes)

    df1 = pd.read_csv(datasheet1, low_memory=True)
    meas_iso = df1.iloc[1:2, 1:meas_num+1].values.tolist()[0]
    print("\nmeasured: {}".format(meas_iso))

    dupl_isotopes = []
    dupl_isotopes_2 = []
    for i in range(0, len(dupl_elements)):
        dupl_isotopes_2_i = []
        for j in range(0, len(dupl_mass[i])):
            dupl_isotopes.append("{}({})".format(dupl_elements[i], dupl_mass[i][j]))
            dupl_isotopes_2_i.append("{}({})".format(dupl_elements[i], dupl_mass[i][j]))
        dupl_isotopes_2.append(dupl_isotopes_2_i)
    print("duplication: {}".format(dupl_isotopes))

    dupl_index = []
    for i in dupl_isotopes:
        index_i = meas_iso.index(i)
        dupl_index.append(index_i)
    dupl_index_2 = []
    for i in dupl_isotopes_2:
        dupl_index_2_i = []
        for j in i:
            index_i = meas_iso.index(j)
            dupl_index_2_i.append(index_i)
        dupl_index_2.append(dupl_index_2_i)

    excl_isotopes = []
    excl_isotopes_2 = []
    for i in range(0, len(excl_elements)):
        excl_isotopes_2_i = []
        for j in range(0, len(excl_mass[i])):
            excl_isotopes.append("{}({})".format(excl_elements[i], excl_mass[i][j]))
            excl_isotopes_2_i.append("{}({})".format(excl_elements[i], excl_mass[i][j]))
        excl_isotopes_2.append(excl_isotopes_2_i)
    print("exclusion: {}\n".format(excl_isotopes))

    excl_index = []
    for i in excl_isotopes:
        index_i = meas_iso.index(i)
        excl_index.append(index_i)
    excl_index_2 = []
    for i in excl_isotopes_2:
        excl_index_2_i = []
        for j in i:
            index_i = meas_iso.index(j)
            excl_index_2_i.append(index_i)
        excl_index_2.append(excl_index_2_i)

    peak_title = df1[:0]
    peak_no = list(peak_title.loc[:, ~df1.columns.str.contains('^Unnamed')])
    #peak_no = [i.strip("'Peak No.") for i in peak_title]
    #peak_no = [int(i) for i in peak_no]

    block = [df1.iloc[:, (meas_num+2)*i:(meas_num+2)*i+(meas_num+1)].dropna() for i in range(0, len(peak_no))]
    #print(block[0].rename({(np.array(df1[:0])[6*i:6*i+(iso_num+1)].tolist() for i in range(0, len(peak_no))) : np.array(block[0][1:2]).tolist()}))
    #print(list(peak_title)[6*i:6*i+(iso_num+1)] for i in range(0, 1))

    dupl_block = []
    dupl_no = 0
    dupl_and_excl = 0
    for i in range(0, len(block)):
        dupl_iso_i = 0
        dupl_no_i = 0
        excl_iso_i = 0
        excl_no_i = 0
        for j in range(0, len(dupl_index_2)):
            dupl_iso_ij = 0
            dupl_sum_ij = 0
            for k in range(0, len(dupl_index_2[j])):
                total_ijk = block[i].iloc[:, dupl_index_2[j][k]+1][0]
                dupl_sum_ij = dupl_sum_ij + int(total_ijk)
                if int(total_ijk) >= thres[k]:
                    dupl_iso_ij = dupl_iso_ij + 1
            if dupl_iso_ij == len(dupl_index_2[j]):
                dupl_iso_i = dupl_iso_i + 1
            if dupl_sum_ij >= thres_sum[j]:
                dupl_no_i = dupl_no_i + 1
        for J in range(0, len(excl_index_2)):
            excl_iso_iJ = 0
            excl_sum_iJ = 0
            for K in range(0, len(excl_index_2[J])):
                ex_total_iJK = block[i].iloc[:, excl_index_2[J][K]+1][0]
                excl_sum_iJ = excl_sum_iJ + int(ex_total_iJK)
                if int(ex_total_iJK) <= excl_thres[K]:
                    excl_iso_iJ = excl_iso_iJ + 1
            if excl_iso_iJ == len(excl_index_2[J]):
                excl_iso_i = excl_iso_i + 1
            if excl_sum_iJ <= excl_thres_sum[J]:
                excl_no_i = excl_no_i + 1
        if (dupl_iso_i == len(dupl_index_2)) and (dupl_no_i == len(dupl_index_2)):
            dupl_no = dupl_no + 1
        if (dupl_iso_i == len(dupl_index_2)) and (dupl_no_i == len(dupl_index_2)) and ((excl_iso_i == len(excl_index_2)) or (excl_no_i == len(excl_index_2))):
            dupl_and_excl = dupl_and_excl + 1
            dupl_block.append(block[i])

    dupl_block_all = dupl_block_all + dupl_block

    print("overall: {} peaks".format(len(block)))
    print("duplication: {} peaks".format(dupl_no))
    if excl_elements != []:
        print("duplication w/o {}: {} peaks".format(excl_isotopes, dupl_and_excl))

    # csv
    if excl_elements == []:
        csv_title1 = "PeakList_{}_{}_{}_{}.csv".format(sample[run], dupl_isotopes, thres, thres_sum)
        #csv_title2 = "Overview_{}_{}_{}_{}.csv".format(sample[run], dupl_isotopes, thres, thres_sum)
    else:
        csv_title1 = "PeakList_{}_{}_{}_{}_no-{}_{}_{}.csv".format(sample[run], dupl_isotopes, thres, thres_sum, excl_isotopes, excl_thres, excl_thres_sum)
        #csv_title2 = "Overview_{}_{}_{}_{}_no-{}_{}_{}.csv".format(sample[run], dupl_isotopes, thres, thres_sum, excl_isotopes, excl_thres, excl_thres_sum)
    f1 = open("{}/{}".format(folder,csv_title1), "w")
    writer = csv.writer(f1)
    csvlist1 = []
    for i in range(1, len(dupl_block)+1):
        csvlist1.append("Peak No.{}".format(i))
        for j in range(0, meas_num):
            csvlist1.append("{}_{}".format(i, j+1))
        csvlist1.append("-NA{}-".format(i))
    writer.writerow(csvlist1)
    f1.close()

    #f2 = open("{}/{}".format(folder,csv_title2), "w")
    #writer = csv.writer(f2)
    #csvlist2 = ["Peak #"]
    #for i in range(0, len(meas_iso)):
        #csvlist2.append(meas_iso[i])
    #writer.writerow(csvlist2)
    #f2.close()

    DF1 = pd.read_csv("{}/{}".format(folder,csv_title1))
    #DF2 = pd.read_csv("{}/{}".format(folder,csv_title2))

    for i in range(0, len(dupl_block)):
        DF1[csvlist1[(meas_num+2)*i:(meas_num+2)*i+(meas_num+1)]] = dupl_block[i]
        DF1[csvlist1[(meas_num+2)*i+(meas_num+1)]] = ""
        #DF2.loc[i] = pd.Series(dupl_block[i].iloc[0:1, 0:meas_num+1].values.tolist()[0], index=csvlist2)
    #DF2[csvlist2[0]] = np.arange(1, len(dupl_block)+1)

    DF1.to_csv("{}/{}".format(folder,csv_title1), index=None)
    #DF2.to_csv("{}/{}".format(folder,csv_title2), index=None)

# extend csv
if excl_elements == []:
    csv_title3 = "Overview_{}_{}_{}_{}.csv".format(sample_label, dupl_isotopes, thres, thres_sum)
else:
    csv_title3 = "Overview_{}_{}_{}_{}_no-{}_{}_{}.csv".format(sample_label, dupl_isotopes, thres, thres_sum, excl_isotopes, excl_thres, excl_thres_sum)

f3 = open("{}/{}".format(folder,csv_title3), "w")
writer = csv.writer(f3)
csvlist3 = ["Peak #"]
for i in range(0, len(meas_iso)):
    csvlist3.append(meas_iso[i])
writer.writerow(csvlist3)
f3.close()

DF3 = pd.read_csv("{}/{}".format(folder,csv_title3))

for i in range(0, len(dupl_block_all)):
    DF3.loc[i] = pd.Series(dupl_block_all[i].iloc[0:1, 0:meas_num+1].values.tolist()[0], index=csvlist3)
DF3[csvlist3[0]] = np.arange(1, len(dupl_block_all)+1)

DF3.to_csv("{}/{}".format(folder,csv_title3), index=None)
print("")
