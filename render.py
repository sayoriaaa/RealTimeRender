# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 22:24:17 2021

@author: sayori
"""
import numpy as np
import math
from canvas import Scene
import drawkit
from drawkit import Triangle
from drawkit import Object
from numpy import array as ar
import model
import tqdm
from PIL import Image

def img_ave(img,i,j,LEVEL,LEVEL_sqrt):
    ave=[]
    total_pixel=[]
    for column in range(LEVEL_sqrt):
        for row in range(LEVEL_sqrt):
            total_pixel.append(img.getpixel((int(i*LEVEL_sqrt+column),int(j*LEVEL_sqrt+row))))
            
    for i in range(3):
        RGB_AVE=0
        for pixel in total_pixel:
            RGB_AVE+=pixel[i]
        ave.append(int(RGB_AVE/LEVEL))
    return tuple(ave)
    
    

def SSAA(func):
    def wrapper(*args,**kargs):
        LEVEL=4
        LEVEL_sqrt=int(math.sqrt(LEVEL))
        new_args=(args[0]*LEVEL_sqrt,args[1]*LEVEL_sqrt)
        final_img=Image.new("RGB",(args[0],args[1]))
        img=func(*new_args,**kargs)
        for i in range(args[0]):
            for j in range(args[1]):
                final_img.putpixel((i,j),img_ave(img,i,j,LEVEL,LEVEL_sqrt))
        final_img.save(kargs['save_path'])
    return wrapper

def normalize(x):
    return x/np.linalg.norm(x)
   

def camera_transformation(position,target=ar([0.,0.,0.]),up=ar([0.,1.,0.])):#P145
    gaze=normalize(target-position)#上手默认gaze单位向量，其实可以直接反一下但是习惯了
    w=-1*gaze
    u=normalize(np.cross(up,w))
    v=np.cross(w,u)
    rotate=ar([[u[0],u[1],u[2],0],[v[0],v[1],v[2],0],[w[0],w[1],w[2],0],[0,0,0,1]])
    translate=ar([[1,0,0,-1*position[0]],[0,1,0,-1*position[1]],[0,0,1,-1*position[2]],[0,0,0,1]])
    return np.dot(rotate,translate)#Mcam

def perspective_transformation(l=0.5,r=-0.5,b=-0.5,t=0.5,n=0.4,f=1000):#P153 Mper=Morth*P
    Mper=ar([[2*n/(r-l),0,(l+r)/(l-r),0],[0,2*n/(t-b),(b+t)/(b-t),0],[0,0,(f+n)/(n-f),2*f*n/(f-n)],[0,0,1,0]])
    return Mper

def viewport_transformation(height=900,width=900):#P142视口变换
    Mvp=ar([[0.5*width,0,0,0.5*width-0.5],[0,0.5*height,0,0.5*height-0.5],[0,0,1,0],[0,0,0,1]])
    return Mvp

def load_model(model, scene, M,load_material=False,load_texture=False):
        
    screen_vertices=[]
    real_vertices=[]#把齐次坐标转回来
    for i in model.vertices:
        x,y,z,w=np.dot(M,i)
        screen_vertices.append([round(x/w),round(y/w),round(z/w)])
        real_vertices.append([i[0],i[1],i[2]])
    
    triangle_set=[]
    uv_set=[]

    for count, i in enumerate(model.indices):
        scr_tri=ar([screen_vertices[idx-1] for idx in i]) 
        ori_tri=ar([real_vertices[idx-1] for idx in i]) 
        norm=model.vn_vertices[count]
        single_triangle=Triangle(ori_tri,norm,scr_tri[0],scr_tri[1],scr_tri[2])
        triangle_set.append(single_triangle)
        
        uv_indices=ar([model.uv_vertices[idx-1] for idx in model.uv_indices[count]])
        uv_set.append(uv_indices)
        
    if load_material:
        Triangle.Ka=ar(model.Ka)/model.illum
        Triangle.Kd=ar(model.Kd)/model.illum
        Triangle.Ks=ar(model.Ks)/model.illum
        
    if load_texture and model.texture_name!=None:
        Triangle.texture=model.texture
        Triangle.u=model.u
        Triangle.v=model.v
        Triangle.load_texture=True
        Triangle.uv_set=uv_set
             
    return triangle_set,uv_set

            
               
def get_transform_matrix(scene):   
    Mper=perspective_transformation(n=0.8,f=100)
    Mcam=camera_transformation(scene.camera)
    Mvp=viewport_transformation(width=scene.width,height=scene.height)
    M=np.dot(np.dot(Mvp,Mper),Mcam)#rendering pipeline P153/p141(7.1)    
    return M

def shade(f_buffer,z_buffer,scene,triangle_set,uv_set):
    count=0
    for i in tqdm.tqdm(triangle_set):
        i.update_buffer(uv_set[count])
        count+=1
        
    for i in range(scene.width):
        for j in range(scene.height):
            if z_buffer[i][j]!=np.inf:
                scene.img.putpixel((i,j), (f_buffer[i][j][0],f_buffer[i][j][1],f_buffer[i][j][2]))



def initial_scene(width=600,height=400,save_path="results/res1.png"):
    """
    Triangle.mode=0:向量叉乘
    Triangle.mode=1：线包围
    Triangle.mode=2：重心法
    """
    Triangle.mode=0####################################################
    sc=Scene(width=width,height=height,save_path=save_path)
    return sc



#@SSAA
def pipline(width,height,save_path="results/res1.png",model_path="model/box.obj",texture_name="model/barrel_side.png"):
    m=model.Model(model_path,texture_name)
    sc=initial_scene(width=width,height=height,save_path=save_path)   
    M=get_transform_matrix(sc)#返回屏幕空间的顶点坐标，总的变换矩阵，z轴最小值
    sc.draw_xyz(M)
    
    triangle_set,uv_set=load_model(m,sc,M,load_material=False,load_texture=True)  
    shade(Object.f_buff,Object.z_buff,sc,triangle_set,uv_set)  
    sc.show()
    return sc.img
    
    
if __name__=="__main__":
    pipline(600,600,save_path="results/res9.png",model_path="model/box.obj")
    

        


    

    
    


        
    
    
        

