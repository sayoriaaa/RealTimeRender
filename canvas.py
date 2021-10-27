# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 21:56:58 2021

@author: sayori
"""

from PIL import Image,ImageColor
import numpy as np
import random


class triangle:
    def __init__(self,a=np.zeros(2),b=np.zeros(2),c=np.zeros(2)):
        self.a=a
        self.b=b
        self.c=c
        self.vec1=a-c
        self.vec2=b-a
        self.vec3=c-b
        self.xmin=min(a[0],b[0],c[0])
        self.xmax=max(a[0],b[0],c[0])
        self.ymin=min(a[1],b[1],c[1])
        self.ymax=max(a[1],b[1],c[1])
        
    def get_dots(self):
        dots=[]
        for i in range(self.xmin,self.xmax):
            for j in range(self.ymin,self.ymax):
                vec=np.array([i,j])
                if np.cross(vec-self.a,self.vec2)>0 and np.cross(vec-self.b,self.vec3)>0 and np.cross(vec-self.c,self.vec1)>0:
                    dots.append((i,j))
        return dots
                    
                

class canvas:
            
    def __init__(self,filename=None,width=900,height=900):
        self.img=Image.new("RGBA",(width,height),(0,0,0,0))
        
    def draw(self,dots,color):
        color=ImageColor.getrgb(color)
        for dot in dots:
            self.img.putpixel(dot, color)
    
    def put_blue(self):
        dots=[]         
        for i in range(900):
            for j in range(900):
                dots.append((i,j))
        self.draw(dots, "blue")
        
    def put_default_tri(self):
        a=np.array([random.randint(0,400),random.randint(0,400)])
        b=np.array([random.randint(700,900),random.randint(700,900)])
        c=np.array([random.randint(700,900),random.randint(300,600)])
        print(a,b,c)
        self.draw(triangle(a,b,c).get_dots(),"green")
        


        
        
        
        