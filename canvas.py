# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 21:56:58 2021

@author: sayori
"""

from PIL import Image,ImageColor
import numpy as np
import random
from numpy import array as ar


class triangle:
    def __init__(self,a=np.zeros(3),b=np.zeros(3),c=np.zeros(3)):
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
        
        self.canvas=canvas
        
    def get_dots(self):
        dots=[]
        colors=[]
        for i in range(self.xmin,self.xmax):
            for j in range(self.ymin,self.ymax):
                vec=np.array([i,j])
                if np.cross(vec-self.a,self.vec2)>0 and np.cross(vec-self.b,self.vec3)>0 and np.cross(vec-self.c,self.vec1)>0:
                    dots.append((i,j))
                    colors.append((0,int(255*i/self.xmax),int(255*j/self.ymax),225))
        return dots,colors      

                    
                

class canvas:
            
    def __init__(self,filename=None,width=900,height=900):
        self.img=Image.new("RGBA",(width,height),(0,0,0,0))
        
    def draw(self,dots,color):
        if isinstance(color,str): color=ImageColor.getrgb(color)
        for i,dot in enumerate(dots):
            self.img.putpixel(dots[i], color[i])
                
    
    def put_yellow(self):      
        for i in range(900):
            for j in range(900):
                self.img.putpixel((j,i),(125,255,0,int(100+100*i/900)))
        
    def put_default_tri(self):
        a=np.array([random.randint(0,400),random.randint(0,400),1])
        b=np.array([random.randint(700,900),random.randint(700,900),1])
        c=np.array([random.randint(700,900),random.randint(300,600),1])
        print(a,b,c)
        dots,colors=triangle(a,b,c).get_dots()
        self.draw(dots,colors)
        

if __name__=="__main__":
    k=canvas()
    k.put_yellow()
    k.put_default_tri()
    k.img.show()
    
        
        
        
        