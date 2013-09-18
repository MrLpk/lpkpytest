#coding=utf-8
'''
Created on 2013-9-17

@author: liaopengkai
'''
import re
import cookielib
import urllib2
import urllib

username = ''
password = ''

def save(filename, contents): 
    fh = open(filename, 'w') 
    fh.write(contents) 
    fh.close() 
    print 'save done'
    
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
            
            
            
            
            
            
    '''贴吧签到'''
    print '开始进行签到...'
    print '查找所有贴吧...'
    '''improtant!!!'''
    'http://tieba.baidu.com/f/like/mylike?v=1379413391641'
    ''''''
#     BAIDU_TIEBA_URL = 'http://tieba.baidu.com/'
#     BAIDU_ITIEBA_URL = 'http://tieba.baidu.com/i/%s?fr=index'
    BAIDU_ITIEBA_URL = 'http://tieba.baidu.com/home/main?un=%s&fr=index'
        
#     tiebaHtml = urllib2.urlopen(BAIDU_TIEBA_URL).read()
#     save('filename.txt', tiebaHtml)
#     name_link = re.search('"name_link":(?P<tokenVal>\w+),"', tiebaHtml).group('tokenVal')
        
#     print 'name_link:', name_link
    BAIDU_ITIEBA_URL = BAIDU_ITIEBA_URL %username
    itiebaHtml = urllib2.urlopen(BAIDU_ITIEBA_URL).read()
    save('filename.txt', itiebaHtml.decode('gbk'))
#         print 'itiebaHtml = \n',itiebaHtml.decode('gbk')
#         save('itiebaHtml.txt', itiebaHtml.decode('gbk'))
        
    itiebas = re.findall(r'kw=([0-9A-Za-z%]*)&fr=itb_favo&fp=favo" target="_blank">([^ ]*)</a>', itiebaHtml) 
    print 'itiebas = \n', itiebas
    if itiebas != []:
        print 'itiebas = \n',itiebas[0][1].decode('gbk')
        for i in range(len(itiebas)):
            print itiebas[i][1]
    else:
        print 'false'

def sign():
        '''贴吧签到'''
        print '开始进行签到...'
        print '查找所有贴吧...'
        
        BAIDU_TIEBA_URL = 'http://tieba.baidu.com/'
        BAIDU_ITIEBA_URL = 'http://tieba.baidu.com/i/%s?fr=index'
        
        tiebaHtml = urllib2.urlopen(BAIDU_TIEBA_URL).read()
        save('filename.txt', tiebaHtml)
        name_link = re.search('"name_link":(?P<tokenVal>\w+),"', tiebaHtml).group('tokenVal')
        
        print 'name_link:', name_link
        BAIDU_ITIEBA_URL = BAIDU_ITIEBA_URL %name_link
        itiebaHtml = urllib2.urlopen(BAIDU_ITIEBA_URL).read()

#         print 'itiebaHtml = \n',itiebaHtml.decode('gbk')
#         save('itiebaHtml.txt', itiebaHtml.decode('gbk'))
        
        itiebas = re.findall(r'kw=([0-9A-Za-z%]*)&fr=itb_favo&fp=favo" target="_blank">([^ ]*)</a>', itiebaHtml)
        print 'itiebas = \n',itiebas[0][1].decode('gbk')
        print len(itiebas)
        if itiebas != []:
            for i in range(len(itiebas)):
                print itiebas[i][1]
        else:
            print 'false'
            
def requstSign(kw):
        BAIDU_TIEBA_URL = 'http://tieba.baidu.com/f?kw=%s&fr=index&ie=utf-8' %kw
        BAIDU_SIGN_URL  = 'http://tieba.baidu.com/sign/add'
        
        resp = urllib2.urlopen(BAIDU_TIEBA_URL)
        fffhtml = resp.read()
#         save('tiebahtml1.txt', fffhtml.decode('gbk'))
        
        tbs = re.search('PageData.tbs = "(?P<tokenVal>\w+)";', fffhtml)
        
        if tbs:
            print 'tbs=',tbs
            tbsVal = tbs.group('tokenVal')
            print 'tbsVal='+tbsVal
        
        pDict = {
            'ie' : 'utf-8',
            'kw' : '缘分0',#%E7%BC%98%E5%88%860
#             'kw' : '%e5%85%a8%e8%81%8c%e9%ab%98%e6%89%8b',#全职高手
            'tbs': tbsVal
                 }

        

        
        
        pData = urllib.urlencode(pDict)
        print pData
        
#         print 'teiba=\n',fffhtml.decode('gbk')

        '''签到'''
#         r = urllib2.Request(signurl, pData)
#         resp = urllib2.urlopen(r)
#         printDelimiter()
#         print resp.read()
        print 'done'

def initData():
    '''获取用户名密码'''
    print 'initing data...'
    
    global username
    global password
    
    iniFile = open('BDu&p.txt', 'r')
    
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
    
def start():
    initData()
    login()
#     sign()

if __name__ == '__main__':
    start()
