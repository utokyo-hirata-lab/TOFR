# ナノ粒子計測時、バックグラウンド＋溶存成分の平均信号強度を見積もって、減算するよ（粒子本来の信号強度を推定するため）
# マイナス値は0で出力されるよ

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as tic
from matplotlib import rcParams
import numpy as np
import pathlib

mode = "calc"  # "calc" = estimate blank+ionic, "blank" = subtract blank

sample = "sample"  # type X for "X_Y.csv"
blank = "blank"  # type X for "X_Y.csv"
label1 = ["_1","_2","_3"]  # type _Y for "X_Y.csv"
label2 = "_bl"  # "" for > 0 signals, "_0" for >= 0 signals, "_bl" for >= 0 signals & ionic subtraction only


# threshold level (baseline calc)
n = 3
#n = [3,3,3,3,3,3,3,1,1]
# number of bins
bin = 60

plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.weight"] = "bold"
plt.rcParams["axes.linewidth"] = 7
plt.rcParams["xtick.labelsize"] = 40
plt.rcParams["ytick.labelsize"] = 40
plt.rcParams["xtick.direction"] = "out"
plt.rcParams["ytick.direction"] = "out"
plt.rcParams["xtick.major.size"] = 15
plt.rcParams["ytick.major.size"] = 15
plt.rcParams["xtick.minor.size"] = 12
plt.rcParams["ytick.minor.size"] = 12
plt.rcParams["xtick.major.pad"] = 5
plt.rcParams["ytick.major.pad"] = 5
plt.rcParams["xtick.minor.pad"] = 3
plt.rcParams["ytick.minor.pad"] = 3
plt.rcParams["xtick.major.width"] = 7
plt.rcParams["ytick.major.width"] = 7
plt.rcParams["xtick.minor.width"] = 5
plt.rcParams["ytick.minor.width"] = 5


folder = "calc_datasheets/{}{}".format(sample, label2)
pathlib.Path(folder).mkdir(parents=True, exist_ok=True)
print(folder)


datasheet_blank = "{}.csv".format(blank)
df_blank = pd.read_csv(datasheet_blank, low_memory=False)
datalist_blank = list(df_blank[:0])

blank_avg_list = []
#blank_thres_list = []
for i in range(1, len(datalist_blank)-1):
    isotope_i = df_blank[datalist_blank[i]]
    #isotope_i_nonzero = []
    #for j in isotope_i:
        #if positive(j, 0):
        #isotope_i_nonzero.append(j)
    blank_avg_i = isotope_i.sum() / len(isotope_i)
    blank_avg_list.append(blank_avg_i)
    #blank_stdev_i = ((sum((np.array(isotope_i_nonzero) - blank_avg_i) ** 2)) / len(isotope_i_nonzero)) ** (1/2)
    #blank_thres_i = blank_avg_i + n * blank_stdev_i
    #blank_thres_i = blank_avg_i + n[i-1] * blank_stdev_i
    #blank_thres_list.append(blank_thres_i)
print(blank_avg_list)
#print(blank_thres_list)
print("blank calc done")

for run in range(0, len(label1)):
    datasheet1 = "{}{}.csv".format(sample, label1[run])
    csv_title1 = "{}{}_{}sd_NP{}.csv".format(sample, label1[run], n, label2)
    csv_title2 = "{}{}_{}sd_NP_stdev{}.csv".format(sample, label1[run], n, label2)
    fig_title1 = "{}{}_{}sd_baselines_barplots{}.png".format(sample, label1[run], n, label2)
    fig_title2 = "{}{}_{}sd_tra_baselines{}.png".format(sample, label1[run], n, label2)
    if mode == "blank":
        csv_title1 = "{}{}_{}sd_NP{}_blank.csv".format(sample, label1[run], n, label2)
        csv_title2 = "{}{}_{}sd_NP_stdev{}_blank.csv".format(sample, label1[run], n, label2)
        fig_title1 = "{}{}_{}sd_baselines_barplots{}_blank.png".format(sample, label1[run], n, label2)
        fig_title2 = "{}{}_{}sd_tra_baselines{}_blank.png".format(sample, label1[run], n, label2)

    # extract Positives
    def positive(x, y):
        if label2 == "":
            return x > y
        if label2 == "_0" or label2 == "_bl":
            return x >= y

    # data
    #df_blank = pd.read_csv(datasheet_blank, low_memory=False)
    #datalist_blank = list(df_blank[:0])
    df1 = pd.read_csv(datasheet1, low_memory=False)
    datalist1 = list(df1[:0])

    time = df1[datalist1[0]]

    # determine threshold
    #blank_avg_list = []
    #blank_thres_list = []
    #for i in range(1, len(datalist_blank)-1):
        #isotope_i = df_blank[datalist_blank[i]]
        #isotope_i_nonzero = []
        #for j in isotope_i:
            #if positive(j, 0):
            #isotope_i_nonzero.append(j)
        #blank_avg_i = isotope_i.sum() / len(isotope_i)
        #blank_avg_list.append(blank_avg_i)
        #blank_stdev_i = ((sum((np.array(isotope_i_nonzero) - blank_avg_i) ** 2)) / len(isotope_i_nonzero)) ** (1/2)
        #blank_thres_i = blank_avg_i + n * blank_stdev_i
        #blank_thres_i = blank_avg_i + n[i-1] * blank_stdev_i
        #blank_thres_list.append(blank_thres_i)
    #print(blank_avg_list)
    #print(blank_thres_list)
    #print("blank calc done")

    # csv
    import csv
    f1 = open("{}/{}".format(folder, csv_title1), "w")
    f2 = open("{}/{}".format(folder, csv_title2), "w")
    writer1 = csv.writer(f1)
    writer2 = csv.writer(f2)
    csvlist = []
    for i in range(0, len(datalist1)-1):
        csvlist.append(datalist1[i])
    writer1.writerow(csvlist)
    writer2.writerow(csvlist)
    f1.close()
    f2.close()

    # figures
    fig1 = plt.figure(figsize = (60, 10 * np.ceil(len(datalist1)/3)), linewidth=10, tight_layout=True)
    fig2 = plt.figure(figsize = (60, 10 * np.ceil(len(datalist1)/3)), linewidth=10, tight_layout=True)

    # search for outliers (NPs)
    DF1 = pd.read_csv("{}/{}".format(folder, csv_title1))
    DF2 = pd.read_csv("{}/{}".format(folder, csv_title2))
    for i in range(0, len(datalist1)-1):
        DF1[datalist1[i]] = df1[datalist1[i]]
        DF2[datalist1[i]] = df1[datalist1[i]]

    for i in range(1, len(datalist1)-1):
    #for i in range(1, 2):
        isotope_i = DF1[datalist1[i]]
        particle_stdev = DF2[datalist1[i]]

        if mode == "blank":
            avg_i = blank_avg_list[i-1]
            thres_i = avg_i * 5

        if mode == "calc":
            isotope_i_bkg = []
            for j in isotope_i:
                if positive(j, 0):
                    isotope_i_bkg.append(j)

            while True:
                avg_i = sum(isotope_i_bkg) / len(isotope_i_bkg)
                stdev_i = ((sum((np.array(isotope_i_bkg) - avg_i) ** 2)) / len(isotope_i_bkg)) ** (1/2)
                thres_i = avg_i + n * stdev_i
        #        thres_i = avg_i + n[i-1] * stdev_i
                print(avg_i, thres_i)

                NP_discriminated = []
                bkg = []
                for k in isotope_i_bkg:
                    if k <= thres_i:
                        bkg.append(k)
                    else:
                        NP_discriminated.append(k)
                isotope_i_bkg = bkg

                if NP_discriminated == []:
                    break

        x_range = max(isotope_i) - min(isotope_i)
        each_cps = (x_range / bin) * np.floor(np.array(isotope_i) / (x_range / bin))
        cps_list = each_cps.tolist()

        cps_list_floor = []
        events_floor_list = []
        for J in range(int(np.array(cps_list).min() / (x_range / bin)), int(np.array(cps_list).max() / (x_range / bin)) + 1):
            J_floor = J * (x_range / bin)
            cps_list_floor.append(J_floor)

            events_sum = 0
            for index in range (0, len(cps_list)):
                if cps_list[index] == J_floor:
                    events_sum = events_sum + 1
            events_floor_list.append(events_sum)

        # plot
        ax1 = fig1.add_subplot(np.ceil(len(datalist1)/3), 3, i)
        ax1.bar(cps_list_floor, events_floor_list, width = (x_range / bin) * 0.8, align="edge", bottom=None, color="grey", label="{}".format(datalist1[i].strip("'[]+")))
        ax1.axvline(x = avg_i, ymin=0, ymax=1, color="orange", ls="--", linewidth=10)
        #ax1.get_xaxis().set_major_locator(tic.MultipleLocator((x_range / bin) * 2))
        ax1.set_yscale("log")
        ax1.set_xlabel("Signal Intensity [cps]", fontsize=40, fontname="Arial", fontweight="bold")
        ax1.tick_params(axis="x", which="major", direction="out", length=15, pad=5, labelsize=40)
        ax1.set_ylabel("Number of Events", fontsize=40, fontname="Arial", fontweight="bold")
        ax1.tick_params(axis="y", which="major", direction="out", length=15, pad=5, labelsize=40)
        ax1.set_xlim(0, max(cps_list) + (x_range / bin))
        ax1.set_ylim(1, max(events_floor_list) * 1.5)
        ax1.grid()
        ax1.legend(fontsize=40, loc="upper right")
        ax1.set_axisbelow(True)

        ax2 = fig2.add_subplot(np.ceil(len(datalist1)/3), 3, i)
        ax2.plot(time, isotope_i, marker="None", ls="-", lw=5, color="black", label="{}".format(datalist1[i].strip("'[]+")))
        ax2.axhline(y = avg_i, xmin=0, xmax=1, color="orange", ls="--", linewidth=10)
        #ax1.get_xaxis().set_major_locator(tic.MultipleLocator((x_range / bin) * 2))
        ax2.set_xlabel("Time [msec]", fontsize=40, fontname="Arial", fontweight="bold")
        ax2.tick_params(axis="x", which="major", direction="out", length=15, pad=5, labelsize=40)
        ax2.set_ylabel("Signal Intensity [cps]", fontsize=40, fontname="Arial", fontweight="bold")
        ax2.tick_params(axis="y", which="major", direction="out", length=15, pad=5, labelsize=40)
        ax2.set_xlim(0, 10)
        ax2.set_ylim(0, thres_i * 3)
        ax2.grid()
        ax2.legend(fontsize=40, loc="upper right")
        ax2.set_axisbelow(True)


        NPs = 0
        if label2 == "_bl":
            for m in range(0, len(isotope_i)):
                if isotope_i[m] <= avg_i:
                    isotope_i[m] = 0
                    particle_stdev[m] = 0
                else:
                    particle_stdev[m] = ((isotope_i[m] * 0.002) ** (1/2)) / 0.002
                    #isotope_i[m] = isotope_i[m] - avg_i
                    isotope_i[m] = isotope_i[m] - avg_i
                    NPs = NPs + 1
        else:
            for m in range(0, len(isotope_i)):
                if isotope_i[m] <= thres_i:
                    isotope_i[m] = 0
                    particle_stdev[m] = 0
                else:
                    particle_stdev[m] = ((isotope_i[m] * 0.002) ** (1/2)) / 0.002
                    isotope_i[m] = isotope_i[m] - avg_i
                    NPs = NPs + 1
        DF1[datalist1[i]] = isotope_i
        DF2[datalist1[i]] = particle_stdev

        print("number of particles = {}".format(NPs))
        print("NPs calc done ({}/{})".format(i, len(datalist1)-2))

    # fig output
    fig1.savefig("{}/{}".format(folder, fig_title1))
    fig2.savefig("{}/{}".format(folder, fig_title2))

    # csv output
    DF1.to_csv("{}/{}".format(folder, csv_title1), index=None)
    DF2.to_csv("{}/{}".format(folder, csv_title2), index=None)

    print("{}{}{} end\n".format(sample, label1[run], label2))
