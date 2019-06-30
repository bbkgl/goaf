#include "udf.h"

#define X_L 300          // 采空区模型的长度
#define L 15             // 基本顶破碎长度
#define Y_L 200          // 工作面宽度
#define DP 0.11          // 平均粒径
#define TIMESTAMP "06301326"   // 时间戳

// 绝对值函数
double my_abs(double x) {
	if (x < 0) return -x;
	else return x;
}

// 单点的孔隙率函数
double porous(double x, double y, double z) {
	double value = ((1 + exp(-0.15 * (Y_L / 2 - my_abs(y - Y_L / 2)))) * (1 - 6 / (9.6 - 3.528 * (1 - exp(-x / (L * 2))))));
	value = sqrt(value);
	if (z >= 60) 
		value = value * (60 - z) / 60;
	return sqrt(value) * 0.6;
}

// 空隙率
DEFINE_PROFILE(porous_profile, thread, position)
{
	real r[ND_ND];
	real x, y, z, value;
	cell_t c;
	begin_c_loop(c, thread)
	{
		C_CENTROID(r, c, thread);
		x = r[0];
		y = r[1];
		z = r[2];
		value = porous(x, y, z);
		C_PROFILE(c, thread, position) = value;
	}
	end_c_loop(c, thread)
}

// 惯性阻力
DEFINE_PROFILE(guanxing, thread, position)
{
	real r[ND_ND];
	real x, y, z, value, n;
	cell_t c;
	printf("Load success!----%s\n", TIMESTAMP);  // 打印时间戳
	begin_c_loop(c, thread)
	{
		C_CENTROID(r, c, thread);
		x = r[0];
		y = r[1];
		z = r[2];
		n = porous(x, y, z);
		value = 3.5 * (1 - n) / (DP * pow(n, 3));
		C_PROFILE(c, thread, position) = value;
	}
	end_c_loop(c, thread)
}

// 粘性阻力系数
DEFINE_PROFILE(nianxing_x, thread, position) 
{
	real r[ND_ND];
	real x, y, z, shentoulv, n;
	cell_t c;
	begin_c_loop(c, thread)
	{
		C_CENTROID(r, c, thread);
		x = r[0];
		y = r[1];
		z = r[2];
		n = porous(x, y, z);
		shentoulv = (DP * DP * pow(n, 3)) / (150 * pow(1 - n, 2));
		C_PROFILE(c, thread, position) = 60 / shentoulv;
	}
	end_c_loop(c, thread)
}

DEFINE_PROFILE(nianxing_y, thread, position) 
{
	real r[ND_ND];
	real x, y, z, shentoulv, n;
	cell_t c;
	begin_c_loop(c, thread)
	{
		C_CENTROID(r, c, thread);
		x = r[0];
		y = r[1];
		z = r[2];
		n = porous(x, y, z);
		shentoulv = (DP * DP * pow(n, 3)) / (150 * pow(1 - n, 2));
		C_PROFILE(c, thread, position) = 10 / shentoulv;
	}
	end_c_loop(c, thread)
}

DEFINE_PROFILE(nianxing_z, thread, position) 
{
	real r[ND_ND];
	real x, y, z, shentoulv, n;
	cell_t c;
	begin_c_loop(c, thread)
	{
		C_CENTROID(r, c, thread);
		x = r[0];
		y = r[1];
		z = r[2];
		n = porous(x, y, z);
		shentoulv = (DP * DP * pow(n, 3)) / (150 * pow(1 - n, 2));
		C_PROFILE(c, thread, position) = 600 / shentoulv;
	}
	end_c_loop(c, thread)
}

// 氧气消耗
//o2_consumption
DEFINE_SOURCE(o2_consumption, cell,thread,dS,i)   /*defining source of oxygen consumption*/
{

	real R;
	real s1 = C_YI(cell, thread, 1);   //oxygen mass fraction
	real T = C_T(cell, thread);
	real x[ND_ND];
	C_CENTROID(x, cell, thread);
	if(s1 > 0) {
		dS[i] = -0.000000308;
		R = dS[i] * s1;
	}
	else { 
		dS[i] = 0; 
		R = 0; 
	} 
	return R;    /*oxygen consumption rate in porous media*/
}
