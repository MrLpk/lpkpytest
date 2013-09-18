#coding=UTF-8
'''
Created on 2013年8月4日

@author: DY
'''

import cookielib
import urllib
import urllib2
import re

def checkAllCookiesExist(cookieNameList, cookieJar) :
    cookiesDict = {};
    for eachCookieName in cookieNameList :
        cookiesDict[eachCookieName] = False;
     
    allCookieFound = True;
    for cookie in cookieJar :
        if(cookie.name in cookiesDict) :
            cookiesDict[cookie.name] = True;
     
    for eachCookie in cookiesDict.keys() :
        if(not cookiesDict[eachCookie]) :
            allCookieFound = False;
            break;
 
    return allCookieFound;

# just for print delimiter
def printDelimiter():
    print '-'*80;
    
def save(filename, contents): 
    fh = open(filename, 'w') 
    fh.write(contents) 
    fh.close() 
    print 'save done'
    
def start(text):
    pass

if __name__ == '__main__':
#   start(u'宿费 13 纸巾')
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    
    baiduMainUrl = "http://www.baidu.com/"
    resp = urllib2.urlopen(baiduMainUrl)
    
    for index, cookie in enumerate(cj):
        print '[',index,']',cookie
    printDelimiter()
    
    getapiUrl = "https://passport.baidu.com/v2/api/?getapi&class=login&tpl=mn&tangram=true"
    getapiResp = urllib2.urlopen(getapiUrl)
    getapiRespHtml = getapiResp.read()
    print 'getapiRespHtml='+getapiRespHtml
    
    printDelimiter()
    foundTokenVal = re.search("bdPass\.api\.params\.login_token='(?P<tokenVal>\w+)';", getapiRespHtml)
    
    if foundTokenVal:
        print 'foundTokenVal=',foundTokenVal
        tokenVal = foundTokenVal.group('tokenVal')
        print 'tokenVal='+tokenVal
        printDelimiter()
    
        staticpage = "http://www.baidu.com/cache/user/html/jump.html"
        baiduMainLoginUrl = "https://passport.baidu.com/v2/api/?login"
        
        postDict = {
            #'ppui_logintime': "",
            'charset'       : "utf-8",
            #'codestring'    : "",
            'token'         : tokenVal, #de3dbf1e8596642fa2ddf2921cd6257f
            'isPhone'       : "false",
            'index'         : "0",
            #'u'             : "",
            #'safeflg'       : "0",
            'staticpage'    : staticpage, #http%3A%2F%2Fwww.baidu.com%2Fcache%2Fuser%2Fhtml%2Fjump.html
            'loginType'     : "1",
            'tpl'           : "mn",
            'callback'      : "parent.bdPass.api.login._postCallback",
            'username'      : 'ansshiwei',
            'password'      : '123123Aa',
            #'verifycode'    : "",
            'mem_pass'      : "on",
        }
        
        postData = urllib.urlencode(postDict)
        print 'postData',postData
        printDelimiter()
    
        req = urllib2.Request(baiduMainLoginUrl, postData)
        req.add_header('Content-Type', "application/x-www-form-urlencoded")
        resp = urllib2.urlopen(req)
        for index, cookie in enumerate(cj):
            print '[',index,']',cookie
        
        printDelimiter()
        cookiesToCheck = ['BDUSS', 'PTOKEN', 'STOKEN', 'SAVEUSERID']
    
        loginBaiduOk = checkAllCookiesExist(cookiesToCheck, cj)
        if loginBaiduOk:
            print 'Emulate login baidu is OK, ^_^'
        else:
            print 'Failed to emulate login baidu !'
            
        '''查询个人信息'''
#         printDelimiter()
#         infoURL = 'http://passport.baidu.com/center?_t=1378735384'
#         infoResp = urllib2.urlopen(infoURL)
#         infoRespHtml = infoResp.read()
#         print 'infoRespHtml=\n',infoRespHtml
        
        tiebaurl = 'http://tieba.baidu.com/f?kw=%C8%AB%D6%B0%B8%DF%CA%D6&fr=index&ie=utf-8'
        signurl = 'http://tieba.baidu.com/sign/add'
        
        resp = urllib2.urlopen(tiebaurl)
        printDelimiter()
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
        
        
        
        '''查找所有关注贴吧'''
        
        tiebaurl = 'http://tieba.baidu.com/'
        tiebaHtml = urllib2.urlopen(tiebaurl).read()
        
        name_link = re.search('"name_link":(?P<tokenVal>\w+),"', tiebaHtml).group('tokenVal')
        printDelimiter()
        print 'name_link = ', name_link
        itiebaurl = 'http://tieba.baidu.com/i/%s?fr=index' %name_link
        itiebaHtml = urllib2.urlopen(itiebaurl).read()
        printDelimiter()
        print 'itiebaHtml = \n',itiebaHtml.decode('gbk')
           
        
        
        
    else:
        print "Fail to extract token value from html=",getapiRespHtml
            
            
            
            
            
            
            
            
            
            
            
            
            
            
    
    
    
    
    