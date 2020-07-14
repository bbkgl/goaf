from matplotlib import pyplot as plt
import numpy as np
from math import exp, sin, pi, sqrt
from mpl_toolkits.mplot3d import Axes3D

num = 200

D = 150.0  # 走向长度
L = 200.0  # 工作面的长度

z_l = 5 # 修改Z得到不同平台的图

fig = plt.figure()
ax = Axes3D(fig)
Y = np.arange(0, D, D / num)
X = np.arange(- L / 2, L / 2, L / num)
X, Y = np.meshgrid(X, Y)
Z = X + Y


def cal_ellipse(x, y):
    return pow(y - D / 2, 2) / 2500 + x * x / 6400

def cal_common(x, y):
    a = 2.94357 * pow(10, -7)
    b = (0.2 * exp(-0.0223 * (D / 2 - abs(D / 2 - y))) + 0.1) ** 2
    c = (exp(-0.15 * (L / 2 - abs(x))) + 1) ** 2
    return a * b * c

def cal_kxl(x, y, z=z_l):
    if (cal_ellipse(x, y) >= 1):
        return cal_common(x, y) * 1.01 ** (2 * z)
    elif (cal_ellipse(x, y) <= 0.25):
        return cal_common(x, y)
    else:
        t = x**2 / 1600 + pow(y - D / 2, 2) / 625
        return cal_common(x, y) * (t ** (0.014356 * z))

for i in range(num):
    for j in range(num):
        x = X[i][j]
        y = Y[i][j]
        Z[i][j] = cal_kxl(x, y)

# 具体函数方法可用 help(function) 查看，如：help(ax.plot_surface)
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='rainbow')

plt.xlabel("倾向坐标x，m", fontproperties="SimHei", fontsize=10)
plt.ylabel("距工作面距离y，m", fontproperties="SimHei", fontsize=10)
ax.set_zlabel("采空区空隙率", fontproperties="SimHei", fontsize=10)

plt.show()
