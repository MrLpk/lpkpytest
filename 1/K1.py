#-*- coding: utf-8 -*-
'''
Created on 2013年7月31日

@author: DY
'''
import time
from flask import Flask, request
from extlibs.Command import Command
from extlibs.Weixin import Weixin
from extlibs.MySQLSAE import MySQLSAE

app = Flask(__name__)
w = Weixin()
m = Command()
db = MySQLSAE()
app.debug = True
         
    
def handleWeixin(request):
    msg = w.parse_msg(request.data)
    if msg['FromUserName'] != 'o8CC5jvvQAgNGif1q-D44XKNrQUw':
        return '你又不是我主人，K-1拒绝为你服务！[抠鼻]'
    if w.isTextMsg(msg):
        command = m.analyzeCommand(msg)
        if command == m.COM_SF_ADD:
            text = msg['Content']
            text = text.split(' ')
            s = u"insert into countmoney(uid,money,time,content) values('%s',%s,'%s','%s')" %(msg['FromUserName'], text[1], time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), text[2])
            db.insertDB(s)
            print 'execute COM_SF_ADD Sucess!!'
            return '[OK]'
        elif command == m.COM_SF_CHECK:
            s = u'select * from countmoney where iscount = 0'
            asd = """%s-￥%s元-%s\n"""
            result = ''
            money = 0
            msgs = db.selectDB(s)
            for row in msgs:
                result = result + asd %(row[3], row[2], row[-1])
                money += row[2]
            result = result + '共￥%s元,3人平均每人%s元' %(money, money/3)
            print 'execute COM_SF_CHECK Sucess!!'
            return result
        elif command == m.COM_SF_CLEAN:
            s = u'update countmoney set iscount = 1 where iscount = 0'
            db.insertDB(s)
            print 'execute COM_SF_CLEAN Sucess!!'
            return '主人[OK][可怜]'
        elif command == m.COM_UNKNOW:
            return '讲人话！！[抠鼻]'
    else:
        return '图片对老子是没用的[抠鼻]'
        
#    ----------------------------------------------------------------------------            
#    ----------------------------------------------------------------------------           
#    ----------------------------------------------------------------------------
        
@app.route('/', methods=['GET'])
def weixin_Get():
    echostr = request.args.get('echostr')
    if w.calibration_WeiXin(request) and echostr is not None:
        return echostr
    return 'weixin_Get fail - -'

@app.route('/', methods=['POST'])
def weixin_Post():
    if w.calibration_WeiXin(request):
        print 'ok...'
        content = handleWeixin(request)
        return w.responseTextMsg(w.parse_msg(request.data), content)
    

if __name__ == '__main__':
    app.run();