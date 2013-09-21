#coding=utf-8
'''
Created on 2013-9-17

@author: liaopengkai
'''
import re
import cookielib
import urllib2
import urllib
import json
import datetime
import time
import threading

username = ''
password = ''

isRunning = True

def save(filename, contents): 
    fh = open(filename, 'w') 
    fh.write(contents) 
    fh.close() 
    print 'save done'
    
def waitToTomorrow(d = 0, h = 0, m = 0, s = 0):
    """定时器"""
 
    tomorrow = datetime.datetime.replace(datetime.datetime.now() + datetime.timedelta(days=d), hour=h, minute=m, second=s)
    delta = tomorrow - datetime.datetime.now()
    print '将休眠 ', delta
    time.sleep(delta.seconds)
    
def waitToTomorrowTemp(d = 0, h = 0, m = 0, s = 0):
    """定时器"""
 
    tomorrow = datetime.datetime.replace(datetime.datetime.now() + datetime.timedelta(days=d), second=59)
    delta = tomorrow - datetime.datetime.now()
    print '将休眠 ', delta
    time.sleep(delta.seconds)
    
def printDelimiter():
    print '-'*80;
    
def login():
    '''登陆百度'''
    print '开始登陆...'
    global username
    global password
    
    BAIDU_MAIN_URL      = "http://www.baidu.com/"
    BAIDU_TOKEN_URL     = "https://passport.baidu.com/v2/api/?getapi&class=login&tpl=mn&tangram=true"
    BAIDU_STATIC_URL    = "http://www.baidu.com/cache/user/html/jump.html"
    BAIDU_LOGIN_URL     = "https://passport.baidu.com/v2/api/?login"
    BAIDU_USERINFO_URL  = 'http://passport.baidu.com/center?_t=1378735384'
 
    '''启用cookie'''
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    
    '''打开百度'''
    urllib2.urlopen(BAIDU_MAIN_URL)

    '''请求token'''
    print '请求token...'
    tokenHtml = urllib2.urlopen(BAIDU_TOKEN_URL).read()
    '''提取token'''
    token = re.search("bdPass\.api\.params\.login_token='(?P<tokenVal>\w+)';", tokenHtml).group('tokenVal')
    
    '''组装POST数据'''
    print '组装POST数据...'
    postDict = {
            #'ppui_logintime': "",
            'charset'       : "utf-8",
            #'codestring'    : "",
            'token'         : token, #de3dbf1e8596642fa2ddf2921cd6257f
            'isPhone'       : "false",
            'index'         : "0",
            #'u'             : "",
            #'safeflg'       : "0",
            'staticpage'    : BAIDU_STATIC_URL, #http%3A%2F%2Fwww.baidu.com%2Fcache%2Fuser%2Fhtml%2Fjump.html
            'loginType'     : "1",
            'tpl'           : "mn",
            'callback'      : "parent.bdPass.api.login._postCallback",
            'username'      : username,
            'password'      : password,
            #'verifycode'    : "",
            'mem_pass'      : "on",
        }
        
    postData = urllib.urlencode(postDict)
    print 'postData:',postData
    
    loginRequest = urllib2.Request(BAIDU_LOGIN_URL, postData)
    loginRequest.add_header('Content-Type', "application/x-www-form-urlencoded")
    
    print '请求登陆...'
    urllib2.urlopen(loginRequest).read()

    '''查询个人信息'''
    infoRespHtml = urllib2.urlopen(BAIDU_USERINFO_URL).read()
    title = re.findall(r'<title>([^ ]*)</title>', infoRespHtml)
    
    if title != []:   
        if title[0] == '个人中心':
            print '登陆成功...'
            print '当前用户:',username
        else:
            print '登陆失败...'
            

def sign():
    '''贴吧签到'''
    print '开始进行签到...'
    print '查找所有贴吧...'

    BAIDU_ITIEBA_URL = 'http://tieba.baidu.com/f/like/mylike?&pn=1'
                            
    itiebaHtml = urllib2.urlopen(BAIDU_ITIEBA_URL).read()

    page = re.findall(u'pn=([^ ]*)">尾页</a>', itiebaHtml.decode('gbk'))[0]
    itiebas = re.findall(r'kw=([0-9A-Za-z%]*)" title="([^ ]*)">', itiebaHtml) 
        
    for index in range(int(page)):
        tempIndex = index + 1
        if tempIndex == 1:
            pass
        else:
            itiebaHtml = urllib2.urlopen('http://tieba.baidu.com/f/like/mylike?&pn=%d' %tempIndex).read()
            itiebas = re.findall(r'kw=([0-9A-Za-z%]*)" title="([^ ]*)">', itiebaHtml) 

        if itiebas != []:      
            # for i in range(len(itiebas)):
            requstSign(itiebas[0][0], itiebas[0][1].decode('gb2312'))
        else:
            print '您还没有关注的贴吧...'
    print '完成所有签到...'
            
def requstSign(url, kw):
    '''签到'''
    print kw+'吧进行签到...'
    time.sleep(1.5)
    BAIDU_TIEBA_URL = 'http://tieba.baidu.com/f?kw=%s&fr=index&ie=utf-8' %url
    BAIDU_SIGN_URL  = 'http://tieba.baidu.com/sign/add'
        
    tiebaHtml = urllib2.urlopen(BAIDU_TIEBA_URL).read()
    '''获取加密因子tbs'''   
    tbs = re.search('PageData.tbs = "(?P<tokenVal>\w+)";', tiebaHtml).group('tokenVal')

    '''组装数据''' 
    pDict = {
        'ie' : 'utf-8',
        'kw' : kw,
        'tbs': tbs
        }    
    pData = urllib.urlencode(pDict)


    '''提交请求'''
    r = urllib2.Request(BAIDU_SIGN_URL, pData)
    respHtml = urllib2.urlopen(r).read()
    result = json.loads(respHtml)
    
    if result['error'] == '':
        print kw+'吧签到成功...'
    else:
        print kw+'吧签到失败,'+result['error'].decode('utf-8')+'...'
        if result['no'] != 1101:
            requstSign(url, kw)
        
    printDelimiter()

def initData():
    '''获取用户名密码'''
    print 'initing data...'
    
    global username
    global password
    
    iniFile = open('ver.txt', 'r')
    
    username = re.findall(r'username:([^\n]*)', iniFile.readline())[0]
    password = re.findall(r'password:([^\n]*)', iniFile.readline())[0]
    if username == '':
        username = 'ansshiwei'
    if password == '':
        password = '123123Aa'
    
    
    print 'username:'+username
    print 'password:'+password
    print 'init Finish...'

    iniFile.close()

def execute():
    global isRunning
    isRunning = True
    while isRunning:
        waitToTomorrowTemp()
        initData()
        login()
        sign()
        
class BD(threading.Thread):
    def run(self):
        execute()
            
def stop():
    global isRunning
    isRunning = False
    
def start():
    bd = BD()
    bd.start()


if __name__ == '__main__':
    start()
