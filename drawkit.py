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
    mode=0
    p=50
    Kd=ar([.8,.3,.4])
    Ka=ar([.2,.2,.2])
    Ks=ar([.6,.6,.6])
    load_texture=False
    
    def __init__(self,i,norm,vertice1=np.zeros(3),vertice2=np.zeros(3),vertice3=np.zeros(3)):#分别传入屏幕坐标的三个点
        if Triangle.mode==0 or Triangle.mode==2:
            self.vector_cross_initial(i,norm,vertice1,vertice2,vertice3)
        elif Triangle.mode==1:
            self.optimize_initial(i,norm,vertice1,vertice2,vertice3)
          
    def update_buffer(self,uv):
        if Triangle.mode==0:
            self.vector_update_buffer(uv)
        elif Triangle.mode==1:
            self.optimize_update_buffer(uv)
        elif Triangle.mode==2:
            self.barycentric_update_buffer(uv)
            
    def shade_color(self,i,j,uv):
        if Triangle.load_texture==False:
            diffuse_light_cos=(self.get_screen_interpolation(i,j,1))
            spect_light_cos=(self.get_screen_interpolation(i,j,Triangle.p))
            color=np.clip(0,1,Triangle.Ka+Triangle.Kd*diffuse_light_cos+Triangle.Ks*spect_light_cos)*255
            return color
        else:
            coord=self.get_uv(i,j,uv)
            xxi=round(Triangle.u*coord[0]-0.5)
            xxj=round(Triangle.v*coord[1]-0.5)
            #print((int(coord[0]*Triangle.u),int(coord[1]*Triangle.v)))
            
            RGB=Triangle.texture.getpixel((xxi%Triangle.u,xxj%Triangle.v))#P254
            Kd=ar([RGB[0]/255,RGB[1]/255,RGB[2]/255])
            diffuse_light_cos=(self.get_screen_interpolation(i,j,1))
            spect_light_cos=(self.get_screen_interpolation(i,j,Triangle.p))
            color=np.clip(0,1,Triangle.Ka+Kd*diffuse_light_cos+Triangle.Ks*spect_light_cos)*255
            return color
            
                                     
    def get_uv(self,i,j,uv):
        coord=[]
        for i in range(2):
            alpha,beta=self.get_interpolation_weight(i,j)
            pos=alpha*uv[0][i]+beta*uv[1][i]+(1-alpha-beta)*uv[2][i]
            coord.append(pos)
        return np.clip(0,1,coord)
    
    def get_depth_screen(self,i,j):
        alpha,beta=self.get_interpolation_weight(i,j)
        return alpha*self.z1+beta*self.z2+(1-alpha-beta)*self.z3

    
    
    def get_vertice_light(self,n):
        vertice_light=[]
        for i in range(3):
            l=normalize(Object.light+Object.camera-2*self.ori[i])
            vertice_light.append(max(math.pow(np.dot(l,self.norm),n),0))
        return vertice_light
        
    def get_screen_interpolation(self,i,j,n):
        vertice_light=self.get_vertice_light(n)
        alpha,beta=self.get_interpolation_weight(i,j)
        return alpha*vertice_light[0]+beta*vertice_light[1]+(1-alpha-beta)*vertice_light[2]
    
    def get_interpolation_weight(self,i,j):
        #alpha,beta=np.dot(ar([i-self.c[0],j-self.c[1]]),np.linalg.inv(ar([[self.a[0]-self.c[0],self.a[1]-self.c[1]],[self.b[0]-self.c[0],self.b[1]-self.c[1]]])))
        a=self.a
        b=self.b
        c=self.c
        alpha=(-1*(i-b[0])*(c[1]-b[1])+(j-b[1])*(c[0]-b[0]))/(-1*(a[0]-b[0])*(c[1]-b[1])+(a[1]-b[1])*(c[0]-b[0]))
        beta=(-1*(i-c[0])*(a[1]-c[1])+(j-c[1])*(a[0]-c[0]))/(-1*(b[0]-c[0])*(a[1]-c[1])+(b[1]-c[1])*(a[0]-c[0]))
        print(alpha,beta)
        return alpha,beta
        
    def vector_cross_initial(self,i,norm,a,b,c):
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
        
    def optimize_initial(self,i,norm,a,b,c):
        vertice_set=[a,b,c]
        a,b,c=sorted(vertice_set,key=lambda k:k[0])
        self.z1=a[2]
        self.z2=b[2]
        self.z3=c[2]
        self.a=ar([a[0],a[1]])
        self.b=ar([b[0],b[1]])
        self.c=ar([c[0],c[1]])
        self.line1=Line((a[0],a[1]),(b[0],b[1]))
        self.line2=Line((a[0],a[1]),(c[0],c[1]))#横穿的线
        self.line3=Line((b[0],b[1]),(c[0],c[1]))
        self.ori=i
        self.norm=norm
#############################################################
#这坨东西等我修完bug用装饰器重写   复用之耻     
    def vector_update_buffer(self,uv):
        for i in range(self.xmin,self.xmax):
                for j in range(self.ymin,self.ymax):
                    vec=np.array([i,j])
                    if np.cross(vec-self.a,self.vec2)>0 and np.cross(vec-self.b,self.vec3)>0 and np.cross(vec-self.c,self.vec1)>0:        
                        depth=self.get_depth_screen(i,j)
            
                        if i>=Object.width or j>=Object.height or i<0 or j<0:    break
                        if depth<Object.z_buff[i][j]:
                            Object.z_buff[i][j]=depth     
                            Object.f_buff[i][j]=self.shade_color(i,j,uv)       
       
    def optimize_update_buffer(self,uv):
        b_continue=0
        b_dots=self.line2.draw_line()
        for count,i in enumerate(range(self.a[0],self.b[0])):
            b_continue=count#b线要记录结束点位置继续
            dots=self.line1.draw_line()
            start=min(dots[count][1],b_dots[count][1])
            end=max(dots[count][1],b_dots[count][1])
            for j in range(start,end):
                depth=self.get_depth_screen(i,j)
                if depth<Object.z_buff[i][j]:
                        Object.z_buff[i][j]=depth
                        Object.f_buff[i][j]=self.shade_color(i,j,uv)
            
        for count,i in enumerate(range(self.b[0],self.c[0])):
            dots=self.line3.draw_line()
            start=min(dots[count][1],b_dots[count+b_continue][1])
            end=max(dots[count][1],b_dots[count+b_continue][1])
            for j in range(start,end):
                depth=self.get_depth_screen(i,j)
                if depth<Object.z_buff[i][j]:
                        Object.z_buff[i][j]=depth
                        Object.f_buff[i][j]=self.shade_color(i,j,uv)
                        
    def barycentric_update_buffer(self,uv):
        for i in range(self.xmin,self.xmax):
            for j in range(self.ymin,self.ymax):
                alpha,beta=self.get_interpolation_weight(i,j)
                if alpha>0 and beta>0 and alpha+beta<=1:
                    depth=self.get_depth_screen(i,j)
                    if i>=Object.width or j>=Object.height or i<0 or j<0:    break
                    if depth<Object.z_buff[i][j]:
                        Object.z_buff[i][j]=depth     
                        Object.f_buff[i][j]=self.shade_color(i,j,uv)
        
        
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
    

        
        
        
        
