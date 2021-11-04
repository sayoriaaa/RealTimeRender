# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 21:56:58 2021

@author: sayori
"""

from PIL import Image,ImageColor
import numpy as np
import random
from drawkit import triangle
from drawkit import line
from numpy import array as ar

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
        
    def draw_grid(self,M):
        set_a=[ar([i,0,10,1]) for i in range(-10,11)]
        set_b=[ar([i,0,-10,1]) for i in range(-10,11)]
        for i,v in enumerate(set_a):
            start=np.dot(M, set_a[i])        
            end=np.dot(M, set_b[i])
            if start[3]==0 or end[3]==0: break
            a=ar([round(start[0]/start[3]),round(start[1]/start[3])])
            b=ar([round(end[0]/end[3]),round(end[1]/end[3])])
            grid_line=line(a,b)
            dots=grid_line.draw_line()
            for dot in dots:
                if dot[0]>=0 and dot[1]>=0 and dot[0]<900 and dot[1]<900:
                    self.img.putpixel((dot[0],dot[1]), (0,0,0,255))
        
        set_a=[ar([10,0,i,1]) for i in range(-10,11)]
        set_b=[ar([-10,0,i,1]) for i in range(-10,11)]
        for i,v in enumerate(set_a):
            start=np.dot(M, set_a[i])
            end=np.dot(M, set_b[i])
            a=ar([round(start[0]/start[3]),round(start[1]/start[3])])
            b=ar([round(end[0]/end[3]),round(end[1]/end[3])])
            grid_line=line(a,b)
            dots=grid_line.draw_line()
            for dot in dots:
                if dot[0]>=0 and dot[1]>=0 and dot[0]<900 and dot[1]<900:
                    self.img.putpixel((dot[0],dot[1]), (0,0,255,255))
                    
    def draw_xyz(self,M):
        set_a=[ar([0,0,0,1]),ar([0,0,0,1]),ar([0,0,0,1])]
        set_b=[ar([10,0,0,1]),ar([0,10,0,1]),ar([0,0,10,1])]
        color=[(255,0,0,255),(0,255,0,255),(0,0,255,255)]
        for i,v in enumerate(set_a):
            print(set_a[i])
            start=np.dot(M, set_a[i])
            
            end=np.dot(M, set_b[i])
            a=ar([round(start[0]/start[3]),round(start[1]/start[3])])
            print(a)
            b=ar([round(end[0]/end[3]),round(end[1]/end[3])])
            grid_line=line(a,b)
            dots=grid_line.draw_line()
            for dot in dots:
                if dot[0]>=0 and dot[1]>=0 and dot[0]<900 and dot[1]<900:
                    self.img.putpixel((dot[0],dot[1]), color[i])
        

        
        

if __name__=="__main__":
    k=canvas()
    k.put_yellow()
    k.put_default_tri()
    k.img.show()
    
        
        
        
        