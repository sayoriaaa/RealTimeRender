# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 10:36:19 2021

@author: sayori
"""
import numpy as np
from numpy import array as ar
import math

def unitize(x):
    return x/np.linalg.norm(x)

def swap(a,b):
    return b,a

def process_z(model,M,start=0,end=1000):
    z_record=[]#把任意的深度范围映射到start-end,或者理解成对深度信息的采样
    for v in model.vertices:
        _,_,z,_=np.dot(M,v)
        z_record.append(z)
    z_max=max(z_record)
    z_min=min(z_record)
    z_update=[round((i-z_min)/(z_max-z_min)*end+start) for i in z_record] 
    return z_update      
        

class triangle:
    def __init__(self,i,law,a=np.zeros(3),b=np.zeros(3),c=np.zeros(3),z_buff=np.zeros((900,900)),f_buff=np.zeros((900,900))):#分别传入屏幕坐标的三个点和z_buffer,f_buff透明度
        self.a=ar([a[0],a[1]])
        self.b=ar([b[0],b[1]])
        self.c=ar([c[0],c[1]])
        self.vec1=self.a-self.c
        self.vec2=self.b-self.a
        self.vec3=self.c-self.b
        self.xmin=min(a[0],b[0],c[0])
        self.xmax=max(a[0],b[0],c[0])
        self.ymin=min(a[1],b[1],c[1])
        self.ymax=max(a[1],b[1],c[1])
        
        
        self.z1=a[2]
        self.z2=b[2]
        self.z3=c[2]
        self.z_ave=(a[2]+b[2]+c[2])/3
        
        self.z_buff=z_buff
        self.f_buff=f_buff
        self.ori=i
        self.law=law#当前面的单位法向量
          
    def get_buffer(self,mode=0):
        
        if mode==0:#默认原点处的水平光
            for i in range(self.xmin,self.xmax):
                for j in range(self.ymin,self.ymax):
                    vec=np.array([i,j])
                    if np.cross(vec-self.a,self.vec2)>0 and np.cross(vec-self.b,self.vec3)>0 and np.cross(vec-self.c,self.vec1)>0:        
                        depth=self.get_depth_screen(i,j)
            
                        if i>=900 or j>=900 or i<0 or j<0:    break
                        if depth<self.z_buff[i][j]:#深度不等于亮度，两个都要保存
                            self.z_buff[i][j]=depth
                            self.f_buff[i][j]=round(self.z_buff[i][j]/5+50)
            return self.z_buff,self.f_buff
        if mode==1:#Blinn-Phong模型(Blinn模型，性能开销小)
            self.get_vertice_light()
            for i in range(self.xmin,self.xmax):
                for j in range(self.ymin,self.ymax):
                    vec=np.array([i,j])
                    if np.cross(vec-self.a,self.vec2)>0 and np.cross(vec-self.b,self.vec3)>0 and np.cross(vec-self.c,self.vec1)>0:        
                        depth=self.get_depth_screen(i,j)
            
                        if i>=900 or j>=900 or i<0 or j<0:    break
                        if depth<self.z_buff[i][j]:#深度不等于亮度，两个都要保存
                            self.z_buff[i][j]=depth
                            ambient_light=50#10为环境光亮度
                            spect_light=(self.get_light_screen(i,j))*200
                            self.f_buff[i][j]=255-ambient_light-spect_light
                            
                    
            return self.z_buff,self.f_buff
            
            
    
    def get_depth_screen(self,i,j):
        alpha,beta=np.dot(ar([i-self.c[0],j-self.c[1]]),np.linalg.inv(ar([[self.a[0]-self.c[0],self.a[1]-self.c[1]],[self.b[0]-self.c[0],self.b[1]-self.c[1]]])))#
        return alpha*self.z1+beta*self.z2+(1-alpha-beta)*self.z3
    def get_depth_appro(self):
        return self.z_ave
    
    
    def get_vertice_light(self):
        light_position=ar([4,6,-10])
        camera_position=([4,6,-10])
        law=self.law
        vec1=light_position-self.ori[0]+camera_position-self.ori[0]
        vec1=unitize(vec1)
        vec2=light_position-self.ori[1]+camera_position-self.ori[1]
        vec2=unitize(vec2)
        vec3=light_position-self.ori[2]+camera_position-self.ori[2]
        vec3=unitize(vec3)
        light1=math.pow(np.dot(vec1,law),101)#不能是偶数不然没法判断背面
        if light1<0:
            light1=0#好蠢啊有没有类似clamp的
        light2=math.pow(np.dot(vec2,law),101)#不能是偶数不然没法判断背面
        if light2<0:
            light2=0
        light3=math.pow(np.dot(vec3,law),101)#不能是偶数不然没法判断背面
        if light3<0:
            light3=0
        self.light1=light1
        self.light2=light2
        self.light3=light3
        
    def get_light_screen(self,i,j):
        alpha,beta=np.dot(ar([i-self.c[0],j-self.c[1]]),np.linalg.inv(ar([[self.a[0]-self.c[0],self.a[1]-self.c[1]],[self.b[0]-self.c[0],self.b[1]-self.c[1]]])))#
        return alpha*self.light1+beta*self.light2+(1-alpha-beta)*self.light3

           
        
class line:
    def __init__(self,a,b):#这里已经是屏幕空间的点了  
        if not b[0]>a[0]:  
            a,b=swap(a,b)#确保Xa在左边
        self.a=a
        self.b=b 
    
    def f_line(self,x,y):
        return (self.b[1]-self.a[1])*x-(self.b[0]-self.a[0])*y+self.b[0]*self.a[1]-self.b[1]*self.a[0]
    
    def draw_line(self):
        dots=[]
        a=self.a
        b=self.b
        if b[0]-a[0]==0:
            slope=10000*(b[1]-a[1])
        else:
            slope=(b[1]-a[1])/(b[0]-a[0]) 
        y_start=a[1]
        x_start=a[0]
        if slope>0:#P162四种情况讨论
            if slope>1:
                for y in range(a[1],b[1]):
                    dots.append([x_start,y])
                    if self.f_line(x_start+0.5,y+1)<0: 
                        x_start+=1
            else:
                for x in range(a[0],b[0]):
                    dots.append([x,y_start])
                    if self.f_line(x+1,y_start+0.5)>0: 
                        y_start+=1
        else:#slope<=0
            if slope>-1:
                for x in range(a[0],b[0]):
                    dots.append([x,y_start])
                    if self.f_line(x+1,y_start-0.5)<0:
                        y_start-=1
            else:
                for y in range(a[1],b[1],-1):
                    dots.append([x_start,y])
                    if self.f_line(x_start+0.5,y-1)>0: 
                        x_start+=1
                    
        return dots
        
    
        
        
