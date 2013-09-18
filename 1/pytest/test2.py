#coding=UTF-8
'''
Created on 2013年8月4日

@author: DY
'''

import cookielib
import urllib
import urllib2
import re
import json

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
    
#     getapiUrl = "https://passport.baidu.com/v2/api/?getapi&class=login&tpl=mn&tangram=true"
                 
    getapiUrl = "https://passport.baidu.com/v2/api/?getapi&tpl=mn&apiver=v3&class=login&logintype=dialogLogin&callback=bd__cbs__rvsnl1"
    getapiResp = urllib2.urlopen(getapiUrl)
    getapiRespHtml = getapiResp.read()
    print 'getapiRespHtml='+getapiRespHtml
    
    printDelimiter()
#     foundTokenVal = re.search("bdPass\.api\.params\.login_token='(?P<tokenVal>\w+)';", getapiRespHtml)

    
    
    temp = '%s'
    temp = temp % getapiRespHtml
    temp = temp.replace('bd__cbs__rvsnl1(', '')
    temp = temp.replace(')', '')
    
#     print 'temp='+temp
    fff = json.loads(temp)
#     print 'fff=',fff
#     print 'fff.keys=', fff.keys()
#     print 'fff.token=', fff['data']['token']
    
    foundTokenVal = fff['data']['token']
    if foundTokenVal:
        print 'foundTokenVal=',foundTokenVal
#         tokenVal = foundTokenVal.group('tokenVal')
#         print 'tokenVal='+tokenVal
        printDelimiter()
        
        staticpage = "http://www.baidu.com/cache/user/html/v3Jump.html"
        baiduMainLoginUrl = "https://passport.baidu.com/v2/api/?login"
        
        
#         postDict = {
#             #'ppui_logintime': "",
#             'usernamelogin' : '1',
#             'sologin'       : 'rate',
#             'charset'       : "utf-8",
#             #'codestring'    : "",
#             'token'         : foundTokenVal, #de3dbf1e8596642fa2ddf2921cd6257f
#             'isPhone'       : "false",
#             'index'         : "0",
#             'u'             : "http://www.baidu.com/",
#             #'safeflg'       : "0",
#             'staticpage'    : staticpage, #http%3A%2F%2Fwww.baidu.com%2Fcache%2Fuser%2Fhtml%2Fjump.html
#             'loginType'     : "1",
#             'tpl'           : "mn",
#             'callback'      : "parent.bdPass.api.login._postCallback",
#             'username'      : 'ansshiwei',
#             'password'      : '123123Aa',
#             #'verifycode'    : "",
#             'mem_pass'      : "on",
#         }

        postDict = {
            'usernamelogin' : '1',
            'username'      : 'ansshiwei00',
            'u'             : "http://www.baidu.com/",
            'tt'            : '',
            'tpl'           : "mn",
            'token'         : foundTokenVal, #de3dbf1e8596642fa2ddf2921cd6257f
            'staticpage'    : staticpage, #http%3A%2F%2Fwww.baidu.com%2Fcache%2Fuser%2Fhtml%2Fjump.html
            'sologin'       : 'rate',
            'safeflg'       : '0',
            'quick_user'    : '0',
            'ppui_logintime': '',
            'password'      : '123123Aa',
            'mem_pass'      : "on",
            'isPhone'       : "false",
            'charset'       : "UTF-8",
            'callback'      : "parent.bd__pcbs__iafaas",
            'apiver'        : 'v3'
        }
        
        postData = urllib.urlencode(postDict)
        print 'postData',postData
        printDelimiter()
    
        req = urllib2.Request(baiduMainLoginUrl, postData)
        req.add_header('Content-Type', "text/html")
        resp = urllib2.urlopen(req)
        
        print 'after long =',resp.read()
        for index, cookie in enumerate(cj):
            print '[',index,']',cookie
        
        printDelimiter()
        cookiesToCheck = ['BDUSS', 'PTOKEN', 'STOKEN', 'SAVEUSERID']
    
        loginBaiduOk = checkAllCookiesExist(cookiesToCheck, cj)
        if loginBaiduOk:
            print 'Emulate login baidu is OK, ^_^'
        else:
            print 'Failed to emulate login baidu !'
            
#         signurl = 'http://tieba.baidu.com/sign/add'
#         pDict = {
#             'ie' : 'utf-8',
# #             'kw' : '%E7%BC%98%E5%88%860',
#             'kw' : '%e5%85%a8%e8%81%8c%e9%ab%98%e6%89%8b',
#             'tbs': 'e85e984e77e0986f1378470472'
#                  }
#         pData = urllib.urlencode(pDict)
#         print pData
#         r = urllib2.Request(signurl, pData)
#  
#         r.add_header('Content-Type', "application/x-www-form-urlencoded")
#         resp = urllib2.urlopen(r)
#         print 'done'
#         printDelimiter()
#         print resp.read()
#        
        printDelimiter()
        infoURL = 'http://passport.baidu.com/center?_t=1378735384'
        infoResp = urllib2.urlopen(infoURL)
        infoRespHtml = infoResp.read()
        print 'infoRespHtml=\n',infoRespHtml
    else:
        print "Fail to extract token value from html=",getapiRespHtml
            
            
            
            
            
            
            
            
            
            
            
            
            
            
    
    
    
    
    