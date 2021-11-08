# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 22:24:17 2021

@author: sayori
"""
import numpy as np
import canvas
import drawkit
from drawkit import triangle
from numpy import array as ar
import model
import time

import tqdm

            
def to_ori(x):
    a=[]
    for i in x:
        a.append(ar([i[0],i[1],i[2]]))
    return a

def unitize(x):
    return x/np.linalg.norm(x)

def camera_transformation(position,target,up=ar([0,1,0])):#P145
    gaze=unitize(target-position)#上手默认gaze单位向量，其实可以直接反一下但是习惯了
    w=-1*gaze
    u=unitize(np.cross(up,w))
    v=np.cross(w,u)
    rotate=ar([[u[0],u[1],u[2],0],[v[0],v[1],v[2],0],[w[0],w[1],w[2],0],[0,0,0,1]])
    translate=ar([[1,0,0,-1*position[0]],[0,1,0,-1*position[1]],[0,0,1,-1*position[2]],[0,0,0,1]])
    return np.dot(rotate,translate)#Mcam

def perspective_transformation(l,r,b,t,n,f):#P153 Mper=Morth*P
    Mper=ar([[2*n/(r-l),0,(l+r)/(l-r),0],[0,2*n/(t-b),(b+t)/(b-t),0],[0,0,(f+n)/(n-f),2*f*n/(f-n)],[0,0,1,0]])
    return Mper

def viewport_transformation(height=900,width=900):#P142视口变换
    Mvp=ar([[0.5*width,0,0,0.5*width-0.5],[0,0.5*height,0,0.5*height-0.5],[0,0,1,0],[0,0,0,1]])
    return Mvp

def get_buff(screen_vertices,model, canvas):
    
    z_buff=np.zeros((900,900))
    f_buff=ar([ar([[1,1,1] for i in range(900)]) for i in range(900)])
    for i in range(900):
        for j in range(900):
            z_buff[i][j]=1000#初始化深度无限远

    for count, i in enumerate(model.indices):
        scr_tri=ar([screen_vertices[idx-1] for idx in i]) 
        ori_tri=ar([model.vertices[idx-1] for idx in i]) 
        ori_tri=to_ori(ori_tri)
        law=model.vn_vertices[count]
        z_buff,f_buff=triangle(ori_tri,law,scr_tri[0],scr_tri[1],scr_tri[2],z_buff,f_buff).get_buffer()

    return f_buff,z_buff
            
               
def render(model,height=900,width=900,filename=None):
    
    Mper=perspective_transformation(0.5,-0.5,-0.5,0.5,0.4,1000)
    Mcam=camera_transformation(ar([4,4,10]), ar([0,0,0]))#这里调整时注意更新drawkit.blinnphong中的camera_position
    Mvp=viewport_transformation()
    M=np.dot(np.dot(Mvp,Mper),Mcam)#rendering pipeline P153/p141(7.1) 暂时忽略mmodeling transformation,to be added later
    
    z_update=drawkit.process_z(model, M)#把z映射到一个较大范围的整数区间，默认0-1000
    screen_vertices=[]
    for i,v in enumerate(model.vertices):
        x,y,z,w=np.dot(M,v)
        screen_vertices.append([round(x/w),round(y/w),z_update[i]])
    return screen_vertices,M

def shade(f_buffer,z_buffer,canvas):
    for i in range(900):
        for j in range(900):
            if z_buffer[i][j]!=1000:
                canvas.img.putpixel((i,j), (f_buffer[i][j][0],f_buffer[i][j][1],f_buffer[i][j][2]))

######################################################################################################
#光线追踪
def intersect_tri_time(tri,direction):#判断是否有交点，若有返回camera距离交点的长度，若无返回10000
    camera=ar([2,2,5])
    '''
    position_a=tri[0]
    beta_vec=tri[1]-tri[0]
    gama_vec=tri[2]-tri[0]
    '''
    matrix_A=ar([[tri[0][0]-tri[1][0],tri[0][0]-tri[2][0],direction[0]],[tri[0][1]-tri[1][1],tri[0][1]-tri[2][1],direction[1]],[tri[0][2]-tri[1][2],tri[0][2]-tri[2][2],direction[2]]])#P78
    matrix_T=ar([[tri[0][0]-tri[1][0],tri[0][0]-tri[2][0],tri[0][0]-camera[0]],[tri[0][1]-tri[1][1],tri[0][1]-tri[2][1],tri[0][1]-camera[1]],[tri[0][2]-tri[1][2],tri[0][2]-tri[2][2],tri[0][2]-camera[2]]])
    
    matrix_beta=ar([[tri[0][0]-camera[0],tri[0][0]-tri[2][0],direction[0]],[tri[0][1]-camera[1],tri[0][1]-tri[2][1],direction[1]],[tri[0][2]-camera[2],tri[0][2]-tri[2][2],direction[2]]])
    matrix_gama=ar([[tri[0][0]-tri[1][0],tri[0][0]-camera[0],direction[0]],[tri[0][1]-tri[1][1],tri[0][1]-camera[1],direction[1]],[tri[0][2]-tri[1][2],tri[0][2]-camera[2],direction[2]]])
    
    det_A=np.linalg.det(matrix_A)
    det_T=np.linalg.det(matrix_T)
    
    det_beta=np.linalg.det(matrix_beta)
    det_gama=np.linalg.det(matrix_gama)
    
    
    if det_A<1e-6:
        return 10000
    else:
        beta=det_beta/det_A
        gama=det_gama/det_A
        if gama<0 or gama>1:
            return 10000
        if beta<0 or beta>1-gama:
            return 10000
        return det_T/det_A
    
    
def intersect_tri(model,direction):
    min_t=10000
    camera=ar([2,2,5])
    direction=unitize(direction)
    
    for count,i in enumerate(model.indices):
        tri=ar([model.vertices[idx-1] for idx in i])
        normal=model.vn_vertices[count]
        t=intersect_tri_time(tri, direction)
        if t<min_t and t>0:#找到最小获得插值
            min_t=t
            object_tri=tri
            object_tri_norm=normal
            
    plane=drawkit.plane()
    if direction[1]<1e-6:#与屏幕平行
        if min_t==10000:#又没有和三角形相交
            return ar([0,0,0])
        else:
            return ar([.8,.3,0])*np.dot(direction,object_tri_norm)*255
        
    else:
        plane_t=(plane.pos[1]-camera[1])/direction[1]
        plane_point=camera+plane_t*direction
        if min_t==10000:
            if plane_t>0:
                return plane.get_color(plane_point)
            else: return ar([0,0,0])
        else:
            if plane_t>0 and plane_t<min_t:
                return plane.get_color(plane_point)
            else:
                return ar([.8,.3,0])*np.dot(direction,object_tri_norm)*255
                
        
        
def intersect_plane(model,canvas):#测试用，只绘制平面
    height=900
    width=900
    camera=ar([10,10,10])
    target=ar([0,0,0])
    up=ar([0,1,0])
    gaze=unitize(target-camera)
    u=unitize(np.cross(up,-1*gaze))
    v=np.cross(-1*gaze,u)
    d=300.
    canvas_center=camera+d*gaze
    canvas_leftdown=canvas_center-height/2*v-width/2*u
    direction=ar([ar([[1,1,1] for i in range(900)]) for i in range(900)])
    
    plane=drawkit.plane()
    
    for i in tqdm.tqdm(range(height)):
        for j in range(width):
            direction[i][j]=canvas_leftdown+i*v+j*u-camera#确立了像素数量的光线方向
            
            plane=drawkit.plane()
            if direction[i][j][1]<1e-6:
                canvas.img.putpixel((j,i),(0,0,0))
                continue#近似平行的情况，警告了处理一下，时间就减半了LOL
                
            plane_t=(plane.pos[1]-camera[1])/direction[i][j][1]
            plane_point=camera+plane_t*direction[i][j]
            
            pixel_color=plane.get_color(plane_point)
            pixel_color=pixel_color*np.dot(ar([0,1,0]), direction[i][j])
            canvas.img.putpixel((j,i),(int(pixel_color[0]),int(pixel_color[1]),int(pixel_color[2])))
            #process_rate=(height*i+j)/(height*width)*100
            #print("已完成："+str(process_rate)+"%")
    
    
            
            
        
def ray_tracing(model,canvas):
    height=900
    width=900
    camera=ar([2,2,5])
    target=ar([0,0,0])
    up=ar([0,1,0])
    gaze=unitize(target-camera)
    u=unitize(np.cross(up,-1*gaze))
    v=np.cross(-1*gaze,u)
    d=100.
    canvas_center=camera+d*gaze
    canvas_leftdown=canvas_center-height/2*v-width/2*u
    direction=ar([ar([[1,1,1] for i in range(900)]) for i in range(900)])
    for i in tqdm.tqdm(range(height)):
        for j in range(width):
            direction[i][j]=canvas_leftdown+i*v+j*u-camera#确立了像素数量的光线方向
            
            pixel_color=intersect_tri(model, direction[i][j])
            canvas.img.putpixel((i,j),(int(pixel_color[0]),int(pixel_color[1]),int(pixel_color[2])))
            
    
########################################################################################

def rasterization_main():
    m=model.Model("model/sph.obj")
    screen_vertices,M=render(m)#返回屏幕空间的顶点坐标，总的变换矩阵，z轴最小值
    print(M)
    bk=canvas.canvas()
    bk.put_yellow()
    bk.draw_grid(M)
    bk.draw_xyz(M)
    
    start=time.perf_counter()
    f_buff,z_buff=get_buff(screen_vertices,m,bk)
    shade(f_buff,z_buff,bk)
    print("渲染时间："+str(time.perf_counter()-start)+"s")
    
    bk.img.show()
    bk.img.save("results/sph.png")
    
def ray_trace_main():
    m=model.Model("model/box.obj")
    bk=canvas.canvas()
   
    start=time.perf_counter()
    ray_tracing(m, bk)
    print("渲染时间："+str(time.perf_counter()-start)+"s")
    
    bk.img.show()
    bk.img.save("results/ray_trace_4.png")
    
    
    
    
    
    
    
if __name__=="__main__":
    ray_trace_main()
    


    


    

    
    


        
    
    
        

