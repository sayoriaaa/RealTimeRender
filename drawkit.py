# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 10:36:19 2021

@author: sayori
"""
import numpy as np
from numpy import array as ar
import math

def normalize(x):
    return x/np.linalg.norm(x)

def swap(a,b):
    return b,a
    
class Object:
    camera=ar([4,4,10]) 
    light=ar([2,6,10])
    z_buff=None#在scene会重写
    f_buff=None
    height=None
    width=None

class Triangle(Object):    
    kd=1
    
    def __init__(self,i,norm,a=np.zeros(3),b=np.zeros(3),c=np.zeros(3)):#分别传入屏幕坐标的三个点
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
        
        self.ori=i
        self.norm=norm
        self.vertice_light=None#效率优化
          
    def update_buffer(self):
        for i in range(self.xmin,self.xmax):
            for j in range(self.ymin,self.ymax):
                vec=np.array([i,j])
                if np.cross(vec-self.a,self.vec2)>0 and np.cross(vec-self.b,self.vec3)>0 and np.cross(vec-self.c,self.vec1)>0:        
                    depth=self.get_depth_screen(i,j)
        
                    if i>=Object.width or j>=Object.height or i<0 or j<0:    break
                    if depth<Object.z_buff[i][j]:
                        Object.z_buff[i][j]=depth
                        diffuse_light_cos=(self.get_screen_interpolation(i,j,1))
                        spect_light_cos=(self.get_screen_interpolation(i,j,101))
                        
                        Object.f_buff[i][j]=ar([.8,.3,0])*(0.2*diffuse_light_cos+0.6*spect_light_cos+0.2)*255
                            
        '''    
       if mode==0:#默认原点处的水平光
            for i in range(self.xmin,self.xmax):
                for j in range(self.ymin,self.ymax):
                    vec=np.array([i,j])
                    if np.cross(vec-self.a,self.vec2)>0 and np.cross(vec-self.b,self.vec3)>0 and np.cross(vec-self.c,self.vec1)>0:        
                        depth=self.get_depth_screen(i,j)
            
                        if i>=900 or j>=900 or i<0 or j<0:    break
                        if depth<self.z_buff[i][j]:#深度不等于亮度，两个都要保存
                            self.z_buff[i][j]=depth
                            self.f_buff[i][j][0]=0
                            self.f_buff[i][j][1]=0
                            self.f_buff[i][j][2]=255-self.z_buff[i][j]/5
            return self.z_buff,self.f_buff
        
        if mode==1:#Lambertian Shading
            kd=1
            for i in range(self.xmin,self.xmax):
                for j in range(self.ymin,self.ymax):
                    vec=np.array([i,j])
                    if np.cross(vec-self.a,self.vec2)>0 and np.cross(vec-self.b,self.vec3)>0 and np.cross(vec-self.c,self.vec1)>0:        
                        depth=self.get_depth_screen(i,j)
            
                        if i>=900 or j>=900 or i<0 or j<0:    break
                        if depth<self.z_buff[i][j]:#深度不等于亮度，两个都要保存
                            self.z_buff[i][j]=depth
                            para_cos=self.get_light_screen(i, j, 1)#光源位置在get_vertice_light设定
                            self.f_buff[i][j]=ar([.8,.3,0])*para_cos*kd*255#*255 之前的是intensity
            return self.z_buff,self.f_buff     
    '''
    def get_depth_screen(self,i,j):
        alpha,beta=np.dot(ar([i-self.c[0],j-self.c[1]]),np.linalg.inv(ar([[self.a[0]-self.c[0],self.a[1]-self.c[1]],[self.b[0]-self.c[0],self.b[1]-self.c[1]]])))#
        return alpha*self.z1+beta*self.z2+(1-alpha-beta)*self.z3
    def get_depth_appro(self):
        return self.z_ave
    
    
    def get_vertice_light(self,n):#参考取值lambertian n=1,blinn-spec n=101,不能是偶数不然没法判断背面
        vertice_light=[]
        for i in range(3):
            l=normalize(Object.light+Object.camera-2*self.ori[i])
            vertice_light.append(max(math.pow(np.dot(l,self.norm),n),0))
        return vertice_light
        
    def get_screen_interpolation(self,i,j,n):
        vertice_light=self.get_vertice_light(n)
        alpha,beta=np.dot(ar([i-self.c[0],j-self.c[1]]),np.linalg.inv(ar([[self.a[0]-self.c[0],self.a[1]-self.c[1]],[self.b[0]-self.c[0],self.b[1]-self.c[1]]])))#
        return alpha*vertice_light[0]+beta*vertice_light[1]+(1-alpha-beta)*vertice_light[2]
    
           
        
class Line:
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
    

        
class Plane:#这里的平面是给光追用的，不用考虑光栅化的东西
    def __init__(self,position=ar([0,-1,0]),norm=ar([0,1,0])):
        self.pos=position
        self.norm=norm
        
    def get_color(self,point):#这里先用默认参数写了,先不管光源夹角
        if (point[0]//1+point[2]//1)%2==0:
            return ar([1,0,0])
        else:
            return ar([0,0,1])
        
        
        
        
