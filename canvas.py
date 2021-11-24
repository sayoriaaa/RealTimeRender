# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 21:56:58 2021

@author: sayori
"""

from PIL import Image,ImageColor
import numpy as np
import random
from drawkit import Triangle
from drawkit import Line
from drawkit import Object
from numpy import array as ar

class Scene:
            
    def __init__(self,save_path=None,width=600,height=400,background=(125,255,0)):
        self.filename=save_path
        self.width=width
        self.height=height
        self.img=Image.new("RGB",(width,height),background)
        initialize_Object(width,height)
        self.camera=Object.camera
        self.light=Object.light
        self.background=background
        
        
    def draw(self,dots,color):
        if isinstance(color,str): color=ImageColor.getrgb(color)
        for i,dot in enumerate(dots):
            self.img.putpixel(dots[i], color[i])
                         
                   
    def draw_xyz(self,M):
        set_a=[ar([0,0,0,1]),ar([0,0,0,1]),ar([0,0,0,1])]
        set_b=[ar([10,0,0,1]),ar([0,10,0,1]),ar([0,0,10,1])]
        color=[(255,0,0),(0,255,0),(0,0,255)]
        for i,v in enumerate(set_a):
            start=np.dot(M, set_a[i])
            
            end=np.dot(M, set_b[i])
            a=ar([round(start[0]/start[3]),round(start[1]/start[3])])
            b=ar([round(end[0]/end[3]),round(end[1]/end[3])])
            grid_line=Line(a,b)
            dots=grid_line.draw_line()
            for dot in dots:
                if dot[0]>=0 and dot[1]>=0 and dot[0]<self.width and dot[1]<self.height:
                    self.img.putpixel((dot[0],dot[1]), color[i])
                    
    def save(self):
        self.img.save(self.filename)
        
    def show(self):
        self.img.show()
        self.save()
        
        
'''       
    def draw_grid(self,M):
        set_a=[ar([i,0,10,1]) for i in range(-10,11)]
        set_b=[ar([i,0,-10,1]) for i in range(-10,11)]
        for i,v in enumerate(set_a):
            start=np.dot(M, set_a[i])        
            end=np.dot(M, set_b[i])
            if start[3]==0 or end[3]==0: break
            a=ar([round(start[0]/start[3]),round(start[1]/start[3])])
            b=ar([round(end[0]/end[3]),round(end[1]/end[3])])
            grid_line=Line(a,b)
            dots=grid_line.draw_Line()
            for dot in dots:
                if dot[0]>=0 and dot[1]>=0 and dot[0]<900 and dot[1]<900:
                    self.img.putpixel((dot[0],dot[1]), (0,0,0))
        
        set_a=[ar([10,0,i,1]) for i in range(-10,11)]
        set_b=[ar([-10,0,i,1]) for i in range(-10,11)]
        for i,v in enumerate(set_a):
            start=np.dot(M, set_a[i])
            end=np.dot(M, set_b[i])
            a=ar([round(start[0]/start[3]),round(start[1]/start[3])])
            b=ar([round(end[0]/end[3]),round(end[1]/end[3])])
            grid_line=Line(a,b)
            dots=grid_line.draw_Line()
            for dot in dots:
                if dot[0]>=0 and dot[1]>=0 and dot[0]<900 and dot[1]<900:
                    self.img.putpixel((dot[0],dot[1]), (0,0,255))
''' 
        
def initialize_Object(width,height):
    Object.z_buff=np.full((width,height),np.inf)
    Object.f_buff=ar([ar([[1,1,1] for i in range(height)]) for i in range(width)])#这里小心了
    Object.height=height
    Object.width=width 
    

    
    
      

if __name__=="__main__":
    k=Scene()
    k.put_yellow()
    k.put_default_tri()
    k.img.show()
    
        
        
        
        