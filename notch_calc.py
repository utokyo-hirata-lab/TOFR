import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tic
from matplotlib import rcParams
import pathlib

# Qmass filter or Notch
mode = "N"  # Q = Qmass filter, N = Notch

m_z = 40  # g/mol
m_z_notch_1 = 40
m_z_notch_2 = 17.6
m_z_notch_3 = 42
m_z_notch_4 = 32
notch_f = 0.985

m = m_z*0.001/(6.02214076 * (10**23))  # kg
m_notch_1 = notch_f * m_z_notch_1*0.001/(6.02214076 * (10**23))  # kg
m_notch_2 = notch_f * m_z_notch_2*0.001/(6.02214076 * (10**23))  # kg
m_notch_3 = notch_f * m_z_notch_3*0.001/(6.02214076 * (10**23))  # kg
m_notch_4 = notch_f * m_z_notch_4*0.001/(6.02214076 * (10**23))  # kg

if mode == "Q":
    Vacc = 20  # acceleration V toward z (negative) [V]
    e = 1.60217662 * (10**(-19))  # elementary charge
    U = 83  # qpole DC [V]
    V = 497  # qpole AC [V]
    W = 14.2 * (10**6)  # qpole RF [rad/s]
    r = 0.0026  # z-axis center ~ qpole [m]
    flight_t = 25  # flight time of ions in q-cell [µs]

if mode == "N":
    Vacc = 12  # acceleration V toward z (negative) [V]
    e = 1.60217662 * (10**(-19))  # elementary charge
    U = 0  # qpole DC [V]
    V = 1402  # qpole AC [V]
    nu = 10 * (10**6)  # qpole RF [Hz]
    r = 0.005  # z-axis center ~ qpole [m]
    Vex1 = 0  # excision field [V]
    #nu_ex1 = 0.963 * (10**6)  # macromotion frequency [Hz]
    Vex2 = 0  # excision field [V]
    #nu_ex2 = 0.963 * (10**6)  # macromotion frequency [Hz]
    Vex3 = 0  # excision field [V]
    #nu_ex3 = 0.963 * (10**6)  # macromotion frequency [Hz]
    Vex4 = 0  # excision field [V]
    #nu_ex4 = 0.963 * (10**6)  # macromotion frequency [Hz]
    flight_t = 24.15  # flight time of ions in q-cell [µs]
    L = 0.15  # qpole length [m]

# initial conditions
x0 = 0.0001
y0 = 0.0001
u0 = 0
v0 = 0

fig_title1 = "ion_trajectories.png"

plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.weight"] = "bold"
plt.rcParams["axes.linewidth"] = 7
plt.rcParams["xtick.labelsize"] = 30
plt.rcParams["ytick.labelsize"] = 30
plt.rcParams["xtick.direction"] = "in"
plt.rcParams["ytick.direction"] = "in"
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

folder_fig = "Figures"
pathlib.Path(folder_fig).mkdir(parents=True, exist_ok=True)


# du/dt, dv/dt (x & y velocities)

if mode == "Q":
    a = 8*e*U/(m*(r*W)**2)
    q = 4*e*V/(m*(r*W)**2)
    m_cutoff = 4 * e * V / (0.909 * (r * W)**2)
    print("mass cutoff: {}".format(m_cutoff/(0.001/(6.02214076*(10**23)))))

    def f(t,x):
        x_acc = -(1/4)*(W**2)*(a+2*q*np.cos(W*t))*x
        return x_acc
    def g(t,y):
        y_acc = (1/4)*(W**2)*(a+2*q*np.cos(W*t))*y
        return y_acc

if mode == "N":
    W = 2 * np.pi * nu
    m_cutoff = 4 * e * V / (0.909 * (r * W)**2)
    w0_1 = 0.32138 * (m_cutoff / m_notch_1) * W
    w0_2 = 0.32138 * (m_cutoff / m_notch_2) * W
    w0_3 = 0.32138 * (m_cutoff / m_notch_3) * W
    w0_4 = 0.32138 * (m_cutoff / m_notch_4) * W
    #w0_1 = 2 * np.pi * nu_ex1
    print("mass cutoff: {} \nnu1 = {} Hz (m/z = {}) \nnu2 = {} Hz (m/z = {}) \nnu3 = {} Hz (m/z = {}) \nnu4 = {} Hz (m/z = {})".format(m_cutoff/(0.001/(6.02214076*(10**23))), w0_1/2/np.pi, m_z_notch_1, w0_2/2/np.pi, m_z_notch_2, w0_3/2/np.pi, m_z_notch_3, w0_4/2/np.pi, m_z_notch_4))

    a = 8*e*U/(m*(r*W)**2)
    q = 4*e*V/(m*(r*W)**2)
    def f(t,x):
        x_acc = -(1/4)*(W**2)*(a+2*q*np.cos(W*t) + 8*e*Vex1*np.cos(2*w0_1*t)/(m*(r*W)**2) + 8*e*Vex2*np.cos(2*w0_2*t)/(m*(r*W)**2) + 8*e*Vex3*np.cos(2*w0_3*t)/(m*(r*W)**2) + 8*e*Vex4*np.cos(2*w0_4*t)/(m*(r*W)**2))*x
        return x_acc
    def g(t,y):
        y_acc = (1/4)*(W**2)*(a+2*q*np.cos(W*t) + 8*e*Vex1*np.cos(2*w0_1*t)/(m*(r*W)**2) + 8*e*Vex2*np.cos(2*w0_2*t)/(m*(r*W)**2) + 8*e*Vex3*np.cos(2*w0_3*t)/(m*(r*W)**2) + 8*e*Vex4*np.cos(2*w0_4*t)/(m*(r*W)**2))*y
        return y_acc

vz = (2*e*Vacc/m)**(1/2)
t0 = 0
#t_end = flight_t*10**(-6)
t_end = L/vz
print(t_end)
dt = (t_end-t0)/10000

tpoints = np.arange(t0,t_end,dt)
xpoints = []
upoints = []
ypoints = []
vpoints = []
zpoints = []

x = x0
y = y0
u = u0
v = v0
for t in tpoints:
    xpoints.append(x)
    upoints.append(u)
    ypoints.append(y)
    vpoints.append(v)
    zpoints.append(t*vz)
    k1u = f(t, x)*dt
    k1x = u*dt
    k2u = f(t+0.5*dt, x+0.5*k1x)*dt
    k2x = (u+0.5*k1u)*dt
    k3u = f(t+0.5*dt, x+0.5*k2x)*dt
    k3x = (u+0.5*k2u)*dt
    k4u = f(t+dt, x+k3x)*dt
    k4x = (u+k3u)*dt
    k1v = g(t, y)*dt
    k1y = v*dt
    k2v = g(t+0.5*dt, y+0.5*k1y)*dt
    k2y = (v+0.5*k1v)*dt
    k3v = g(t+0.5*dt, y+0.5*k2y)*dt
    k3y = (v+0.5*k2v)*dt
    k4v = g(t+dt, y+k3y)*dt
    k4y = (v+k3v)*dt
    u += (k1u+2*k2u+2*k3u+k4u)/6
    v += (k1v+2*k2v+2*k3v+k4v)/6
    x += (k1x+2*k2x+2*k3x+k4x)/6
    y += (k1y+2*k2y+2*k3y+k4y)/6

fig1 = plt.figure(figsize = (15,16), linewidth=7, tight_layout=True)
ax1 = fig1.add_subplot(2,1,1)
ax2 = fig1.add_subplot(2,1,2)
ax1.plot(np.array(zpoints)*100, np.array(xpoints)*1000, marker="None", ls="-", lw=5, color="black", label="m/z = {}".format(m_z))
ax2.plot(np.array(zpoints)*100, np.array(ypoints)*1000, marker="None", ls="-", lw=5, color="black", label="m/z = {}".format(m_z))
ax1.set_xlim(0, L*100)
ax2.set_xlim(0, L*100)
"""
ax1.plot(np.array(tpoints)*10**6, np.array(xpoints)*1000, marker="None", ls="-", lw=5, color="black", label="m/z = {}".format(m_z))
ax2.plot(np.array(tpoints)*10**6, np.array(ypoints)*1000, marker="None", ls="-", lw=5, color="black", label="m/z = {}".format(m_z))
ax1.set_xlim(0, max(tpoints)*10**6)
ax2.set_xlim(0, max(tpoints)*10**6)
"""
ax1.set_ylim(-r*1000, r*1000)
ax2.set_ylim(-r*1000, r*1000)
ax1.set_xlabel("Distance (z-axis) / cm", fontsize=40, fontname="Arial", fontweight="bold")
ax2.set_xlabel("Distance (z-axis) / cm", fontsize=40, fontname="Arial", fontweight="bold")
#ax1.set_xlabel("Flight Time / µs", fontsize=30, fontname="Arial", fontweight="bold")
#ax2.set_xlabel("Flight Time / µs", fontsize=30, fontname="Arial", fontweight="bold")
ax1.set_ylabel("Distance (x-axis) / mm", fontsize=40, fontname="Arial", fontweight="bold")
ax2.set_ylabel("Distance (y-axis) / mm", fontsize=40, fontname="Arial", fontweight="bold")
ax1.grid()
ax2.grid()
ax1.legend(fontsize=30, loc="upper left")
#ax2.legend(fontsize=30, loc="upper left")
ax1.set_axisbelow(True)
ax2.set_axisbelow(True)

fig1.savefig("{}/{}".format(folder_fig,fig_title1))
