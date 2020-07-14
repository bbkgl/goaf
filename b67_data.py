import pandas as pd
import numpy as np
from math import exp, sin, pi, sqrt
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

data = pd.read_csv("C:\\Users\\admin\\Documents\\Tencent Files\\1248703394\\FileRecv\\cavity.csv")

data = data[(data["z"] == 25) & (data["y"] >= 0) & (data["x"] >= 0)]


x = data["x"]
y = data["y"]
c = data["c"]

fig = plt.figure()

ax = Axes3D(fig)

# 下面分别表示曲面图和散点图，使用一个的时候注释另外一个
ax.plot_trisurf(x, y, c,  cmap='rainbow', linewidth=0.8, antialiased=True)
# ax.scatter3D(x, y, z, c = z, cmap="rainbow", marker='o')

plt.xlabel("倾向坐标x，m", fontproperties="SimHei", fontsize=10)
plt.ylabel("距工作面距离y，m", fontproperties="SimHei", fontsize=10)
ax.set_zlabel("CH4浓度", fontproperties="SimHei", fontsize=10)

plt.show()
