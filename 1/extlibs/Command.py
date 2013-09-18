#coding=UTF-8
'''
Created on 2013年8月17日

@author: liaopengkai
'''
from MTool import MTool

class Command:
    
    COM_UNKNOW      = 0
#   SF_COMMAND    1-50
    COM_SF_ADD      = 1
    COM_SF_CHECK    = 2
    COM_SF_CLEAN    = 3
    
    mt = MTool() 
    # 解析命令
    def analyzeCommand(self, msg):
        text = msg['Content']
        text = text.split(' ')
        
        #print len(text)
        if text[0] == u'宿费' or text[0] == u'sf' or text[0] == u'SF' or text[0] == u'舍费':
            if self.mt.isNum(text[1]):
                print 'COM_SF_ADD!!'
                return self.COM_SF_ADD
            elif text[1] == u'check':
                print 'COM_SF_CHECK!!'
                return self.COM_SF_CHECK
            elif text[1] == u'clean':
                print 'COM_SF_CLEAN!!'
                return self.COM_SF_CLEAN
            else:
                print 'UNKNOW_COMMAND'
                return self.COM_UNKNOW
        else:
            print 'UNKNOW_COMMAND'
            return self.COM_UNKNOW
