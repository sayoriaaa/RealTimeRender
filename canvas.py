# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 21:56:58 2021

@author: sayori
"""

from PIL import Image,ImageColor
import numpy as np
import random
from drawkit import triangle

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
    
        
        
        
        