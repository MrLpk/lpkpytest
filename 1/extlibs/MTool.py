#-*- coding: utf-8 -*-
'''
Created on 2013-8-27

@author: liaopengkai
'''

class MTool:
    
    def isNum(self, tempStr):
        """判断字符串是否为数字，整型和浮点型皆适用"""
        try:
            float(tempStr)
            return True
        except Exception:
            return False
        
if __name__ == '__main__':
    pass