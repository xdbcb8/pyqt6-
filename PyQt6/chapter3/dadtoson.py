#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   dadtoson.py
@Time    :   2023/04/07 19:22:19
@Author  :   yangff 
@Version :   1.0
@微信公众号:  xdbcb8
'''

# 简单的类继承使用

class Dad(): 
   '''爸爸类'''
   def __init__(self):  
       print('我是爸爸。')
       self.hungry = True
   def eat(self):  
       if self.hungry:  
           print('我吃饭啦！')
           self.hungry = False
       else:  
           print('我吃过了啊！')

class Son(Dad): 
   '''儿子类'''
   def __init__(self):
       super().__init__()
       print('我是儿子。')

class Daughter(Dad):
   '''女儿类'''
   def __init__(self):
       print('我是女儿。')

dad = Dad()
dad.eat()
dad.eat()
print()
son = Son()
son.eat()
son.eat()
print()
daughter = Daughter()
daughter.eat()
daughter.eat()
