# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 22:24:17 2021

@author: sayori
"""
import numpy as np
import canvas
from drawkit import triangle
from numpy import array as ar
import model
import time

            
def to_homo(x):
    a=ar([x[0],x[1],x[2],1],dtype=float)
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

def z_buffer(screen_vertices, world_vertices,model, canvas):
    buff=np.zeros((900,900))
    for i in range(900):
        for j in range(900):
            buff[i][j]=1000#初始化深度无限远

    for i in model.indices:
        scr_tri=ar([screen_vertices[idx-1] for idx in i]) 
        buff=triangle(scr_tri[0],scr_tri[1],scr_tri[2],buff).get_buffer()

    for i in range(900):
        for j in range(900):
            if buff[i][j]!=1000:
                canvas.img.putpixel((i,j), (255,0,0,round(buff[i][j]*150/255+50)))
            
               
def render(model,height=900,width=900,filename=None):
    
    Mper=perspective_transformation(0.5,-0.5,-0.5,0.5,4,1000)
    Mcam=camera_transformation(ar([-4,-6,20]), ar([0,0,0]))
    Mvp=viewport_transformation()
       
    world_vertices=model.vertices
    M=np.dot(np.dot(Mvp,Mper),Mcam)#rendering pipeline P153/p141(7.1) 暂时忽略mmodeling transformation,to be added later
    
    screen_vertices=[]
    
    z_record=[]#把任意的深度范围映射到0-255,或者理解成对深度信息的采样
    for v in model.vertices:
        _,_,z,_=np.dot(M,v)
        z_record.append(z)
    z_max=max(z_record)
    z_min=min(z_record)
    z_update=[round((i-z_min)/(z_max-z_min)*255) for i in z_record]
       
    for i,v in enumerate(model.vertices):
        x,y,z,w=np.dot(M,v)
        
        screen_vertices.append([round(x/w),round(y/w),z_update[i]])
  
    return screen_vertices,world_vertices

if __name__=="__main__":
    m=model.Model("model/box.obj")
    screen_vertices,world_vertices=render(m)
    bk=canvas.canvas()
    bk.put_yellow()
    
    start=time.perf_counter()
    z_buffer(screen_vertices,world_vertices,m,bk)
    print("渲染时间："+str(time.perf_counter()-start)+"s")
    
    bk.img.show()
    bk.img.save("results/cube_2.png")
    


    


    

    
    


        
    
    
        

