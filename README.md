# SoftRenderer-for-pythonclass
python课堂大作业，基于GAMES101以及Fundamentals of Computer Graphics

21/10/27
v1.0.0    实现最简单的光栅化渲染管线，无优化，无其他功能

21/10/29
v1.0.1    实现基于屏幕空间的深度插值以及Z-Buffer算法

21/10/31
v1.0.1.1    修复v1.0.1只有小部分实现透明度区分的问题,解决导入其他模型出现buffer越界的问题(可能是由于camera未适应模型的大小导致)

21/10/31
v1.0.1.2    修复渲染时可能出现面缺失的问题，现支持三角形和四边形格式的OBJ模型

21/11/1
v1.0.2    进行了光栅化部分代码的重构，实现了基于Blinn-Phong的shader，可选择正面平行光或点光源进行渲染

21/11/4
v1.0.2.1    增加坐标轴，网格显示功能

21/11/5
v1.0.2.1    改进了之前对shader认识不完善的部分，实现lambertian和blinn-phong shaing


