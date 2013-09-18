#coding=UTF-8
'''
Created on 2013年8月4日

@author: DY
'''
# from Command import Command as M
from flask import g
import time
# def analyzeCommand(text):
#     text = text.split(' ')
#     if text[0] == None:
#         print 'UNKNOW_COMMAND'
#         return M.COM_UNKNOW
#     elif text[0] == '宿费' or text[0] == 'sf' or text[0] == 'SF' or text[0] == '舍费':
#         if text[1].isdigit:
#             print 'COM_SF_ADD!!'
#             c = g.db.cursor()
#             c.execute('insert into countmoney(uid,money,time,iscount) values(%s,%s,%s,%s)' ,(text))
#             return M.COM_SF_ADD
#         elif text[1] == 'check':
#             print 'COM_SF_CHECK!!'
#             return M.COM_SF_CHECK
#         elif text[1] == 'clean':
#             print 'COM_SF_CLEAN!!'
#             return M.COM_SF_CLEAN
            
            
def doSomeThing(text):           
#     analyzeCommand(text)
#     print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
#             print 'success'
#     print 'fail'
    if '4.5'.isdigit():
        print 'true'
    else:
        print 'false'

if __name__ == '__main__':
    doSomeThing(u'宿费 13 纸巾')