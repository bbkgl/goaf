from matplotlib import pyplot as plt
import numpy as np
from math import exp, sin, pi, sqrt
from mpl_toolkits.mplot3d import Axes3D

num = 200

x_l = 300    # 采空区的长度
y_l = 200    # 工作面的长度

fig = plt.figure()
ax = Axes3D(fig)
X = np.arange(0, x_l, x_l / num)
Y = np.arange(0, y_l, y_l / num)
X, Y = np.meshgrid(X, Y)
Z = X + Y
Z1 = Z

for i in range(num):
    for j in range(num):
        x = X[i][j]
        y = Y[i][j]
        t = ((1 + exp(-0.15 * (y_l / 2 - abs(y - y_l / 2)))) * (1 - 6 / (9.6 - 3.528 * (1 - exp(-x / 60)))))
        # t = 0.2
        # if x <= 100 :
        #     t = 0.00001 * x * x - 0.002 * x + 0.3
        Z[i][j] = sqrt(t) * 0.6
        # shentoulv = (0.11 * 0.11 * pow(Z[i][j], 3)) / (150 * pow(1 - Z[i][j], 2))
        # Z1[i][j] = 100 / shentoulv

# 具体函数方法可用 help(function) 查看，如：help(ax.plot_surface)
ax.plot_surface(X, Y, Z1, rstride=1, cstride=1, cmap='rainbow')

# plt.xlabel("距工作面距离x，m", fontproperties="SimHei")
# plt.ylabel("距进风侧距离y，m", fontproperties="SimHei")
# ax.set_zlabel("采空区平面孔隙率", fontproperties="SimHei")

plt.xlabel("距工作面距离x，m", fontproperties="SimHei", fontsize = 10)
plt.ylabel("距进风侧距离y，m", fontproperties="SimHei", fontsize = 10)
ax.set_zlabel("采空区空隙率", fontproperties="SimHei", fontsize = 10)

plt.show()
