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
    else:
        print "Fail to extract token value from html=",getapiRespHtml
            
            
            
            
            
            
            
            
            
            
            
            
            
            
    
    
    
    
    