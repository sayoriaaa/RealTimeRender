# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 22:24:17 2021

@author: sayori
"""
import numpy as np
from canvas import Scene
import drawkit
from drawkit import Triangle
from numpy import array as ar
import model
import tqdm

            
def to_ori(x):
    a=[]
    for i in x:
        a.append(ar([i[0],i[1],i[2]]))
    return a

def normalize(x):
    return x/np.linalg.norm(x)
   

def camera_transformation(position,target,up=ar([0,1,0])):#P145
    gaze=normalize(target-position)#上手默认gaze单位向量，其实可以直接反一下但是习惯了
    w=-1*gaze
    u=normalize(np.cross(up,w))
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

def get_buff(screen_vertices,model, scene):
    
    z_buff=np.zeros((scene.width,scene.height))
    f_buff=ar([ar([[1,1,1] for i in range(scene.width)]) for i in range(scene.height)])
    for i in range(scene.width):
        for j in range(scene.height):
            z_buff[i][j]=1000#初始化深度无限远

    for count, i in enumerate(model.indices):
        scr_tri=ar([screen_vertices[idx-1] for idx in i]) 
        ori_tri=ar([model.vertices[idx-1] for idx in i]) 
        ori_tri=to_ori(ori_tri)
        law=model.vn_vertices[count]
        z_buff,f_buff=Triangle(ori_tri,law,scr_tri[0],scr_tri[1],scr_tri[2],z_buff,f_buff).get_buffer()

    return f_buff,z_buff
            
               
def render(model):
    
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

def shade(f_buffer,z_buffer,scene):
    for i in tqdm.tqdm(range(scene.width)):
        for j in range(scene.height):
            if z_buffer[i][j]!=1000:
                scene.img.putpixel((i,j), (f_buffer[i][j][0],f_buffer[i][j][1],f_buffer[i][j][2]))


def rasterization_main():
    m=model.Model("model/box.obj")
    sc=Scene(width=600,height=400,save_path="results/sph.png")
    
    
    screen_vertices,M=render(m)#返回屏幕空间的顶点坐标，总的变换矩阵，z轴最小值  
    sc.set_background_color()
    #bk.draw_grid(M)
    sc.draw_xyz(M)
    
    f_buffer,z_buffer=get_buff(screen_vertices,m,sc)
    shade(f_buffer,z_buffer,sc)
    
    sc.show()
    
    
    
    
    
    
    
    
if __name__=="__main__":
    rasterization_main()
    


    


    

    
    


        
    
    
        

