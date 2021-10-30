# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 10:36:19 2021

@author: sayori
"""
import numpy as np
from numpy import array as ar

class triangle:
    def __init__(self,a=np.zeros(3),b=np.zeros(3),c=np.zeros(3),buff=np.zeros((900,900))):#分别传入屏幕坐标的三个点和buffer
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
        
        self.buff=buff
          
    def get_buffer(self):
        
        for i in range(self.xmin,self.xmax):
            for j in range(self.ymin,self.ymax):
                vec=np.array([i,j])
                if np.cross(vec-self.a,self.vec2)>0 and np.cross(vec-self.b,self.vec3)>0 and np.cross(vec-self.c,self.vec1)>0:        
                    depth=self.get_depth_screen(i,j)

                    if i>=900 or j>=900 or i<0 or j<0:    break
                    if depth<self.buff[i][j]:
                        self.buff[i][j]=depth
        return self.buff
    
    def get_depth_screen(self,i,j):
        alpha,beta=np.dot(ar([i-self.c[0],j-self.c[1]]),np.linalg.inv(ar([[self.a[0]-self.c[0],self.a[1]-self.c[1]],[self.b[0]-self.c[0],self.b[1]-self.c[1]]])))#
        return alpha*self.z1+beta*self.z2+(1-alpha-beta)*self.z3
    def get_depth_appro(self):
        return self.z_ave
