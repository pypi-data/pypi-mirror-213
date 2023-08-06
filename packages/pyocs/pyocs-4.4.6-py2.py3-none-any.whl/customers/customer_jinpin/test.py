#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from tkinter import *
class Window:
  def __init__(self, title='游戏', width=300, height=120, staFunc=bool, stoFunc=bool):
    self.w = width
    self.h = height
    self.stat = True
    self.staFunc = staFunc
    self.stoFunc = stoFunc
    self.staIco = None
    self.stoIco = None
    self.root = Tk(className=title)


 def click(self):
    h=0#正面次数
    t=0#反面次数
    allcount=0
    count =int(self.e1.get())
    for i in range(count):
        num=random.randint(0,1)
        if num==0:
            h=h+1
        else:
            t=t+1  
        allcount=allcount+1          
    print(allcount)
    self.hc.set(str(h))#正面次数
    self.p.set(str(h/count))#正面概率
    


#你写的脚本模块既可以导入到别的模块中用，另外该模块自己也可执行
if __name__ == '__main__':
    w = Window(width=350, height=150)
